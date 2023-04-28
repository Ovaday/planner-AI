import os
import unittest
from pathlib import Path

from helpers import MessageHistoryHelpers
from helpers.openAIHelper import *
from helpers.DatabaseHelpers import *
from telegram import Message
from unittest.mock import AsyncMock
from helpers.openAIHelper import chatGPT_req
from helpers.resourcesPacker import listFiles, handleExtension, encrypt, decrypt, get_fernet_key, read_encrypted
from asgiref.sync import sync_to_async
import os
from helpers.tokenHelpers import retrieve_and_cache_secrets, get_token, get_db_conn, get_mongo_db_conn
from helpers.ScheduleHelpers import schedule_my_task, get_my_reminders, async_to_schedule
import asyncio
from unittest.mock import MagicMock, patch
from django.test import TestCase
from django_q.models import Schedule
from service_routine.models import ServiceM
from helpers.SQSHelpers import async_call_receiver, task_receiver


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

class TestChatGPTReq(unittest.IsolatedAsyncioTestCase):
    async def test_chatGPT_req(self):
        message = "Hello, how are you?"
        tg_chat = AsyncMock()
        tg_chat.language = "en"
        tg_chat.role = "user"
        response_mock = AsyncMock()
        response_mock.choices = [AsyncMock(message=AsyncMock(content="Hi there!"))]
        response_mock.usage.total_tokens = 10
        with patch("openai.ChatCompletion.create", return_value=response_mock) as chat_mock:
            result = await chatGPT_req(message, tg_chat, "normal", "test-model")
            chat_mock.assert_called_once_with(
                model="test-model",
                max_tokens=1000,
                messages=[
                    {"role": "system", "content": "Use max limit of 1000 words. Preferred language: en"},
                    {"role": "user", "content": message}
                ]
            )
        self.assertEqual(result, "Hi there!")

root_file_path = Path(__file__).resolve().parent.parent
basedir_extracted = os.path.join(root_file_path, 'resources/extracted/')
basedir_packed = os.path.join(root_file_path, 'resources/')

def test_listFiles():
    # Test for when is_encrypt is True
    assert listFiles(basedir_packed, True) == ['file1.enc', 'file2.enc']

    # Test for when is_encrypt is False
    assert listFiles(basedir_packed, False) == ['file1.txt', 'file2.jpg']

def test_handleExtension():
    # Test for when is_encrypt is True
    assert handleExtension('file1.txt', True) == 'file1.txt.enc'
    assert handleExtension('file1.txt.enc', True) == 'file1.txt.enc'

    # Test for when is_encrypt is False
    assert handleExtension('file1.txt.enc', False) == 'file1.txt'
    assert handleExtension('file1.txt', False) == 'file1.txt'

def test_encrypt_decrypt():
    key = get_fernet_key()

    # Test encryption and decryption for a text file
    filename_origin = basedir_extracted + 'file1.txt'
    filename_destination = basedir_packed + 'file1.txt.enc'
    encrypt(filename_origin, filename_destination, key)
    decrypted_data = read_encrypted('file1.txt', key, is_normal_read=False)
    assert decrypted_data == b'test'

    filename_origin = basedir_packed + 'file1.txt.enc'
    filename_destination = basedir_extracted + 'file1.txt'
    decrypt(filename_origin, filename_destination, key)
    with open(filename_destination, "r") as file:
        assert file.read() == 'test'

    # Test encryption and decryption for a binary file
    filename_origin = basedir_extracted + 'file2.jpg'
    filename_destination = basedir_packed + 'file2.jpg.enc'
    encrypt(filename_origin, filename_destination, key)
    decrypted_data = read_encrypted('file2.jpg', key, is_normal_read=False)
    with open(filename_origin, "rb") as file:
        assert decrypted_data == file.read()

    filename_origin = basedir_packed + 'file2.jpg.enc'
    filename_destination = basedir_extracted + 'file2.jpg'
    decrypt(filename_origin, filename_destination, key)
    with open(filename_destination, "rb") as file:
        assert file.read() == decrypted_data

def test_read_encrypted():
    key = get_fernet_key()

    # Test reading an encrypted text file
    filename = 'file1.txt.enc'
    decrypted_data = read_encrypted(filename, key)
    assert decrypted_data.getvalue() == 'test\n'

    # Test reading an encrypted binary file
    filename = 'file2.jpg.enc'
    decrypted_data = read_encrypted(filename, key, is_normal_read=False)
    with open(basedir_extracted + 'file2.jpg', "rb") as file:
        assert decrypted_data == file.read()


class TestScheduleHelpers(TestCase):

    def setUp(self):
        self.chat_id = 123
        self.future_time = '2023-05-05 18:00:00'
        self.request_data = {'text': 'Test request'}

    def test_schedule_my_task(self):
        scheduled_obj = schedule_my_task(self.future_time)
        self.assertIsInstance(scheduled_obj, Schedule)
        self.assertEqual(scheduled_obj.func, 'tg_routine.main.task_handler')
        self.assertEqual(scheduled_obj.schedule_type, 'O')
        self.assertEqual(scheduled_obj.next_run, self.future_time)
        self.assertEqual(scheduled_obj.repeats, 1)

    @sync_to_async
    def create_service_m_obj(self):
        return ServiceM.objects.create(chat_id=self.chat_id)

    def test_get_my_reminders(self):
        # create mock schedule object with success method
        mock_schedule_obj = MagicMock()
        mock_schedule_obj.success.return_value = False

        # create service_m object with schedule object
        service_m_obj = self.create_service_m_obj()
        service_m_obj.schedule = mock_schedule_obj
        service_m_obj.request = self.request_data
        service_m_obj.save()

        # get reminders and assert that service_m_obj is returned
        result = get_my_reminders(service_m_obj.chat)
        expected_result = {
            service_m_obj.id: {
                'request': self.request_data,
                'schedule': mock_schedule_obj
            }
        }
        self.assertEqual(result, expected_result)

    def test_async_to_schedule(self):
        chat = MagicMock()
        chat.id = self.chat_id

        scheduled_obj = MagicMock()

        with self.assertLogs() as cm:
            async_to_schedule(chat, self.future_time, self.request_data)

        service_m_obj = ServiceM.objects.get(chat_id=self.chat_id)
        self.assertEqual(service_m_obj.chat, chat)
        self.assertEqual(service_m_obj.request, self.request_data)
        self.assertEqual(service_m_obj.schedule, scheduled_obj)
        self.assertRegex(str(cm.output), 'Try to exec!.*Woke up after execution!')


class TestSQSHelpers(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем фиктивный объект Schedule и ServiceM для тестов
        cls.schedule_obj = Schedule.objects.create(func='tg_routine.main.task_handler',
                                                   schedule_type='O',
                                                   next_run=asyncio.get_event_loop().time() + 5,
                                                   repeats=1)
        cls.chat_id = 1234
        cls.service_m_obj = ServiceM.objects.create(chat_id=cls.chat_id, schedule=cls.schedule_obj, request='test request')

    @patch('tg_routine.main.task_handler')
    def test_task_receiver(self, mock_task_handler):
        update_json = {'test': 'update_json'}
        task_receiver(update_json)
        mock_task_handler.assert_called_once_with(update_json)

    @patch('helpers.openAIHelper.chatGPT_req_test')
    def test_async_call_receiver(self, mock_chatGPT_req_test):
        message = 'test message'
        mock_chatGPT_req_test.return_value = 'test response'
        result = async_call_receiver(message)
        mock_chatGPT_req_test.assert_called_once_with(message, None, None, None, None)
        self.assertEqual(result, 'test response')

class TestTokenHelpers:
    def test_retrieve_and_cache_secrets(self):
        with patch.dict(os.environ, {
            'IAM_ACCESS_KEY': 'access_key',
            'IAM_SECRET_KEY': 'secret_key',
            'IAM_AWS_REGION': 'us-west-2'
        }):
            cache = retrieve_and_cache_secrets()
            assert cache.get_secret_string('my_secret') == 'my_secret_value'

    def test_get_token_with_env_variable(self):
        with patch.dict(os.environ, {'MY_TOKEN': 'my_token_value'}):
            assert get_token('MY_TOKEN') == 'my_token_value'

    def test_get_token_with_vercel(self):
        with patch.dict(os.environ, {'VERCEL': 'true'}), \
             patch('tokenHelpers.settings', spec_set=['SECRETS']) as mock_settings, \
             patch('tokenHelpers.json.loads', return_value={'MY_TOKEN': 'my_token_value'}):
            mock_settings.SECRETS.get_secret_string.return_value = '{"MY_TOKEN": "my_token_value"}'
            assert get_token('MY_TOKEN') == 'my_token_value'

    def test_get_token_with_iam(self):
        with patch('tokenHelpers.config', return_value='my_iam_token_value'):
            assert get_token('IAM_TOKEN') == 'my_iam_token_value'

    def test_get_token_with_secrets_path(self):
        with patch('tokenHelpers.config', return_value='secrets_path'), \
             patch('tokenHelpers.settings', spec_set=['SECRETS']), \
             patch('tokenHelpers.json.loads', return_value={'MY_TOKEN': 'my_token_value'}):
            mock_secrets = type('Secrets', (), {'get_secret_string': lambda self, path: '{"MY_TOKEN": "my_token_value"}'})
            mock_settings = type('Settings', (), {'SECRETS': mock_secrets})
            assert get_token('MY_TOKEN') == 'my_token_value'

    def test_get_db_conn(self):
        with patch.dict(os.environ, {
            'DB_NAME': 'my_db_name',
            'DB_USER': 'my_db_user',
            'DB_PASSWORD': 'my_db_password',
            'DB_HOST': 'my_db_host'
        }):
            expected_conn = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'my_db_name',
                'USER': 'my_db_user',
                'PASSWORD': 'my_db_password',
                'HOST': 'my_db_host',
                'PORT': '5432',
            }
            assert get_db_conn() == expected_conn

    def test_get_mongo_db_conn(self):
        with patch.dict(os.environ, {
            'MONGO_DB_USER': 'my_mongo_user',
            'MONGO_DB_PASSWORD': 'my_mongo_password',
            'MONGO_DB_ENVIROMENT': 'my_mongo_host'
        }):
            expected_conn = {
                'USER': 'my_mongo_user',
                'PASSWORD': 'my_mongo_password',
                'HOST': 'my_mongo_host',
            }
            assert get_mongo_db_conn() == expected_conn

