import asyncio
from time import time
from datetime import datetime
from modules.helpers.filters import command
from modules.helpers.command import commandpro
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)
    
   

@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/8e71217a281c15f73a306.jpg",
        caption=f"""**━━━━━━━━━━━━━━━━━━━━━━━━
💥 ʜᴇʏ, 𝐓𝐒𝐅 𝐑𝐎𝐂𝐊𝐒 ʜᴇʀᴇ sᴜᴘᴇʀ ғᴀsᴛ ᴠᴄ ᴘʟᴀʏᴇʀ
ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs ...
┏━━━━━━━━━━━━━━━━━┓
┣★ ᴄʀᴇᴀᴛᴏʀ : [𝚂•4•𝚂𝙷𝙸𝚅](https://t.me/SHIVAMDEMON)
┣★ ɢʀᴏᴜᴘ : [𝚂𝙴𝙲𝚁𝙴𝚃 𝚂𝙾𝙲𝙸𝙴𝚃𝚈](https://t.me/SECRET_CITTY)
┣★ ɴᴇᴛᴡᴏʀᴋ : [𝚃𝚂𝙵 𝙽𝙴𝚃𝚆𝙾𝙺](https://t.me/TSFNETWORK)
┣★ 🔥ᴏᴡɴᴇʀ😇› : [𝚃𝚂𝙵•𝚁𝙰𝙿𝚂𝚃𝙰𝚁](https://t.me/II_TSF_OWNER_II)
┗━━━━━━━━━━━━━━━━━┛

🔥ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs ᴛʜᴇɴ sᴏʟᴜᴛɪᴏɴ🔜
ᴅᴍ ᴛᴏ ᴍᴇ[𝚃𝚂𝙵•𝚁𝙰𝙿𝚂𝚃𝙰𝚁](https://t.me/II_TSF_OWNER_II) ...
━━━━━━━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ ❰ ᴊᴏɪɴ ʜᴇʀᴇ ғᴏʀ Tɪᴍᴇᴘᴀss ❱ ➕", url=f"https://t.me/SECRET_CITTY")
                ]
                
           ]
        ),
    )
    
    
@Client.on_message(commandpro(["/start", "/alive", "Candy"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/3c190879a1301a29659c3.jpg",
        caption=f"""""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝚃𝚂𝙵 𝙽𝙴𝚃𝚆𝙾𝚁𝙺", url=f"https://t.me/TSFNETWORK")
                ]
            ]
        ),
    )


@Client.on_message(commandpro(["repo", "#repo", "@repo", "/repo", "source"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/319ecc64d7c22862ca432.jpg",
        caption=f"""""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ᴀsᴋ ғᴏʀ ʀᴇᴘᴏ 💞", url=f"https://t.me/SHIVAMDEMON")
                ]
            ]
        ),
    )
