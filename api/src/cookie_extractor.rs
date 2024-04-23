use cookie::Cookie;
use axum::{
    async_trait,
    extract::FromRequestParts,
    routing::get,
    Router,
    http::{
        StatusCode,
        header::{HeaderValue, USER_AGENT, COOKIE},
        request::Parts,
    },
};

#[derive(Default)]
pub struct Cookies {
    pub cookies: Option<String>
}

#[async_trait]
impl<'a, S> FromRequestParts<S> for Cookies
where
    S: Send + Sync,
{
    type Rejection = core::convert::Infallible;

    async fn from_request_parts(parts: &mut Parts, _state: &S) -> Result<Self, Self::Rejection> {
        let Some(cookies) = parts.headers.get(COOKIE) else {
            return Ok(Self::default());
        };

        let string = cookies
            .to_str()
            .expect("cookies are always ascii")
            .to_string();

        Ok(Self {
            cookies: Some(string)
        })
    }
}

impl Cookies {
    pub fn to_cookies(&self) -> Option<Vec<Cookie>> {
        let Some(ref s) = self.cookies else {
            return None;
        };

        let cookies = Cookie::split_parse(s)
            .filter_map(|maybe_cookie| {
                maybe_cookie.ok()
            })
            .map(|cookie| cookie.clone())
            .collect::<Vec<_>>();

        Some(cookies)
    }
}
