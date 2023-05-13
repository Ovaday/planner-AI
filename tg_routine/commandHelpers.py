from helpers.translationsHelper import get_label
from tg_bot.models import Chat


def user_balance_helper(chat=None, chat_id=None):
    # ToDO #115: Add code to retrieve user's balance.
    # ToDo: If both chat and user's id are none, raise error

    if not chat:
        chat = Chat.objects.filter(chat_id=chat_id)

    # Use 'chat' object to get values from its properties. /tg_bot/models.py/Chat

    # Consider that right now we don't have a balance, but only user's expenses, so you have to display a balance as a
    # negative value.
    init_balance = 0
    expenses = 10.1  # ToDo: Change.
    amount = init_balance - expenses  # ToDo: Fix to display only 2 digits after the comma.

    response = f'Your balance is: $ {amount}'
    # ToDo: use labels, add english and russian translations with appropriate label to /helpers/translationHelper.py. Use get_label("text")

    return response, amount


def all_users_balance_helper():
    # ToDO #115: Add code to retrieve all users balance.

    chat_list = Chat.objects.all()

    # What you'll need to do:
    # ToDo: Iterate over users, sum all their expenses into all_expenses and display as a negative value.
    init_balance = 0
    all_expenses = 10.1  # ToDo: Change.
    amount = init_balance - all_expenses  # ToDo: Fix to display only 2 digits after the comma.

    response = f'Balance of all users is: $ {amount}'
    # ToDo: use labels, add english and russian translations with appropriate label to /helpers/translationHelper.py. Use get_label("text")

    return response


def list_users_helper():
    # ToDO #116: Retrieve all users - their usernames, status and balance.

    # ToDo: use labels, add english and russian translations with appropriate label to /helpers/translationHelper.py. Use get_label("text")
    response = f"""All user's list:
"""

    chat_list = Chat.objects.all()

    # What you'll need to do:
    # ToDo: Iterate over users, add each user's properties to the response text.
    # Use 'chat' object to get values from its properties. /tg_bot/models.py/Chat

    for chat in chat_list:
        user_balance = user_balance_helper(chat)
        # ToDo: fill with username from the chat object
        # ToDo: if username string should be exact 20 symbols, if it's not - fill with spaces at the end.
        username = ''
        # ToDo: instead of "ok" use chat.is_approved as a code of a tick and a cross
        status = 'ok'

        response += f"* {username} | {status} | {user_balance}\n"

    return response


def list_admin_commands_helper():
    # ToDO #116: List all admin commands.
    # ToDo: use labels, add english and russian translations with appropriate label to /helpers/translationHelper.py. Use get_label("text")
    response = f"""Admin commands:
"""
    admin_commands = [
        "list_users_balance_command",  # /admin_users_balance
        "list_users_command",  # /admin_list_users
        "list_admin_commands",  # /admin_commands
        "write_specific",  # /admin_write
    ]

    for command in admin_commands:
        command_descr = get_label(command)  # ToDo: to retrieve further labels you need to add it in get_label

        response += command_descr

    return response


def write_specific_helper(message: str, from_label: str, chat=None, chat_id=None):
    # ToDO #117: Write code to write a message from an admin.
    # ToDo: If both chat and user's id are none, raise error

    if not chat:
        chat = Chat.objects.filter(chat_id=chat_id)

    # Use 'chat' object to get chat_id from it if chat_id is null

    response = f"""Message from {from_label}:
{message}"""
    # ToDo: use labels, add english and russian translations with appropriate label to /helpers/translationHelper.py. Use get_label("text")
    print(response)
    return response, chat_id
