import os

CFG_BOT_TOKEN = os.getenv("BOT_TOKEN")

def print_current_config():
    print(f"CFG_BOT_TOKEN: {CFG_BOT_TOKEN}")
