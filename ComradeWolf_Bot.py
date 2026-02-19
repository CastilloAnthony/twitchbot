from importlib import reload
import webbrowser
import asyncio
from fetch_ids import fetch_ids
asyncio.run(fetch_ids())

import logging
from typing import TYPE_CHECKING

import asqlite

import twitchio
from twitchio import eventsub
from twitchio.ext import commands

if TYPE_CHECKING:
    import sqlite3

LOGGER: logging.Logger = logging.getLogger("Bot")

from readClientSettings import readClientSettings
import CommandsCore
import CommandsMath
import CommandsPZ

class ComradeWolf_Bot(commands.AutoBot):
    def __init__(self, *, token_database: asqlite.Pool, subs: list[
        eventsub.SubscriptionPayload, 
        ]) -> None:
        self.token_database = token_database
        self.__client_settings = readClientSettings()
        super().__init__(
            client_id=self.__client_settings['client_id'],
            client_secret=self.__client_settings['client_secret'],
            bot_id=self.__client_settings['bot_id'],
            owner_id=self.__client_settings['owner_id'],
            prefix=self.__client_settings['prefix'],
            subscriptions=subs,
            force_subscribe=True,
            )
        webbrowser.open('http://localhost:4343/oauth?scopes=channel:bot%20channel:read:ads&force_verify=true')
    # end __init__

    async def setup_hook(self) -> None:
        # Add our component which contains our commands...
        # These components can be swapped out, but the bot must be restarted for changes here to go into effect.
        self.__componentModules = [CommandsCore, CommandsMath, CommandsPZ] # Modules where these command components can be found
        self.__components = []
        # Changes to these files/modules must simply be reloaded with the bot's !reload command.
        self.__components.append(CommandsCore.CommandsCore(self))
        self.__components.append(CommandsMath.CommandsMath(self))
        self.__components.append(CommandsPZ.CommandsPZ(self))
        for i in self.__components:
            await self.add_component(i)
        #     LOGGER.info(f'{i.name} has been loaded.')
    # end setup_hook

    async def reloadComponents(self,) -> None:
        for i in self.__components:
            await self.remove_component(i.name)
            # LOGGER.info(f'{i.name} has been unloaded.')
        for i in self.__componentModules:
            reload(i)
        await self.setup_hook()
        LOGGER.info(f'{', '.join(component.name for component in self.__components)} have been reloaded.')
    # end reloadComponents

    async def event_oauth_authorized(self, payload: twitchio.authentication.UserTokenPayload) -> None:
        # Go to this link in a web browser where the BOT is logged in.
        # BOT: http://localhost:4343/oauth?scopes=user:read:chat%20user:write:chat%20user:bot%20moderator:read:followers%20channel:read:ads&force_verify=true
        
        # Then go to this link in a web browser where the USER is logged in.
        # USER: http://localhost:4343/oauth?scopes=channel:bot%20channel:read:ads&force_verify=true
        # This link is set to open automatically when the bot is initialized
        await self.add_token(payload.access_token, payload.refresh_token)

        if not payload.user_id:
            return

        if payload.user_id == self.bot_id:
            # We usually don't want subscribe to events on the bots channel...
            return

        # A list of subscriptions we would like to make to the newly authorized channel...
        subs: list[eventsub.SubscriptionPayload] = [
            eventsub.ChatMessageSubscription(broadcaster_user_id=payload.user_id, user_id=self.bot_id),
            eventsub.ChannelFollowSubscription(broadcaster_user_id=payload.user_id, moderator_user_id=self.bot_id),
            eventsub.AdBreakBeginSubscription(broadcaster_user_id=payload.user_id),
            eventsub.ChannelRaidSubscription(to_broadcaster_user_id=payload.user_id),
        ]

        resp: twitchio.MultiSubscribePayload = await self.multi_subscribe(subs)
        for i in resp.errors:
            if resp.errors:
                LOGGER.warning("Failed to subscribe to: %r, for user: %s \n", i, payload.user_id)
        for i in resp.success:
            if resp.success:
                LOGGER.warning('Subbed to: %r, for user: %s \n', i, payload.user_id)
    # end event_oauth_authorized

    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        # Make sure to call super() as it will add the tokens interally and return us some data...
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(token, refresh)

        # Store our tokens in a simple SQLite Database when they are authorized...
        query = """
        INSERT INTO tokens (user_id, token, refresh)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            token = excluded.token,
            refresh = excluded.refresh;
        """

        async with self.token_database.acquire() as connection:
            await connection.execute(query, (resp.user_id, token, refresh))

        LOGGER.info("Added token to the database for user: %s", resp.user_id)
        return resp
    # end add_token

    async def event_ready(self) -> None:
        LOGGER.info(f'Logged in as {self.user} with User Id {self.bot_id}')
        # LOGGER.info(f'User id is | {self.bot_id}')
    # end event_ready
# end Bot