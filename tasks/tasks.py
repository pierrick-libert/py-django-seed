"""Dummy tasks for the Celery app server"""

from celery import shared_task
from celery.utils.log import get_task_logger

LOGGER = get_task_logger(__name__)


@shared_task
def test(data) -> bool:
    """Dummy task which outputs the data sent"""
    LOGGER.info(data)
    return True
