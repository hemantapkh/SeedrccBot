from plugins.functions.bars import space_bar
from plugins.functions.convert import convert_size
from pyrogram import Client, filters, types
from seedrcc import Seedr


@Client.on_message(filters.custom.cmd("account") & filters.custom.login_required)
async def account(Client: Client, message: types.Message):
    seedr: Seedr = message.seedr
    seedr_config = seedr.getSettings()
    account_setting = seedr_config.get("account", {})

    text = """
    <b>{account}</b>

    {username}: {username_value}
    {bandwidth}: {bandwidth_value}
    {country}: {country_value}
    {invite_link}: {invite_link_value}
    {invite_remaining}: {invite_remaining_value}
    {invite_accepted}: {invite_accepted_value}

    {space_used} / {space_max}
    {bars}
    """.format(
        account=Client.language.get_button_text("account"),
        username=Client.language.get_text("username"),
        bandwidth=Client.language.get_text("totalBandwidthUsed"),
        country=Client.language.get_text("country"),
        username_value=account_setting.get("username"),
        invite_link=Client.language.get_text("inviteLink"),
        invite_remaining=Client.language.get_text("inviteRemaining"),
        invite_accepted=Client.language.get_text("inviteAccepted"),
        bandwidth_value=convert_size(account_setting.get("bandwidth_used")),
        country_value=seedr_config.get("country"),
        invite_link_value=f"https://seedr.cc?r={account_setting.get('user_id')}",
        invite_remaining_value=account_setting.get("invites"),
        invite_accepted_value=account_setting.get("invites_accepted"),
        space_used=convert_size(account_setting.get("space_used")),
        space_max=convert_size(account_setting.get("space_max")),
        bars=space_bar(
            account_setting.get("space_max"), account_setting.get("space_used")
        ),
    )

    buttons = [
        [
            types.InlineKeyboardButton(
                Client.language.get_button_text("removeAccount"), "logout"
            )
        ]
    ]

    await Client.send_message(
        message.from_user.id,
        text=text,
        reply_markup=types.InlineKeyboardMarkup(buttons),
    )
