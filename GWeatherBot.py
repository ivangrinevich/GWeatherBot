from pyrogram import Client, filters


app = Client("bot",
             plugins=dict(root='plugins'))


app.run()
