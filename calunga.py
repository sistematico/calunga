#!/usr/bin/env python3
# coding: utf-8

import os
import youtube_dl
from telegram import Update
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
DOWNLOAD = 'downloads/'

def download(update: Update, context: CallbackContext):
    url = update.message.text
    opts = {
        'format': 'best',
        'ignoreerrors': True,
        'nooverwrites': True,
        'continuedl': True,
        'youtube_include_dash_manifest': False,
        'socket_timeout': 8,
        'retries': 3,
        'outtmpl': DOWNLOAD + '/%(title)s-%(id)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(opts) as ydl:
        update.message.reply_text('Baixando: ' + url,quote=True)
        try:
            # ydl.download([url])
            result = ydl.extract_info(url, download=True)

            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result

            
            try:
                filename = open(ydl.prepare_filename(video), 'rb')
                update.message.reply_video(filename, supports_streaming=True)
            except IOError:
                update.message.send_message("Impossível abrir o arquivo do vídeo.")
            finally:
                filename.close()


            #update.message.reply_text(ydl.prepare_filename(video),quote=True)
            #update.message.reply_video(ydl.prepare_filename(video),quote=True)
            #update.message.reply_video(ydl.prepare_filename(video),quote=True)

            #bot.send_video(chat_id=update.message.chat_id, video=open('output.mp4', 'rb'), supports_streaming=True)
            #update.message.reply_video(video=open(ydl.prepare_filename(video), 'rb'), supports_streaming=True)

        except:
            update.message.reply_text('Um erro ocorreu',quote=True)    


updater = Updater(TOKEN, use_context=True)
#updater.dispatcher.add_handler(MessageHandler(Filters.text, download))
#updater.dispatcher.add_handler(MessageHandler(Filters.text, download))
updater.dispatcher.add_handler(MessageHandler(Filters.entity('url'), download))

updater.start_polling()
updater.idle()