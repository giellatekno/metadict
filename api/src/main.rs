use tokio_postgres::{NoTls, Error};
use axum::response::{IntoResponse, Response};

use axum::{
    routing::get,
    Router,
};

async fn search_handler() -> Response {
    "search".into_response()
}

async fn lookup_handler() -> Response {
    "lookup".into_response()
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    // Connect to the database.
    let (client, connection) =
        tokio_postgres::connect("host=localhost user=postgres", NoTls).await?;


    // The connection object performs the actual communication with the database,
    // so spawn it off to run on its own.
    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("connection error: {}", e);
        }
    });

    // Now we can execute a simple statement that just returns its parameter.
    let rows = client
        .query("SELECT $1::TEXT", &[&"hello world"])
        .await?;

    // And then check that we got back the same string we sent over.
    let value: &str = rows[0].get(0);
    assert_eq!(value, "hello world");


    // build our application with a single route
    let app = Router::new()
        .route("/", get(|| async { "metadictionary" }))
        .route("/search", get(search_handler))
        .route("/lookup", get(lookup_handler));

    // run our app with hyper, listening globally on port 3000
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();

    Ok(())
}
