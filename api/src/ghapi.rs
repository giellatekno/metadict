use serde::Deserialize;
use anyhow::anyhow;
use crate::auth::GhUserResponse;

#[derive(Deserialize)]
struct TeamMembershipResponse {
    // "active" or "pending" (if team invite hasn't been accepted yet)
    pub state: String,
    // "maintainer" or "member"
    role: String,
    // e.g. "https://api.github.com/organizations/54359201/team/9970092/memberships/Phaqui
    url: String,
}

/// Query the Github API, to see if a user is a member of the
/// "metadictionary-access" team (and therefore has access to restriced
/// dictionaries)
pub async fn ghuser_in_our_team(
    gh_user: &GhUserResponse,
    access_token: &str
) -> anyhow::Result<bool> {
    let username = &gh_user.login;
    let url = format!("https://api.github.com/orgs/giellatekno/teams/metadictionary-access/memberships/{username}");
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
        reqwest::StatusCode::NOT_FOUND => Ok(false),
        _ => {
            Err(anyhow!("non 200"))
        }
    }
}

