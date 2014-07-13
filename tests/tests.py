import unittest
import secrets as s

TEST_THREAD = 'http://www.reddit.com/r/redditreplier/comments/2akb3w/autogithubbot_test_thread/'

class TestReplier(unittest.TestCase):

    def setUp(self):
        self.user_agent = 'redditreplier bot by /u/naiyt'
        self.replier = Replier(test_parser, test_replier, s.user, s.password, 'redditreplier', debug=True)

    def test_that_parser_returns_true_correctly(self):
        reply = self.replier.start()
        self.assertEqual('Replying to message ciw02wx by naiyt', reply)

    def test_that_parser_returns_false_correctly(self):
        replier_2 = Replier(test_parser_2, test_replier, s.user, s.password, 'redditreplier', debug=True)
        reply = replier_2.start()
        self.assertEqual(reply, None)

    def test_that_bot_does_not_reply_to_self(self):
        replier_3 = Replier(test_parser_3, test_replier, s.user, s.password, 'redditreplier', debug=True)
        reply = replier_3.start()
        self.assertEqual(reply, None)


def test_parser(message):
    if 'Hello Robot, you should reply to this comment' in message.body:
        return True
    else:
        return False

def test_parser_2(message):
    if 'No comment like this, do not reply 1234234324324324' in message.body:
        return True
    else:
        return False

def test_parser_3(message):
    if "Hello Robot, you should reply to this comment (but don't really, because you shouldn't reply to yourself)" in message.body:
        return True
    else:
        return False

def test_replier(message):
    return "Replying to message {} by {}".format(message.id, message.author)

if __name__ == "__main__" and __package__ is None:
    import sys, os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    from redditreplier import Replier
    __package__ = str("redditreplier")
    del sys, os
    unittest.main()
