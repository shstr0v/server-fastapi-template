from collections.abc import AsyncIterator

import boto3
from aiohttp import ClientSession
from argon2 import PasswordHasher as ArgonPasswordHasher
from dishka import Provider, Scope, WithParents, from_context, provide, provide_all
from fastapi import Request
from redis.asyncio import Redis

from app.adapters.auth.idp import BearerParser, SessionIdProvider
from app.adapters.auth.password_hasher import PasswordHasherImpl
from app.adapters.auth.session import SessionProcessorImpl
from app.adapters.auth.sha256_hasher import SHA256Hasher
from app.adapters.auth.token_processor import Algorithm, TokenProcessor
from app.adapters.aws import AwsFileManagerImpl
from app.adapters.config import AwsConfig, JwtConfig, MailchimpConfig, RedisConfig, SmsConfig
from app.adapters.data.dao.session import SessionDAOImpl
from app.adapters.email import EmailSenderImpl
from app.adapters.mailchimp import MailchimpClientImpl, MailchimpMarketingClientImpl, MailchimpOauthClientImpl
from app.adapters.sms_client import SmsClientImpl
from app.adapters.totp import TOTPGeneratorImpl, TOTPValidatorImpl
from app.application.common.email_sender import EmailSender
from app.application.common.file_manager import AwsFileManager
from app.application.common.mailchimp import MailchimpClient, MailchimpMarketingClient, MailchimpOauthClient
from app.application.common.sms_client import SmsClient


class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    request = from_context(Request, scope=Scope.REQUEST)
    bearer_parser = provide(BearerParser, scope=Scope.REQUEST)
    idp = provide(SessionIdProvider, scope=Scope.REQUEST)
    email_sender = provide(EmailSenderImpl, provides=EmailSender, scope=Scope.REQUEST)
    sha256_hasher = provide(SHA256Hasher, provides=SHA256Hasher, scope=Scope.REQUEST)
    providers = provide_all(
        WithParents[PasswordHasherImpl],
        WithParents[SessionDAOImpl],
        WithParents[SessionProcessorImpl],
        WithParents[TOTPGeneratorImpl],
        WithParents[TOTPValidatorImpl],
    )

    @provide(scope=Scope.REQUEST, provides=SmsClient)
    async def get_sms_client(self, config: SmsConfig) -> AsyncIterator[SmsClient]:
        session = ClientSession(
            base_url="https://api.brevo.com/v3/",
            headers={
                "Content-Type": "application/json",
                "api-key": config.api_key,
                "accept": "application/json",
            },
        )
        client = SmsClientImpl(client=session)
        yield client
        await session.close()

    @provide(scope=Scope.APP, provides=TokenProcessor)
    def get_token_processor(self, config: JwtConfig) -> TokenProcessor:
        algorithm: Algorithm = "HS256"
        if config.algorithm in {"HS256", "HS384", "HS512", "RS256", "RS384", "RS512"}:
            algorithm = config.algorithm  # type: ignore[assignment]
        return TokenProcessor(secret=config.secret, algorithm=algorithm)

    @provide(scope=Scope.REQUEST, provides=MailchimpClient)
    async def get_mailchimp_client(self, config: MailchimpConfig) -> AsyncIterator[MailchimpClient]:
        session = ClientSession(base_url="https://api.mailchimp.com")
        client = MailchimpClientImpl(api_key=config.api_key, client=session)
        yield client
        await session.close()

    @provide(scope=Scope.REQUEST, provides=MailchimpMarketingClient)
    async def get_mailchimp_marketing_client(self) -> AsyncIterator[MailchimpMarketingClient]:
        session = ClientSession()
        yield MailchimpMarketingClientImpl(client=session)
        await session.close()

    @provide(scope=Scope.REQUEST, provides=MailchimpOauthClient)
    async def get_mailchimp_oauth_client(self, config: MailchimpConfig) -> AsyncIterator[MailchimpOauthClient]:
        session = ClientSession(base_url="https://login.mailchimp.com")
        client = MailchimpOauthClientImpl(
            client=session,
            client_id=config.client_id,
            client_secret=config.client_secret,
        )
        yield client
        await session.close()

    @provide(scope=Scope.REQUEST, provides=AwsFileManager)
    async def get_file_manager(self, config: AwsConfig) -> AwsFileManager:
        client = boto3.client(
            "s3",
            aws_access_key_id=config.access_key,
            aws_secret_access_key=config.secret_key,
            region_name=config.region or None,
        )
        return AwsFileManagerImpl(client=client, config=config)

    @provide(scope=Scope.REQUEST, provides=Redis)
    async def get_redis(self, config: RedisConfig) -> AsyncIterator[Redis]:
        redis = await Redis.from_url(config.connection_url, decode_responses=True)
        yield redis
        await redis.aclose()

    @provide(scope=Scope.REQUEST, provides=ArgonPasswordHasher)
    def get_argon_password_hasher(self) -> ArgonPasswordHasher:
        return ArgonPasswordHasher()
