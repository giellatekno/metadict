//! Authenticating and authorization with Github-related functionality
use serde::Deserialize;
use std::path::PathBuf;

/// The Github App's settings
#[derive(Debug, Deserialize)]
pub struct GhAppConfig {
    pub client_id: String,
    pub client_secret: String,
}

impl GhAppConfig {
    pub fn read_config() -> Result<Self, config::ConfigError> {
        config::Config::builder()
            .add_source(config::File::from(PathBuf::from("./gh_app.toml")))
            .build()?
            .try_deserialize()
    }
}
