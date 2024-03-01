from discord import Message
import logging
from random import choice


def get_response(user_input: str, quotes: list[str]) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return choice(quotes)
    elif lowered == 'aide' or lowered == 'help' or lowered == 'man' or lowered == '\?':
        return '''
        C\'est pas bien compliqué, nous sommes chez les salauds mais avec du théatre.\nJe réponds au mots, lettres et autres conneries. Tant que je suis mentionné dans le message.\n\nPar exemple, @Roi Loth D'Orcanie mundis.
        "Je vais te répondre avec une citation qui contient \'mundis\'."\n\nAutrement, pour avoir la liste des citations tu peux me le demander en utilisant un de ces mots [list|quotes|citations].
        "Par example, @Roi Loth D'Orcanie citations."'''
    elif lowered == 'list' or lowered == 'quotes' or lowered == 'citations':
        return '\n'.join(quotes)
    else:
        candidates = [x for x in filter(lambda x: lowered in x.lower(), quotes)]
        return choice(candidates)


async def send_message(message: Message, user_message: str, bot_id: str, quotes: list[str]) -> None:
    logging.debug(f'message: \"{message}\"')

    if not user_message:
        logging.debug('Message is empty')
        return

    # Works on mention
    mentions = [str(x.id) for x in message.mentions]
    bot_mentionned: bool = bot_id in mentions
    logging.debug(f'bot_mentionned: \"{bot_mentionned}\"')
    
    if bot_mentionned:
        # Cleanup / remove all mentions ids
        for mention in mentions:
            user_message = user_message.replace(f'<@{mention}>','')
        user_message = user_message.strip()
        logging.debug(f'parsed user_message: \"{user_message}\"')

        # Private messaging if starts with '?'
        if is_private := user_message[0] == '?':
            user_message = user_message[1:]

        try:
            response: str = get_response(user_message, quotes)
            await message.author.send(response) if is_private else await message.channel.send(response)
        except Exception as e:
            print(e)
