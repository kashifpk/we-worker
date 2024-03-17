from datetime import datetime

from we_worker.executors import OSExecutor
from we_worker.schemas import Execution, ExecutionResponseSchema


def test_os_executor_response():
    executor = OSExecutor({})
    execution = Execution(
        _key='test-execution',
        label="Test execution",
        timestamp=datetime.now(),
        start_execution_id='parent',
        graph_step_name='test-step',
        executor='os',
        execute_async=True,
        call='hostname',
        state='requested'
    )

    res: ExecutionResponseSchema = executor.execute(execution)
    assert isinstance(res, ExecutionResponseSchema)
    assert res.status == 'success'
    assert isinstance(res.data, bytes)
    assert len(res.data) > 0


def test_os_executor_error_response():
    executor = OSExecutor({})
    execution = Execution(
        _key='test-execution',
        label="Test execution",
        timestamp=datetime.now(),
        start_execution_id='parent',
        graph_step_name='test-step',
        executor='os',
        execute_async=True,
        call='false',  # syntax error
        state='requested'
    )

    res: ExecutionResponseSchema = executor.execute(execution)
    assert isinstance(res, ExecutionResponseSchema)
    assert res.status == 'failure'
    assert res.data is None
    assert len(res.errors) > 0
    assert res.errors[0] == "Command 'false' returned non-zero exit status 1."
