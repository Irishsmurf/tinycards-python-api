import unittest

from tinycards.model import User, Favorite, Side, Concept, Card, Deck, Fact
from tinycards.networking import json_converter


class JsonConverterTest(unittest.TestCase):

    _TEST_USER_ID = 'UserID'
    _TEST_FACT = Fact(text='Fact: This is a test.')
    _TEST_CONCEPT = Concept(_TEST_FACT, _TEST_USER_ID)
    _TEST_SIDE = Side(_TEST_USER_ID, concepts=[_TEST_CONCEPT])
    _TEST_CARD = Card(_TEST_SIDE, _TEST_SIDE)
    _TEST_DECK = Deck('Deckx', deck_id='DeckID', cards=[_TEST_CARD])
    _TEST_FAVORITE = Favorite('Favorite', _TEST_DECK)

    def setUp(self):
        super(JsonConverterTest, self).setUp()

    def tearDown(self):
        super(JsonConverterTest, self).tearDown()

    def test_json_dict_to_user(self):
        json_input = {
            'creationDate': 1547906391,
            'email': 'test@example.com',
            'fullname': 'Test McTesterson',
            'id': 1000,
            'learningLanguage': 'fr',
            'picture': 'www.example.com/avatar.jpg',
            'subscribed': False,
            'subscriberCount': 42,
            'subscriptionCount': 84,
            'uiLanguage': 'en',
            'username': 'example_user'
        }
        user_obj = json_converter.json_to_user(json_input)
        self.assertTrue(isinstance(user_obj, User))
        self.assertEqual(user_obj.ui_language, 'en')

    def test_json_to_trendable_error(self):
        json_value_error_input = {
            'test': 0
        }
        json_key_error_input = {
            'data': {
                'blacklistedQuestionTypes': 'blah'
            }
        }

        with self.assertRaisesRegex(ValueError, r'.+ontains no \'data\' field'):
            json_converter.json_to_trendable(json_value_error_input)
        with self.assertRaises(KeyError):
            json_converter.json_to_trendable(json_key_error_input)

    def test_json_to_searchable_error(self):
        json_value_error_input = {
            'test': 0
        }
        json_key_error_input = {
            'data': {
                'id': 123
            }
        }

        with self.assertRaisesRegex(ValueError, r'.+ontains no \'data\' field'):
            json_converter.json_to_searchable(json_value_error_input)
        with self.assertRaises(KeyError):
            json_converter.json_to_searchable(json_key_error_input)

    def test_json_to_favorite(self):
        fav_json = json_converter.favorite_to_json(self._TEST_FAVORITE)
        self.assertEqual(
            str(json_converter.json_to_favorite(fav_json)),
            str(self._TEST_FAVORITE))


if __name__ == '__main__':
    unittest.main()
