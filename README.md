# SingularChatelet

A discord bot to speak with.

if you want to invite it : [click here](https://discord.com/api/oauth2/authorize?client_id=710407264070139944&permissions=536870912&scope=bot%20applications.commands)
notice that :
- it will be online only 22days/month
- it has only `/brainshopai` and `/aichatbot` slash commands to chat with (because other command use more disk space)
- the branch using for deployment is the `master`

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
-	/settings set_bot name:name avatar_url:avatar_url 
		Create a custom webhook with name and avatar url. The ChatBot will speek with it.
-	/settings remove_bot 
		Remove your custom webhook that exists in the context channel
```
1 search command:
```txt
-   /duckduckgo question:question to browse
        Get an Instant Response from duckduckgo
```
And for the bot owner:
```txt
-   /re_init_transformers_data
        If the data is corumpted by bias, re init the data.
-   /shutdown
        Close the bot
```

## launch

```shell
python3 -m pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
```

```shell
python main.py
```

## folder

-   /cogs                               : where commmands are
-   /data/chatterbot                    : the database for chatterbot
-   /data/transformers                  : the database for transformers
-   /data/documentations-ressources     : .txt file with good ressource to start
-   /data/image                         : the SingularChatelet profile picture

## License
MIT
