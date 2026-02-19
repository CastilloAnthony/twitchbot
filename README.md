# ComradeWolf_Bot
## Developed by Anthony Castillo

A personalized twitch bot made using the twitchio 3.2.1 library for twitch specific interactions alongside the asqlite 2.0.0 library for data storage and manipulation. Includes custom commands, logging, and files for inputting your own authentication information.

### QuickStart:
1. Install requirements.txt using pipreqs (pip install -r requirements.txt)
2. Launch \_\_main\_\_.py
3. Fill out the newly created client_settings.json
    - bot_id and owner_id can be left blank, the program will fetch those automatically; everything else must be filled out.
4. Relaunch \_\_main\_\_.py
5. You should now be able to interact with the bot in chat channels. Try the '!help' command.

## Todo:
- Add user interface to help monitor and manage the bot accessible via http://localhost:portnumber 
- Add an api for the bot