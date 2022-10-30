# SingularChatelet

A discord bot to speak with.

You cant host it if u want

if you want to invite it : [click here](https://discord.com/oauth2/authorize?client_id=710407264070139944&permissions=415001528384&scope=bot%20applications.commands)
notice that :
- it will run only when i run it

## commands

It has 4 chat slash commands:
```txt
-   /pytorch message:the message here
        speak with the transformers/pytorch part
-   /chatterbot message:the message here
        speak with the ChatterBot part
-   /brainshopai message:the message here
        speak with the brainshopai api
-   /aichatbot message:the message here
        speak with the aichatbot api
```
You can set a custom bot that respond to you (It need manage webhooks permission)
```txt
-    /bot create_custom name:name avatar_url:avatar_url 
        Create a custom webhook with name and avatar url. The ChatBot will speek with it.
-    /bot remove_custom 
        Remove your custom webhook that exists in the context channel
```
1 search command:
```txt
-   /ddg question:question to browse
        Get an Instant Response from duckduckgo
```
And for the bot owner:
```txt
-   /developpers re_init_transformers_data
        If the data is corumpted by bias, re init the data.
-   /developpers shutdown
        Close the bot
```

## launch

1.  install dependencies
```shell
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements_full.txt
python3 -m spacy download en_core_web_sm
```
or 
```shell
./install.sh
```

2.  start
```shell
python3 main.py
```

## folder

-   /plugins                            : where commmands are
-   /data/chatterbot                    : the database for chatterbot
-   /data/transformers                  : the database for transformers
-   /data/documentations-ressources     : .txt file with good ressource to start
-   /data/image                         : the SingularChatelet profile picture

## License
MIT
