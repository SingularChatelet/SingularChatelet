# SingularChatelet

A discord bot to speak with.

## commands

It has 2 chat commands :
```shell
-   .pt <the sentence here>
        speak with the transformers/pytorch part
-   .cb <the sentence here>
        speak with the ChatterBot part
```
And 1 clear :
```shell
-   .clear_my_history
        Clear message history of the user for .pt.
```
And for the bot owner :
```shell
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

-   /cogs : where commmands are
-   /data/chatterbot  : the database for chatterbot
-   /data/transformers    : the database for transformers
-   /data/documentations-ressources   : .txt file with good ressource to start
-   /lib/ChatterBot   : (the github repo contain some error) the chatterbot lib
-   /lib/chatterbot-corpus/   : the chatterbot-corpus module to enhance chatterbot

## License
MIT