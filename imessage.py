import applescript
from imessage_reader import fetch_data
import subprocess

DB_PATH = '/Users/mehularora/Library/Messages/chat.db'

fd = fetch_data.FetchData(DB_PATH)

# Tuple
my_data = fd.get_messages()

target_user = "" # Update to target user

target_user_texts = filter(lambda x: x[0] == target_user and x[5] == 0, my_data)

last_target_message = list(target_user_texts)[-1][1]

# TODO: Make endpoint request to finetuned model, get back response

res = "This is a dummy response"

subprocess.run(['osascript', 'sendCliText.scpt', target_user, res])