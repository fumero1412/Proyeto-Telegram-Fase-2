from telethon import TelegramClient, events
import asyncio, threading, os, glob
from flask import Flask

API_ID = 32695956
API_HASH = '8d939c8130ea03c01cd9abe6a6e83d7a'
GRUPO = -1003764262854
TOPIC = 717696
CANAL = 'https://t.me/Horny_J'

app = Flask(__name__)
@app.route('/')
def home(): return "Bot vivo"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

s = glob.glob("*.session")
client = TelegramClient(s[0].replace('.session','') if s else 'sesion_nube', API_ID, API_HASH)

async def main():
    await client.start()
    print("CLIENTE CONECTADO OK")
    o = await client.get_entity(CANAL)
    d = await client.get_entity(GRUPO)
    async for m in client.iter_messages(o, reverse=True):
        if not (m.media or (m.text or "").startswith("https://telegra.ph")): continue
        try:
            if m.media: await client.send_file(d, m.media, caption=m.text, reply_to=TOPIC)
            else: await client.send_message(d, m.text, reply_to=TOPIC)
            print(f"Copiado {m.id}")
            await asyncio.sleep(1)
        except Exception as e: print(e); await asyncio.sleep(3)
    print("HISTORIAL LISTO - EN VIVO")
    @client.on(events.NewMessage(chats=CANAL))
    async def h(e):
        if not (e.message.media or (e.message.text or "").startswith("https://telegra.ph")): return
        if e.message.media: await client.send_file(d, e.message.media, caption=e.message.text, reply_to=TOPIC)
        else: await client.send_message(d, e.message.text, reply_to=TOPIC)
    await client.run_until_disconnected()
asyncio.run(main())
