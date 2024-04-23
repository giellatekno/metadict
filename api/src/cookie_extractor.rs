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

/*
struct CookiesIter<'a> {
    done: bool,
    it: Option<&dyn std::iter::Iterator<Item = Cookie<'static>>>,
}
*/

impl Cookies {
    /*
    pub fn iter(&self) -> CookiesIter {
        match self.cookies {
            None => CookiesIter {
                done: true,
                it: None,
            },
            Some(s) => {
                let it = cookie::Cookie::split_parse(s)
                    .filter_map(|maybe_cookie| maybe_cookie.ok())
                    .map(|cookie| cookie.clone());
                CookiesIter {
                    done: false,
                    it: Some(it),
                }
            }
        }
    }
    */

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

pub fn validate_jwt(cookies: crate::cookie_extractor::Cookies) -> bool {
    let Some(cookies) = cookies.to_cookies() else {
        return false;
    };

    let cookie = cookies.iter().find(|cookie| cookie.name() == "metadict-creds");
    let Some(cookie) = cookie else {
        return false;
    };

    let token = cookie.value_trimmed();
    let key = jsonwebtoken::DecodingKey::from_secret(crate::JWT_SECRET.get().unwrap());
    let mut validation = jsonwebtoken::Validation::new(jsonwebtoken::Algorithm::HS256);
    validation.set_audience(&["giellatekno"]);
    match jsonwebtoken::decode::<crate::auth::Claims>(token, &key, &validation) {
        Err(e) => {
            println!("jwt validation failed: {}", e);
            false
        }
        Ok(_) => true,
    }
}

