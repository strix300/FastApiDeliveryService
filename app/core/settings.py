from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    REDIS_URL: str

    KAFKA_BROKER_ID: int
    KAFKA_ZOOKEEPER_CONNECT: str
    KAFKA_LISTENERS: str
    KAFKA_ADVERTISED_LISTENERS: str
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: int
    KAFKA_BOOTSTRAP_SERVERS: str
    ZOOKEEPER_CLIENT_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()