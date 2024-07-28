from pyrogram import Client, filters, types

@Client.on_message(filters.custom.cmd("add"))
async def add_account(Client: Client, message: types.Message):
    await Client.send_message(
        message.from_user.id,
        text=Client.language.get_text("addAccount"),
        reply_markup=Client.keyboard.add_accounts(),
    )
