from pyrogram.client import Client
import pyrogram.filters
import pyrogram
from pyrogram.types import WebPage, WebPageEmpty
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

API_ID = 0
API_HASH = ""

triggers = ["https://opensea.io/collection/whatthefluff", "Play-To-Earn"]

trusted_users: list[pyrogram.types.User] = []

app = Client("session", api_id=API_ID, api_hash=API_HASH)

def fuck_or_not(filter: pyrogram.filters.Filter, client: pyrogram.client.Client, update: pyrogram.types.Message) -> bool:
    if not update.from_user:
        return False
    if update.from_user:
        if update.from_user in trusted_users:
            return False
    if update.media == pyrogram.enums.MessageMediaType.WEB_PAGE_PREVIEW:
        if not isinstance(update.web_page_preview.webpage, WebPage):
            return True
        for trigger in triggers:
            if not trigger.lower() in update.web_page_preview.webpage.description.lower() or trigger.lower() in update.text.lower():
                return False
        return True
    return False


async def fuck_nigger(client: Client, msg: pyrogram.types.Message):
    if isinstance(msg.web_page_preview.webpage, WebPageEmpty):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(msg.web_page_preview.webpage.url)
        should_fuck = True
        for trigger in triggers:
            if driver.page_source.lower().find(trigger.lower()) == -1:
                should_fuck = False
                break
        driver.quit()
        if not should_fuck:
            return
    if msg.from_user.username:
        nigger = "@"+msg.from_user.username
    else:
        nigger = f"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id})"
    try:
        await client.delete_messages(chat_id=msg.chat.id, message_ids=msg.id)
        await client.ban_chat_member(chat_id=msg.chat.id, user_id=msg.from_user.id)
    except Exception as e:
        await client.send_message(chat_id=msg.chat.id, text=f"Can't fuck nigger {nigger}. The error is \"{str(e)}\".")
        return
    await client.send_message(chat_id=msg.chat.id, text=f"Fucked nigger {nigger}.\n\n DON'T SEND NFT SHIT YOU ASSHOLE")


async def dont_fuck_me(client: Client, msg: pyrogram.types.Message):
    if msg.from_user in trusted_users:
        await msg.reply("You are already in the list")
        return
    trusted_users.append(msg.from_user)
    await msg.reply("Okay, I won't fuck you. But that doesn't mean you can send NFT shit.")


filter = pyrogram.filters.create(fuck_or_not)
app.add_handler(pyrogram.handlers.message_handler.MessageHandler(fuck_nigger, filter))
app.add_handler(pyrogram.handlers.message_handler.MessageHandler(dont_fuck_me, pyrogram.filters.command("dont_fuck_me")))
print("Starting NFT-Fucker-8000")
app.run()

