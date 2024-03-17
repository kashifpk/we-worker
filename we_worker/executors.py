"""Single step executors."""

import logging
from subprocess import check_output, CalledProcessError

from .utils import code_exec

from .schemas import Execution, ExecutionResponseSchema


class ExecutorBase:
    def __init__(self, context):
        self.context = context
        self.log = logging.getLogger("gde." + self.__class__.__name__)

    def execute(self, execution: Execution) -> ExecutionResponseSchema:
        raise NotImplementedError("execute method not implemented.")


class PythonExecutor(ExecutorBase):
    def execute(self, execution: Execution) -> ExecutionResponseSchema:
        self.log.info(f"Executing {execution.graph_step_name} ({execution.key_})")

        try:
            r = code_exec(execution.call)
            return ExecutionResponseSchema(execution_id=execution.key_, status="success", data=r)

        except Exception as exp:
            self.log.error(
                f"Execution {execution.key_} failed.\n {exp.__class__.__name__}: {str(exp)}"
            )
            return ExecutionResponseSchema(execution_id=execution.key_, status="failure", errors=[str(exp)])


class OSExecutor(ExecutorBase):
    """Run OS command."""

    def execute(self, execution: Execution) -> ExecutionResponseSchema:
        self.log.info(f"Executing task for execution: {execution}")
        cmd = execution.call

        try:
            r = check_output(cmd, shell=True)
            return ExecutionResponseSchema(execution_id=execution.key_, status="success", data=r)

        except CalledProcessError as cpe:
            self.log.error(
                f"Execution {execution.key_} failed.\n {cpe.__class__.__name__}: {str(cpe)}"
            )
            return ExecutionResponseSchema(execution_id=execution.key_, status="failure", errors=[str(cpe)])


executors_map = {"python": PythonExecutor, "os": OSExecutor}
