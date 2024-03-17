from functools import lru_cache
from typing import Any
import os

from pydantic import Field, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import dotenv_values

from . import PROJECT_ROOT


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.environ.get("WE_WORKER_ENV_FILE", PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="allow",
    )

    environment: str = Field(..., env="ENVIRONMENT")

    # Workflow executor related config
    broker_url: str = Field(..., env="broker_url")
    exchange: str = Field(..., env="exchange")
    exchange_type: str = Field(..., env="exchange_type")
    task_requests_queue: str = Field(..., env="task_requests_queue")
    task_results_queue: str = Field(..., env="task_results_queue")
    task_start_routing_key: str = Field(..., env="task_start_routing_key")

    # celery related config
    worker_prefetch_multiplier: int = Field(1, env="worker_prefetch_multiplier")

    @field_validator("*", mode="before")
    @classmethod
    def use_testing_config(cls, v: Any, vinfo: ValidationInfo) -> Any:
        # settings.__class__.model_fields['db_name'].json_schema_extra
        if vinfo.data.get("environment", "") == "testing":
            if cls.model_fields[vinfo.field_name].json_schema_extra is None:
                return v

            env_var = cls.model_fields[vinfo.field_name].json_schema_extra.get("env", None)
            if env_var:
                testing_env_var = "testing_" + env_var
                env_file_values = dotenv_values(cls.model_config["env_file"])
                return env_file_values.get(testing_env_var, v)

        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
