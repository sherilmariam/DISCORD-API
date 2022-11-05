import os
import discord
import json
import requests
import random
from replit import db
from breakless import breakless

client = discord.Client()
sadwd = [
    "sad", "depressed", "dying", "freaking", "depressing", "suicide",
    "suicidal", "hopeless", "miserable", "heartbroken", "broken", "self hatred","panick",
]
senc = ["hang in there", "cheer up", "you r not alone", "help is available","you are loved",""]
if "mirai" not in db.keys():
    db["mirai"] = True


def get_quote():
    res = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(res.text)
    quote = json_data[0]['q'] + '-' + json_data[0]['a']
    return (quote)


def update_enc(enc_msg):
    if "enc" in db.keys():
        enc = db["enc"]
        enc.append(enc_msg)
    else:
        db["enc"] = [enc_msg]


def delete_tsk(index):
    tsk = db["tsk"]
    if len(tsk) > index:
        del tsk[index]
        db["tsk"] = tsk


def update_list(ntask):
    if "tsk" in db.keys():
        tsk = db["tsk"]
        tsk.append(ntask)
    else:
        db["tsk"] = [ntask]


@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))


@client.event
async def on_message(msg):
    if msg.author != client.user:
        if msg.content.lower().startswith("!hi"):
            await msg.channel.send(f"Hi,{msg.author.display_name}")
    if msg.author == client.user:
        return
    if msg.content.startswith("!mirai"):
        value = msg.content.split("!mirai", 1)[1]
        if value.lower() == " initiate":
            db["mirai"] = True
            await msg.channel.send("responding is on")
        else:
            db["mirai"] = False
            await msg.channel.send("responding is off")

    if msg.content.startswith('!to do'):
        await msg.channel.send('list coming up')
    if msg.content.startswith('!inspire'):
        quote = get_quote()
        await msg.channel.send(quote)
    m = msg.content
    word = m.split(" ")
    for i in word:
        if i == "suicide" or i == "suicidal":
            await msg.channel.send("help is available")
            await msg.channel.send("reach out to someone or call a therapist")
        else:
            if db["mirai"] == True:
                options = senc
                if "enc" in db.keys():
                    options = options + db["enc"].value

                if i in sadwd:
                    await msg.channel.send(
                        f"{random.choice(options)},{msg.author.display_name}")
            if m.startswith("!new"):
                enc_msg = m.split("!new", 1)[1]
                update_enc(enc_msg)
                await msg.channel.send("new message has been added")
            if m.startswith("!del"):
                tsk = []
                if "tsk" in db.keys():
                    index = int(m.split("!del", 1)[1])
                    delete_tsk(index)
                    tsk = db['tsk']
                    await msg.channel.send(tsk)

            if m.startswith("!list"):
                await msg.channel.send("list of encouraging messages")
                enc = []
                if "enc" in db.keys():
                    enc = db["enc"]
                    await msg.channel.send(enc)
            if m.startswith("!newtask"):
                ntask = m.split("!newtask", 1)[1]
                update_list(ntask)
                await msg.channel.send("new task has been added")
            if m.startswith("!task"):
                await msg.channel.send("to do list")
                tsk = []
                if "tsk" in db.keys():
                    tsk = db["tsk"]
                    await msg.channel.send(tsk)


breakless()
client.run(os.environ['TOKEN'])
