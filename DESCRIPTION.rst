redditreplier
=============

A simple Python module that simplifies creating Reddit bots that reply to comments based on criteria you specify.

All you need to do is write a parser method that is passed into the Replier class that will parse a Reddit message that returns whether or not you should reply to said message as well as the text to reply with, and redditreplier will take care of the rest. It will communicate with the Reddit API using praw, continually watching whatever subreddits you specific.

Please checkout the GitHub repository for more info. (https://github.com/naiyt/reddit-replier)