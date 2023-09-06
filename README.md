# Sally Assistant: Telegram Bot for GPT-4

Sally Assistant is a private and secured open-source client for GPT-4 on Telegram. It acts as a proxy to the OpenAI API, providing users with a seamless experience to interact with the latest version of ChatGPT. With added features like templates and context management, it enhances the user experience.

## Features

- **Commands**: Easily manage your interaction with the bot using commands.
- **Templates**: Save and invoke frequently used text templates.
- **Context Management**: The bot remembers the context of the conversation, allowing for more coherent interactions.

## Getting Started

### Prerequisites

Ensure you have the following environment variables set:

- `OPENAI_API_KEY`: Your OpenAI API key.
- `TELEGRAM_API_KEY`: Your Telegram API key.

### Deployment

The project includes a `Dockerfile` and `docker-compose` for easy deployment.

To start the bot:

1. Clone the repository.
2. Set the environment variables.
3. Use `docker-compose up` to start the bot.

The entry point for the bot is `bot.py`.

## Commands

- `/start`: Start or restart the bot.
- `/reset`: Reset the context.
- `/help`: Display help.
- `/templates`: Display a list of all saved templates.
- `/template template_name`: Display the text of a specific template.
- `/save_template`: Save a new template. Format: `/save_template template_name template_body`. To invoke the template after saving, type `$template_name`.
- `/delete_template`: Delete a template. Format: `/delete_template template_name`.

## About

**What are templates?**

Templates allow you to save frequently used text. For instance, you can create an English Teacher template using the command `/save_template eng_teacher “Act as an English teacher...”` and then invoke this template by typing `$eng_teacher`.

**What is context?**

The bot operates in context mode by default, remembering previous messages. This ensures a coherent conversation within a single topic. Use the `/reset` command to reset the context.

## Limits

Currently, the bot is free to use, with a limit of 15 requests per day.

## Contribute

Interested in contributing to Sally Assistant? Check out the project on [GitHub](https://github.com/petrNikolaev1/sally-assistant).

## Contact

For AI/ML product development inquiries, reach out on Telegram: [@impecableMe](https://t.me/impecableMe).
