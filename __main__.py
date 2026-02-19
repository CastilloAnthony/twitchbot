import asyncio
from fetch_ids import fetch_ids
asyncio.run(fetch_ids())

import twitchio
from twitchio import eventsub

from typing import TYPE_CHECKING
import asqlite
if TYPE_CHECKING:
    import sqlite3

import logging
LOGGER: logging.Logger = logging.getLogger("Bot")

from readClientSettings import readClientSettings
from ComradeWolf_Bot import ComradeWolf_Bot

# Our main entry point for our Bot
# Best to setup_logging here, before anything starts
def main() -> None:
    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        async with asqlite.create_pool("tokens.db") as tdb:
            tokens, subs = await setup_database(tdb)

            async with ComradeWolf_Bot(token_database=tdb, subs=subs) as bot:
                for pair in tokens:
                    await bot.add_token(*pair)

                await bot.start(load_tokens=False)

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt")
# end main

async def setup_database(db: asqlite.Pool) -> tuple[list[tuple[str, str]], list[
    eventsub.SubscriptionPayload, 
    eventsub.ChannelFollowSubscription, 
    eventsub.AdBreakBeginSubscription, 
    eventsub.ChannelRaidSubscription,
    ]]:
    # Create our token table, if it doesn't exist..
    # You should add the created files to .gitignore or potentially store them somewhere safer
    # This is just for example purposes...

    query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
    async with db.acquire() as connection:
        await connection.execute(query)

        # Fetch any existing tokens...
        rows: list[sqlite3.Row] = await connection.fetchall("""SELECT * from tokens""")

        tokens: list[tuple[str, str]] = []
        subs: list[
            eventsub.SubscriptionPayload,
            eventsub.ChannelFollowSubscription, 
            eventsub.AdBreakBeginSubscription, 
            eventsub.ChannelRaidSubscription,
            ] = []

        client_settings = readClientSettings()

        for row in rows:
            tokens.append((row["token"], row["refresh"]))

            if row["user_id"] == client_settings['bot_id']:
                continue

            subs.extend([
                eventsub.ChatMessageSubscription(broadcaster_user_id=row["user_id"], user_id=client_settings['bot_id']),
                ])

    return tokens, subs
# end setup_database

if __name__ == "__main__":
    main()