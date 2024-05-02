/// IAT - Installation Access Token
/// Code for generating the JWT we need to query the GH API for an IAT

use serde::Serialize;
use std::sync::{Arc, OnceLock};
use tokio::sync::RwLock;

// ID of installation of app, as in, the number in the url at
// https://github.com/organizations/giellatekno/settings/installations/50166123
const INSTALLATION_ID: u32 = 50166123;
// app id, as in the "App Id" on
// https://github.com/organizations/giellatekno/settings/apps/giellatekno-metadictionary
const APP_ID: u64 = 880740;

// Towards the bottom of the page
// https://github.com/organizations/giellatekno/settings/apps/giellatekno-metadictionary
// There is a "private key" area. This is the key we need to sign the JWT
// that we need to get an IAT, and we store it in OnceLock, and load it
// from a file at the beginning of the program.
pub static IAT_PRIVATE_KEY: OnceLock<Vec<u8>> = OnceLock::new();

// The key is stored in this file
// TODO store this path in a Config instead?
const IAT_PK_PATH: &str = "giellatekno-metadictionary.2024-04-26.private-key.pem";

pub struct IAT(Arc<RwLock<Option<Inner>>>);

impl Clone for IAT {
    fn clone(&self) -> Self {
        Self(Arc::clone(&self.0))
    }
}

impl IAT {
    pub fn new() -> Self {
        Self(Arc::new(RwLock::new(None)))
    }

    /// Get the current IAT, as long as it hasn't expired.
    /// Create a new one if there is None.
    pub async fn get(&self) -> anyhow::Result<String> {
        let inner = self.0.read().await;
        match *inner {
            None => {
                drop(inner);
                let mut inner_guard = self.0.write().await;
                let inner = Inner::new().await?;
                let token = inner.token.to_owned();
                *inner_guard = Some(inner);
                Ok(token)
            }
            Some(ref inner) => {
                if !inner.has_expired() {
                    Ok(inner.token.to_owned())
                } else {
                    let new_inner = Inner::new().await?;
                    let mut inner_guard = self.0.write().await;
                    let token = new_inner.token.to_owned();
                    *inner_guard = Some(new_inner);
                    Ok(token)
                }
            }
        }
        
    }
}

/// What we need from the IAT response body that we get
pub struct Inner {
    token: String,
    expires_at: chrono::DateTime<chrono::offset::FixedOffset>,
}

impl Inner {
    pub async fn new() -> anyhow::Result<Self> {
        let iat_jwt = generate_app_jwt();
        let resp_body = crate::ghapi::get_app_installation_access_token(
            INSTALLATION_ID, &iat_jwt).await?;
        let expires_at = chrono::DateTime::parse_from_rfc3339(&resp_body.expires_at)?;
        let token = resp_body.token;
        Ok(Self {
            token,
            expires_at,
        })
    }

    pub fn has_expired(&self) -> bool {
        self.expires_at < chrono::offset::Utc::now()
    }

    pub fn token(&self) -> &str {
        self.token.as_str()
    }
}

#[derive(Serialize)]
struct AppJwtClaims {
    /// Issued at time
    iat: u64,
    /// JWT expiration time (10 minutes maximum)
    exp: u64,
    /// GitHub App's identifier (an integer, the app ID)
    iss: u64,
}

pub fn generate_app_jwt() -> String {
    let header = jsonwebtoken::Header::new(jsonwebtoken::Algorithm::RS256);

    let iat_private_key = IAT_PRIVATE_KEY
        .get_or_init(|| std::fs::read(IAT_PK_PATH).unwrap());
    let signing_key = jsonwebtoken::EncodingKey::from_rsa_pem(iat_private_key)
        .expect("key we gave is RS256, so key validates");
    let now = jsonwebtoken::get_current_timestamp();

    let claims = AppJwtClaims {
        iat: now,
        exp: now + 60 * 5,
        iss: APP_ID,
    };
    jsonwebtoken::encode(&header, &claims, &signing_key)
        .expect("jwt encoding succeeds, because we used correct key/algo combo")
}
