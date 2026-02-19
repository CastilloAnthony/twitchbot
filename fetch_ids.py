import asyncio
import twitchio
# import logging
from readClientSettings import readClientSettings
from updateClientSettings import updateClientSettings

async def fetch_ids() -> None:
    client_settings = readClientSettings()
    if client_settings['client_id'] != '' and client_settings['client_secret'] != '':
        async with twitchio.Client(client_id=client_settings['client_id'], client_secret=client_settings['client_secret']) as client:
            await client.login()
            user = await client.fetch_users(logins=[client_settings['owner_username'], client_settings['bot_username']])
            for u in user:
                # LOGGER.info(f"User: {u.name} - ID: {u.id}")
                if str(client_settings['bot_username']).lower() == u.name:
                    client_settings['bot_id'] = u.id
                    updateClientSettings(client_settings)
                    # LOGGER.info(f'Updated id for username {u.name}')
                elif str(client_settings['owner_username']).lower() == u.name:
                    client_settings['owner_id'] = u.id
                    updateClientSettings(client_settings)
                    # LOGGER.info(f'Updated id for username {u.name}')

if __name__ == "__main__":
    asyncio.run(fetch_ids())