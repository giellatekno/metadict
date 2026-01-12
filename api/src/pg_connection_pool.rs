/// Connection pool of postgres connections
use anyhow::anyhow;

#[derive(serde::Deserialize, serde::Serialize)]
struct Config {
    pg: deadpool_postgres::Config,
}

impl Config {
    /// Load the deadpool config (which contains postgres, connection and
    /// pool configuration) from environment variables.
    pub fn from_env() -> Result<Self, config::ConfigError> {
        config::Config::builder()
            .set_default("pg.dbname", "postgres")?
            .set_default("pg.user", "postgres")?
            .set_default("pg.port", 3515)?
            .set_default("pg.host", "deliberately.invalid")?
            .add_source(config::Environment::default().separator("__"))
            //.add_source(config::File::from(PathBuf::from("./config.toml")))
            .build()?
            .try_deserialize()
    }
}

#[derive(Clone)]
pub struct ConnectionPool {
    pool: deadpool_postgres::Pool,
    config: deadpool_postgres::Config,
}

impl ConnectionPool {
    pub fn new() -> Self {
        let config = Config::from_env().unwrap();
        let pool = config
            .pg
            .create_pool(
                Some(deadpool_postgres::Runtime::Tokio1),
                tokio_postgres::NoTls,
            )
            .unwrap();
        Self {
            pool,
            config: config.pg,
        }
    }

    pub async fn get(&self) -> Result<deadpool_postgres::Object, anyhow::Error> {
        self.pool.get().await.map_err(|e| {
            let port = self.config.port.unwrap();
            let host: String = self.config.host.as_ref().unwrap().clone();
            let connection_info = format!("api: can't connect to db at host={host}:{port}");
            anyhow!(e).context(connection_info)
        })
    }
}
