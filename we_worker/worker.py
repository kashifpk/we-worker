"""
Tasks Worker Runner.

Contains celery task for running workers and sending their results back.
"""

import logging

import pika
from celery import current_app

from .settings import get_settings
from .schemas import Execution, ExecutionResponseSchema
from .executors import executors_map, ExecutorBase

log = logging.getLogger(__name__)

celery_app = current_app._get_current_object()
settings = get_settings()


@celery_app.task(name="we_worker.run_worker")
def run_worker(execution_dict):
    """
    Run worker.

    Function responsible for processing incoming request, running the target
    worker and posting it's result or error status back to the event processor.
    """

    execution = Execution(**execution_dict)

    assert execution.execute_async is True
    log.info("worker request: %r", execution_dict)

    # TODO: we can't have unresolved context in worker. So resolved context and execution call
    # should be passed.

    executor: ExecutorBase = executors_map[execution_dict["executor"]](context={})
    resp: ExecutionResponseSchema = executor.execute(execution_dict)

    send_worker_response(resp.model_dump_json(by_alias=True))


def send_worker_response(wr: str):
    """Connect to RabbitMQ and return worker response."""
    broker_url = settings.broker_url
    exchange = settings.exchange
    exchange_type = settings.exchange_type
    results_queue = settings.task_requests_queue

    # TODO: Channel should be reused throughout the lifetime of the celery worker process.
    log.info("Connecting to broker ...")
    parameters = pika.URLParameters(broker_url)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)

    channel.basic_publish(
        exchange=exchange,
        routing_key=results_queue,
        body=wr,
        properties=pika.BasicProperties(
            delivery_mode=2  # make message persistent
        ),
    )

    log.info("Task response sent!")
    connection.close()
