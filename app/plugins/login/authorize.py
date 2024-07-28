from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from seedrcc import Login


@Client.on_callback_query(filters.regex("authorize_device"))
async def authorize_device(Client: Client, callback: types.CallbackQuery):
    response = Login().getDeviceCode()

    buttons = [
        [
            InlineKeyboardButton(
                text=Client.language.get_button_text("done"),
                callback_data=f"authorize_confirm_{response['device_code']}",
            )
        ],
        [
            InlineKeyboardButton(
                text=Client.language.get_button_text("back"),
                callback_data="add_account",
            )
        ],
    ]

    await Client.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=Client.language.get_text("authorize").format(response["user_code"]),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True,
    )
