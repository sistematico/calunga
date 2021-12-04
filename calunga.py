#!/usr/bin/env python3
# coding: utf-8

import os, time
#from datetime import datetime, timedelta
import youtube_dl
from telegram import Update
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
DOWNLOAD = 'downloads/'

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        #context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_VIDEO)
        return func(update, context,  *args, **kwargs)

    return command_func

# @send_typing_action
# def my_handler(update, context):
#     pass # Will send 'typing' action while processing the request.


def older(dir_path, n):
    all_files = os.listdir(dir_path)
    now = time.time()
    #max = n * 86400
    max = 60
    for f in all_files:
        file_path = os.path.join(dir_path, f)
        if not os.path.isfile(file_path):
            continue
        if os.stat(file_path).st_mtime < now - max:
            os.remove(file_path)
            print("Deleted ", f)

@send_typing_action
def download(update: Update, context: CallbackContext):
    older(DOWNLOAD, 7)

    url = update.message.text

    opts = {
        'format': 'best',
        'ignoreerrors': True,
        'nooverwrites': True,
        'continuedl': True,
        'youtube_include_dash_manifest': False,
        'socket_timeout': 8,
        'retries': 3,
        'outtmpl': DOWNLOAD + '%(title)s-%(id)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(opts) as ydl:
        downloading = update.message.reply_text('Baixando: ' + url, quote=True, disable_web_page_preview=True)

        try:
            result = ydl.extract_info(url, download=True)

            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result
            
            try:
                filename = open(ydl.prepare_filename(video), 'rb')
                #update.message.reply_video(filename, supports_streaming=True)
                update.message.send_video(filename, supports_streaming=True, quote=True)
            except IOError:
                update.message.send_message("Impossível abrir o arquivo do vídeo.")
            finally:
                filename.close()

        except:
            update.message.reply_text('Um erro ocorreu, tente novamente.',quote=True)    

        context.bot.delete_message(downloading)

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.entity('url'), download))

updater.start_polling()
updater.idle()