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

use axum::{
    extract::{Path, Query, State},
    http::HeaderMap,
    response::{IntoResponse, Redirect, Response},
    routing::get,
    Json, Router,
};
use listenfd::ListenFd;
use serde_json::json;
use std::collections::HashMap;
use std::sync::OnceLock;
use tokio::net::TcpListener;
use tracing::{debug, error};
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
                error!(desc = ?redirect.description, msg = ?redirect.message, "a function caused a redirect error");
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
                    let cookie = format!("metadict-api=; Max-Age=0; Path=/");
                    let cookie_header = (http::header::SET_COOKIE, cookie);
                    ([cookie_header], Redirect::to(url)).into_response()
                } else {
                    Redirect::to(url).into_response()
                }
            }
            AppError::Other(e) => {
                error!(error = ?e, "an error occured");
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
    (msg=$msg:expr) => {
        AppError::Redirect(RedirectError {
            message: Some($msg.to_string()),
            description: None,
            clear_cookie: true,
            url: format!("{}/error", FRONTEND.get().unwrap()),
        })
    };
    (msg=$msg:expr, desc=$desc:expr) => {
        AppError::Redirect(RedirectError {
            message: Some($msg.to_string()),
            description: Some($desc.to_string()),
            clear_cookie: true,
            url: format!("{}/error", FRONTEND.get().unwrap()),
        })
    };
    (desc=$desc:expr) => {
        AppError::Redirect(RedirectError {
            message: None,
            description: Some($desc.to_string()),
            clear_cookie: true,
            url: format!("{}/error", FRONTEND.get().unwrap()),
        })
    };
    (message=$msg:expr, description=$desc:expr, clear_cookie=true) => {{
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
async fn handler_auth_callback(
    State(AppState { iat, .. }): State<AppState>,
    Query(params): Query<HashMap<String, String>>,
) -> Result<Response, AppError> {
    let code = params
        .get("code")
        .ok_or_else(|| redirect_to_errorpage!(msg = "no 'code' in query params"))?;

    let access_token_future = ghapi::exchange_code_for_access_token(
        &GH_APP_CONFIG.get().unwrap().client_id,
        &GH_APP_CONFIG.get().unwrap().client_secret,
        code,
    );

    let creds = access_token_future
        .await
        .map_err(|e| redirect_to_errorpage!(msg = e, desc = "exchange access code"))?;

    let gh_user = ghapi::get_user(&creds.access_token)
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

/// /search/:lang/:query
/// Finds all matching lemmas to the :query, in all dictionaries.
async fn handler_search(
    cookies: Cookies,
    Path((lang, query)): Path<(String, String)>,
    State(AppState { connpool, iat }): State<AppState>,
) -> Result<Response, AppError> {
    let mut headers = HeaderMap::new();
    let can_see_closed = match our_jwt::DecodedJwt::try_from(cookies) {
        Ok(jwt) => {
            debug!(jwt = ?jwt, "jwt is");
            if !jwt.has_expired() {
                jwt.restricted_dicts()
            } else {
                let new_jwt = jwt.refresh(&iat.get().await.unwrap()).await?;
                let can_see_closed = new_jwt.restricted_dicts();
                let new_jwt_string = new_jwt.encode(crate::JWT_SECRET.get().unwrap()).unwrap();
                let cookie = cookie::Cookie::build((COOKIE_NAME, new_jwt_string))
                    .path("/")
                    .http_only(true)
                    .secure(true)
                    .build()
                    .to_string()
                    .parse()
                    .unwrap();
                headers.insert(http::header::SET_COOKIE, cookie);
                can_see_closed
            }
        }
        Err(e @ our_jwt::CookieParseError::NoCookies) => {
            debug!(errorkind = ?e, errortext = ?e.to_string(), "no cookies found");
            false
        }
        Err(our_jwt::CookieParseError::NoMetadictCredsCookie) => {
            debug!("no metadict-creds cookie");
            false
        }
        Err(our_jwt::CookieParseError::DecodeError(inner_error)) => {
            redirect_to_errorpage!(
                message = inner_error,
                description = "error while decoding jwt",
                clear_cookie = true
            );
        }
    };

    let connection = connpool.get().await?;
    let rows = crate::db::find_lemmas(connection, &lang, &query, can_see_closed).await?;
    let response_body = Json(json!(rows));
    let response = (headers, response_body).into_response();
    Ok(response)
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
    let can_see_closed = match our_jwt::DecodedJwt::try_from(cookies) {
        Ok(jwt) => {
            if !jwt.has_expired() {
                jwt.restricted_dicts()
            } else {
                let new_jwt = jwt.refresh(&iat.get().await.unwrap()).await?;
                let can_see_closed = new_jwt.restricted_dicts();
                let new_jwt_string = new_jwt.encode(crate::JWT_SECRET.get().unwrap()).unwrap();
                let cookie = cookie::Cookie::build((COOKIE_NAME, new_jwt_string))
                    .path("/")
                    .http_only(true)
                    .secure(true)
                    .build()
                    .to_string()
                    .parse()
                    .unwrap();
                headers.insert(http::header::SET_COOKIE, cookie);
                can_see_closed
            }
        }
        Err(e @ our_jwt::CookieParseError::NoCookies) => {
            debug!(errorkind = ?e, errortext =?e.to_string(), "no cookies found");
            false
        }
        Err(our_jwt::CookieParseError::NoMetadictCredsCookie) => {
            debug!("no metadict-creds cookie");
            false
        }
        Err(our_jwt::CookieParseError::DecodeError(inner_error)) => {
            redirect_to_errorpage!(
                message = inner_error,
                description = "error while decoding jwt",
                clear_cookie = true
            );
        }
    };

    let rows = crate::db::find_articles_for_lemma(db, &lang, &lemma, can_see_closed).await?;
    let response_body = Json(json!(rows));
    let response = (headers, response_body).into_response();
    Ok(response)
}

/// /article/:id
async fn handler_article(
    cookies: Cookies,
    Path(id): Path<i32>,
    State(AppState { connpool, iat }): State<AppState>,
) -> Result<Response, AppError> {
    let db = connpool.get().await?;
    let mut headers = HeaderMap::new();
    let can_see_closed = match our_jwt::DecodedJwt::try_from(cookies) {
        Ok(jwt) => {
            if !jwt.has_expired() {
                jwt.restricted_dicts()
            } else {
                let new_jwt = jwt.refresh(&iat.get().await.unwrap()).await?;
                let can_see_closed = new_jwt.restricted_dicts();
                let new_jwt_string = new_jwt.encode(crate::JWT_SECRET.get().unwrap()).unwrap();
                let cookie = cookie::Cookie::build((COOKIE_NAME, new_jwt_string))
                    .path("/")
                    .http_only(true)
                    .secure(true)
                    .build()
                    .to_string()
                    .parse()
                    .unwrap();
                headers.insert(http::header::SET_COOKIE, cookie);
                can_see_closed
            }
        }
        Err(our_jwt::CookieParseError::NoCookies)
        | Err(our_jwt::CookieParseError::NoMetadictCredsCookie) => false,
        Err(our_jwt::CookieParseError::DecodeError(inner_error)) => {
            redirect_to_errorpage!(
                message = inner_error,
                description = "error while decoding jwt",
                clear_cookie = true
            );
        }
    };

    let rows = crate::db::find_article_by_id(db, id, can_see_closed).await?;
    let response_body = Json(json!(rows));
    let response = (headers, response_body).into_response();
    Ok(response)
}

// /neighbors/:id
async fn handler_neighbors(
    cookies: Cookies,
    Path(id): Path<i32>,
    State(AppState { connpool, iat }): State<AppState>,
) -> Result<Response, AppError> {
    let db = connpool.get().await?;
    let mut headers = HeaderMap::new();
    let can_see_closed = match our_jwt::DecodedJwt::try_from(cookies) {
        Ok(jwt) => {
            if !jwt.has_expired() {
                jwt.restricted_dicts()
            } else {
                let new_jwt = jwt.refresh(&iat.get().await.unwrap()).await?;
                let can_see_closed = new_jwt.restricted_dicts();
                let new_jwt_string = new_jwt.encode(crate::JWT_SECRET.get().unwrap()).unwrap();
                let cookie = cookie::Cookie::build((COOKIE_NAME, new_jwt_string))
                    .path("/")
                    .http_only(true)
                    .secure(true)
                    .build()
                    .to_string()
                    .parse()
                    .unwrap();
                headers.insert(http::header::SET_COOKIE, cookie);
                can_see_closed
            }
        }
        Err(our_jwt::CookieParseError::NoCookies)
        | Err(our_jwt::CookieParseError::NoMetadictCredsCookie) => false,
        Err(our_jwt::CookieParseError::DecodeError(inner_error)) => {
            redirect_to_errorpage!(
                message = inner_error,
                description = "error while decoding jwt",
                clear_cookie = true
            );
        }
    };
    let rows = crate::db::find_neighboring_articles(db, id, can_see_closed).await?;
    let response_body = Json(json!(rows));
    Ok((headers, response_body).into_response())
}

/// /dictionary/:article_id
/// Given an article, return information about the dictionary it belongs to
async fn handler_dictionary(
    cookies: Cookies,
    Path(id): Path<i32>,
    State(AppState { connpool, iat }): State<AppState>,
) -> Result<Response, AppError> {
    let db = connpool.get().await?;
    let mut headers = HeaderMap::new();
    let can_see_closed = match our_jwt::DecodedJwt::try_from(cookies) {
        Ok(jwt) => {
            if !jwt.has_expired() {
                jwt.restricted_dicts()
            } else {
                let new_jwt = jwt.refresh(&iat.get().await.unwrap()).await?;
                let can_see_closed = new_jwt.restricted_dicts();
                let new_jwt_string = new_jwt.encode(crate::JWT_SECRET.get().unwrap()).unwrap();
                let cookie = cookie::Cookie::build((COOKIE_NAME, new_jwt_string))
                    .path("/")
                    .http_only(true)
                    .secure(true)
                    .build()
                    .to_string()
                    .parse()
                    .unwrap();
                headers.insert(http::header::SET_COOKIE, cookie);
                can_see_closed
            }
        }
        Err(our_jwt::CookieParseError::NoCookies)
        | Err(our_jwt::CookieParseError::NoMetadictCredsCookie) => false,
        Err(our_jwt::CookieParseError::DecodeError(inner_error)) => {
            redirect_to_errorpage!(
                message = inner_error,
                description = "error while decoding jwt",
                clear_cookie = true
            );
        }
    };

    let rows = crate::db::find_dictionary_by_article_id(db, id, can_see_closed).await?;
    let response_body = Json(json!(rows));
    let response = (headers, response_body).into_response();
    Ok(response)
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
    let _ = state.connpool.get().await.inspect_err(|e| {
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
        .route("/search/:lang/:query", get(handler_search))
        .route("/lookup/:lang/:lemma", get(handler_lookup))
        .route("/article/:id", get(handler_article))
        .route("/neighbors/:id", get(handler_neighbors))
        .route("/dictionary/:id", get(handler_dictionary))
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

    axum::serve(listener, app).await.unwrap();
    Ok(())
}
