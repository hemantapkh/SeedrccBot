from plugins.functions.convert import convert_size
from pyrogram import Client, filters, types
from seedrcc import Seedr

from .keyboards import item_keyboard


@Client.on_inline_query(filters.regex("#files") & filters.custom.login_required)
async def query_search(Client: Client, inline_query: types.InlineQuery):
    seedr: Seedr = inline_query.seedr

    folder_id: str = inline_query.query.split()[-1]

    contents = seedr.listContents(folder_id)
    results = []

    for items in ["torrents", "folders", "files"]:
        for item in contents[items]:
            results.append(
                types.InlineQueryResultArticle(
                    title=item.get("name"),
                    thumb_url=item.get("thumb") or None,
                    description="💾 {} 📅 {}".format(
                        convert_size(item.get("size")),
                        item.get("last_update"),
                    ),
                    input_message_content=types.InputTextMessageContent(
                        item.get("name")
                    ),
                    reply_markup=item_keyboard(
                        item_id=item.get("id"),
                        is_folder=True if items == "folders" else False,
                    ),
                ),
            )

    await Client.answer_inline_query(
        inline_query.id,
        results=results,
        cache_time=10,
        switch_pm_parameter="inlineQuery",
    )
