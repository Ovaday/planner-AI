import unittest

from helpers import MessageHistoryHelpers
from helpers.openAIHelper import *
from helpers.DatabaseHelpers import *
from django.test import TestCase
from telegram import Message

# ToDO: add new tests
class ParseResponseCase(TestCase):
    input_text = "Here is your output: {'is_reminder': True, 'is_event': False}"
    output_parsable_expected = "Here is your output: {'is_reminder': true, 'is_event': false}"
    output_parsed_json = {"is_reminder": True, "is_event": False}

    def test_bool_replaced(self):
        self.assertEqual(replace_bools(self.input_text), self.output_parsable_expected)

    def test_parse_json(self):
        self.assertEqual(parse_json(self.input_text), self.output_parsed_json)

class DatabaseHelpersTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.DB_NAME = 'test_db'
        cls.db_handle, cls.client = get_db_handle(db_name=cls.DB_NAME)
        cls.collection_name = 'test_collection'
        cls.collection_handle = get_collection_handle(cls.db_handle, cls.collection_name)
        cls.chat_id = '12345'
        cls.language = 'en'
        cls.chat_data = {
            "chat_id": cls.chat_id,
            "counter": 0,
            "language": cls.language,
            "is_approved": False
        }
        cls.chat = Chat.objects.create(
            chat_id=cls.chat_data['chat_id'],
            counter=cls.chat_data['counter'],
            language=cls.chat_data['language'],
            is_approved=cls.chat_data['is_approved']
        )

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database(cls.DB_NAME)
        cls.client.close()

    def test_get_db_handle(self):
        db_handle, client = get_db_handle(db_name=self.DB_NAME)
        self.assertIsNotNone(db_handle)
        self.assertIsNotNone(client)
        self.assertIsInstance(db_handle, MongoClient)
        self.assertIsInstance(client, MongoClient)
        self.assertEqual(db_handle.name, self.DB_NAME)

    def test_get_collection_handle(self):
        collection_handle = get_collection_handle(self.db_handle, self.collection_name)
        self.assertIsNotNone(collection_handle)
        self.assertIsInstance(collection_handle, MongoClient)

    def test_get_chat(self):
        chat = get_chat(self.chat_id)
        self.assertIsNotNone(chat)
        self.assertIsInstance(chat, Chat)
        self.assertEqual(chat.chat_id, self.chat_id)

    def test_get_creator(self):
        creator = get_creator()
        self.assertIsNotNone(creator)
        self.assertIsInstance(creator, Chat)
        self.assertEqual(creator.pk, 1)

    def test_set_language(self):
        language = 'fr'
        set_language(self.chat_id, language)
        chat = get_chat(self.chat_id)
        self.assertEqual(chat.language, language)

    def test_set_approved(self):
        set_approved(self.chat_id, True)
        chat = get_chat(self.chat_id)
        self.assertTrue(chat.is_approved)

    def test_tick_counter(self):
        chat = get_chat(self.chat_id)
        prev_counter = chat.counter
        tick_counter(self.chat_id)
        chat = get_chat(self.chat_id)
        self.assertEqual(chat.counter, prev_counter + 1)

    def test_tick_tokens(self):
        chat = get_chat(self.chat_id)
        prev_tokens = chat.tokens_used
        tokens = 5
        tick_tokens(self.chat_id, tokens)
        chat = get_chat(self.chat_id)
        self.assertEqual(chat.tokens_used, prev_tokens + tokens)

    def test_assign_last_conversation(self):
        conversation = 'test_conversation'
        assign_last_conversation(self.chat_id, conversation)
        chat = get_chat(self.chat_id)
        self.assertEqual(chat.last_conversation, conversation)

    def test_assign_last_conversation(self):
        conversation = 'test_conversation'
        assign_last_conversation(self.chat_id, conversation)
        chat = get_chat(self.chat_id)
        self.assertEqual(chat.last_conversation, conversation)

    def test_return_records_list(self):
        records_list = return_records_list([1, 2, 3, 4, 5])
        self.assertIsNotNone(records_list)
        self.assertIsInstance(records_list, list)
        self.assertEqual(records_list, [1, 2, 3, 4, 5])

    def test_return_single_record(self):
        record = return_single_record(123)
        self.assertIsNotNone(record)
        self.assertIsInstance(record, int)
        self.assertEqual(record, 123)

    @sync_to_async
    async def test_async_get_chat(self):
        chat = await async_get_chat(self.chat_id)
        self.assertIsNotNone(chat)
        self.assertIsInstance(chat, Chat)
        self.assertEqual(chat.chat_id, self.chat_id)

    @sync_to_async
    async def test_async_get_creator(self):
        creator = await async_get_creator()
        self.assertIsNotNone(creator)
        self.assertIsInstance(creator, Chat)
        self.assertEqual(creator.pk, 1)

    @sync_to_async
    async def test_async_set_language(self):
        language = 'fr'
        await async_set_language(self.chat_id, language)
        chat = await async_get_chat(self.chat_id)
        self.assertEqual(chat.language, language)

    @sync_to_async
    async def test_async_set_approved(self):
        await async_set_approved(self.chat_id, True)
        chat = await async_get_chat(self.chat_id)
        self.assertTrue(chat.is_approved)

    @sync_to_async
    async def test_async_tick_counter(self):
        chat = await async_get_chat(self.chat_id)
        prev_counter = chat.counter
        await async_tick_counter(self.chat_id)
        chat = await async_get_chat(self.chat_id)
        self.assertEqual(chat.counter, prev_counter + 1)

    @sync_to_async
    async def test_async_tick_tokens(self):
        chat = await async_get_chat(self.chat_id)
        prev_tokens = chat.tokens_used
        tokens = 5
        await async_tick_tokens(self.chat_id, tokens)
        chat = await async_get_chat(self.chat_id)
        self.assertEqual(chat.tokens_used, prev_tokens + tokens)

    @sync_to_async
    async def test_async_assign_last_conversation(self):
        conversation = 'test_conversation'
        await async_assign_last_conversation(self.chat_id, conversation)
        chat = await async_get_chat(self.chat_id)
        self.assertEqual(chat.last_conversation, conversation)


class TestMessageHistoryHelpers(unittest.TestCase):
    def setUp(self):
        # Инициализация объекта MessageHistoryHelpers
        self.message_history_helpers = MessageHistoryHelpers()

    def tearDown(self):
        # Удаление временных данных после тестирования
        # (например, удаление записей из базы данных)
        pass

    def test_insert_input_message(self):
        # Тест метода insert_input_message
        # Создание тестового сообщения
        in_msg = Message(chat_id=1, date=1234567890, message_id=1, chat=None, text='Test message')
        # Вызов метода insert_input_message
        result = self.message_history_helpers.insert_input_message(in_msg)
        # Проверка наличия результата
        self.assertIsNotNone(result)

    def test_insert_response(self):
        # Тест метода insert_response
        # Создание тестового сообщения
        in_msg = Message(chat_id=1, date=1234567890, message_id=1, chat=None, text='Test message')
        response_text = 'Test response'
        tokens_used = 5
        # Вызов метода insert_response
        result = self.message_history_helpers.insert_response(in_msg, response_text, tokens_used)
        # Проверка наличия результата
        self.assertIsNotNone(result)

    def test_get_messages_for_user(self):
        # Тест метода get_messages_for_user
        user_id = 1
        # Вызов метода get_messages_for_user
        result = self.message_history_helpers.get_messages_for_user(user_id)
        # Проверка типа результата
        self.assertIsInstance(result, list)

    def test_get_last_user_messages(self):
        # Тест метода get_last_user_messages
        user_id = 1
        # Вызов метода get_last_user_messages
        result = self.message_history_helpers.get_last_user_messages(user_id)
        # Проверка типа результата
        self.assertIsInstance(result, list)
