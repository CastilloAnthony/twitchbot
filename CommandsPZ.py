# import twitchio
from twitchio.ext import commands

# from ComradeWolf_Bot import ComradeWolf_Bot

class CommandsPZ(commands.Component):
    # An example of a Component with some simple commands and listeners
    # You can use Components within modules for a more organized codebase and hot-reloading.

    def __init__(self, bot) -> None:
        # Passing args is not required...
        # We pass bot here as an example...
        self.__bot = bot # Not necessary here
        self.__map = 'https://b42map.com/?10628x9815'
        self.__modpack = 'https://steamcommunity.com/sharedfiles/filedetails/?id=3656145637'
        # LOGGER.info(f'{self.name} component loaded.')
    # end __init__

    @commands.command()
    async def map(self, ctx: commands.Context) -> None:
        """Command that replies with a link to an online project zomboid map.

        !map
        """
        await ctx.reply(f'Here is a link to the B42 map: {self.__map}')
    # end map

    @commands.command()
    async def mods(self, ctx: commands.Context) -> None:
        """Command that replies with a link to the mod collection we're using on steam.

        !mods
        """
        await ctx.reply(f'Here is a link to the modpack we are using: {self.__modpack}')
    # end mods

    @commands.command()
    async def server(self, ctx: commands.Context) -> None:
        """Command that replies with information on the server.

        !server
        """
        await ctx.reply(f'We are currently plaing on a server hosted and managed by @Pedguin.')
    # end mods
# end PZCommandComponent