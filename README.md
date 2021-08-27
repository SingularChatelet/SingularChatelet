# SingularChatelet - branch for heroku

A discord bot to speak with.

#### this branch is set to deal with the 500MB max storage for free app on heroku

## commands

It has 2 chat commands:
```txt
-   .aichatbot <the sentence here>
        speak using the https://rapidapi.com/farish978/api/ai-chatbot/ api
-   .brainshopai <the sentence here>
        speak using the https://brainshop.ai/ api
```
You can set a custom webhook that respond to you (It need manage webhooks permission)
```txt
-	.set_my_bot <avatar_url> <name of the bot>
		Create a custom webhook with name and avatar url. The ChatBot will speek with it.
-	.remove_my_bot <name of the bot>
		Remove your custom webhook named 'name'
```
clear converssation command:
```txt
-   .clear_message_channel
        Clear your message and bot's message if it respond to you.
```
browse an instant answer:
```txt
-   .duckduckgo <query ..>
        Get an Instant Response from duckduckgo.
```
And for the bot owner:
```txt
-   .shutdown
        Close the bot
```

## launch

```shell
python -m pip install -r requirements.txt
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
