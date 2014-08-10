import praw
import logging
import os.path
import traceback
from time import sleep

__version__ = '1.0.0a1'

class Replier:
    def __init__(self,
                 parser,
                 user_name,
                 user_pass,
                 subreddits='all',
                 user_agent='redditreplier v{} by /u/naiyt'.format(__version__),
                 limit=1000,
                 debug=False):
        print("Setting things up...")
        self.parser = parser
        self.user_agent = user_agent
        self.subreddits = subreddits
        self.user_name = user_name
        self.user_pass = user_pass
        self.limit = limit
        self.debug = debug
        self.r = praw.Reddit(self.user_agent)
        self.blacklist = self._setup_blacklist('BLACKLIST.txt')
        self.rest_time = 3
        self.comments_replied_to = 0

    def start(self):
        print("Logging into Reddit...")
        self._login()
        print("Starting the comments stream...")
        comments = praw.helpers.comment_stream(self.r, self.subreddits, self.limit)
        return self._main_loop(comments)

    def _login(self):
        self.r.login(self.user_name, self.user_pass)

    def _main_loop(self, comments):
        while True:
            try:
                self._search_comments(comments)
            except Exception as e:
                self._handle_exception(e)
        
    def _search_comments(self, comments):
        for comment in comments:
            should_reply, text = self.parser.parse(comment)
            if should_reply and text:
                if self._should_reply(comment):
                    self._make_comment(comment, text)
                    self.comments_replied_to += 1

    def _make_comment(self, comment, text):
        if self.debug:
            print(text)
        else:
            comment.reply(text)
        print("Replied to {}'s comment at {}".format(comment.author.name, comment.permalink))

    def _should_reply(self, comment):
        if comment.author.name.lower() in self.blacklist:
            return False
        replies = [x.author.name.lower() for x in comment.replies]
        if self.user_name.lower() in replies:
            return False
        return True

    def _setup_blacklist(self, f):
        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, f))
        try:
            f = open(filepath)
            blacklist = [x.lower() for x in f.read().splitlines()]
            f.close()
        except (OSError, IOError) as e:
            blacklist = []
        blacklist.append(self.user_name.lower())
        return blacklist

    def _handle_exception(self, e):
        traceback.print_exc()
        logging.warning("Something bad happened! I'm going to try to keep going, though. Error: {}".format(e))
        sleep(self.rest_time)
        self.start()
        exit()
