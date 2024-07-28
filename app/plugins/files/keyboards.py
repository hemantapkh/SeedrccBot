from pyrogram import Client, types


def item_keyboard(item_id: str, is_folder=True) -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                Client.language.get_button_text("getLink"), "get_download_link_"
            ),
            types.InlineKeyboardButton(
                Client.language.get_button_text("delete"), "delete_"
            ),
        ],
        [
            types.InlineKeyboardButton(
                Client.language.get_button_text("openInPlayer"), "open_media_"
            ),
        ],
    ]

    if is_folder:
        buttons.append(
            [
                types.InlineKeyboardButton(
                    "Search", switch_inline_query_current_chat=f"#files {item_id}"
                )
            ]
        )

    return types.InlineKeyboardMarkup(buttons)
