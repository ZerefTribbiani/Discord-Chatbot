import os

import discord
import openai
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
completion = openai.Completion()

DB_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
sessions = None   # Keeps track of conversations created when bot is connected

start_sequence = '\nAI:'
restart_sequence = '\nHuman: '
session_prompt = 'The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: '


def get_response(message, chat_log):
    prompt_text = f'{chat_log}{restart_sequence}{message}{start_sequence}'
    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=prompt_text,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    response = response['choices'][0]['text']
    return str(response)


def append_chat_log(message, response, chat_log):
    return f'{chat_log}{restart_sequence}{message}{start_sequence}{response}'


@bot.event
async def on_ready():
    global sessions
    sessions = {guild.id: {channel.id: None for channel in guild.text_channels} for guild in bot.guilds}
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def start(ctx):
    if sessions[ctx.guild.id][ctx.channel.id]:
        await ctx.send('There is already an ongoing conversation in this channel')
    else:
        sessions[ctx.guild.id][ctx.channel.id] = session_prompt
        await ctx.send('Session started')


@bot.command()
async def chat(ctx, *, message):
    chat_log = sessions[ctx.guild.id][ctx.channel.id]
    if chat_log:
        response = get_response(message, chat_log)
        sessions[ctx.guild.id][ctx.channel.id] = append_chat_log(message, response, chat_log)
        await ctx.send(response)
    else:
        await ctx.send("You haven't started a session in this channel")


@bot.command()
async def end(ctx):
    sessions[ctx.guild.id][ctx.channel.id] = None
    await ctx.send('Ended any session in this channel')


bot.run(DB_TOKEN)

