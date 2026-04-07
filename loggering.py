import logging
from pyrogram import Client
from db import Database
db = Database()
import time
import asyncio

logger = logging.getLogger(__name__)
config = open("config.ini", "r").read().split("\n")
api_id = config[1].split(" = ")[1]
api_hash = config[2].split(" = ")[1]
app = None
loop = None

def load(client):
    print("loading")
    global app, loop
    app = client
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()
    print("loaded app")

async def send_message(log_entry):
    if app is None:
        print("App not initialized, cannot send log.")
        return
    print("Sending log message to Telegram...")
    group_id = db.get("main", "group_id")
    topic_id = db.get("main", "logs_topic_id")
    if group_id is not None and topic_id is not None:
        try:
            await app.send_message(group_id, log_entry, message_thread_id=topic_id)
            print("Log message sent successfully.")
        except Exception as e:
            print(f"Failed to send log message: {e}")
    else:
        print("Group ID or Topic ID not found in database. Cannot send log message.")

class loggerhandler(logging.Handler):
    def emit(self, record):
        global app, loop
        if app is None:
            print("App not initialized, cannot send log.")
            return  
        
        log_entry = self.format(record)
        print("App is initialized, sending log.")
        
        if not hasattr(app, 'is_connected') or not app.is_connected:
            print(f"[LOG] {log_entry}")
            return
        try:
            try:
                current_loop = asyncio.get_running_loop()
                asyncio.create_task(send_message(log_entry))
            except RuntimeError:
                if loop and loop.is_running():
                    asyncio.run_coroutine_threadsafe(send_message(log_entry), loop)
                else:
                    print(f"[LOG] {log_entry}")
        except Exception as e:
            print(f"Failed to send log: {e}")
            print(f"[LOG] {log_entry}")