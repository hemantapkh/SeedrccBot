from pyrogram import Client, filters, types


@Client.on_callback_query(filters.regex("add_account"))
async def add_account(Client: Client, callback: types.CallbackQuery):
    await Client.edit_message_text(
        callback.message.chat.id,
        message_id=callback.message.id,
        text=Client.language.get_text("addAccount"),
        reply_markup=Client.keyboard.add_accounts(),
    )
