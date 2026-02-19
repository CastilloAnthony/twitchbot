from twitchio.ext import commands

class CommandsMath(commands.Component):
    def __init__(self, bot) -> None:
        # Passing args is not required...
        # We pass bot here as an example...
        self.__bot = bot # Not necessary here
        # LOGGER.info(f'{self.name} component loaded.')
    # end __init__

    @commands.group(invoke_fallback=True)
    async def math(self, ctx: commands.Context) -> None:
        """Command to invite a chatter to use math!

        !math
        """
        await ctx.reply(f'What kind of math do you want? (!math help)')
    # end math

    @math.command()
    async def help(self, ctx: commands.Context) -> None:
        """Command that replies with help on math formatting.

        !math help
        """
        await ctx.reply(f"Try one of these: !math < {' | '.join(self.math.commands.keys())} > i.e.: !math * 7 7")
    # end add

    @math.command(aliases=['+'])
    async def add(self, ctx: commands.Context, left: int, right: int) -> None:
        """Command which adds two integers.

        !math add <number> <number>
        """
        await ctx.reply(f"{left} + {right} = {left + right}")
    # end add

    @math.command(aliases=['-'])
    async def subtract(self, ctx: commands.Context, left: int, right: int) -> None:
        """Command which subtracts two integers.

        !math subtract <number> <number>
        """
        await ctx.reply(f"{left} - {right} = {left - right}")
    # end add

    @math.command(aliases=['*'])
    async def multiply(self, ctx: commands.Context, left: int, right: int) -> None:
        """Command which multiplies two integers.

        !math multiply <number> <number>
        """
        await ctx.reply(f"{left} * {right} = {left * right}")
    # end multiply

    @math.command(aliases=['/'])
    async def divide(self, ctx: commands.Context, left: int, right: int) -> None:
        """Command which divides two integers.

        !math divide <number> <number>
        """
        await ctx.reply(f"{left} / {right} = {left / right}")
    # end add
# end CommandsMath