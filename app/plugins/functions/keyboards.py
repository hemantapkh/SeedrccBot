from pyrogram import Client, types


class KeyBoard:
    def __init__(self, client):
        self.client = client

    def add_accounts(self) -> types.InlineKeyboardMarkup:
        buttons = [
            [
                types.InlineKeyboardButton(
                    Client.language.get_button_text("signup"), url="https://seedr.cc"
                )
            ],
            [
                types.InlineKeyboardButton(
                    Client.language.get_button_text("authorizeWithDevice"),
                    "authorize_device",
                )
            ],
            [
                types.InlineKeyboardButton(
                    Client.language.get_button_text("loginWithEmail"),
                    "login_with_email",
                )
            ],
        ]

        return types.InlineKeyboardMarkup(buttons)

    def main_menu(self) -> types.ReplyKeyboardMarkup:
        buttons = [
            [
                types.KeyboardButton(Client.language.get_button_text("files")),
                types.KeyboardButton(Client.language.get_button_text("active")),
            ],
            [
                types.KeyboardButton(Client.language.get_button_text("account")),
            ],
        ]

        return types.ReplyKeyboardMarkup(
            buttons,
            resize_keyboard=True,
            is_persistent=True,
        )
