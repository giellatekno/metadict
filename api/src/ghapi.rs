use anyhow::Context;
use serde::Deserialize;

/// The json object returned when exchanging the code for an access token, at
/// https://github.com/login/oauth/access_token
#[derive(Debug, Deserialize)]
pub struct AccessTokenResponse {
    /// The user access token. The token starts with "ghu_".
    pub access_token: String,
    /// The number of seconds until access_token expires. If you disabled
    /// expiration of user access tokens, this parameter will be omitted.
    /// The value is always 28800 (8 hours).
    pub expires_in: u64,
    /// The refresh token. If you disabled expiration of user access tokens,
    /// this parameter will be omitted. The token starts with "ghr_".
    pub refresh_token: String,
    /// The number of seconds until refresh_token expires. If you disabled
    /// expiration of user access tokens, this parameter will be omitted.
    /// The value is always 15897600 (6 months).
    pub refresh_token_expires_in: u64,
    /// The scopes that the token has. Unlike a traditional OAuth token, the
    /// user access token is limited to the permissions that both your app
    /// and the user have. This value is always "".
    pub scope: String,
    /// The type of token. The value is always "bearer".
    pub token_type: String,
}

/// Call github.com/login/oauth/access_token
/// with our client id, secret, and code, to get an access token in return
pub async fn exchange_code_for_access_token(
    client_id: &str,
    client_secret: &str,
    code: &str,
) -> anyhow::Result<AccessTokenResponse> {
    Ok(reqwest::Client::new()
        .post("https://github.com/login/oauth/access_token")
        .header("Accept", "application/json")
        .form(&[
            ("client_id", client_id),
            ("client_secret", client_secret),
            ("code", code),
        ])
        .timeout(std::time::Duration::from_secs(6))
        .send()
        .await
        .with_context(|| "POST to https://github.com/login/oauth/access_token")?
        .json()
        .await
        .with_context(|| "decoding json response body")?)
}

#[derive(Deserialize)]
pub struct GhUserResponse {
    pub login: String,
    pub id: i32,
    pub node_id: String,
    pub avatar_url: String,
    pub gravatar_id: String,
    pub url: String,
    pub html_url: String,
    pub followers_url: String,
    pub following_url: String,
    pub gists_url: String,
    pub starred_url: String,
    pub subscriptions_url: String,
    pub organizations_url: String,
    pub repos_url: String,
    pub events_url: String,
    pub received_events_url: String,
    pub r#type: String,
    pub site_admin: bool,
    pub name: Option<String>,
    pub company: Option<String>,
    pub blog: Option<String>,
    pub location: Option<String>,
    pub email: Option<String>,
    pub hireable: Option<bool>,
    pub bio: Option<String>,
    pub twitter_username: Option<String>,
    // bugfix: lene had this field in the response for her user.
    // this field did not exist at all in neither mine nor brede's!
    // serde(default) will deserialize with Default::default()
    // (which is None for Option<T>) if the field is not present
    #[serde(default)]
    pub notification_email: Option<String>,
    pub public_repos: u32,
    pub public_gists: u32,
    pub followers: u32,
    pub following: u32,
    pub created_at: String,
    pub updated_at: String,
}

/// api.github.com/user - get user info, given an access token
pub async fn get_user(access_token: &str) -> anyhow::Result<GhUserResponse> {
    let resp = reqwest::Client::new()
        .get("https://api.github.com/user")
        .header("User-Agent", "reqwest/0.12.3")
        .header("Accept", "application/vnd.github+json")
        .header("Authorization", format!("Bearer {}", access_token))
        .header("X-GitHub-Api-Version", "2022-11-28")
        .timeout(std::time::Duration::from_secs(6))
        .send()
        .await?
        .error_for_status()?;

    let bytes: axum::body::Bytes = resp.bytes().await?;

    let json = match serde_json::from_slice(&bytes) {
        Ok(json) => json,
        Err(e) => {
            let text = match String::from_utf8(bytes.to_vec()) {
                Ok(text) => text,
                Err(_) => {
                    anyhow::bail!("response body bytes from gh api is not a utf-8 string");
                }
            };
            anyhow::bail!("could not decode json: {} - text response is: {}", e, text);
        }
    };

    Ok(json)
}

#[derive(Deserialize)]
pub struct TeamMembershipResponseBody {
    // "active" or "pending" (if team invite hasn't been accepted yet)
    pub state: String,
    // "maintainer" or "member"
    pub role: String,
    // e.g. "https://api.github.com/organizations/54359201/team/9970092/memberships/Phaqui
    pub url: String,
}

/// Query the Github API, to see if a user is a member of a team.
/// Authorization is the Installation App Token.
pub async fn user_in_team(
    login_name: &str,
    org_name: &str,
    team_name: &str,
    iat: &str,
) -> anyhow::Result<bool> {
    let url = format!(
        "https://api.github.com/orgs/{org_name}/teams/{team_name}/memberships/{login_name}"
    );
    let response = reqwest::Client::new()
        .get(&url)
        .header("User-Agent", "reqwest/0.12.3")
        .header("Accept", "application/vnd.github+json")
        .header("Authorization", format!("Bearer {}", iat))
        .header("X-GitHub-Api-Version", "2022-11-28")
        .send()
        .await
        .with_context(|| format!("GET to {url}"))?;

    match response.status() {
        reqwest::StatusCode::OK => {
            let body = response.json::<TeamMembershipResponseBody>().await?;
            Ok(body.state == "active")
        }
        reqwest::StatusCode::NOT_FOUND => Ok(false),
        _ => {
            // checking for expiration of iat is done by the iat code
            let msg = response.text().await?;
            anyhow::bail!(msg)
        }
    }
}

// Fields in this struct must be named exactly, because it will be deserializeds
// from json. But otherwise they are not used, so to silence the compiler,
// we allow dead code in this struct.
#[derive(serde::Deserialize)]
pub struct RefreshAccessTokenResponseBody {
    /// The user access token. The token starts with "ghu_".
    pub access_token: String,
    /// The number of seconds until access_token expires. If you disabled
    /// expiration of user access tokens, this parameter will be omitted.
    /// The value will always be 28800 (8 hours).
    pub expires_in: u32,
    /// The refresh token. If you disabled expiration of user access tokens,
    /// this parameter will be omitted. The token starts with "ghr_".
    pub refresh_token: String,
    /// The number of seconds until refresh_token expires. If you disabled
    /// expiration of user access tokens, this parameter will be omitted.
    /// The value will always be 15897600 (6 months).
    pub refresh_token_expires_in: u32,
    /// The scopes that the token has. This value will always be an empty string. Unlike a traditional OAuth token, the user access token is limited to the permissions that both your app and the user have.
    pub scope: String,
    /// The type of token. The value will always be "bearer".
    pub token_type: String,
}

// xxx (anders): I don't actually think I need this.
// We only do user authentication once, on login, and that's only
// to get the user id, which we use to see if that user is a part
// of our team. When _our_ jwt token is refreshed, we still just
// use the same user name from the first login. It doesn't matter to
// us that the login token has expired at that point, because we use
// the IAT to check user membership - we never use the user token
// for anything (except getting the username, and making sure the
// user has a github user).
//pub async fn refresh_access_token(
//    refresh_token: &str,
//    client_id: &str,
//    client_secret: &str,
//) -> anyhow::Result<RefreshAccessTokenResponseBody> {
//    Ok(reqwest::Client::new()
//        .post("https://github.com/login/oauth/access_token")
//        .header("User-Agent", "reqwest/0.12.3")
//        .header("Accept", "application/vnd.github+json")
//        .header("X-GitHub-Api-Version", "2022-11-28")
//        .json(&serde_json::json!({
//            "client_id": client_id,
//            "client_secret": client_secret,
//            "grant_type": "refresh",
//            "refresh_token": refresh_token,
//        }))
//        .send()
//        .await
//        .with_context(|| "POST to https://github.com/login/oauth/access_token")?
//        .json()
//        .await
//        .with_context(|| "decoding json response body")?)
//}

// e.g. {"token":"ghs_xOgq7vewfbFdUdShzybGhRrAOdnwVo26WTic","expires_at":"2024-04-29T11:16:07Z","permissions":{"members":"read"},"repository_selection":"selected"}

#[derive(Deserialize)]
pub struct Permissions {
    pub members: String,
}

#[derive(Deserialize)]
pub struct IatResponseBody {
    pub token: String,
    pub expires_at: String,
    pub permissions: Permissions,
    pub repository_selection: String,
}

/// Get an installation access token, using the jwt we created
pub async fn get_app_installation_access_token(
    installation_id: u32,
    jwt: &str,
) -> anyhow::Result<IatResponseBody> {
    let url = format!("https://api.github.com/app/installations/{installation_id}/access_tokens");
    Ok(reqwest::Client::new()
        .post(&url)
        .header("User-Agent", "reqwest/0.12.3")
        .header("Accept", "application/vnd.github+json")
        .header("X-GitHub-Api-Version", "2022-11-28")
        .header("Authorization", format!("Bearer {jwt}"))
        .send()
        .await
        .with_context(|| format!("POST to {url}"))?
        .json()
        .await?)
}
