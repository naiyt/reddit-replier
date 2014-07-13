import praw
import os.path

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
        self.blacklist.append(self.user_name)


    def start(self):
        if self.debug:
            comments = self.r.get_subreddit(self.subreddits).get_comments(limit=50)
        else:
            comments = praw.helpers.comment_stream(self.r, self.subreddits, self.limit)
        return self.check_and_post(comments)

    def check_and_post(self, comments):
        for comment in comments:
            if comment.author.name.lower() not in self.blacklist:
                result = self.parser(comment)
                if result:
                    args = [comment]
                    try:
                        args.extend(result)
                    except TypeError:
                        pass
                    reply = self.replier(*args)
                    if reply:
                        if self.debug:
                            return reply
                        else:
                            comment.reply(reply)

    def _setup_blacklist(self):
        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, 'BLACKLIST.txt'))
        blacklist = []
        with open(filepath) as f:
            for user in f:
                blacklist.append(user.lower())
        return blacklist