

import config
from MusicSp import app
try:
    from pyrogram.enums import ButtonStyle
except ImportError:
    class ButtonStyle:
        PRIMARY = None
        SECONDARY = None
        SUCCESS = None
        DANGER = None
        DEFAULT = None
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_GROUP),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.PRIMARY,
            )
        ],
        [InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper")],
        [
            InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL, icon_custom_emoji_id="6289681091880039542"),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_GROUP, icon_custom_emoji_id="6289371012421132934" ),
        ],
        [InlineKeyboardButton(text="𝐎𝐰𝐧𝐞𝐫", user_id=config.OWNER_ID, style=ButtonStyle.SUCCESS, icon_custom_emoji_id="6289755072691707859")],
    ]
    return buttons
