//! Our JWT functionality. Our JWT, as opposed to the JWT that we need
//! to create for getting an installation access token (IAT) from GH.

use crate::cookie_extractor::Cookies;
use jsonwebtoken::{decode, encode, Algorithm, DecodingKey, EncodingKey, Validation};
use serde::{Deserialize, Serialize};

/// aud and iss fields in our jwts
const AUDIENCE: &str = "Giellatekno";
const ISSUER: &str = AUDIENCE;
pub const COOKIE_NAME: &str = "metadict-creds";

#[derive(Debug, Default, Serialize, Deserialize)]
pub struct OurClaims {
    /// Standard jwt field: Audience. Optional.
    aud: String,
    /// Standard jwt field: Expiration time of token (as UTC timestamp)
    /// Required (validate_exp defaults to true in validation)
    exp: u64,
    /// Standard jwt field: Issued at (utc timestamp). Optional.
    iat: u64,
    /// Standard jwt field: Issuer. Optional.
    iss: String,
    ///nbf: usize,    // Optional. Not Before (as UTC timestamp)
    /// Standard jwt field: Subject (whom token refers to). Optional.
    sub: String,
    /// If the user can see restricted dictionaries
    pub restricted_dicts: bool,
    /// Github user access token
    pub gh_uat: String,
    /// Github refresh token
    pub gh_refresh_token: String,
    /// Name field in gh access token
    pub gh_fullname: String,
    /// Login name on Github
    pub gh_login_name: String,
    /// Avatar url in the gh access token
    pub gh_avatar_url: String,
}

#[derive(Debug, Serialize)]
pub struct DecodedJwt(OurClaims);

impl std::fmt::Display for DecodedJwt {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self.0)
    }
}

impl DecodedJwt {
    pub fn encode(&self, signing_key: &[u8]) -> Result<String, jsonwebtoken::errors::Error> {
        let header = jsonwebtoken::Header::default();
        let key = EncodingKey::from_secret(signing_key);
        let claims = self;
        Ok(encode(&header, &claims, &key)?)
    }

    pub fn has_expired(&self) -> bool {
        let now = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .expect("systemtime's now() is not before the unix epoch")
            .as_secs();
        self.0.exp < now
    }

    /// Refresh our JWT. When we do, we want to check against GH if the user
    /// still has restricted access, so we need the user's login name,
    /// as well as our installation access token (iat).
    pub async fn refresh(&self, iat: &str) -> anyhow::Result<DecodedJwt> {
        assert!(self.has_expired());
        // TODO this may fail because the IAT has expired
        let can_see_closed = crate::ghapi::user_in_team(
            self.gh_login_name(),
            "giellatekno",
            "metadictionary-access",
            iat,
        )
        .await?;
        let jwt = crate::our_jwt::OurJwt::builder()
            .sub(self.gh_login_name().to_string())
            .restricted_dicts(can_see_closed)
            .gh_uat(self.gh_uat().to_string())
            .gh_refresh_token(self.gh_refresh_token().to_string())
            .gh_fullname(self.gh_fullname().to_string())
            .gh_avatar_url(self.gh_avatar_url().to_string())
            .build()
            .unwrap();
        Ok(jwt)
    }

    pub fn gh_refresh_token(&self) -> &str {
        &self.0.gh_refresh_token
    }

    pub fn gh_uat(&self) -> &str {
        &self.0.gh_uat
    }

    pub fn gh_login_name(&self) -> &str {
        &self.0.gh_login_name
    }

    pub fn gh_fullname(&self) -> &str {
        &self.0.gh_fullname
    }

    pub fn gh_avatar_url(&self) -> &str {
        &self.0.gh_avatar_url
    }

    pub fn restricted_dicts(&self) -> bool {
        self.0.restricted_dicts
    }
}

#[derive(thiserror::Error, Debug)]
pub enum CookieParseError {
    #[error("No cookie header")]
    NoCookies,
    #[error("No cookie '{}'", COOKIE_NAME)]
    NoMetadictCredsCookie,
    #[error("jwt decoding failed: {0}")]
    DecodeError(#[from] jsonwebtoken::errors::Error),
}

impl TryFrom<Cookies> for DecodedJwt {
    type Error = CookieParseError;

    fn try_from(cookies: Cookies) -> Result<Self, Self::Error> {
        let cookies = cookies.0.ok_or_else(|| CookieParseError::NoCookies)?;
        let token = cookies
            .iter()
            .find(|cookie| cookie.name() == COOKIE_NAME)
            .ok_or_else(|| CookieParseError::NoMetadictCredsCookie)?
            .value_trimmed();

        let key = DecodingKey::from_secret(crate::JWT_SECRET.get().unwrap());
        let mut validation = Validation::new(Algorithm::HS256);

        // we can't validate exp, because if we validate exp and a jwt
        // doesn't validate, then we have no way to access the fields of the
        // expired jwt (which we need to create a new jwt)
        validation.validate_exp = false;
        validation.set_audience(&[AUDIENCE]);

        let our_claims = decode::<OurClaims>(token, &key, &validation)
            .map_err(|e| CookieParseError::DecodeError(e))?
            .claims;

        Ok(DecodedJwt(our_claims))
    }
}

pub struct OurJwt;

impl OurJwt {
    pub fn builder() -> OurJwtBuilder {
        OurJwtBuilder::default()
    }
}

#[derive(Default)]
pub struct OurJwtBuilder {
    exp: Option<u64>,
    iat: Option<u64>,
    sub: Option<String>,
    restricted_dicts: Option<bool>,
    gh_uat: Option<String>,
    gh_refresh_token: Option<String>,
    gh_login_name: Option<String>,
    gh_fullname: Option<String>,
    gh_avatar_url: Option<String>,
}

#[derive(Debug)]
pub struct OurJwtBuilderError;

macro_rules! impl_field {
    ($field:ident, $type:ty) => {
        pub fn $field(mut self, $field: $type) -> Self {
            self.$field = Some($field);
            self
        }
    };
}

impl OurJwtBuilder {
    pub fn build(self) -> Result<DecodedJwt, OurJwtBuilderError> {
        let iat = self.iat.unwrap_or_else(now_utc);
        // default expiry time for our jwt is 10 minutes
        let exp = self.exp.unwrap_or(iat + 60 * 10);
        let sub = self.sub.ok_or(OurJwtBuilderError)?;
        let restricted_dicts = self.restricted_dicts.ok_or(OurJwtBuilderError)?;
        let gh_uat = self.gh_uat.ok_or(OurJwtBuilderError)?;
        let gh_refresh_token = self.gh_refresh_token.ok_or(OurJwtBuilderError)?;
        let gh_login_name = self.gh_login_name.ok_or(OurJwtBuilderError)?;
        let gh_fullname = self.gh_fullname.ok_or(OurJwtBuilderError)?;
        let gh_avatar_url = self.gh_avatar_url.ok_or(OurJwtBuilderError)?;
        let claims = OurClaims {
            aud: AUDIENCE.to_string(),
            exp,
            iat,
            iss: ISSUER.to_string(),
            sub,
            restricted_dicts,
            gh_uat,
            gh_login_name,
            gh_fullname,
            gh_refresh_token,
            gh_avatar_url,
        };
        Ok(DecodedJwt(claims))
    }

    impl_field!(exp, u64);
    impl_field!(iat, u64);
    impl_field!(sub, String);
    impl_field!(restricted_dicts, bool);
    impl_field!(gh_uat, String);
    impl_field!(gh_refresh_token, String);
    impl_field!(gh_login_name, String);
    impl_field!(gh_fullname, String);
    impl_field!(gh_avatar_url, String);
}

#[inline]
fn now_utc() -> u64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .expect("We are not in a time before the unix epoch")
        .as_secs()
}
