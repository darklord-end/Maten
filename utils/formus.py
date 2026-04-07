from pyrogram import Client
from pyrogram.raw.functions.channels import ToggleForum, CreateChannel
from pyrogram.raw.functions.messages import CreateForumTopic
from db import Database
import time
import logging

logger = logging.getLogger(__name__)

db = Database()

async def create_group(client):
    if db.get("main", "group_id") is not None:
        logger.info("Группа уже существует. ID:", db.get("main", "group_id"))
        return
    channel = await client.invoke(
        CreateChannel(
            title="Maten",
            about="",
            megagroup=True
        )
    )
    group_id = int(f"-100{channel.chats[0].id}")
    group = await client.get_chat(group_id)
    print(f"Группа '{group.title}' создана с ID: {group.id}")
    await client.invoke(
        ToggleForum(
            channel=await client.resolve_peer(group_id),
            enabled=True,
            tabs=False,
        )
    )
    print(f"Форум для группы '{group.title}' включен.")
    random_id = int(time.time() * 1000) % (2**63 - 1)
    print(f"Генерируем random_id для топика: {random_id}")
    icon_colors = [0x6FB9F0, 0xFFD67E, 0xCB86DB, 0x8EEE98, 0xFF93B2, 0xFB6F5F]
    topic_result = await client.invoke(
        CreateForumTopic(
            peer=await client.resolve_peer(group_id),
            title="logs",
            random_id=random_id,
            icon_color=icon_colors[0],  # голубой цвет
        )
    )
    topic_id = None
    for update in topic_result.updates:
        print(f"Update: {update}")
        print(dir(update))
        if hasattr(update, 'id'):
            topic_id = update.id
            break
        elif hasattr(update, 'channel_id') and hasattr(update, 'topic_id'):
            topic_id = update.topic_id
            break

    print(f"Найденный topic_id: {topic_id}")
    db.set("main", "group_id", group_id)
    db.set("main", "logs_topic_id", topic_id)