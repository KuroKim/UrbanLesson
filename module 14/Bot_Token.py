import os

token_file_path = os.path.join(os.path.dirname(__file__), 'BOT_TOKEN.txt')

with open(token_file_path, 'r') as file:
    BOT_TOKEN = file.read().strip()
