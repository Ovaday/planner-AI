# What is Planner-AI
Planner-AI is a project that implements ChatGPT integration in Telegram via Bots and provides altering functionality on the Website.
It includes several new functions that were not available on ChatGPT, such as messages classification and accepting audio messages from users.

**Demo**
* Production: https://planner-ai.vercel.app/ 
* Development: https://planner-ai-git-mig-ovaday.vercel.app/

## To launch the project locally:

**On Windows**
```bash
python -m venv virt_env
virt_env\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

**On Linux**
```bash
python -m venv virt_env
./virt_env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## Working with local data files

To decrypt (unpack) .enc files in /resources/ run:
```bash
python manage.py decrypt_resources
```

To encrypt (pack) files in /resources/extracted/, for example to push them to git, run:
```bash
python manage.py encrypt_resources
```