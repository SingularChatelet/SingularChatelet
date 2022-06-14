# SingularChatelet - branch for heroku

A discord bot to speak with.

#### this branch is set to deal with the 500MB max storage for free app on heroku

-> so the bot dont use transformers and chatterbot lib

->if you want to invit him : https://discord.com/api/oauth2/authorize?client_id=710407264070139944&permissions=536870912&scope=bot%20applications.commands

## slash commands

2 chat slash commands:
```txt
-   /aichatbot message:message here
        speak using the https://rapidapi.com/farish978/api/ai-chatbot/ api
-   /brainshopai message:the message here 
        speak using the https://brainshop.ai/ api
```
You can set a custom webhook that respond to you (It need manage webhooks permission)
```txt
-	/settings set_bot name:name for the pseudo to use avatar_url:avater for the webhook 
		Create a custom webhook with name and avatar url. The ChatBot will speek with it.
-	/settings remove_bot
		Remove your custom webhook that existed in the context channel
```
browse an instant answer:
```txt
-   /duckcuckgo question:anything you want to browse 
        Get an Instant Response from duckduckgo.
```
And for the bot owner:
```txt
-   /developper shutdown 
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
-   /data/documentations-ressources     : .txt file with good ressource to start
-   /data/image                         : the SingularChatelet profile picture

## License
MIT
