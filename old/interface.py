import time
from json import dumps
from threading import Thread

from bot import Bot

import requests
import uvicorn
import fastapi
from fastapi import FastAPI, Request, HTTPException # and Jinja for templating
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# https://fastapi.tiangolo.com/
# https://fastapi.tiangolo.com/advanced/templates/

# app = FastAPI()
# app.mount('/static', StaticFiles(directory='./static'), name='static')
# templates = Jinja2Templates(directory="./templates")

class Interface():
    def __init__(self):
        self.__app = FastAPI()
        self.__twitchBot = Bot()
        self.__botThread = Thread(name='twithcBot', target=self.__twitchBot.start).start()
        self.__app.mount('/static', StaticFiles(directory='./static'), name='static')
        self.__templates = Jinja2Templates(directory="./templates")

        # Routes
        self.__app.add_api_route('/', endpoint=self.index)

        # Bot
        self.__app.add_api_route('/bot/status', endpoint=self.status)
        self.__app.add_api_route('/bot/channels', endpoint=self.channels)
        self.__app.add_api_route('/bot/commands', endpoint=self.commands)
        self.__app.add_api_route('/bot/settings', endpoint=self.settings)
        self.__app.add_api_route('/bot/bannedUsers', endpoint=self.bannedUsers)

        self.__origins = [
            'http://localhost',
            'http://localhost:7777',
            'http://192.168.0.11',
            'http://192.168.0.11:7777',
        ]

        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=self.__origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
    # end __init__
        
    def __del__(self):
        if self.__botThread.is_alive():
           self.__twitchBot.stop()
           self.__botThread.join(timeout=3)
           if self.__botThread.is_alive():
                self.__twitchBot.stop()
                self.__botThread.join(timeout=3)
    # end __del__

    def start(self):
        uvicorn.run(self.__app, host="0.0.0.0", port=8888)
    # end start
    
    async def index(self, request: Request):
        return self.__templates.TemplateResponse(request=request, name='index.html', context={'message':'Hello World!'})
    # end index

    # Bot
    async def status(self, request: Request):
        connectedChannels = []
        status = False
        for i in self.__twitchBot.connected_channels:
            connectedChannels.append(i.name)
        if len(connectedChannels) > 0:
            status = True
        return status
    # end status
    
    async def channels(self, request: Request):
        connectedChannels = []
        for i in self.__twitchBot.connected_channels:
            connectedChannels.append(i.name)
        return connectedChannels
    # end channels

    async def commands(self, request: Request):
        listOfCommands = {}
        for key in self.__twitchBot.commands:
            listOfCommands[key] = {'aliases': self.__twitchBot.commands[key].aliases}
        return dumps(listOfCommands)
    # end commands

    async def settings(self, request: Request):
        return dumps(self.__twitchBot.getSettings())
    # end settings

    async def bannedUsers(self, request: Request):
        return ['temporary',]
    # end bannedUsers
# end Interface

if __name__ == "__main__":
    newInterface = Interface()
    newInterface.start()
    # uvicorn.run('interface:app', host="0.0.0.0", port=7777, reload=True)