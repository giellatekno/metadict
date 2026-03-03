mod auth;
mod base64;
mod cookie_extractor;
mod db;
mod ghapi;
mod iat;
mod jwt;
mod our_jwt;
mod pg_connection_pool;
mod timing_middleware;

use anyhow::anyhow;
use axum::extract::{Path, Query, State};
use axum::response::{IntoResponse, Redirect, Response};
use axum::{http::HeaderMap, routing::get, Json, Router};
use listenfd::ListenFd;
use serde_json::json;
use std::collections::HashMap;
use std::sync::OnceLock;
use tokio::net::TcpListener;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

use crate::cookie_extractor::Cookies;
use crate::our_jwt::COOKIE_NAME;
use crate::pg_connection_pool::ConnectionPool;
use crate::timing_middleware::timing_middleware;

static GH_APP_CONFIG: OnceLock<crate::auth::GhAppConfig> = OnceLock::new();
static JWT_SECRET: OnceLock<Vec<u8>> = OnceLock::new();
static FRONTEND: OnceLock<String> = OnceLock::new();

#[derive(Clone)]
struct AppState {
    /// The connection pool to the PostgreSQL database.
    connpool: ConnectionPool,
    iat: crate::iat::IAT,
}

#[derive(Default)]
struct RedirectError {
    description: Option<String>,
    message: Option<String>,
    clear_cookie: bool,
    url: String,
}

enum AppError {
    Redirect(RedirectError),
    Other(anyhow::Error),
}

impl From<anyhow::Error> for AppError {
    fn from(err: anyhow::Error) -> Self {
        Self::Other(err)
    }
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        match self {
            AppError::Redirect(redirect) => {
                let mut query_params = vec![];
                tracing::error!(desc = ?redirect.description, msg = ?redirect.message, "a function caused a redirect error");
                if let Some(desc) = redirect.description {
                    query_params.push(("description", desc));
                };
                if let Some(message) = redirect.message {
                    query_params.push(("message", message));
                };
                let url = reqwest::Client::new()
                    .get(redirect.url.to_string())
                    .query(&query_params)
                    .build()
                    .unwrap();
                /* rust: temporary value dropped while borrowed */
                let url = url.url().as_str();
                if redirect.clear_cookie {
                    let cookie = String::from("metadict-api=; Max-Age=0; Path=/");
                    let cookie_header = (http::header::SET_COOKIE, cookie);
                    ([cookie_header], Redirect::to(url)).into_response()
                } else {
                    Redirect::to(url).into_response()
                }
            }
            AppError::Other(e) => {
                tracing::error!(error = ?e, "an error occured");
                (
                    http::StatusCode::INTERNAL_SERVER_ERROR,
                    #[cfg(debug_assertions)]
                    format!("{e}"),
                    #[cfg(not(debug_assertions))]
                    "Something went wrong",
                )
                    .into_response()
            }
        }
    }
}

// fn internal_error<E>(err: E) -> (http::StatusCode, String)
// where
//     E: std::error::Error,
// {
//     (
//         http::StatusCode::INTERNAL_SERVER_ERROR,
//         #[cfg(debug_assertions)]
//         err.to_string(),
//         #[cfg(not(debug_assertions))]
//         "Something went wrong".to_string(),
//     )
// }

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

macro_rules! redirect_to_errorpage {
    (msg=$msg:expr) => {{
        let msg = $msg.to_string();
        tracing::trace!(msg, "redirect_to_errorpage");
        AppError::Redirect(RedirectError {
            message: Some(msg),
            description: None,
            clear_cookie: true,
            url: format!("{}/error", FRONTEND.get().unwrap()),
        })
    }};
    (msg=$msg:expr, desc=$desc:expr) => {{
        let msg = $msg.to_string();
        let description = $desc.to_string();
        tracing::trace!(msg, description, "redirect_to_errorpage");
        AppError::Redirect(RedirectError {
            message: Some(msg),
            description: Some(description),
            clear_cookie: true,
            url: format!("{}/error", FRONTEND.get().unwrap()),
        })
    }};
    (desc=$desc:expr) => {{
        let description = $desc.to_string();
        tracing::trace!(description, "redirect_to_errorpage");
        AppError::Redirect(RedirectError {
            message: None,
            description: Some(description),
            clear_cookie: true,
            url: format!("{}/error", FRONTEND.get().unwrap()),
        })
    }};
    (message=$msg:expr, description=$desc:expr, clear_cookie=true) => {{
        let msg = $msg.to_string();
        let description = $desc.to_string();
        tracing::trace!(msg, description, "redirect_to_errorpage, also clear cookie");

        let cookie = cookie::Cookie::build(COOKIE_NAME)
            .path("/")
            .http_only(true)
            .secure(true)
            .same_site(cookie::SameSite::None)
            .removal()
            .build()
            .to_string();
        let cookie_header = (http::header::SET_COOKIE, cookie);
        let url = format!(
            "{}/error?description={}&message={}",
            FRONTEND.get().unwrap(),
            $desc,
            $msg
        );
        let response = ([cookie_header], Redirect::to(&url)).into_response();
        return Ok(response);
    }};
}

/// /auth/callback
/// After a user has authenticated with github - and accepted the installation
/// of our github app (a one time thing, unless it gets revoked) - github will
/// redirect the users browser to this route. It includes an authorization
/// code that we will then send to github.
#[tracing::instrument(level = "trace")]
async fn handler_auth_callback(
    State(AppState { iat, .. }): State<AppState>,
    Query(params): Query<HashMap<String, String>>,
) -> Result<Response, AppError> {
    let code = params
        .get("code")
        .ok_or_else(|| redirect_to_errorpage!(msg = "no 'code' in query params"))?;
    tracing::trace!(code, "query param 'code'");

    let client_id = &GH_APP_CONFIG.get().unwrap().client_id;
    let secret = &GH_APP_CONFIG.get().unwrap().client_secret;
    let creds = ghapi::exchange_code_for_access_token(client_id, secret, code)
        .await
        .map_err(|e| {
            use std::error::Error;

            if let Some(source) = e.source() {
                tracing::error!(source, "source");
            } else {
                tracing::warn!("no source...");
            }
            redirect_to_errorpage!(msg = e, desc = "exchange access code")
        })?;

    let access_token = &creds.access_token;
    tracing::trace!(access_token, "got access token");

    tracing::trace!("get access token");
    let gh_user = ghapi::get_user(access_token)
        .await
        .map_err(|e| redirect_to_errorpage!(msg = e, desc = "querying github api for user info"))?;

    let can_see_closed = ghapi::user_in_team(
        &gh_user.login,
        "giellatekno",
        "metadictionary-access",
        &iat.get().await?,
    )
    .await
    .map_err(|e| redirect_to_errorpage!(msg = e, desc = "calling ghapi user in team"))?;

    let jwt_string = crate::our_jwt::OurJwt::builder()
        .sub(gh_user.login.to_string())
        .restricted_dicts(can_see_closed)
        .gh_uat(creds.access_token)
        .gh_refresh_token(creds.refresh_token)
        .gh_login_name(gh_user.login)
        .gh_fullname(gh_user.name.unwrap_or_else(|| "".to_string()).to_string())
        .gh_avatar_url(gh_user.avatar_url.to_string())
        .build()
        .expect("Our jwt always builds")
        .encode(JWT_SECRET.get().unwrap())
        .expect("encoding our jwt as actual jwt is ok");

    let cookie = cookie::Cookie::build((COOKIE_NAME, jwt_string))
        .path("/")
        .secure(true)
        .http_only(true)
        .same_site(cookie::SameSite::None)
        .build()
        //.encoded()
        //.stripped()
        .to_string();

    // anders: Tried to send the data to sveltekit, and have sveltekit set
    // the cookie, so that it would always send it on requests

    let cookie_header = (http::header::SET_COOKIE, cookie);
    tracing::trace!("handler_auth_callback returning");

    //let login_route = format!("{}", FRONTEND.get().unwrap(), cookie);
    Ok(([cookie_header], Redirect::to(FRONTEND.get().unwrap())).into_response())
    //Ok(Redirect::to(&login_route).into_response())
}

/// /auth/logout
async fn handler_auth_logout(Query(params): Query<HashMap<String, String>>) -> Response {
    let redirect_url: &str = match params.get("redirect") {
        Some(v) => v,
        None => FRONTEND.get().unwrap(),
    };

    let cookie = cookie::Cookie::build(crate::our_jwt::COOKIE_NAME)
        .path("/")
        .http_only(true)
        .secure(true)
        .removal()
        .build()
        .to_string();

    (
        [(http::header::SET_COOKIE, cookie)],
        Redirect::to(redirect_url),
    )
        .into_response()
}

#[derive(Debug, serde::Deserialize)]
struct SearchQueryParams {
    l2: Option<String>,
}

#[allow(non_camel_case_types)]
#[derive(serde::Serialize, strum::Display, strum::EnumString)]
pub enum Language {
    deu,
    eng,
    est,
    fin,
    nob,
    sma,
    sme,
    smj,
    smn,
    swe,
}

pub const LANGUAGES_STR_QUOTED_COMMA_SEPARATED: &str =
    "'deu','eng','est','fin','nob','sma','sme','smj','smn','swe'";

#[derive(Debug, thiserror::Error)]
pub enum LanguageError {
    #[error("not 3 characers long (was {0})")]
    InvalidLength(usize),
    #[error("non a-z character '{0}' at position {1}")]
    InvalidChar(char, usize),
}

fn parse_l2s(s: &str) -> Result<Vec<Language>, &'static str> {
    const ERR: &str = "invalid lang, choose between 'deu,eng,est,fin,nob,sma,sme,smj,smn,swe'";
    s.trim()
        .split(',')
        .map(|s| s.parse().map_err(|_| ERR))
        .collect()
}

macro_rules! handle_can_see_closed {
    ($cookies:ident, $iat:ident, $headers:ident) => {{
        let jwt = match our_jwt::DecodedJwt::try_from($cookies) {
            Ok(jwt) => Some(jwt),
            Err(our_jwt::CookieParseError::NoCookies)
            | Err(our_jwt::CookieParseError::NoMetadictCredsCookie) => None,
            Err(our_jwt::CookieParseError::DecodeError(inner_error)) => {
                redirect_to_errorpage!(
                    message = inner_error,
                    description = "error while decoding jwt",
                    clear_cookie = true
                );
            }
        };
        match jwt {
            Some(jwt) => match jwt.refresh_if_needed(&$iat.get().await.unwrap()).await {
                Ok(None) => jwt.restricted_dicts(),
                Ok(Some(new_jwt)) => {
                    $headers.insert(http::header::SET_COOKIE, new_jwt.to_cookie());
                    new_jwt.restricted_dicts()
                }
                Err(e) => {
                    redirect_to_errorpage!(
                        message = e,
                        description = "error while refreshing jwt",
                        clear_cookie = true
                    );
                }
            },
            None => false,
        }
    }};
}

/// /search/:lang/:query
/// Finds all matching lemmas to the :query, in all dictionaries.
async fn handler_search(
    cookies: Cookies,
    Path((lang, query)): Path<(String, String)>,
    Query(SearchQueryParams { l2 }): Query<SearchQueryParams>,
    State(AppState { connpool, iat }): State<AppState>,
) -> Result<Response, AppError> {
    let db = connpool.get().await?;
    let mut headers = HeaderMap::new();
    let can_see_closed = handle_can_see_closed!(cookies, iat, headers);
    let l2s = match l2 {
        Some(s) => match parse_l2s(&s) {
            Ok(l2s) => Some(l2s),
            Err(e) => return Err(AppError::from(anyhow!("invalid l2: {e}"))),
        },
        None => None,
    };

    if query.bytes().all(|b| b == b'%') {
        return Ok((headers, Json(json!({ "error": "narrow your search" }))).into_response());
    }

    let rows = crate::db::find_lemmas(db, &lang, &query, l2s.as_deref(), can_see_closed).await?;
    Ok((headers, Json(json!(rows))).into_response())
}

/// /lookup/:lang/:lemma
/// Return articles for a specific lemma (one that does NOT contain wildcard %)
/// Return type:
///   [ [lemma, dictionary_name, and article_id], ... ]
async fn handler_lookup(
    cookies: Cookies,
    Path((lang, lemma)): Path<(String, String)>,
    State(AppState { connpool, iat }): State<AppState>,
) -> Result<Response, AppError> {
    let db = connpool.get().await?;
    let mut headers = HeaderMap::new();
    let can_see_closed = handle_can_see_closed!(cookies, iat, headers);
    let rows = crate::db::find_articles_for_lemma(db, &lang, &lemma, can_see_closed).await?;
    Ok((headers, Json(json!(rows))).into_response())
}

/// /article/:id
async fn handler_article(
    cookies: Cookies,
    Path(id): Path<i32>,
    State(AppState { connpool, iat }): State<AppState>,
) -> Result<Response, AppError> {
    let mut headers = HeaderMap::new();
    let closed = handle_can_see_closed!(cookies, iat, headers);
    let conn1 = connpool.get().await?;
    let conn2 = connpool.get().await?;
    let conn3 = connpool.get().await?;
    let articles = tokio::spawn(crate::db::find_article_by_id(conn1, id, closed));
    let neighbors = tokio::spawn(crate::db::find_neighboring_articles(conn2, id, closed));
    let dictionary = tokio::spawn(crate::db::find_dictionary_by_article_id(conn3, id, closed));
    let joined = tokio::join!(articles, neighbors, dictionary);
    let (articles, neighbors, dictionary) = match joined {
        (Ok(Ok(a)), Ok(Ok(b)), Ok(Ok(c))) => (a, b, c),
        _ => return Err(AppError::Other(anyhow::anyhow!("failed"))),
    };
    let body = json!({
        "articles": articles,
        "neighbors": neighbors,
        "dictionary_info": dictionary,
    });
    Ok((headers, Json(body)).into_response())
}

async fn shutdown_signal() {
    use tokio::signal;

    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env().unwrap_or_else(|_| {
                // axum logs rejections from built-in extractors with the `axum::rejection`
                // target, at `TRACE` level. `axum::rejection=trace` enables showing those events
                "metadict_api=trace,tower_http=debug,axum::rejection=trace".into()
            }),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    GH_APP_CONFIG
        .set(crate::auth::GhAppConfig::read_config()?)
        .unwrap();
    JWT_SECRET.set(std::fs::read("jwt_secret.txt")?).unwrap();
    FRONTEND
        .set(std::env::var("FRONTEND").unwrap_or_else(|_| {
            tracing::warn!("Env var FRONTEND not set, using default of localhost:5173");
            String::from("http://localhost:5173")
        }))
        .expect("Nobody else set the FRONTEND static at the same time as this.");

    let state = AppState {
        connpool: ConnectionPool::new(),
        iat: crate::iat::IAT::new(),
    };

    // do a check on the connection to the database on startup
    let _ = state.connpool.get().await.inspect_err(move |e| {
        use deadpool_postgres::PoolError;
        match e.downcast_ref::<PoolError>() {
            Some(e) => match e {
                PoolError::Timeout(_timeout_type) => {
                    tracing::warn!("timeout");
                }
                PoolError::Backend(backend_error) => {
                    tracing::warn!(error = backend_error.to_string(), "backend");
                }
                PoolError::Closed => {}
                PoolError::NoRuntimeSpecified => {}
                PoolError::PostCreateHook(_x) => {}
            },
            None => unreachable!("state.connpool.get() is only PoolError"),
        }

        tracing::warn!(error = e.to_string(), "Could not connect to db on startup");
    });

    // does this simply work?
    let cors_layer = tower_http::cors::CorsLayer::very_permissive();
    //let cors_layer = tower_http::cors::CorsLayer::new()
    //    .allow_origin([
    //        FRONTEND
    //            .get()
    //            .unwrap()
    //            .parse::<http::HeaderValue>()
    //            .unwrap(),
    //        // When sveltekit internally calls the api, the hostname is this
    //        // special podman domain name...I think
    //        "http://host.containers.internal".parse::<http::HeaderValue>().unwrap(),
    //    ])
    //    // Error: Allow-Credentials: true  cannot exist at the same time as
    //    // Allow-Origin: *
    //    //.allow_origin(tower_http::cors::Any)
    //    .allow_credentials(true)
    //    .allow_methods([http::Method::GET]);

    let trace_layer = tower_http::trace::TraceLayer::new_for_http();

    let app = Router::new()
        .route("/", get(handler_root))
        .route("/search/{lang}/{query}", get(handler_search))
        .route("/lookup/{lang}/{lemma}", get(handler_lookup))
        .route("/article/{id}", get(handler_article))
        .route("/auth/callback", get(handler_auth_callback))
        .route("/auth/logout", get(handler_auth_logout))
        .fallback(handler_404)
        .layer(cors_layer)
        .layer(trace_layer)
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

    let port = listener.local_addr().unwrap().port();
    tracing::info!(port = port, "Metadict started");

    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
    Ok(())
}
