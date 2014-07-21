import unittest
from unittest import mock
from redditreplier import Replier
import praw

TEST_USER = 'test_user'
TEST_PASS = 'test_pass'
TEST_USER_AGENT = 'My Reddit Replier Test'
TEST_SUB = 'programming'
TEST_LIMIT = 100

def test_parser(comment):
    if 'Reply to me' in comment.body:
        return True, 'Praise the Sun!'
    else:
        return False, None


class AuthorMock:
    def __init__(self, name):
        self.name = name


class CommentMock:
    def __init__(self, author_name, replies=[], body='Reply to me', permalink='http://reddit.com/coolcomment'):
        self.author = AuthorMock(author_name)
        self.replies = [CommentMock(x, []) for x in replies]
        self.body = body
        self.permalink = permalink

    def reply(self, message):
        return message


class TestInit(unittest.TestCase):
    def setUp(self):
        self.replier = Replier(test_parser,
                               TEST_USER, TEST_PASS,
                               TEST_SUB, TEST_USER_AGENT,
                               TEST_LIMIT)

    def test_init(self):
        self.assertEqual(self.replier.parser, test_parser)
        self.assertEqual(self.replier.user_name, TEST_USER)
        self.assertEqual(self.replier.user_pass, TEST_PASS)
        self.assertEqual(self.replier.subreddits, TEST_SUB)
        self.assertEqual(self.replier.limit, TEST_LIMIT)


class TestStart(unittest.TestCase):
    def setUp(self):
        self.replier = Replier(test_parser,
                               TEST_USER, TEST_PASS,
                               TEST_SUB, TEST_USER_AGENT,
                               TEST_LIMIT)

    @mock.patch.object(Replier, '_login')
    @mock.patch.object(praw.helpers, 'comment_stream')
    @mock.patch.object(Replier, '_main_loop')
    def test_start(self, mock_loop, mock_stream, mock_login):
        self.replier.start()
        mock_loop.assert_called_with(mock_stream.return_value)
        mock_stream.assert_called_with(self.replier.r, self.replier.subreddits, self.replier.limit)
        mock_login.assert_called_with()



class TestMainLoop(unittest.TestCase):
    '''How does one test an infinite loop?'''
    def setUp(self):
        pass


class TestSearchComments(unittest.TestCase):
    def setUp(self):
        self.replier = Replier(test_parser,
                       TEST_USER, TEST_PASS,
                       TEST_SUB, TEST_USER_AGENT,
                       TEST_LIMIT)
        self.comments = [
            CommentMock('Laurentius'),
            CommentMock('Tarkus', [], "TAAAAARRRRKUUUUSSS!!"),
            CommentMock('Logan', [], 'Big Hats are Best Hats'),
            CommentMock('Giant Dad', [], 'Git Gud'),
            CommentMock('Sif'),
            CommentMock(TEST_USER)
        ]

    def test_searching(self):
        '''
        Basic test for comments being replied to. Keep in mind
        that it's your responsibility to test your own replier
        '''
        self.replier._search_comments(self.comments)
        self.assertEqual(self.replier.comments_replied_to, 2)


class TestMakeComment(unittest.TestCase):
    def setUp(self):
        self.replier = Replier(test_parser,
                       TEST_USER, TEST_PASS,
                       TEST_SUB, TEST_USER_AGENT,
                       TEST_LIMIT)
        self.comment = CommentMock('Ornstein', [], 'Pikachu')

    @mock.patch.object(CommentMock, 'reply')
    def test_non_debug_reply(self, reply_mock):
        self.replier._make_comment(self.comment, 'Pikachu')
        reply_mock.assert_called_with('Pikachu')

    @mock.patch.object(CommentMock, 'reply')
    def test_debug_reply(self, reply_mock):
        self.replier.debug = True
        self.replier._make_comment(self.comment, 'Pikachu')
        self.assertFalse(reply_mock.called)

class TestShouldReply(unittest.TestCase):
    def setUp(self):
        self.replier = Replier(test_parser,
                       TEST_USER, TEST_PASS,
                       TEST_SUB, TEST_USER_AGENT,
                       TEST_LIMIT)
        self.bots_comment = CommentMock(TEST_USER, [])
        self.other_comment = CommentMock('Siegmeyer', ['Gwyn, Gwyndolin, Gwynevere'])
        self.blacklist_comment = CommentMock('test_user', [])
        self.already_replied = CommentMock('Solaire', [TEST_USER, 'Crestfallen', 'Andre'])

    def test_should_not_reply_to_self(self):
        self.replier._should_reply(self.bots_comment)
        self.assertFalse(self.replier._should_reply(self.bots_comment))

    def test_should_not_reply_to_blacklist(self):
        self.assertFalse(self.replier._should_reply(self.blacklist_comment))

    def test_should_not_reply_to_same_comment_twice(self):
        self.assertFalse(self.replier._should_reply(self.already_replied))

    def test_should_reply_to_others(self):
        self.assertTrue(self.replier._should_reply(self.other_comment))


class TestSetupBlacklist(unittest.TestCase):
    def setUp(self):
        self.replier = Replier(test_parser,
                               TEST_USER, TEST_PASS,
                               TEST_SUB, TEST_USER_AGENT,
                               TEST_LIMIT)

    def test_blacklist_contains_current_user(self):
        self.assertIn(TEST_USER.lower(), self.replier._setup_blacklist('BLACKLIST.txt'))

    def test_blacklist_only_contains_user_if_no_file(self):
        self.assertEqual([TEST_USER.lower()], self.replier._setup_blacklist('blah'))


class TestHandleException(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == "__main__" and __package__ is None:
    unittest.main()