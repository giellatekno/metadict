mod pg_connection_pool;
mod timing_middleware;
mod auth;
mod cookie_extractor;

use std::{collections::HashMap, sync::Arc};
use std::sync::OnceLock;
use anyhow::anyhow;
use axum::{
    extract::{Path, Query, State},
    response::{IntoResponse, Response, Redirect},
    routing::get,
    Json, Router,
};
use listenfd::ListenFd;
use serde_json::json;
use tokio::net::TcpListener;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

use crate::pg_connection_pool::ConnectionPool;
use crate::timing_middleware::timing_middleware;

static GH_APP_CONFIG: OnceLock<crate::auth::GhAppConfig> = OnceLock::new();
static JWT_SECRET: OnceLock<Vec<u8>> = OnceLock::new();

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
    concat!(
        env!("CARGO_PKG_NAME"),
        " v",
        env!("CARGO_PKG_VERSION"),
        "\n"
    )
    .into_response()
}

async fn handler_404() -> Response {
    (http::StatusCode::NOT_FOUND, "Not found\n").into_response()
}

/// /auth/callback
/// After a user has authenticated with github - and accepted the installation
/// of our github app (a one time thing, unless it gets revoked) - github will
/// redirect the users browser to this route. It includes an authorization
/// code that we will then send to github.
async fn handler_auth_callback(
    Query(params): Query<HashMap<String, String>>,
) -> Result<Response, AppError> {
    let Some(code) = params.get("code") else {
        return Err(AppError(anyhow!("no 'code' in query params")));
    };

    let client_id = &GH_APP_CONFIG.get().unwrap().client_id;
    let client_secret = &GH_APP_CONFIG.get().unwrap().client_secret;
    let creds = crate::auth::exchange_code_for_access_token(
        client_id,
        client_secret,
        code,
    ).await?;

    use base64::{engine::general_purpose::URL_SAFE, Engine as _};
    let creds = URL_SAFE.encode(creds);
    println!("got auth credentials from github: {:?}", creds);
    let obj = crate::auth::AccessTokenResponse::from_urlencoded_string(creds.clone())?;
    println!("decoded: {:?}", obj);
    let gh_user = crate::auth::gh_get_user(&obj.access_token).await?;

    // check if gh user is member of the team
    let cookie = match crate::auth::check_restricted_access(&gh_user, &obj.access_token).await {
        Ok(user_has_restricted_access) => {
            let jwt = crate::auth::create_jwt(&gh_user, user_has_restricted_access, JWT_SECRET.get().unwrap())?;
            format!("metadict-creds={jwt}; Path=/")
        },
        Err(e) => {
            println!("{}", e);
            return Err(e.into());
        }
    };


    Ok(
        (
            [(http::header::SET_COOKIE, cookie)],
            Redirect::to("http://localhost:5173/"),
        )
        .into_response()
    )
}

/// /auth/logout
async fn handler_auth_logout(
    Query(params): Query<HashMap<String, String>>
) -> Response {
    let redirect_url = match params.get("redirect") {
        Some(v) => v,
        None => "http://localhost:5173/",
    };

    (
        [(http::header::SET_COOKIE, "metadict-creds=; Max-Age=0; Path=/")],
        Redirect::to(redirect_url),
    )
    .into_response()
}

use crate::cookie_extractor::Cookies;

/// /search/:lang/:query
/// Finds all matching lemmas to the :query, in all dictionaries.
async fn handler_search(
    Path((lang, query)): Path<(String, String)>,
    cookies: Cookies,
    State(AppState { connpool }): State<AppState>,
) -> Result<Response, AppError> {
    let client = connpool.get().await?;
    let creds: Option<String> = match cookies.to_cookies() {
        None => None,
        Some(cookies) => {
            cookies.iter()
                .find(|cookie| cookie.name() == "metadict-gh-creds")
                .map(|cookie| cookie.value().to_string())
        },
    };
    
    let user_can_see_restricted = true;

    //println!("creds in cookie: {:?}", creds);

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
    cookies: Cookies,
    State(AppState { connpool }): State<AppState>,
) -> Result<Response, AppError> {
    let client = connpool.get().await?;

    let can_see_closed = crate::cookie_extractor::validate_jwt(cookies);
    println!("handler_lookup: can_see_closed={}", can_see_closed);

    // TODO is this injection safe?
    let statement = if can_see_closed {
        r#"
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
        "#
    } else {
        r#"
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
                AND
                dictionaries.closed = FALSE
            ;
        "#
    };
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

    // TODO: Validate jwt, so it requires login to see closed articles!
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
async fn main() -> anyhow::Result<()> {
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

    GH_APP_CONFIG.set(crate::auth::GhAppConfig::read_config()?).unwrap();
    JWT_SECRET.set(std::fs::read("jwt_secret.txt")?).unwrap();

    let connpool = ConnectionPool::new();
    let state = AppState {
        connpool: Arc::new(connpool),
    };

    let cors_layer = tower_http::cors::CorsLayer::new()
        .allow_origin("http://localhost:5173".parse::<http::HeaderValue>().unwrap())
        .allow_credentials(true)
        .allow_methods([http::Method::GET]);

    let app = Router::new()
        .route("/", get(handler_root))
        .route("/search/:lang/:query", get(handler_search))
        .route("/lookup/:lang/:lemma", get(handler_lookup))
        .route("/article/:id", get(handler_article))
        .route("/auth/callback", get(handler_auth_callback))
        .route("/auth/logout", get(handler_auth_logout))
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
