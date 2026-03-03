use axum::{body::Body, http::Request, middleware::Next, response::Response};

pub async fn timing_middleware(request: Request<Body>, next: Next) -> Response {
    let t0 = std::time::Instant::now();
    let mut response = next.run(request).await;
    let duration = t0.elapsed().as_secs_f64();
    let duration = format!("req;desc=\"Request time\";dur={duration}");
    let duration = http::header::HeaderValue::from_str(&duration).unwrap();
    response.headers_mut().insert("Server-Timing", duration);
    response
}
