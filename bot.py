import random
import datetime
from pathlib import Path
import logging
import time

import twitchio
from twitchio.ext import commands
# import requests

from db_agent import Agent
from dice import Dice

# https://twitchio.dev/en/stable/
# https://twitchio.dev/en/stable/quickstart.html
# https://twitchio.dev/en/stable/exts/commands.html
# https://twitchio.dev/en/stable/twitchio.html
# https://twitchio.dev/en/stable/reference.html
# https://twitchio.dev/en/stable/exts/routines.html

class Bot(commands.Bot):
    def __init__(self) -> None:
        self.__currTime = time.localtime()
        if not Path('./logs').is_dir():
            Path('./logs').mkdir()
        logging.basicConfig(filename='./logs/twitchbot_'+'runtime_'+self._configureFilename(self.__currTime)+'.log', encoding='utf-8', level=logging.INFO)
        self._printLog('Initializing...')
        self._printLog('Saving log to '+'./logs/twitchbot_'+'runtime_'+self._configureFilename(self.__currTime)+'.log')
        if not self._checkFiles():
            self.__currTime = True
            return None
        super().__init__(token=self._readToken(), prefix='!', initial_channels=self._readChannel())
        self.__agent = Agent()
        self.__agent.connect()
        self.__diceBag = [Dice(4), Dice(6), Dice(8), Dice(10), Dice(12), Dice(20),]
        self.__secretDiceBag = [Dice(4), Dice(6), Dice(8), Dice(10), Dice(12), Dice(20),]
        self.__command_names = []
        for cmd in self.commands:
            if cmd not in ['shoutout', 'rollHistory', 'addQuote']: # Removing commands needing special privlages 
                self.__command_names.append(cmd)
    # end __init__

    def __del__(self) -> None:
        self._printLog('Shutting down bot...')
        if isinstance(self.__currTime, bool):
            self.__currTime
        else:
            del self.__currTime, self.__agent, self.__diceBag, self.__secretDiceBag, self.__command_names, 
        self._printLog('Bot successfully shutdown.')
        self._printLog('-----------------------------------------------------------')
    # end __del__

    def _configureFilename(self, timeData) -> str:
        currTimeString = str(timeData[0])
        if len(str(timeData[1])) == 1:
            currTimeString += '0'+str(timeData[1])
        else:
            currTimeString += str(timeData[1])
        if len(str(timeData[2])) == 1:
            currTimeString += '0'+str(timeData[2])
        else:
            currTimeString += str(timeData[2])
        return currTimeString
    # end configureFilename
    
    def _printLog(self, text:str)  -> None:
        currTime = str(time.ctime())
        print(currTime+' - '+text)
        logging.info(currTime+' - '+text)
    # end _printLog

    def _checkFiles(self) -> bool:
        status = []
        if not Path('./keys').is_dir():
            Path('./keys').mkdir()
            self._printLog('./keys directory has been created.')
        if not Path('./data').is_dir():
            Path('./data').mkdir()
            self._printLog('./data directory has been created.')
        if not Path('./keys/token.txt').is_file():
            with open('./keys/token.txt', 'w') as file:
                file.write()
            self._printLog('./token.txt has been created.')
            self._printLog('Please fill out the newly created token file. \nTokens can be generated at this link: https://twitchtokengenerator.com/')
            status.append(False)
        else:
            status.append(True)
        if not Path('./keys/password.txt').is_file():
            with open('./keys/password.txt', 'w') as file:
                file.write()
            self._printLog('./keys/password.txt has been created.')
            self._printLog('Please fill out the newly created password file.')
            status.append(False)
        else:
            status.append(True)
        if not Path('./keys/channels.txt').is_file():
            with open('./keys/channels.txt', 'w') as file:
                file.write()
            self._printLog('./keys/channels.txt has been created.')
            status.append(False)
        else:
            status.append(True)
        if not Path('./data/who.txt').is_file():
            with open('./data/who.txt', 'w') as file:
                file.write()
            self._printLog('./data/who.txt has been created.')
        if False in status:
            return False
        else:
            return True
    # end _checkDirs

    def _readToken(self) -> str:
        with open('./keys/token.txt', 'r') as file:
            for line in file.readlines():
                if line != '' and len(line) > 0:
                    return line        
    # end _readToken

    def _readChannel(self) -> list[str]:
        channels = []
        with open('./keys/channels.txt', 'r') as file:
            for line in file.readlines():
                if line != '' and len(line) > 0:
                    channels.append(line)
        return channels
    # end _readChannel

    async def _verifyUser(self, user) -> twitchio.User | None:
        users = await self.fetch_users(names=[user])
        for i in users:
            if i.name.lower() == user.lower():
                return i
        return None
    # end _verifyUser

    def start(self) -> None:
        self.run()
    # end start

    async def event_ready(self) -> None:
        self._printLog(f'Logged in as | {self.nick}')
        self._printLog(f'User id is | {self.user_id}')
        for i in self.connected_channels:
            self._printLog(f'Bot now active in {i.name}')
            await i.send('Beep Boop, WolfBot now online.')
        # await commands.Context.send('Beep-Boop, WolfBot now online.')
    # end event_ready

    # async def event_command_error(self, ctx: commands.Context, error: Exception):
    #     print('Error: ', ctx.author.name, ': ', ctx.message.content, ' | ', error)
    # end event_command_error

    async def event_message(self, ctx: commands.Context) -> None:
        if type(ctx.author) != type(None):
            user = await self._verifyUser(ctx.author.name)
            if user != None:
                while not self.__agent._checkUserExistence(ctx.channel.name, user.id, user.name,):
                    self._printLog('Attempting to reconnect to the Database...')
                    if self.__agent.connect():
                        self._printLog('Successfully reconnected to Database.')
                    else:
                        self._printLog('Could not connect to Database.')
                        self._printLog(f'Failed to add user {user.name} with id {user.id} to the database')
                await self.handle_commands(ctx)
    # end event_message

    ###         COMMANDS         ###
    @commands.command(name="hello")
    async def hello_command(self, ctx: commands.Context) -> None:
        await ctx.send(f'Hello there {ctx.author.name}!')
    # end hello

    @commands.command(name="howl")
    async def howl_command(self, ctx: commands.Context) -> None:
        await ctx.send(f'Awooooooo!')
    # end howl_command

    @commands.command(name="help")
    async def help_command(self, ctx: commands.Context, commandName:str | None) -> None:
        if commandName != None:
            if commandName in self.commands:
                # print(self.commands[commandName].__doc__)
                print(exec("self."+commandName+"_command.__doc__"))
                # print(self.commands)
                # print(self.commands['shoutout'].name, self.commands['shoutout'].cog, self.commands['shoutout'].aliases, )
                # await ctx.send(f'Usage of {commandName}: {exec("self."+commandName+"_command.__doc__")}')
        else:
            await ctx.send(f'The following commands can be used: {', '.join(self.__command_names)}')
    # end help

    @commands.command(name="uptime")
    async def uptime_command(self, ctx: commands.Context) -> None:
        streamer = await self._verifyUser(ctx.channel.name)
        if streamer != None:
            streams = await self.fetch_streams(user_ids=[streamer.id])
            for i in streams:
                if i.user.name == ctx.channel.name:
                    await ctx.send(f'{self.nick} has been live for {(datetime.datetime.now(datetime.UTC).replace(microsecond=0) - i.started_at.replace(microsecond=0))}')
                    break
    # end uptime

    @commands.command(name="shoutout", aliases=("so",))
    async def shoutout_command(self, ctx: commands.Context, targetUser:str) -> None:
        """testing does this work? hello? !shoutout targetUser"""
        # moderators = [] # Should see if the author is in a list of moderators
        if ctx.author.name == ctx.channel.name:
            exists = await self.fetch_channel(targetUser)#search_channel(user)
            if exists.user.name.lower() == targetUser.lower():
                self._printLog(f'Shoutout given to {targetUser} by {ctx.author.name}')
                await ctx.send(f'Everyone go checkout '+f'@{targetUser} at https://twitch.tv/{targetUser} They were last seen in the {exists.game_name} category! Be sure to give them a follow!' )
            else:
                self._printLog(f'Shoutout to {targetUser} by {ctx.author.name} failed.')
    # end shoutout_command

    @commands.command(name="love")
    async def love_command(self, ctx: commands.Context, targetUser:str | None) -> None:
        if targetUser != None:
            user2 = await self._verifyUser(targetUser)
            if user2 != None:
                user1 = await self._verifyUser(ctx.author.name)
                result1 = self.__agent.queryDB(ctx.channel.name, user1.id, user1.name, 'cookies')
                result2 = self.__agent.queryDB(ctx.channel.name, user2.id, user2.name, 'cookies')
                dice1 = self.__secretDiceBag[5].roll()*(result1['cookies']/100)*5
                dice2 = self.__secretDiceBag[5].roll()*(result2['cookies']/100)*5
                result = (dice1+dice2) / 2
                await ctx.send(f'The love between @{user1.name} and @{user2.name} is {result}%')
        else:
            user1 = await self._verifyUser(ctx.author.name)
            if user1 != None:
                result1 = self.__agent.queryDB(ctx.channel.name, user1.id, user1.name, 'cookies')
                dice1 = self.__secretDiceBag[5].roll()*(result1['cookies']/100)*5
                result = (dice1+self.__secretDiceBag[5].roll()*5)/2
                await ctx.send(f'The love between @{user1.name} and WolfBot is {result}%')
    # end love_command

    @commands.command(name="who")
    async def who_command(self, ctx: commands.Context) -> None:
        people = []
        with open('who.txt', 'r') as file:
            for line in file.readlines():
                if line != '' and len(line) > 0:
                    people.append('@'+str(line))
        if len(people) == 1:
            await ctx.send(f'Now streaming with {people[0]}.')
        elif len(people) > 1:
            await ctx.send(f'Now streaming with {', '.join(people[:-1])}, and {people[-1]}.')
        else:
            await ctx.send(f'ComradeWolf is not currently streaming with anyone.')
    # end who_command

    @commands.command(name="cookie", aliases=("cookies", "biscuits"))
    async def cookie_command(self, ctx: commands.Context, targetUser:str | None) -> None:
        if targetUser == None:
            user1 = await self._verifyUser(ctx.author.name)
            if user1 != None:
                resultTime = self.__agent.queryDB(ctx.channel.name, user1.id, user1.name, 'cookiesRewardTime')
                if datetime.datetime.now() > resultTime['cookiesRewardTime'] + datetime.timedelta(days=1):
                    result = self.__agent.queryDB(ctx.channel.name, user1.id, user1.name, 'cookies')
                    amount = int(self.__secretDiceBag[5].roll()*(100/result['cookies'])) # Give more to them if they have less, and give less to them if they have more
                    self.__agent.incrementDB(ctx.channel.name, user1.id, user1.name, 'cookies', amount)
                    result = self.__agent.queryDB(ctx.channel.name, user1.id, user1.name, 'cookies')
                    if amount != 1:
                        await ctx.send(f'@{user1.name} has been given {amount} cookies and they have {result['cookies']} cookies.')
                    else:
                        await ctx.send(f'@{user1.name} has been given {amount} cookie and they have {result['cookies']} cookies.')
                else:
                    result = self.__agent.queryDB(ctx.channel.name, user1.id, user1.name, 'cookies')
                    await ctx.send(f'{user1.name} has {result['cookies']} cookies.')
        else:
            if targetUser[0] == '@':
                targetUser = targetUser[1:]
            user2 = await self._verifyUser(targetUser)
            if user2 != None:
                result = self.__agent.queryDB(ctx.channel.name, user2.id, user2.name, 'cookies')
                await ctx.send(f'@{user2.name} has {result['cookies']} cookies.')
    # end cookie_command

    @commands.command(name='giveCookies')
    async def giveCookies_command(self, ctx: commands.Context, amount:int, targetUser:str | None) -> None:
        if targetUser != None:
            if targetUser[0] == '@':
                targetUser = targetUser[1:]
            user1 = await self._verifyUser(ctx.author.name)
            user2 = await self._verifyUser(targetUser)
            if user1 != None and user2 != None:
                result = self.__agent.queryDB(ctx.channel.name, user1.id, user1.name, 'cookies')
                if result['cookies'] == 0:
                    await ctx.send(f'{ctx.author.name} has no cookies to give.')
                elif result['cookies'] > amount:
                    self.__agent.incrementDB(ctx.channel.name, user1.id, user1.name, 'cookies', -amount)
                    self.__agent.incrementDB(ctx.channel.name, user2.id, user2.name, 'cookies', amount)
                    if amount > 1:
                        await ctx.send(f'{ctx.author.name} gave {amount} cookies to @{user2.name}.')
                    else:
                        await ctx.send(f'{ctx.author.name} gave 1 cookie to @{user2.name}.')
                else:
                    self.__agent.incrementDB(ctx.channel.name, user1.id, user1.name, 'cookies', -result['cookies'])
                    self.__agent.incrementDB(ctx.channel.name, user2.id, user2.name, 'cookies', result['cookies'])
                    if result['cookies'] > 1:
                        await ctx.send(f'{ctx.author.name} gave {result['cookies']} cookies to @{user2.name}.')
                    else:
                        await ctx.send(f'{ctx.author.name} gave 1 cookie to @{user2.name}.')
    # end give_cookies

    @commands.command(name="stealCookies")
    async def stealCookies_command(self, ctx: commands.Context, targetUser:str | None) -> None: # Needs timing
        if targetUser != None:
            if targetUser[0] == '@':
                targetUser = targetUser[1:]
            user1 = await self._verifyUser(ctx.author.name)
            user2 = await self._verifyUser(targetUser)
            if user1 != None and user2 != None:
                result = self.__agent.queryDB(ctx.channel.name, user2.id, user2.name, 'cookies')
                if result['cookies'] > 0:
                    result2 = self.__agent.queryDB(ctx.channel.name, user1.id, user1.name, 'cookies')
                    attacker = self.__secretDiceBag[5].roll()*(100/result2['cookies'])
                    defender = self.__secretDiceBag[5].roll()*(100/result['cookies'])
                    if attacker > defender:
                        stealQuantity = int((result['cookies']*.5)*(self.__secretDiceBag[5].roll()*5)*(100/result2['cookies']))#+random.randint(1, int(result['cookies']*0.1))
                        if stealQuantity > 0:
                            self.__agent.incrementDB(ctx.channel.name, user2.id, user2.name, 'cookies', -stealQuantity)
                            self.__agent.incrementDB(ctx.channel.name, user1.id, user1.name, 'cookies', stealQuantity)
                            result = self.__agent.queryDB(ctx.channel.name, user1.id, user1.name, 'cookies')
                            if stealQuantity == 1:
                                await ctx.send(f'@{ctx.author.name} stole {stealQuantity} cookie from @{user1.name}!')
                            else:
                                await ctx.send(f'@{ctx.author.name} stole {stealQuantity} cookies from @{user1.name}!')
                        else:
                            await ctx.send(f'@{ctx.author.name} failed to steal cookies from @{user1.name}!')
                    else:
                        await ctx.send(f'@{ctx.author.name} failed to steal cookies from @{user1.name}!')
                else:
                    await ctx.send(f'@{user1.name} has no cookies to steal.')
    # end steal_cookies

    @commands.command(name='roll')
    async def roll_command(self, ctx:commands.Context, dice:str) -> None:
        user = await self._verifyUser(ctx.author.name)
        if user != None:
            for key, value in enumerate(['d4', 'd6', 'd8', 'd10', 'd12', 'd20']):
                if dice == value:
                    roll = self.__diceBag[key].roll()
                    self.__agent.updateDB(ctx.channel.name, user.id, user.name, 'lastRoll', roll)
                    self.__agent.updateDB(ctx.channel.name, user.id, user.name, 'lastRolledDice', dice)
                    await ctx.send(f'{ctx.author.name} rolled a {dice} and got {roll}.')
                    break
    # end roll

    @commands.command(name='lastRoll')
    async def lastRoll_command(self, ctx:commands.Context) -> None:
        user = await self._verifyUser(ctx.author.name)
        if user != None:
            roll = self.__agent.queryDB(ctx.channel.name, user.id, user.name, 'lastRoll')
            dice = self.__agent.queryDB(ctx.channel.name, user.id, user.name, 'lastRolledDice')
            await ctx.send(f'{ctx.author.name} rolled a {dice['lastRolledDice']} and got {roll['lastRoll']}.')
    # end lastRoll

    @commands.command(name='rollHistory')
    async def rollHistory_command(self, ctx:commands.Context, dice:str) -> None:
        if ctx.author.name == ctx.channel.name:
            for key, value in enumerate(['d4', 'd6', 'd8', 'd10', 'd12', 'd20']):
                if dice == value:
                    history = [str(i) for i in self.__diceBag[key].history()]
                    await ctx.send(f'{dice} hisotry: {', '.join(history)}.')
                    break
    # end rollHistory

    @commands.command(name='addQuote')
    async def addQuote_command(self, ctx:commands.Context, *args) -> None:
        # moderators = []
        quote = ' '.join(args)
        if ctx.author.name == ctx.channel.name:
            if self.__agent.addQuote(ctx.channel.name, quote):
                self._printLog(f'New quote added by {ctx.author.name}: "{quote}"')
    # end add_quote

    @commands.command(name='quote')
    async def quote_command(self, ctx:commands.Context, number:int | None) -> None: # Might be off by 1, double check later
        # quotes = ['Beep Boop, no quotes found.',]
        if number != None:
            if number > 0:
                if number < self.__agent.getQuoteCount(ctx.channel.name):
                    result = self.__agent.getQuote(ctx.channel.name, number)
                    if result != False:
                        await ctx.send(f'Quote #{number}: "{result['quote']}"')
                    else:
                        await ctx.send(f'Beep Boop, Quote #{number} was not found.')
        else:
            count = self.__agent.getQuoteCount(ctx.channel.name)
            if count == 1:
                result = self.__agent.getQuote(ctx.channel.name, 1)
                await ctx.send(f'Quote #{1}: "{result['quote']}"')
            elif count > 1:
                pick = random.randint(1, count)
                result = self.__agent.getQuote(ctx.channel.name, pick)
                await ctx.send(f'Quote #{pick}: "{result['quote']}"')
            else:
                await ctx.send(f'Beep Boop, no quotes were found.')
    # end quote_command
# end Bot