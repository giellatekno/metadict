use axum::{
    async_trait,
    extract::FromRequestParts,
    http::{header::COOKIE, request::Parts},
};
use cookie::Cookie;

#[derive(Default)]
pub struct Cookies(pub Option<Vec<Cookie<'static>>>);

#[async_trait]
impl<S> FromRequestParts<S> for Cookies
where
    S: Send + Sync,
{
    type Rejection = core::convert::Infallible;

    async fn from_request_parts(parts: &mut Parts, _state: &S) -> Result<Self, Self::Rejection> {
        let Some(cookies) = parts.headers.get(COOKIE) else {
            return Ok(Self::default());
        };

        let cookies_str = cookies.to_str().expect("cookies are always ascii");

        let vec = cookie::Cookie::split_parse(cookies_str)
            .filter_map(|maybe_cookie| maybe_cookie.ok())
            .map(|cookie| cookie.into_owned())
            .collect::<Vec<_>>();
        Ok(Self(Some(vec)))
    }
}
