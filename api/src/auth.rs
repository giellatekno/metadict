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

#[derive(Deserialize)]
pub struct GhUserResponse {
    //"Phaqui"
    pub login: String,
    //204055,
    id: i32,
    //"MDQ6VXNlcjIwNDA1NQ==",
    node_id: String,
    //"https://avatars.githubusercontent.com/u/204055?v=4",
    avatar_url: String,
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

#[derive(Deserialize)]
struct TeamMembershipResponse {
    // "active" or "pending" (if team invite hasn't been accepted yet)
    state: String,
    // "maintainer" or "member"
    role: String,
    // e.g. "https://api.github.com/organizations/54359201/team/9970092/memberships/Phaqui
    url: String,
}

/// Query the Github API, to see if a user is a member of the
/// "metadictionary-access" team (and therefore has access to restriced
/// dictionaries)
pub async fn check_restricted_access(gh_user: &GhUserResponse, access_token: &str) -> anyhow::Result<bool> {
    let username = &gh_user.login;
    let url = format!("https://api.github.com/orgs/giellatekno/teams/metadictionary-access/memberships/{username}");
    println!("> {url}");
    let response = reqwest::Client::new()
        .get(url)
        .header("User-Agent", "reqwest/0.12.3")
        .header("Accept", "application/vnd.github+json")
        .header("Authorization", format!("Bearer {}", access_token))
        .header("X-GitHub-Api-Version", "2022-11-28")
        .send()
        .await
        .map_err(|e| anyhow!(e))?;

    match response.status() {
        reqwest::StatusCode::OK => {
            let parsed = response.json::<TeamMembershipResponse>().await?;
            Ok(parsed.state == "active")
        }
        _ => {
            Err(anyhow!("non 200"))
        }
    }
}

// Our jwt
#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    aud: String,   // Optional. Audience
    exp: usize,    // Required (validate_exp defaults to true in validation). Expiration time (as UTC timestamp)
    iat: usize,    // Optional. Issued at (as UTC timestamp)
    iss: String,   // Optional. Issuer
    //nbf: usize,    // Optional. Not Before (as UTC timestamp)
    sub: String,   // Optional. Subject (whom token refers to)
    restricted_dicts: bool,
    gh_fullname: String,
    gh_avatar_url: String,
}

pub fn create_jwt(gh_user: &GhUserResponse, has_restricted_access: bool, jwt_key: &[u8]) -> anyhow::Result<String> {
    let header = jsonwebtoken::Header::default();
    let iat = jsonwebtoken::get_current_timestamp();
    let exp = iat + 60 * 5;
    let claims = Claims {
        aud: "".to_string(),
        exp: exp.try_into()?,
        iat: iat.try_into()?,
        iss: "Giellatekno".to_string(),
        sub: gh_user.login.to_string(),
        restricted_dicts: has_restricted_access,
        gh_fullname: gh_user.name.to_string(),
        gh_avatar_url: gh_user.avatar_url.to_string(),
    };
    let key = jsonwebtoken::EncodingKey::from_secret(jwt_key);
    Ok(jsonwebtoken::encode(&header, &claims, &key)?)
}
