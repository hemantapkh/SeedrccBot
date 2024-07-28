"""API to connect to the database server"""

import datetime

from database.models import Session, Setting, User, Account


class DataBase:
    def __init__(self):
        self.session = Session

    async def _query(self, method, *args, **kwargs):
        async with self.session() as session:
            auto_commmit = kwargs.pop("auto_commit", True)
            result = await getattr(session, method)(*args, **kwargs)
            if auto_commmit:
                await session.commit()
            return result

    def __getattr__(self, method):
        def wrapper(*args, **kwargs):
            return self._query(method, *args, **kwargs)

        return wrapper

    async def set_user(self, message, referrer=None):
        # If chat type if group/channel
        if message.chat.type.name != "PRIVATE":
            message.chat.first_name = message.chat.title
            message.chat.last_name = None

        user = User(
            user_id=message.chat.id,
            user_type=message.chat.type.name,
            username=message.chat.username,
            first_name=message.chat.first_name,
            last_name=message.chat.last_name,
            referrer=str(referrer) if referrer else None,
            last_active=datetime.datetime.now(),
        )

        settings = Setting(user_id=message.chat.id)

        async with Session() as session:
            await session.merge(user)
            await session.merge(settings)

            await session.commit()
            
    async def set_account(self, user_id: str, account_config: dict, token: str):
        account = Account(
            user_id=user_id,
            account_id=account_config['account']['user_id'],
            username=account_config['account']['username'],
            token=token,
            is_premium=account_config['account']['premium'],
            invites_remaining=account_config['account']['invites'],
            email=account_config['account']['email'],
            timestamp=datetime.datetime.now()
        )
        
        async with Session() as session:
            await session.merge(account)

            await session.commit()
        
        