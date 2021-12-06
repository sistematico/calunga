#!/usr/bin/env python3
# coding: utf-8

import os, time
import youtube_dl
from telegram import Update, ChatAction
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
DOWNLOAD = 'downloads/'
DAYS = 1

def older(dir_path, n):
    all_files = os.listdir(dir_path)
    now = time.time()
    max = n * 86400
    for f in all_files:
        file_path = os.path.join(dir_path, f)
        if not os.path.isfile(file_path):
            continue
        elif file_path.endswith(".gitkeep"):
            continue
        if os.stat(file_path).st_mtime < now - max:
            os.remove(file_path)

def download(update: Update, context: CallbackContext):
    older(DOWNLOAD, DAYS)

    url = update.message.text
    
    messageId = update.message.message_id
    chatId = update.message.chat.id

    # opts = {
    #     'format': 'best',
    #     'ignoreerrors': True,
    #     'nooverwrites': True,
    #     'continuedl': True,
    #     'youtube_include_dash_manifest': False,
    #     'socket_timeout': 10,
    #     'retries': 3,
    #     'quiet': True,
    #     'outtmpl': DOWNLOAD + '%(title)s-%(id)s.%(ext)s',
    # }
    
    opts = {
        'format': 'best',
        'socket_timeout': 20,
        'retries': 5,
        'quiet': False,
        'outtmpl': DOWNLOAD + '%(title)s-%(id)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(opts) as ydl:
        downloading = update.message.reply_text('Baixando: ' + url, quote=True, disable_web_page_preview=True)
        
        result = ydl.extract_info(url, download=True)

        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result

        if os.path.isfile(ydl.prepare_filename(video)):
            try:
                filename = open(ydl.prepare_filename(video), 'rb')
                update.message.reply_video(filename, supports_streaming=True)
                context.bot.delete_message(chat_id=downloading.chat.id, message_id=downloading.message_id)
            except IOError:
                update.message.send_message('Impossível abrir o arquivo do vídeo.')
        else:
            update.message.send_message('Impossível abrir o arquivo do vídeo.')


updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.entity('url'), download))

updater.start_polling()
updater.idle()