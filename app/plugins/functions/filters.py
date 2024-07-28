import re

from database.models import Admin, Account
from pyrogram import filters, types, Client, types
from sqlalchemy import exists, select

from seedrcc import Seedr


class Filter:
    def __init__(self, Client: Client):
        self.Client = Client

    # Filter message from bot admins
    async def admin_flt(_, Client: Client, message: types.Message):
        query = select(exists().where(Admin.user_id == message.from_user.id))
        is_admin = await Client.DB.execute(query)

        return is_admin.scalar()

    # Filter message from chat admins
    def chat_admin_flt(self, alert=True):
        async def func(flt: filters, Client: Client, message: types.Message):
            if isinstance(message, types.CallbackQuery):
                callback_id = message.id
                from_user = message.from_user.id
                message = message.message
                message.from_user.id = from_user

            if message.chat.type.name == "PRIVATE":
                return True

            member = await Client.get_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
            )

            if member.status.name != "MEMBER":
                return True

            # Show alert message to non-admins users
            if flt.alert:
                user_lang = await Client.misc.user_lang(message)
                if "callback_id" in locals():
                    await Client.answer_callback_query(
                        callback_query_id=callback_id,
                        text=Client.language.STR("noPermission", user_lang),
                        show_alert=True,
                    )

                else:
                    await Client.send_message(
                        chat_id=message.chat.id,
                        text=Client.language.STR("noPermission", user_lang),
                        reply_to_message_id=message.id,
                    )

        return filters.create(func, alert=alert)

    # Command filters with reply keyboard
    def cmd(self, data):
        async def func(flt:filters, Client: Client, message: types.Message):
            if message.text:
                language = "english"
                text = re.sub(r"^\/?([^@]+).*", r"\1", message.text)

                if text in [flt.data, self.Client.language.get_button_text(flt.data, language)]:
                    return True

        return filters.create(func, data=data)
    
    # Filter for checking user accounts
    async def login_required(_, Client: Client, message: types.Message | types.CallbackQuery):
        if isinstance(message, types.CallbackQuery):
            from_user = message.from_user.id
            message = message.message
            message.from_user.id = from_user
                
        # language_query = select(Setting.language).where(Setting.user_id == message.from_user.id)
        # result = await Client.DB.execute(language_query)
        # language = result.scalar()
        
        # if not language:
        #     await Client.DB.set_user(message)
            
        message.language = "english"

        query = select(Account.token).where(Account.user_id == message.from_user.id)
        result = await Client.DB.execute(query)
        seedr_token = result.scalar()
        
        if not seedr_token:
            await Client.send_message(
                message.from_user.id,
                text=Client.language.get_text("addAccount"),
                reply_markup=Client.keyboard.add_accounts(),
            )
            
            return False
        
        message.seedr = Seedr(seedr_token)

        return True
            

    # Filter via message from own
    async def via_flt(_, Client: Client, message: types.Message):
        if message.via_bot:
            return message.via_bot.id == Client.me.id

    admin = filters.create(admin_flt)
    via_me = filters.create(via_flt)
    chat_admin = filters.create(chat_admin_flt)
    login_required = filters.create(login_required)