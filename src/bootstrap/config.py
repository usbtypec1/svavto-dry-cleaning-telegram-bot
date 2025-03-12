import pathlib
import tomllib
from dataclasses import dataclass
from typing import Final


CONFIG_FILE_PATH: Final[pathlib.Path] = (
        pathlib.Path(__file__).parent.parent.parent / 'config.toml'
)


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseUrlsConfig:
    msk_base_url: str
    spb_base_url: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    telegram_bot_token: str
    whitelist_user_ids: set[int]
    web_app: BaseUrlsConfig
    api: BaseUrlsConfig


def load_config_from_file(
        file_path: pathlib.Path = CONFIG_FILE_PATH
) -> Config:
    config_toml = file_path.read_text(encoding='utf-8')
    config = tomllib.loads(config_toml)

    return Config(
        telegram_bot_token=config['telegram_bot']['token'],
        whitelist_user_ids=set(config['telegram_bot']['whitelist_user_ids']),
        web_app=BaseUrlsConfig(
            msk_base_url=config['web_app']['msk_base_url'],
            spb_base_url=config['web_app']['spb_base_url'],
        ),
        api=BaseUrlsConfig(
            msk_base_url=config['api']['msk_base_url'],
            spb_base_url=config['api']['spb_base_url'],
        ),
    )
