# Aditya Halder // @Itz_VeNom_xD 

import os
import aiofiles
import aiohttp
import ffmpeg
import requests
from os import path
from asyncio.queues import QueueEmpty
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from modules.cache.admins import set
from modules.clientbot import clientbot, queues
from modules.clientbot.clientbot import client as USER
from modules.helpers.admins import get_administrators
from youtube_search import YoutubeSearch
from modules import converter
from modules.downloaders import youtube
from modules.config import DURATION_LIMIT, que, SUDO_USERS
from modules.cache.admins import admins as a
from modules.helpers.filters import command, other_filters
from modules.helpers.command import commandpro
from modules.helpers.decorators import errors, authorized_users_only
from modules.helpers.errors import DurationLimitError
from modules.helpers.gets import get_url, get_file_name
from PIL import Image, ImageFont, ImageDraw
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

# plus
chat_id = None
useer = "NaN"


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def generate_cover(requested_by, title, views, duration, foreground):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("resource/20220122_161057.jpg")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("resource/font.otf", 32)
    draw.text((190, 550), f"Title: {title[:50]} ...", (255, 255, 255), font=font)
    draw.text((190, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Powered By: @shivamdemon",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    commandpro(["/play", "/yt", "/ytp", "play", "yt", "ytp", "@", "#"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer
    
    lel = await message.reply("**🔎 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 ...**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "TSF_MUSIC"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "**😇𝐀𝐭 𝐅𝐢𝐫𝐬𝐭 𝐌𝐚𝐤𝐞 𝐌𝐞 𝐀𝐝𝐦𝐢𝐧 ...**")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "** 𝐈 𝐀𝐦 𝐑𝐞𝐚𝐝 𝐓𝐨 𝐏𝐥𝐚𝐲 𝐒𝐨𝐧𝐠𝐬...🐬**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"**👉👅𝐏𝐥𝐞𝐚𝐬𝐞 𝐌𝐚𝐧𝐮𝐚𝐥𝐥𝐲 𝐀𝐝𝐝 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐎𝐫 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐓𝐨 : @II_TSF_OWNER_II 🥀** ")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"**👉👅𝐏𝐥𝐚𝐞𝐚𝐬𝐞 𝐌𝐚𝐧𝐮𝐚𝐥𝐥𝐲 𝐀𝐝𝐝 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐎𝐫 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐓𝐨 : @II_TSF_OWNER_II 🥀 ...*")
        return
    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**💥𝐘𝐨𝐮𝐫 𝐌𝐮𝐬𝐢𝐜 𝐈𝐬 𝐋𝐨𝐧𝐠𝐞𝐫 𝐭𝐡𝐚𝐧 {DURATION_LIMIT} 💞 𝐌𝐢𝐧𝐮𝐭𝐞 ...**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/8e71217a281c15f73a306.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝐒𝐮𝐩𝐩𝐨𝐫𝐭🔉",
                            url=f"https://t.me/SECRET_CITTY")

                ]
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝐒𝐮𝐩𝐩𝐨𝐫𝐭🔉",
                            url=f"https://t.me/SECRET_CITTY")

                ]
            ]
        )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/8e71217a281c15f73a306.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝐒𝐮𝐩𝐩𝐨𝐫𝐭🔉",
                            url=f"https://t.me/SECRET_CITTY")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**💥𝐘𝐨𝐮𝐫 𝐌𝐮𝐬𝐢𝐜 𝐈𝐬 𝐋𝐨𝐧𝐠𝐞𝐫 𝐭𝐡𝐚𝐧 {DURATION_LIMIT} 💞 𝐌𝐢𝐧𝐮𝐭𝐞 ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "**𝐆𝐢𝐯𝐞 𝐒𝐨𝐦𝐞𝐭𝐡𝐢𝐧𝐠 𝐓𝐨 𝐏𝐥𝐚𝐲 𝐁𝐚𝐛𝐞🤭**"
        await lel.edit("**🔄 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "**🔊𝐈 𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧🧐...**"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝐒𝐮𝐩𝐩𝐨𝐫𝐭🔉",
                            url=f"https://t.me/SECRET_CITTY")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**💥𝐘𝐨𝐮𝐫 𝐌𝐮𝐬𝐢𝐜 𝐈𝐬 𝐋𝐨𝐧𝐠𝐞𝐫 𝐭𝐡𝐚𝐧 {DURATION_LIMIT} 💞 𝐌𝐢𝐧𝐮𝐭𝐞 ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption="**𝐓𝐒𝐅 𝐑𝐨𝐜𝐤𝐬\n🔊 𝐀𝐭 𝐏𝐨𝐬𝐢𝐭𝐢𝐨𝐧 » `{}` ...**".format(position),
            reply_markup=keyboard,
        )
    else:
        await clientbot.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**𝐓𝐒𝐅 𝐑𝐨𝐜𝐤𝐬 𝐍𝐨𝐰 💞\n🔊 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 𝐎𝐩 🔜...**".format(),
           )

    os.remove("final.png")
    return await lel.delete()
    
    
@Client.on_message(commandpro(["/pause", "pause"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await clientbot.pytgcalls.pause_stream(message.chat.id)
    await message.reply_text(**𝐏𝐚𝐮𝐬𝐞𝐝🎧 ...**"
    )


@Client.on_message(commandpro(["/resume", "resume"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await clientbot.pytgcalls.resume_stream(message.chat.id)
    await message.reply_text(**𝐑𝐞𝐬𝐮𝐦𝐞𝐝 🔜 ...**"
    )



@Client.on_message(commandpro(["/skip", "/next", "skip", "next"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("**🔥𝐓𝐒𝐅 𝐑𝐨𝐜𝐤𝐬 \n𝐍𝐨𝐭𝐡𝐢𝐧𝐠 🚫 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 ...**")
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await clientbot.pytgcalls.leave_group_call(chat_id)
        else:
            await clientbot.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        clientbot.queues.get(chat_id)["file"],
                    ),
                ),
            )


    await message.reply_photo(
                             photo="https://telegra.ph/file/1ca8c27be50581f86aa3f.jpg", 
                             caption=f'**💥 Kaal Tornado 🔈 𝐌𝐮𝐬𝐢𝐜🤞𝐍𝐨𝐰 🥀\n⏩ 𝐒𝐤𝐢𝐩𝐩𝐞𝐝 🌷 ...**'
   ) 


@Client.on_message(commandpro(["/end", "end", "/stop", "stop", "x"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        clientbot.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await clientbot.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text(**𝐍𝐨𝐨𝐛 𝐔❌ 𝐒𝐭𝐨𝐩𝐩𝐞𝐝 𝐄𝐯𝐞𝐫𝐲𝐭𝐡𝐢𝐧𝐠...**"
    )


@Client.on_message(commandpro(["reload", "refresh"]))
@errors
@authorized_users_only
async def admincache(client, message: Message):
    set(
        message.chat.id,
        (
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ),
    )

    await message.reply_text(**𝐑𝐞𝐥𝐨𝐚𝐝𝐞𝐝 𝐃𝐨𝐧𝐞...**"
    )
