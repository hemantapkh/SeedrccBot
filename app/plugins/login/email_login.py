from pyrogram import Client, filters, types

@Client.on_callback_query(filters.regex("login_with_email"))
async def email_login(Client: Client, callback: types.CallbackQuery):
    await Client.answer_callback_query(
        callback.id,
        "Login with email is not available. Please use another method.",
        show_alert=True
    )