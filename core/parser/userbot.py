import asyncio
from telethon import TelegramClient, events
from data.database import log_interaction
from config.settings import API_ID, API_HASH

# Создаем клиент
client = TelegramClient('my_bot_v2', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    # Нас интересуют только ответы на сообщения (Reply)
    if event.reply_to_msg_id:
        try:
            # Получаем отправителя сообщения
            sender = await event.get_sender()
            # Получаем сообщение, на которое ответили
            replied_msg = await event.get_reply_message()
            replied_sender = await replied_msg.get_sender()

            if sender and replied_sender and sender.id != replied_sender.id:
                # Логируем связь в БД
                log_interaction(
                    from_id=sender.id,
                    from_user=getattr(sender, 'username', 'None'),
                    to_id=replied_sender.id,
                    to_user=getattr(replied_sender, 'username', 'None'),
                    chat_id=event.chat_id
                )
                print(f"[+] Связь: @{sender.username} ответил @{replied_sender.username}")
        except Exception as e:
            print(f"[-] Ошибка обработки сообщения: {e}")

async def run_parser():
    print("[*] Парсер запущен...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(run_parser())