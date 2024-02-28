from typing import Final
import os
import sys
from dotenv import load_dotenv
from discord import Intents, Client, Message
from messaging import send_message
import logging
import argparse


def read_file(filename: str) -> list[str]:
    logging.debug(f'reading file "{filename}"')
    with open(filename, 'r', encoding='utf-8') as fp:
        return fp.readlines()


# Load ENV VARIABLES
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
BOT_ID: Final[str] = os.getenv('BOT_ID')
QUOTES_FILENAME: Final[str] = os.getenv('QUOTES_FILENAME')
QUOTES: Final[list[str]] = read_file(QUOTES_FILENAME)

# Setup Bot
intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)

# Botting
@client.event
async def on_ready() -> None:
    logging.info(f'{client.user} is now running!')


# Message Handling
@client.event
async def on_message(message: Message) -> None:
    # Prevent recursive/infinite loop
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    logging.debug(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message, BOT_ID, QUOTES)


def parse_arguments(args):
    parser =  argparse.ArgumentParser(description='A bot that gives Roi Loth quotes.')
    parser.add_argument(
        'logging', 
        help='setup the logging level', 
        choices=[
            'CRITICAL',
            'ERROR',
            'WARNING',
            'INFO',
            'DEBUG'
        ])
    
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    logging.basicConfig(level=args.logging)
    client.run(token=TOKEN)
