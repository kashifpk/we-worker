from typing import Literal, Any
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class Execution(BaseModel):
    model_config = ConfigDict(extra="allow")

    key_: str = Field(..., alias="_key")  # graph name
    label: str | None = None
    timestamp: datetime | None = None
    start_execution_id: str
    graph_step_name: str
    executor: str
    execute_async: bool
    plugins: dict = {}
    call: str
    input: dict = {}
    state: Literal["requested", "running", "completed", "failed"] = "requested"
    status: str | None = None
    result: Any | None = None
    errors: list | None = None


class ExecutionResponseSchema(BaseModel):
    """Execution response representation."""

    execution_id: str
    status: Literal["success", "failure", "timeout"]
    data: Any | None = None
    errors: list | None = None
