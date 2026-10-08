from dishka import AsyncContainer, make_async_container
from taskiq import TaskiqScheduler
from taskiq_redis import ListQueueBroker

from app.adapters.config import (
    AwsConfig,
    Config,
    DatabaseConfig,
    EmailConfig,
    JwtConfig,
    MailchimpConfig,
    RedisConfig,
    SmsConfig,
)
from app.entrypoint.di.providers.adapters import AdaptersProvider
from app.entrypoint.di.providers.command import CommandProvider
from app.entrypoint.di.providers.dao import DAOProvider
from app.entrypoint.di.providers.db_connection import ConnectionProvider
from app.entrypoint.di.providers.interactors import InteractorsProvider
from app.entrypoint.di.providers.query import QueryProvider
from app.entrypoint.di.providers.repository import RepositoryProvider
from app.entrypoint.di.providers.services import ServiceProvider
from app.entrypoint.di.providers.tasks import TaskProvider


def get_async_container(
    config: Config,
    broker: ListQueueBroker | None = None,
    scheduler: TaskiqScheduler | None = None,
) -> AsyncContainer:
    context = {
        AwsConfig: config.aws,
        DatabaseConfig: config.database,
        EmailConfig: config.email,
        JwtConfig: config.jwt,
        MailchimpConfig: config.mailchimp,
        RedisConfig: config.redis,
        SmsConfig: config.sms,
    }
    if broker is not None:
        context[ListQueueBroker] = broker
    if scheduler is not None:
        context[TaskiqScheduler] = scheduler

    providers = [
        AdaptersProvider(),
        ServiceProvider(),
        InteractorsProvider(),
        ConnectionProvider(),
        DAOProvider(),
        RepositoryProvider(),
        CommandProvider(),
        QueryProvider(),
    ]
    if broker is not None:
        providers.append(TaskProvider())

    return make_async_container(*providers, context=context)
