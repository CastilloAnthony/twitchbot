import random
import datetime
from pathlib import Path
import logging
import time

import twitchio
from twitchio.ext import commands
import requests

from db_agent import Agent
from dice import Dice

# https://twitchio.dev/en/stable/
# https://twitchio.dev/en/stable/quickstart.html
# https://twitchio.dev/en/stable/exts/commands.html
# https://twitchio.dev/en/stable/twitchio.html
# https://twitchio.dev/en/stable/reference.html
# https://twitchio.dev/en/stable/exts/routines.html

class Bot(commands.Bot):
    def __init__(self):
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
            if cmd not in ['shoutout']: # Removing commands needing special privlages 
                self.__command_names.append(cmd)
    # end __init__

    def __del__(self):
        if isinstance(self.__currTime, bool):
            self.__currTime
        else:
            del self.__currTime, self.__agent, self.__diceBag, self.__secretDiceBag, self.__command_names, 
    # end __del__

    def _configureFilename(self, timeData):
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
    
    def _printLog(self, text:str):
        currTime = str(time.ctime())
        print(currTime+' - '+text)
        logging.info(currTime+' - '+text)
    # end _printLog

    def _checkFiles(self):
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

    def _readToken(self):
        with open('./keys/token.txt', 'r') as file:
            for line in file.readlines():
                if line != '' and len(line) > 0:
                    return line        
    # end _readToken

    def _readChannel(self):
        channels = []
        with open('./keys/channels.txt', 'r') as file:
            for line in file.readlines():
                if line != '' and len(line) > 0:
                    channels.append(line)
        return channels
    # end _readChannel

    def start(self):
        self.run()
    # end start

    async def event_ready(self):
        self._printLog(f'Logged in as | {self.nick}')
        self._printLog(f'User id is | {self.user_id}')
        # await commands.Context.send('Beep-Boop, WolfBot now online.')
    # end event_ready

    # async def event_command_error(self, ctx: commands.Context, error: Exception):
    #     print('Error: ', ctx.author.name, ': ', ctx.message.content, ' | ', error)
    # end event_command_error

    async def event_message(self, ctx: commands.Context):
        if type(ctx.author) != type(None):
            while not self.__agent._checkUserExistence(ctx.channel.name, ctx.author.name):
                self._printLog('Attempting to reconnect to the Database...')
                self.__agent.connect()
            await self.handle_commands(ctx)
    # end event_message

    ###         COMMANDS         ###
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello there {ctx.author.name}!')
    # end hello

    @commands.command(name="howl")
    async def howl_command(self, ctx: commands.Context):
        await ctx.send(f'Awooooooo!')
    # end howl_command

    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.send(f'The following commands can be used: {', '.join(self.__command_names)}')
    # end help

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        print(f'https://twitch.tv/{ctx.channel.name}')
        if 'isLiveBroadcast' in requests.get(f'https://twitch.tv/{ctx.channel.name}').content.decode('utf-8'):
            stream = await self.fetch_streams(user_logins=[ctx.channel.name])
            print('Uptime Test | ', type(stream), stream)
            await ctx.send(f'{self.nick} has been live for {datetime.datetime.now() - stream.started_at}')
    # end uptime

    @commands.command(name="shoutout", aliases=("so",))
    async def shoutout_command(self, ctx: commands.Context, user:str):
        if ctx.author.name == ctx.channel.name:
            self._printLog(f'Shouting out {user}')
            await ctx.send(f'/shoutout {user}')
    # end shoutout_command

    @commands.command(name="love")
    async def love_command(self, ctx: commands.Context, user:str):
        if user != None:
            result1 = self.__agent.queryDB(ctx.channel.name, ctx.author.name, 'cookies')
            result2 = self.__agent.queryDB(ctx.channel.name, user, 'cookies')
            dice1 = self.__secretDiceBag[5].roll()*(result1['cookies']/100)*5
            dice2 = self.__secretDiceBag[5].roll()*(result2['cookies']/100)*5
            result = (dice1+dice2) / 2
            await ctx.send(f'The love between @{ctx.author.name} and @{user} is {result}%')
    # end love_command

    @commands.command(name="who")
    async def who_command(self, ctx: commands.Context):
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
    async def cookie_command(self, ctx: commands.Context, user:str | None) -> None:
        if user == None:
            result = self.__agent.queryDB(ctx.channel.name, ctx.author.name, 'cookies')
            await ctx.send(f'{ctx.author.name} has {result['cookies']} cookies.')
        else:
            if user[0] == '@':
                user = user[1:]
            result = self.__agent.queryDB(ctx.channel.name, user, 'cookies')
            await ctx.send(f'@{user} has {result['cookies']} cookies.')
    # end cookie_command

    @commands.command(name='give')
    async def give_cookies(self, ctx: commands.Context, amount:int, user:str | None) -> None:
        if user[0] == '@':
            user = user[1:]
        result = self.__agent.queryDB(ctx.channel.name, ctx.author.name, 'cookies')
        if result['cookies'] == 0:
            await ctx.send(f'{ctx.author.name} has no cookies to give.')
        elif result['cookies'] > amount:
            self.__agent.incrementDB(ctx.channel.name, ctx.author.name, 'cookies', -amount)
            self.__agent.incrementDB(ctx.channel.name, user, 'cookies', amount)
            if amount > 1:
                await ctx.send(f'{ctx.author.name} gave {amount} cookies to @{user}.')
            else:
                await ctx.send(f'{ctx.author.name} gave 1 cookie to @{user}.')
        else:
            self.__agent.incrementDB(ctx.channel.name, ctx.author.name, 'cookies', -result['cookies'])
            self.__agent.incrementDB(ctx.channel.name, user, 'cookies', result['cookies'])
            if result['cookies'] > 1:
                await ctx.send(f'{ctx.author.name} gave {result['cookies']} cookies to @{user}.')
            else:
                await ctx.send(f'{ctx.author.name} gave 1 cookie to @{user}.')
    # end give_cookies

    @commands.command(name="steal")
    async def steal_cookies(self, ctx: commands.Context, user:str | None) -> None:
        if user != None:
            if user[0] == '@':
                user = user[1:]
            result = self.__agent.queryDB(ctx.channel.name, user, 'cookies')
            if result['cookies'] > 0:
                # attack = self.roll(ctx, 'd20')
                stealQuantity = random.randint(1, int(result['cookies']*0.1))
                self.__agent.incrementDB(ctx.channel.name, user, 'cookies', -stealQuantity)
                self.__agent.incrementDB(ctx.channel.name, ctx.author.name, 'cookies', stealQuantity)
                result = self.__agent.queryDB(ctx.channel.name, ctx.author.name, 'cookies')
                if stealQuantity == 1:
                    await ctx.send(f'{ctx.author.name} stole {stealQuantity} cookie from @{user}!')
                else:
                    await ctx.send(f'{ctx.author.name} stole {stealQuantity} cookies from @{user}!')
            else:
                await ctx.send(f'@{user} has no cookies to steal.')
    # end steal_cookies

    @commands.command(name='roll')
    async def roll(self, ctx:commands.Context, dice:str) -> None:
        for key, value in enumerate(['d4', 'd6', 'd8', 'd10', 'd12', 'd20']):
            if dice == value:
                roll = self.__diceBag[key].roll()
                self.__agent.updateDB(ctx.channel.name, ctx.author.name, 'lastRoll', roll)
                self.__agent.updateDB(ctx.channel.name, ctx.author.name, 'lastRolledDice', dice)
                await ctx.send(f'{ctx.author.name} rolled a {dice} and got {roll}.')
                break
    # end roll

    @commands.command(name='lastRoll')
    async def lastRoll(self, ctx:commands.Context) -> None:
        roll = self.__agent.queryDB(ctx.channel.name, ctx.author.name, 'lastRoll')
        dice = self.__agent.queryDB(ctx.channel.name, ctx.author.name, 'lastRolledDice')
        await ctx.send(f'{ctx.author.name} rolled a {dice['lastRolledDice']} and got {roll['lastRoll']}.')
    # end lastRoll

    @commands.command(name='rollHistory')
    async def rollHistory(self, ctx:commands.Context, dice:str) -> None:
        for key, value in enumerate(['d4', 'd6', 'd8', 'd10', 'd12', 'd20']):
            if dice == value:
                history = [str(i) for i in self.__diceBag[key].history()]
                await ctx.send(f'{dice} hisotry: {', '.join(history)}.')
                break
    # end rollHistory
# end Bot