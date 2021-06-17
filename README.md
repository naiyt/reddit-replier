# NOTE: This repository has not been updated in 7+ years, and is currently *archived*!

It was something I messed around with ages ago, but I haven't looked at it or played with it since. I wouldn't recommend trying to use it.

reddit-replier
==============

[![Build Status](https://travis-ci.org/naiyt/reddit-replier.svg?branch=master)](https://travis-ci.org/naiyt/reddit-replier)

*A simple Python module that simplifies creating Reddit bots that reply to comments based on specified criteria.*

The [Python Reddit API Wrapper](http://praw.readthedocs.org/en/v2.1.16/) (praw) greatly simplifies working with the Reddit API. Writing bots, a common use for praw, is still rather tricky. The purpose of this framework is to take care of the automation parts of writing a Reddit bot, letting you focus on the logic of what it should say and when it should say it.

To accomplish this, you write a `Parser` class that contains a `parse` method. An instance of your class will be used when instatiating a `Replier` object. The `Replier` will watch the subreddits that you specify and pass all the messages to your `parse` method. Your `parse` will determine if a message should be replied to; if so, it will also return the message to be posted. This may sound more difficult than it actually is. Taking a look at the `Examples` section should help.

This is still in beta, and there may be bugs.

Installation
------------

    pip install redditreplier --pre

This is still a "pre-release" package, so you need to make sure you include `--pre` when installing via pip. (Alternatively you could just clone this repo.)

Compatability
------------

Currently tested w/Python 3.2, 3.3 and 3.4. Python 2 support may be added in the future. (Pull requests welcome!)

Replier Parameters
==================
```python
class Replier(parser, user_name, user_pass, subreddits='all', user_agent='redditreplier v0.01 by /u/naiyt', limit=1000, debug=False)
```

Arguments
---------

    parser

The `parser` should be an object that takes no parameters. It must have a `parse` method that takes one argument (message) and returns 2 values. The first value should be `True` or `False` based on whether redditreplier should reply to that comment. The second value should be the text that you want redditreplier to reply with. (Feel free to leave this as an empty string if your first value is `False`)

    user_name

Your bot's Reddit username.

    user_pass

Your bot's Reddit password

    subreddits

The subreddits you want your bot to watch. (For multiple subreddits, use the format `sub1+sub2+sub3`) By default it follows /r/all.

    user_agent

The default user_agent should be okay, but I would prefer if you defined your own.

    limit

The limit of posts to request at once. The Reddit API restricts you to at most 1000 per request. Less should be just fine if you are watching smaller subreddits. praw ensures that you are staying with Reddit API limits, so you don't need to worry about that. (Unless you are running multiple bots on the same machine.)

    debug

Debug mode makes redditreplier print the message to `stdout` rather than post it to Reddit.

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

And there you go! It will start watching your subreddits and replying when needed. You can run it with nohup or a detached screen/tmux session if you want it to be running continuously.

Disclaimer: this is a bad example, and not something that you should create a bot to do. Try to come up with more interesting and useful bots than this.

Running tests
-------------

`python tests.py`


Blacklist
---------

If you have a Reddit user you never want to reply to, add their username to `BLACKLIST.TXT`. The bot being run will automatically be added to the blacklist (so that it won't get stuck in a loop with itself). A bot will never reply to itself or reply to a comment it has already replied to. Sometimes bots can get stuck in loops with other bots, so if you see that happen make sure you add the offending bot to `BLACKLIST.txt`.

TODO
----

* Improve test coverage
* Implement OAuth instead of plain text passwords?
* Better logging and error handling
* Python 2 support
* Support for other types of bots
