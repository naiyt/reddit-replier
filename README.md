reddit-replier
==============

[![Build Status](https://travis-ci.org/naiyt/reddit-replier.svg?branch=master)](https://travis-ci.org/naiyt/reddit-replier)

A simple Python module that simplifies creating Reddit bots that reply to comments based on specific criteria. 

The `Replier` class takes a `parser` function and a `replier` function. The `parser` function is passed a `praw` formatted Reddit message and should return `True` or `False`.

If your `parser` function returns `True` for that message, then your `Replier` object will reply to the specified message using your `replier` function, which should just return a string. (Your `replier` gets a copy of the message, so you can use it to format your response.)

This is very much in beta and there are likely bugs.

Replier Parameters
==================
    class Replier(parser, replier, user_name, user_pass, subreddits='all', user_agent='redditreplier v0.01 by /u/naiyt', limit=1000, debug=False)

Arguments
---------

    parser

The `parser` should be a function that takes one argument (message) and returns `True` or `False`.

    replier

The `replier` should be a function that takes one argument (message) and returns a string that will be posted in reply to the message.

    user_name

Your bot's Reddit username.

    user_pass

Your bot's Reddit password

    subreddits

The subreddits you want your bot to watch. (For multiple subreddits, use the format `sub1+sub2+sub3`) Defaults to /r/all.

    user_agent

The default user_agent should be okay, but I would prefer if you defined your own for your own bot.

    limit

The limit of posts to request at once. The Reddit API restricts you to at most 1000 per request. Less should be just fine if you are watching smaller subreddits.

    debug

Mainly used for tests.

Examples
========

Say I want to respond and thank anybody who says 'redditreplier is awesome!' on /r/redditreplier. First, I would write a `parser` method:

    def parser(message):
        if 'redditreplier is awesome' in message.body.lower():
            return True
        else:
            return False

Then, create a replier with the message you want to send:

    def replier(message):
        return 'Hey, thanks {}! You are pretty swell yourself.'.format(message.author.name)

Then create and run your Replier Bot:

    from redditreplier import Replier
    bot = Replier(
		parser,
		replier,
		your_reddit_username,
		your_reddit_pass,
		'redditreplier' # The subreddit, leave blank for /r/all
		user_agent='My cool bot by /u/username'
    )
    bot.start()

And there you go! It will start watching your subreddits and replying when needed.


Running tests
-------------

Just run `python tests/tests.py`. You need to create a file called `secrets.py` in `/tests` with your bot's `user` and `password` defined as variables.

Installation
------------

Just clone the repo for now. Will get it on pip soon.

Help
----

You can post on [/r/redditreplier](http://reddit.com/r/redditreplier). (Although I'm mainly just using it for bot tests now.)

Blacklist
---------

Add users you never want to reply to to `BLACKLIST.txt`. The bot being run will automatically be added to the blacklist (so that it won't get stuck in a loop with itself).

TODO
----

* Improve test coverage
* Implement OAuth instead of plain text passwords?
* Logging
* Error handling