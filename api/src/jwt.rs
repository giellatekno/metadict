use serde::{Deserialize, Serialize};
use jsonwebtoken::{
    Algorithm,
    encode,
    decode,
    Validation, DecodingKey, EncodingKey, TokenData};
use crate::auth::GhUserResponse;
use crate::cookie_extractor::Cookies;
use anyhow::anyhow;

#[derive(Debug, Serialize, Deserialize)]
pub struct Claims {
    // Standard jwt field: Audience. Optionl.
    aud: String,
    // Standard jwt field: Expiration time of token (as UTC timestamp)
    // Required (validate_exp defaults to true in validation)
    exp: usize,
    // Standard jwt field: Issued at (utc timestamp). Optional.
    iat: usize,
    // Standard jwt field: Issuer. Optional.
    iss: String,
    //nbf: usize,    // Optional. Not Before (as UTC timestamp)
    // Standard jwt field: Subject (whom token refers to). Optional.
    sub: String,
    // if the user can see restricted dictionaries
    pub restricted_dicts: bool,
    // name field in gh access token
    pub gh_fullname: String,
    // avatar url in the gh access token
    pub gh_avatar_url: String,
}

pub fn create_jwt(
    gh_user: &GhUserResponse,
    has_restricted_access: bool,
    jwt_key: &[u8]
) -> anyhow::Result<String> {
    let header = jsonwebtoken::Header::default();
    let iat = jsonwebtoken::get_current_timestamp();
    let exp = iat + 60 * 5;
    let claims = Claims {
        aud: "giellatekno".to_string(),
        exp: exp.try_into()?,
        iat: iat.try_into()?,
        iss: "Giellatekno".to_string(),
        sub: gh_user.login.to_string(),
        restricted_dicts: has_restricted_access,
        gh_fullname: gh_user.name.to_string(),
        gh_avatar_url: gh_user.avatar_url.to_string(),
    };
    let key = EncodingKey::from_secret(jwt_key);
    Ok(encode(&header, &claims, &key)?)
}

pub fn validate_jwt(cookies: Cookies) -> anyhow::Result<TokenData<Claims>> {
    let cookies = cookies.0
        .ok_or_else(|| anyhow!("cookies is None"))?;
    let token = cookies
        .iter()
        .find(|cookie| cookie.name() == "metadict-creds")
        .ok_or_else(|| anyhow!("no cookie 'metadict-creds'"))?
        .value_trimmed();

    let key = DecodingKey::from_secret(crate::JWT_SECRET.get().unwrap());
    let mut validation = Validation::new(Algorithm::HS256);
    validation.set_audience(&["giellatekno"]);

    decode::<Claims>(token, &key, &validation)
        .map_err(|e| anyhow::anyhow!("jwt validation failed: {}", e))
}

pub fn user_has_restricted_access(token: &TokenData<Claims>) -> bool {
    token.claims.restricted_dicts
}
