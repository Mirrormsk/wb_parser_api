from telethon import TelegramClient, events
from config import settings
from parsers.wb_parser import wb_parser

bot = TelegramClient('bot', settings.API_ID, settings.API_HASH).start(bot_token=settings.BOT_TOKEN)


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Hi! Welcome to the WBParser.\nSend "wild: <product name>" to get list of products.')
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='wild:'))
async def echo(event):
    """Parse user query and sends results from WB"""
    query = event.text.lstrip('wild:').strip()
    raw_results = wb_parser.parse_query(query)
    normalized_results = wb_parser.normalize_results(raw_results)
    text = '\n\n'.join(normalized_results)
    await event.respond(text)


def main():
    """Start the bot."""
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
