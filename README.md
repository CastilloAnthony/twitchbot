# WolfBot
## Developed by Anthony Castillo

A personalized twitch bot made using the twitchio library for twitch specific interactions alongside the mysql library for data storage and manipulation. Includes custom commands, logging, and files for inputting your own authentication information. The bot can also be ran in multiple channels.

### QuickStart:
1. Download and install MySQL server and host it on the same computer that will be running this bot.
    - In the MySQL server configuration you should create a user named "twitchbot" and give them persmissions for creating and managing tables. The password used here will be put into the './keys/password.txt' file.
    - Additionally, you should create a scheme called "twitch", this will be where the bot saves data on users per channel the bot is operating in.
2. Install requirements.txt
3. Launch \_\_main\_\_.py
4. Fill out the newly created files in the keys directory (token.txt, password.txt and, channels.txt):
    - ./keys/token.txt
        - Should contain the access token for the bot. Tokens can be generated at this link: https://twitchtokengenerator.com/
    - ./keys/password.txt
        - Should contain the password for the MySQL database access for the twitchbot username
    - ./keys/channels.txt
        - Should contain the names of channels (one per line) that the bot should be operating in
5. Relaunch \_\_main\_\_.py
6. You should now be able to interact with the bot in chat channels. Try the '!help' command.

### Additional Files:
- ./data/who.txt
    - Can be blank, but should otherwise have the usernames of the people the streamer is streaming with. Can be updated without restarting the bot.