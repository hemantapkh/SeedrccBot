from pyrogram import Client, filters, types
from seedrcc import Seedr


@Client.on_message(filters.custom.cmd("active") & filters.custom.login_required)
async def active_torrents(Client: Client, message: types.Message):
    seedr: Seedr = message.seedr

    account_contents = seedr.listContents()

    if not account_contents.get("torrents"):
        await Client.send_message(
            message.from_user.id,
            text=Client.language.get_text("noActiveTorrents"),
        )
        return
