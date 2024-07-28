from database.models import Account
from pyrogram import Client, filters, types
from seedrcc import Login, Seedr
from sqlalchemy import delete


@Client.on_callback_query(filters.regex("logout"))
async def logout(Client: Client, callback: types.CallbackQuery):
    account_id = callback.data.split("_")[-1]
    query = (
        delete(Account)
        .where(Account.user_id == callback.from_user.id)
        .where(Account.account_id == account_id)
    )
    await Client.DB.execute(query)

    await Client.send_message(
        chat_id=callback.message.chat.id, text="Account logout successfully."
    )
