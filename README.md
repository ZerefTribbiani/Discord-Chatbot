# Discord-Chatbot
Very simple discord chatbot that makes use of the OpenAI API and dicord.py python library

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [discord.py](https://pypi.org/project/discord.py/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [openai library](https://pypi.org/project/openai/)
- a .env file in the same directory with your discord bot token (named 'DISCORD_BOT_TOKEN') and OpenAI token (named 'OPENAI_API_KEY')

## Features
Bot has 3 commands, .start to start a session in a channel, .chat to chat with the bot and .end to end an existing session

Conversations are channel specific, one channel can only have one session but you can have multiple sessions across different channels
