from django.test import TestCase
from tg_bot.models import Chat


class ChatTestCase(TestCase):
    def setUp(self):
        Chat.objects.create(chat_id="chat1", counter=0, tokens_used=0, is_approved=False,
                            role='none', language='english', last_conversation='', username='',
                            current_mode='chatGPT')

        Chat.objects.create(chat_id="chat2", counter=0, tokens_used=0, is_approved=False,
                            role='none', language='english', last_conversation='', username='',
                            current_mode='chatGPT')

    def test_money_used(self):
        """Test money_used() method of Chat model"""
        chat1 = Chat.objects.get(chat_id="chat1")
        chat2 = Chat.objects.get(chat_id="chat2")
        self.assertEqual(chat1.money_used(), '$ 0.0')  # Ожидаемое значение при counter=0, tokens_used=0
        self.assertEqual(chat2.money_used(), '$ 0.0')  # Ожидаемое значение при counter=0, tokens_used=0

        # Изменяем значения полей и проверяем результат
        chat1.counter = 10
        chat1.tokens_used = 100
        chat1.save()
        chat2.counter = 20
        chat2.tokens_used = 200
        chat2.save()

        self.assertEqual(chat1.money_used(), '$ 0.002')  # Ожидаемое значение при counter=10, tokens_used=100
        self.assertEqual(chat2.money_used(), '$ 0.004')
