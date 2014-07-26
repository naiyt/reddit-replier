reddit-replier
==============

[![Build Status](https://travis-ci.org/naiyt/reddit-replier.svg?branch=master)](https://travis-ci.org/naiyt/reddit-replier)

A simple Python module that simplifies creating Reddit bots that reply to comments based on criteria you specify.

All you need to do is write a `Parser` class that is passed into the `Replier` class that will parse a Reddit message that returns whether or not you should reply to said message as well as the text to reply with, and redditreplier will take care of the rest. It will communicate with the Reddit API using [praw](http://praw.readthedocs.org/en/v2.1.16/), continually watching whatever subreddits you specific.

This is very much in beta and there are likely bugs.

Installation
------------

    pip install redditreplier --pre

Make sure to include the `--pre` as pip ignores 'pre-release' packages by default. Or just clone the repo.

Compatability
------------

Currently only tested w/Python 3.3 and 3.4. (Hey, I'm trying to finally switch over to Python 3!) Adding Python 3.2 and Python 2 support should be pretty easy if someone wants to give it a try.


Replier Parameters
==================
```python
class Replier(parser, user_name, user_pass, subreddits='all', user_agent='redditreplier v0.01 by /u/naiyt', limit=1000, debug=False)
```

Arguments
---------

    parser

The `parser` should be an object that takes no parameters. It must have a `parse` method that takes one argument (message) and returns 2 values. The first should be `True` or `False` based on whether redditreplier should reply to that comment. The second value should be the text that you want redditreplier to reply with. (Feel free to leave this as an empty string if you are replying `False` for the first value.)

(`parser` used to be just a function, but defining it as a class gives you a lot more flexibility with doing what you want with your parsing.)

    user_name

Your bot's Reddit username.

    user_pass

Your bot's Reddit password

    subreddits

The subreddits you want your bot to watch. (For multiple subreddits, use the format `sub1+sub2+sub3`) Defaults to /r/all.

    user_agent

The default user_agent should be okay, but I would prefer if you defined your own for your own bot.

    limit

The limit of posts to request at once. The Reddit API restricts you to at most 1000 per request. Less should be just fine if you are watching smaller subreddits. praw ensures that you are staying with Reddit API limits, so you don't need to worry about that.

    debug

Prints the message being posted rather than actually posting it.

Examples
========

For a full fledged example, see [AutoGitHubBot](https://github.com/naiyt/autogithub).

Simple example:

Say I want to respond and thank anybody who says 'redditreplier is awesome!' on /r/redditreplier. First, I would write a `parser` class:

```python
class Parser:
    def parse(self, message):
        if 'redditreplier is awesome' in message.body.lower():
            return True, 'Hey thanks! You are pretty cool yourself'
        else:
            return False, ''
```

Then create and run your Replier Bot:

```python
from redditreplier import Replier
bot = Replier(
	Parser(),
	your_reddit_username,
	your_reddit_pass,
	'redditreplier' # The subreddit, leave blank for /r/all
	user_agent='My cool bot by /u/username'
)
bot.start()
```

And there you go! It will start watching your subreddits and replying when needed. Run it with nohup or a detached screen/tmux session if you want it to be running continuously.

Please not that this is a bad example, and not something that you should create a bot to do. Try to come up with more interesting and useful bots than that.

Running tests
-------------

`python tests.py`

Help
----

You can post on [/r/redditreplier](http://reddit.com/r/redditreplier). (Although I'm mainly just using it for bot tests now.)

Blacklist
---------

Add users you never want to reply to to `BLACKLIST.txt`. The bot being run will automatically be added to the blacklist (so that it won't get stuck in a loop with itself). A bot will never reply to itself or reply to a comment it has already replied to. Sometimes bots can get stuck in loops with other bots, so if you see that happen make sure you add it to `BLACKLIST.txt`.

TODO
----

* Improve test coverage
* Implement OAuth instead of plain text passwords?
* Better logging and error handling
* Get on pip
* Port/test with other Python versions