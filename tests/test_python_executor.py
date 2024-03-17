from datetime import datetime

from we_worker.executors import PythonExecutor
from we_worker.schemas import Execution, ExecutionResponseSchema


def test_python_executor_response():
    executor = PythonExecutor({})
    execution = Execution(
        _key='test-execution',
        label="Test execution",
        timestamp=datetime.now(),
        start_execution_id='parent',
        graph_step_name='test-step',
        executor='python',
        execute_async=True,
        call='import os\n{"env": os.environ.get("ENVIRONMENT", "")}',
        state='requested'
    )

    res: ExecutionResponseSchema = executor.execute(execution)
    assert isinstance(res, ExecutionResponseSchema)
    assert res.status == 'success'
    assert res.data == {'env': 'testing'}


def test_python_executor_error_response():
    executor = PythonExecutor({})
    execution = Execution(
        _key='test-execution',
        label="Test execution",
        timestamp=datetime.now(),
        start_execution_id='parent',
        graph_step_name='test-step',
        executor='python',
        execute_async=True,
        call='print(")',  # syntax error
        state='requested'
    )

    res: ExecutionResponseSchema = executor.execute(execution)
    assert isinstance(res, ExecutionResponseSchema)
    assert res.status == 'failure'
    assert res.data is None
    assert len(res.errors) > 0
