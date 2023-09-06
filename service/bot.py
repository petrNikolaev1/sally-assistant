import logging
import re
from typing import List, Dict

from aioredis import Redis
from aiotg import Bot, Chat, BotApiError
from openai import InvalidRequestError

from service.constants import TELEGRAM_API_KEY, OPENAI_API_KEY, HELP_TEXT, INITIAL_PROMPT
from service.gpt_client import ChatGPT
from service.models import Message
from service.storage.context_storage import Storage

bot = Bot(api_token=TELEGRAM_API_KEY)
chat_gpt = ChatGPT(openai_api_key=OPENAI_API_KEY)
redis: Dict[int, List[Message]] = {}
storage = Storage(Redis(host="127.0.0.1", port=9876))
logger = logging.getLogger()


@bot.command("/start")
async def start(chat: Chat, match):
    await storage.reset_context(chat.id)
    await chat.send_text("Hello, I'm Sally. How can I assist you today? "
                         "Use /help to list all commands")


@bot.command("/help")
async def help(chat: Chat, match):
    await chat.send_text(HELP_TEXT, parse_mode="MarkdownV2")


@bot.command("/reset")
async def reset(chat: Chat, match):
    await storage.reset_context(chat.id)
    await chat.send_text("Context reset")


@bot.command("/save_template ([\\w]+) (.*)")
async def save_template(chat: Chat, match):
    match = re.findall(r"/save_template (\w+) (.*)", chat.message["text"])
    await storage.save_template(
        user_id=chat.id,
        name=match[0][0],
        template=match[0][1],
    )
    await chat.send_text("Template saved", )


@bot.command("/delete_template ([\\w]+)")
async def delete_template(chat: Chat, match):
    await storage.delete_template(
        user_id=chat.id,
        name=match.group(1),
    )
    await chat.send_text("Template deleted")


@bot.command("/template ([\\w]+)")
async def get_template(chat: Chat, match):
    text = await storage.get_template(
        user_id=chat.id,
        name=match.group(1),
    )
    await chat.send_text(f"Template text:\n\n{text}")


@bot.command("/templates")
async def list_templates(chat: Chat, match):
    template_names = await storage.list_templates(
        user_id=chat.id,
    )
    if template_names:
        await chat.send_text("Templates: \n\n" + "\n* ".join(template_names))
    else:
        await chat.send_text("You don't have any templates")


@bot.command(r"\$\w+")
async def gpt_template(chat: Chat, match):
    message = chat.message["text"]
    for template_name in re.findall(r"\$\w+", message):
        template = await storage.get_template(chat.id, template_name[1:])
        if template:
            chat.message["text"] = message.replace(template_name, template)

    await gpt_fallback(chat, match)


@bot.command(r".*")
async def gpt_fallback(chat: Chat, match):
    context = await storage.get_context(chat.id)
    message = chat.message["text"]
    context.chat_context.append(
        {
            "role": "user",
            "content": message,
        }
    )
    tmp_message = await chat.send_text("Loading...")
    response = None
    for retry in range(3):
        try:
            response = await chat_gpt.process(context.chat_context)
        except InvalidRequestError:  # ушли за контекст
            context.chat_context = [INITIAL_PROMPT] + context.chat_context[3:]

    await chat.delete_message(tmp_message["result"]["message_id"])

    if response is None:
        await storage.reset_context(chat.id)
        await chat.reply("Unexpected error occurred. Context reset")

    reply_text = response.choices[0].message.content
    try:
        formatted_text = reply_text\
            .replace("!", "\!") \
            .replace("-", "\-") \
            .replace("<", "\<") \
            .replace(">", "\>") \
            .replace("(", "\(") \
            .replace(")", "\)") \
            .replace("[", "\[") \
            .replace("]", "\]") \
            .replace("}", "\}") \
            .replace("{", "\{") \
            .replace("+", "\+") \
            .replace("~", "\~") \
            .replace("#", "\#") \
            .replace("=", "\=") \
            .replace("_", "\_") \
            .replace("**", "~") \
            .replace("*", "__") \
            .replace("~", "*") \
            .replace(".", "\.")
        await chat.reply(formatted_text, parse_mode="MarkdownV2")
    except BotApiError:
        await chat.reply(reply_text)
    context.chat_context.append(
        {
            "role": "system",
            "content": reply_text,
        }
    )
    await storage.update_context(chat.id, context)
