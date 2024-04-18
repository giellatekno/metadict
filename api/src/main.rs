mod pg_connection_pool;
mod timing_middleware;

use anyhow::anyhow;
use axum::{
    extract::{Path, State},
    response::{IntoResponse, Response},
    routing::get,
    Json, Router,
};
use listenfd::ListenFd;
use serde_json::json;
use std::sync::Arc;
use tokio::net::TcpListener;
use tokio_postgres::Error;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

use crate::pg_connection_pool::ConnectionPool;
use crate::timing_middleware::timing_middleware;

struct AppState {
    /// The connection pool to the PostgreSQL database.
    connpool: Arc<ConnectionPool>,
}

impl Clone for AppState {
    fn clone(&self) -> Self {
        Self {
            connpool: Arc::clone(&self.connpool),
        }
    }
}

struct AppError(anyhow::Error);

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        (
            http::StatusCode::INTERNAL_SERVER_ERROR,
            #[cfg(debug_assertions)]
            format!("{}", self.0),
            #[cfg(not(debug_assertions))]
            "Something went wrong",
        )
            .into_response()
    }
}

impl From<anyhow::Error> for AppError {
    fn from(err: anyhow::Error) -> Self {
        Self(err)
    }
}

fn internal_error<E>(err: E) -> (http::StatusCode, String)
where
    E: std::error::Error,
{
    (
        http::StatusCode::INTERNAL_SERVER_ERROR,
        #[cfg(debug_assertions)]
        err.to_string(),
        #[cfg(not(debug_assertions))]
        "Something went wrong".to_string(),
    )
}

async fn handler_root() -> Response {
    concat!(env!("CARGO_PKG_NAME"), " v", env!("CARGO_PKG_VERSION"), "\n").into_response()
}

async fn handler_404() -> Response {
    (http::StatusCode::NOT_FOUND, "Not found\n").into_response()
}

/// /search/:lang/:query
/// Finds all matching lemmas to the :query, in all dictionaries.
async fn handler_search(
    Path((lang, query)): Path<(String, String)>,
    State(AppState { connpool }): State<AppState>,
) -> Result<Response, AppError> {
    let client = connpool.get().await?;

    // TODO is this injection safe?
    let statement = r#"
        SELECT DISTINCT
            lemma
        FROM
            articles
        WHERE
            lang = $1
            AND
            lemma LIKE $2
        ;
    "#;
    // TODO prepared statement cache? Is that a thing?
    //let statement = match client.prepare(sql_query).await {
    //    Ok(statement) => statement,
    //    Err(e) => return format!("{}", e).into_response(),
    //};
    let rows = client
        .query(statement, &[&lang, &query])
        .await
        .map_err(|e| anyhow!(e))?;
    // rust: temporary value dropped while borrowed
    let rows = rows
        .iter()
        .map(|row| {
            // tuple of row.get(index), but have to tell which type for each
            // column (and a (or the) correct rust type that the postgres type
            // can be converted into. E.g. if field N had pg type TEXT, then
            // it could not be converted to f32, but it can be converted to &str.
            row.get::<usize, &str>(0)
            //row.columns()
            //    .iter()
            //    .map(|column_info| row.get::<&str, column_info.type_()>(column_info.name()))
            //    .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();
    Ok(Json(json!(rows)).into_response())
}

/// /lookup/:lang/:lemma
/// Return articles for a specific lemma (one that does NOT contain wildcard %)
/// Return type:
///   [ [lemma, dictionary_name, and article_id], ... ]
async fn handler_lookup(
    Path((lang, lemma)): Path<(String, String)>,
    State(AppState { connpool }): State<AppState>,
) -> Result<Response, AppError> {
    let client = connpool.get().await?;

    // TODO is this injection safe?
    let statement = r#"
        SELECT
            articles.lemma,
            dictionaries.name,
            articles.id
        FROM
            articles
        INNER JOIN
            dictionaries
        ON
            articles.dictionary = dictionaries.id
        WHERE
            lang = $1
            AND
            lemma LIKE $2
        ;
    "#;
    let rows = client
        .query(statement, &[&lang, &lemma])
        .await
        .map_err(|e| anyhow!(e))?;
    let rows = rows
        .iter()
        .map(|row| {
            (
                row.get::<usize, &str>(0),
                row.get::<usize, &str>(1),
                row.get::<usize, i32>(2),
            )
        })
        .collect::<Vec<_>>();
    Ok(Json(json!(rows)).into_response())
}

/// /article/:id
async fn handler_article(
    Path(id): Path<i32>,
    State(AppState { connpool }): State<AppState>,
) -> Result<Response, AppError> {
    let client = connpool.get().await?;
    let statement = "SELECT rendered FROM articles WHERE id = $1;";
    let rows = client
        .query(statement, &[&id])
        .await
        .map_err(|e| anyhow!(e))?;
    let rows = rows
        .iter()
        .map(|row| row.get::<usize, &str>(0))
        .collect::<Vec<_>>();
    Ok(Json(json!(rows)).into_response())
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env().unwrap_or_else(|_| {
                // axum logs rejections from built-in extractors with the `axum::rejection`
                // target, at `TRACE` level. `axum::rejection=trace` enables showing those events
                "metadict-api=debug,tower_http=debug,axum::rejection=trace".into()
            }),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    let connpool = ConnectionPool::new();
    let state = AppState {
        connpool: Arc::new(connpool),
    };

    let cors_layer = tower_http::cors::CorsLayer::new()
        .allow_origin(tower_http::cors::Any)
        .allow_methods([http::Method::GET]);

    let app = Router::new()
        .route("/", get(handler_root))
        .route("/search/:lang/:query", get(handler_search))
        .route("/lookup/:lang/:lemma", get(handler_lookup))
        .route("/article/:id", get(handler_article))
        .fallback(handler_404)
        .layer(cors_layer)
        .layer(axum::middleware::from_fn(timing_middleware))
        .with_state(state);

    let listener = match ListenFd::from_env().take_tcp_listener(0).unwrap() {
        // if we are given a tcp listener on listen fd 0, we use that one
        Some(listener) => {
            listener.set_nonblocking(true).unwrap();
            TcpListener::from_std(listener).unwrap()
        }
        // otherwise fall back to local listening
        None => TcpListener::bind("0.0.0.0:3000").await.unwrap(),
    };

    axum::serve(listener, app).await.unwrap();
    Ok(())
}
