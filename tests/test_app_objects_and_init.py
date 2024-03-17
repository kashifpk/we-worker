import logging

from we_worker.settings import get_settings
from we_worker.logging import configure_logging


def test_settings():
    settings = get_settings()
    assert settings.environment == "testing"


def test_logging(caplog):
    configure_logging()

    invalid_logger = logging.getLogger('test')
    invalid_logger.info("This should not be logged")

    log = logging.getLogger('we_worker.test')
    log.info("Welcome to we-worker")

    # Test that we only have logs from `log` logger
    assert caplog.text.startswith('INFO')
    assert caplog.messages[0] == "Welcome to we-worker"
    assert caplog.records[0].name == "we_worker.test"


def test_celery_config():
    from we_worker.celery import celery_app  # top level import breaks ENVIRONMENT override
    settings = get_settings()
    assert celery_app.conf.broker_url == settings.broker_url
