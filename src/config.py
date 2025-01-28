from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DISCORD_TOKEN: str
    GUILD_ID: int
    DATABASE_URL: str
    ATTENDANCE_CHANNEL_ID: int
    COMMITTEE_ROLE_ID: int

    class Config:
        env_file = ".env"
        extra = "ignore"


config = Config()
