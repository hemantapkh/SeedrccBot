from pyrogram import Client, filters, types
from seedrcc import Seedr


@Client.on_message(filters.custom.cmd("files") & filters.custom.login_required)
async def files(Client: Client, message: types.Message):
    buttons = [
        [
            types.InlineKeyboardButton(
                "Click the button below to list your contents",
                switch_inline_query_current_chat="#files",
            )
        ]
    ]

    await Client.send_message(
        message.from_user.id,
        text=Client.language.get_text("files"),
        reply_markup=types.InlineKeyboardMarkup(buttons),
    )
