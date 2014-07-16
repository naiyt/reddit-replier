import praw
import os.path
import traceback
from time import sleep

__version__ = '0.01'

class Replier:
    def __init__(self,
                 parser,
                 replier,
                 user_name,
                 user_pass,
                 subreddits='all',
                 user_agent='redditreplier v{} by /u/naiyt'.format(__version__),
                 limit=1000,
                 debug=False):
        self.parser = parser
        self.replier = replier
        self.user_agent = user_agent
        self.subreddits = subreddits
        self.user_name = user_name
        self.user_pass = user_pass
        self.limit = limit
        self.debug = debug
        self.r = praw.Reddit(self.user_agent)
        self.r.login(self.user_name, self.user_pass)
        self.blacklist = self._setup_blacklist()
        self.rest_time = 3

    def start(self):
        comments = praw.helpers.comment_stream(self.r, self.subreddits, self.limit)
        return self._main_loop(comments)

    def _main_loop(self, comments):
        while True:
            try:
                self._search_comments(comments)
            except Exception as e:
                self._handle_exception(e)
        
    def _search_comments(self, comments):
        for comment in comments:
            result = self.parser(comment)
            if result:
                if self._should_reply(comment):
                    self._make_comment(comment, result)

    def _make_comment(self, comment, result):
        args = self._extract_args(comment, result)
        reply = self.replier(*args)
        if self.debug:
            print(reply)
        else:
            comment.reply(reply)

    def _extract_args(self, comment, result):
        args = [comment]
        try:
            args.extend(result)
        except TypeError:
            pass
        return args

    def _should_reply(self, comment):
        if comment.author.name.lower() in self.blacklist:
            return False
        replies = [x.author.name.lower() for x in comment.replies]
        if self.user_name.lower() in replies:
            return False
        return True

    def _setup_blacklist(self):
        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, 'BLACKLIST.txt'))
        try:
            blacklist = open(filepath).read().splitlines()
        except FileNotFoundError:
            blacklist = []
        blacklist.append(self.user_name.lower())
        return blacklist

    def _handle_exception(self, e):
        traceback.print_exc()
        print('Error: {}'.format(e))
        sleep(self.rest_time)
        self.start()
        exit()
