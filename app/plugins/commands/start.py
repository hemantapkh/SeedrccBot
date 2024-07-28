from pyrogram import Client, filters, types


@Client.on_message(filters.custom.cmd("start") & filters.custom.login_required)
async def start(Client: Client, message: types.Message):
    await Client.send_message(
        message.chat.id,
        text=Client.language.get_text("greet"),
        reply_markup=Client.keyboard.main_menu(),
    )
