from dataclasses import dataclass
from environs import Env


@dataclass
class BotToken:
    token: str

@dataclass
class Logging:
    log_level: str
    log_format: str

@dataclass
class Config:
    bot: BotToken
    log: Logging


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path=path)

    return Config(
        bot=BotToken(token=env("BOT_TOKEN")),
        log=Logging(log_level=env("LOG_LEVEL"), log_format=env("LOG_FORMAT"))
    )