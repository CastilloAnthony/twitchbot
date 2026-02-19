import datetime
# import random

import twitchio
from twitchio.ext import commands

# from ComradeWolf_Bot import Bot
from dice import Dice

class CommandsCore(commands.Component):
    # An example of a Component with some simple commands and listeners
    # You can use Components within modules for a more organized codebase and hot-reloading.

    def __init__(self, bot) -> None:
        # Passing args is not required...
        # We pass bot here as an example...
        self.__bot = bot
        self.__diceBag = [Dice(4), Dice(6), Dice(8), Dice(10), Dice(12), Dice(20),]
        self.__secretDiceBag = [Dice(4), Dice(6), Dice(8), Dice(10), Dice(12), Dice(20),]
        self.__socials = {
            'github':'https://github.com/CastilloAnthony',
            'bluesky':'https://bsky.app/profile/comradewolf7.bsky.social',
            }
        # LOGGER.info(f'{self.name} component loaded.')
    # end __init__

    # An example of listening to an event
    # We use a listener in our Component to display the messages received.
    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"{datetime.datetime.now()} [{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")
        if "hello there" in payload.text:
            await payload.respond(f'General {payload.chatter}')
        elif payload.text in ['hi', 'hello', 'howdy']:
            await payload.respond(f'Hello {payload.chatter}')
    # end event_message

    @commands.Component.listener()
    async def event_follow(self, payload: twitchio.ChannelFollow) -> None:
        # LOGGER.info(f'New follow for {payload.broadcaster} by {payload.user}!')
        await payload.respond(f'Hey, thanks for following {payload.user}!')
    # end event_follow
    
    @commands.Component.listener()
    async def event_ad_break(self, payload: twitchio.ChannelAdBreakBegin) -> None:
        if payload.automatic:
            # LOGGER.info(f'A {payload.duration} automatic AD break has just begun for {payload.broadcaster}')
            await payload.broadcaster.send_message(f'A {payload.duration} AD break has just begun, sorry twitch makes them run.')
        else:
            # LOGGER.info(f'A {payload.duration} AD break has just begun for {payload.broadcaster}')
            await payload.broadcaster.send_message(
                f'A {payload.duration} AD break has just begun.', 
                self #self.__client_settings['bot_id']
                )
    # end event_ad_break
    
    @commands.Component.listener()
    async def event_raid(self, payload: twitchio.ChannelRaid) -> None:
        # LOGGER.info(f'Raided for {payload.to_broadcaster} from {payload.from_broadcaster}!')
        await payload.to_broadcaster.send_message(
            f'Woah! Thanks for the raid {payload.from_broadcaster.mention} and welcome in Raiders!!!', 
            self
            )
    # end event_raid

    @commands.command(name='reload')
    async def reload(self, ctx: commands.Context) -> None:
        if ctx.chatter == ctx.broadcaster:
            await self.__bot.reloadComponents()
        else:
            await ctx.reply(f'Sorry, you don\t have permission to do that.')
    # end reload

    @commands.command(name='help')
    async def help(self, ctx: commands.Context) -> None:
        print(f'Here is a list of all available commands: {', '.join(self.__bot.commands)}')
        await ctx.reply(f'Here is a list of all available commands: {', '.join(self.__bot.commands)}')
    # end help

    @commands.group(invoke_fallback=True)
    async def socials(self, ctx: commands.Context) -> None:
        """Group command for our social links.

        !socials
        """
        # await ctx.send("discord.gg/..., youtube.com/..., twitch.tv/...")
        await ctx.send(f'I don\'t really use social media; however I do have a github! {self.__socials['github']}')
    # end group

    @socials.command(name="github")
    async def socials_github(self, ctx: commands.Context) -> None:
        """Sub command of socials that sends only our github invite.

        !socials github
        """
        await ctx.send(f"Github: {self.__socials['github']}")
    # end socials_discord

    @socials.command(name="bluesky")
    async def socials_github(self, ctx: commands.Context) -> None:
        """Sub command of socials that sends only our bluesky invite.

        !socials bluesky
        """
        await ctx.send(f"BlueSky: {self.__socials['bluesky']}")
    # end socials_discord

    @socials.command(name="discord")
    async def socials_discord(self, ctx: commands.Context) -> None:
        """Sub command of socials that sends only our discord invite.

        !socials discord
        """
        await ctx.send("I do not have a discord server setup for public use at the momemnt, however that might change in the future.")
    # end socials_discord

    @commands.command(name="howl")
    async def howl_command(self, ctx: commands.Context):
        """Makes the bot howl in chat.

        !howl
        """
        await ctx.send(f'Awooooooo!')
    # end howl_command

    @commands.command(name="roll")
    async def roll(self, ctx: commands.Context, dice:str) -> None:
        """Command to roll a type of dice in the chat for the chatter

        Takes in a 'dx' argument and
        !roll <d4|d6|d8|d10|d12|d20>
        """
        for key, value in enumerate(['d4', 'd6', 'd8', 'd10', 'd12', 'd20']):
            if dice == value:
                roll = self.__diceBag[key].roll()
                await ctx.send(f'{ctx.author.name} rolled a {dice} and got {roll}.')
                break
    # end roll

    @commands.command(name="love")
    async def love_command(self, ctx: commands.Context, user:twitchio.User):
        """Command to generate a random percentage that represents "love" between two users and outputs a chat message in the form of "The love between [Source] and [Target] is [percentage]%"

        Requires an additional username as an input
        !love <Yogscast|Pedguin|xRandomSarahx>
        """
        if user != None: # Minimum percentage will be 5%, maximum will be 100%
            results = []
            results.append(self.__secretDiceBag[5].roll())
            results.append(self.__secretDiceBag[5].roll())
            results.append(self.__secretDiceBag[5].roll())
            results.append(self.__secretDiceBag[5].roll())
            results.append(self.__secretDiceBag[5].roll())
            await ctx.send(f'The love between {ctx.chatter.mention} and {user.mention} is {sum(results)}%')
    # end love_command

    # @commands.command()
    # async def choice(self, ctx: commands.Context, *choices: str) -> None:
    #     """Command which takes in an arbitrary amount of choices and randomly chooses one.

    #     !choice <choice_1> <choice_2> <choice_3> ...
    #     """
    #     await ctx.reply(f"You provided {len(choices)} choices, I choose: {random.choice(choices)}")
    # # end choice

    # @commands.command(aliases=["thanks", "thank"])
    # async def give(self, ctx: commands.Context, user: twitchio.User, amount: int, *, message: str | None = None) -> None:
    #     """A more advanced example of a command which has makes use of the powerful argument parsing, argument converters and
    #     aliases.

    #     The first argument will be attempted to be converted to a User.
    #     The second argument will be converted to an integer if possible.
    #     The third argument is optional and will consume the reast of the message.

    #     !give <@user|user_name> <number> [message]
    #     !thank <@user|user_name> <number> [message]
    #     !thanks <@user|user_name> <number> [message]
    #     """
    #     msg = f"with message: {message}" if message else ""
    #     await ctx.send(f"{ctx.chatter.mention} gave {amount} thanks to {user.mention} {msg}")
    # # end give

# end MyComponent