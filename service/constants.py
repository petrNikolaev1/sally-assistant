import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

INITIAL_PROMPT = {
"role": "user",
"content": """
You are a Sally assistant – a Telegram bot. You assist people with a background in product, business, and marketing. Below are the basic instructions that should be applied to each prompt:

Instructions list:
1) Keep in mind that your messages will be displayed in Telegram. Ensure they are readable.
2) Make headers bold in all your answers, using this format:**TEXT**.
3) You can use italic text by following this format: *TEXT*.
4) Insert '____________________' after large text blocks. But do not place it at the end of your answer.
5) Start sentences without spaces at the beginning.
6) Provide concrete and concise answers.
"""
}


HELP_TEXT = """Private and secured open\-source client for GPT\-4 in Telegram\. Want to contribute\? github link

*Commands*

\/start
Start or restart the bot

\/reset
Reset the context

\/help
Help

\/templates
Display a list of all saved templates

\/template template\_name
Display the text of the template

\/save\_template
Save a new template\. Format: \/save\_template template\_name template\_body\. To invoke the template after saving, type \$template\_name

\/delete\_template
Delete a template\. Format: \/delete\_template template\_name

**About the bot**

The bot operates through the official ChatGPT API from OpenAI's latest version\.

*What are templates?*

You can save any text as a template to save time if you often ask similar questions\.

For example, create an English Teacher template using the command \/save\_template eng\_teacher “Act as an English teacher\.\.\.”

Then invoke this template by typing $eng\_teacher

*What is context?*

By default, the bot operates in context mode, meaning it remembers previous messages\. This is done so that you can specify additions or have a conversation within a single topic\. The \/reset command resets the context\.

*Limits*

For now, the bot is free, and you can make 15 requests per day\.

*Want to develop an AI/ML product\?*

Contact — @rinatkh\."""