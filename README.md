# SingularChatelet

A discord bot to speak with.

## commands

It has 2 chat commands:
```txt
-   .pt <the sentence here>
        speak with the transformers/pytorch part
-   .cb <the sentence here>
        speak with the ChatterBot part
```
2 clear commands:
```txt
-   .clear_my_history
        Clear message history of the user for .pt.
-   .clear_message_channel
        Clear your message and bot's message if it respond to you.
```
1 search command:
```txt
-   .ddg <query ..>
        Get an Instant Response from duckduckgo
```
And for the bot owner:
```txt
-   .delete_conversations
        Delete all current conversations history. Mainly for ressource usage
-   .re_init_transformers_data
        If the data is corumpted by bias, re init the data.
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
-   /data/chatterbot                    : the database for chatterbot
-   /data/transformers                  : the database for transformers
-   /data/documentations-ressources     : .txt file with good ressource to start
-   /data/image                         : the SingularChatelet profile picture
## License
MIT