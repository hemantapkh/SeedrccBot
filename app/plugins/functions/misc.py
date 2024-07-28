from loguru import logger
from sqlalchemy import select

from database.models import Admin


class Misc:
    def __init__(self, Client):
        self.Client = Client

    # Message admins
    async def message_admins(self, message):
        query = select(Admin.user_id)

        admins = await self.Client.DB.execute(query)
        admins = admins.all()

        for admin in admins:
            user_lang = await self.user_lang(admin.user_id)
            try:
                await self.Client.send_message(
                    chat_id=admin.user_id,
                    text=message,
                    reply_markup=self.Client.keyboard.main(user_lang),
                )

            except Exception as err:
                logger.warning(f"Error sending message to admin: {err}")
