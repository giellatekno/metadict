/// Authenticating and authorization with Github-related functionality

use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use anyhow::anyhow;

#[derive(Debug, Deserialize)]
pub struct GhAppConfig {
    pub client_id: String,
    pub client_secret: String,
}

impl GhAppConfig {
    pub fn read_config() -> Result<Self, config::ConfigError> {
        config::Config::builder()
            .add_source(config::File::from(PathBuf::from("./gh_app.toml")))
            .build()?
            .try_deserialize()
    }
}


#[derive(Debug, Deserialize)]
pub struct AccessTokenResponse {
    /// base64-encoded json object (I think)
    pub access_token: String,
    /// always "bearer"
    token_type: String,
    /// Comma-separated list of claims
    scope: String,
}

impl AccessTokenResponse {
    pub fn from_urlencoded_string(s: String) -> anyhow::Result<Self> {
        use base64::{engine::general_purpose::URL_SAFE, Engine as _};
        let bytes = URL_SAFE.decode(s).map_err(|e| anyhow::anyhow!(e))?;
        let obj = serde_json::from_slice::<Self>(&bytes)
            .map_err(|e| anyhow::anyhow!(e))?;
        Ok(obj)
    }
}

/// Call github.com/login/oauth/access_token
/// with our client id, secret, and code, to get an access token in return
pub async fn exchange_code_for_access_token(
    client_id: &str,
    client_secret: &str,
    code: &str,
) -> anyhow::Result<String> {
    Ok(reqwest::Client::new()
        .post("https://github.com/login/oauth/access_token")
        .header("Accept", "application/json")
        .form(&[
            ("client_id", client_id),
            ("client_secret", client_secret),
            ("code", code),
        ])
        .send()
        .await?
        .text()
        .await?)
}

#[derive(Deserialize)]
pub struct GhUserResponse {
    //"Phaqui"
    pub login: String,
    //204055,
    id: i32,
    //"MDQ6VXNlcjIwNDA1NQ==",
    node_id: String,
    //"https://avatars.githubusercontent.com/u/204055?v=4",
    pub avatar_url: String,
    //"",
    gravatar_id: String,
    //"https://api.github.com/users/Phaqui",
    url: String,
    //"https://github.com/Phaqui",
    html_url: String,
    //"https://api.github.com/users/Phaqui/followers",
    followers_url: String,
    //"https://api.github.com/users/Phaqui/following{/other_user}",
    following_url: String,
    //"https://api.github.com/users/Phaqui/gists{/gist_id}",
    gists_url: String,
    //"https://api.github.com/users/Phaqui/starred{/owner}{/repo}",
    starred_url: String,
    //"https://api.github.com/users/Phaqui/subscriptions",
    subscriptions_url: String,
    //"https://api.github.com/users/Phaqui/orgs",
    organizations_url: String,
    //"https://api.github.com/users/Phaqui/repos",
    repos_url: String,
    //"https://api.github.com/users/Phaqui/events{/privacy}",
    events_url: String,
    //"https://api.github.com/users/Phaqui/received_events",
    received_events_url: String,
    //"User",
    // remember: "type", not "type_" (but type is a keyword in rust)
    r#type: String,
    //false,
    site_admin: bool,
    //"Anders Lorentsen",
    pub name: String,
    //null,
    company: Option<String>,
    //"",
    blog: String,
    //null,
    location: Option<String>,
    //null,
    email: Option<String>,
    //null,
    hireable: Option<bool>,
    //null,
    bio: Option<String>,
    //null,
    twitter_username: Option<String>,
    //15,
    public_repos: u32,
    //4,
    public_gists: u32,
    //10,
    followers: u32,
    //1,
    following: u32,
    //"2010-02-15T16:31:59Z",
    created_at: String,
    //"2024-04-03T12:19:15Z"
    updated_at: String,
}

/// api.github.com/user - get user info, given an access token
pub async fn gh_get_user(access_token: &str) -> anyhow::Result<GhUserResponse> {
    let user_req_resp = reqwest::Client::new()
        .get("https://api.github.com/user")
        .header("User-Agent", "reqwest/0.12.3")
        .header("Accept", "application/vnd.github+json")
        .header("Authorization", format!("Bearer {}", access_token))
        .header("X-GitHub-Api-Version", "2022-11-28")
        .send()
        .await
        .map_err(|e| anyhow!(e))?
        .text()
        .await
        .map_err(|e| anyhow!(e))?;
    Ok(serde_json::from_str(&user_req_resp)?)
}
