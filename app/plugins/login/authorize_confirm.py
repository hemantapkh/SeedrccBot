from pyrogram import Client, filters, types
from seedrcc import Login, Seedr


@Client.on_callback_query(filters.regex("authorize_confirm"))
async def authorize_confirm(Client: Client, callback: types.CallbackQuery):
    device_code = callback.data.split("_")[-1]
    
    seedr = Login()
    seedr.authorize(device_code)
    
    if seedr.token:
        # Fetching user settings from seedr
        ac = Seedr(token=seedr.token)
        account_settings = ac.getSettings()
        
        # Add user info on database
        await Client.DB.set_account(
            user_id=callback.message.chat.id,
            account_config=account_settings,
            token=seedr.token
        )
        
        await Client.delete_messages(
            chat_id=callback.message.chat.id,
            message_ids=callback.message.id
        )
        
        await Client.send_message(
            chat_id=callback.message.chat.id,
            text=Client.language.get_text("loggedInAs").format(account_settings['account']['username']),
            reply_markup=Client.keyboard.main_menu()
        )
        
    else:
        await Client.answer_callback_query(
            callback.id,
            Client.language.get_text("notAuthorized"),
            show_alert=True
        )
