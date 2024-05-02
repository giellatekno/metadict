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
        .send()
        .await?
        .json()
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
pub async fn get_user(access_token: &str) -> anyhow::Result<GhUserResponse> {
    Ok(reqwest::Client::new()
        .get("https://api.github.com/user")
        .header("User-Agent", "reqwest/0.12.3")
        .header("Accept", "application/vnd.github+json")
        .header("Authorization", format!("Bearer {}", access_token))
        .header("X-GitHub-Api-Version", "2022-11-28")
        .send()
        .await?
        .json()
        .await?)
}

#[derive(Deserialize)]
pub struct TeamMembershipResponseBody {
    // "active" or "pending" (if team invite hasn't been accepted yet)
    pub state: String,
    // "maintainer" or "member"
    role: String,
    // e.g. "https://api.github.com/organizations/54359201/team/9970092/memberships/Phaqui
    url: String,
}

/// Query the Github API, to see if a user is a member of a team.
/// Authorization is the Installation App Token.
pub async fn user_in_team(
    login_name: &str,
    org_name: &str,
    team_name: &str,
    iat: &str,
) -> anyhow::Result<bool> {
    let response = reqwest::Client::new()
        .get(format!(
            "https://api.github.com/orgs/{org_name}/teams/{team_name}/memberships/{login_name}"
        ))
        .header("User-Agent", "reqwest/0.12.3")
        .header("Accept", "application/vnd.github+json")
        .header("Authorization", format!("Bearer {}", iat))
        .header("X-GitHub-Api-Version", "2022-11-28")
        .send()
        .await?;

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

#[derive(serde::Deserialize)]
pub struct RefreshAccessTokenResponseBody {
    /// The user access token. The token starts with "ghu_".
    access_token: String,
    /// The number of seconds until access_token expires. If you disabled
    /// expiration of user access tokens, this parameter will be omitted.
    /// The value will always be 28800 (8 hours).
    expires_in: u32,
    /// The refresh token. If you disabled expiration of user access tokens,
    /// this parameter will be omitted. The token starts with "ghr_".
    refresh_token: String,
    /// The number of seconds until refresh_token expires. If you disabled
    /// expiration of user access tokens, this parameter will be omitted.
    /// The value will always be 15897600 (6 months).
    refresh_token_expires_in: u32,
    /// The scopes that the token has. This value will always be an empty string. Unlike a traditional OAuth token, the user access token is limited to the permissions that both your app and the user have.
    scope: String,
    /// The type of token. The value will always be "bearer".
    token_type: String,
}

pub async fn refresh_access_token(
    refresh_token: &str,
    client_id: &str,
    client_secret: &str,
) -> anyhow::Result<RefreshAccessTokenResponseBody> {
    Ok(reqwest::Client::new()
        .post("https://github.com/login/oauth/access_token")
        .header("User-Agent", "reqwest/0.12.3")
        .header("Accept", "application/vnd.github+json")
        .header("X-GitHub-Api-Version", "2022-11-28")
        .json(&serde_json::json!({
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh",
            "refresh_token": refresh_token,
        }))
        .send()
        .await?
        .json()
        .await?)
}


// e.g. {"token":"ghs_xOgq7vewfbFdUdShzybGhRrAOdnwVo26WTic","expires_at":"2024-04-29T11:16:07Z","permissions":{"members":"read"},"repository_selection":"selected"}

#[derive(Deserialize)]
pub struct Permissions {
    members: String,
}

#[derive(Deserialize)]
pub struct IatResponseBody {
    pub token: String,
    pub expires_at: String,
    permissions: Permissions,
    repository_selection: String,
}

/// Get an installation access token, using the jwt we created
pub async fn get_app_installation_access_token(
    installation_id: u32,
    jwt: &str,
) -> anyhow::Result<IatResponseBody> {
    Ok(reqwest::Client::new()
        .post(format!("https://api.github.com/app/installations/{installation_id}/access_tokens"))
        .header("User-Agent", "reqwest/0.12.3")
        .header("Accept", "application/vnd.github+json")
        .header("X-GitHub-Api-Version", "2022-11-28")
        .header("Authorization", format!("Bearer {jwt}"))
        .send()
        .await?
        .json()
        .await?)
}
