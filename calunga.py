#!/usr/bin/env python3
# coding: utf-8

import os, time
#from datetime import datetime, timedelta
import youtube_dl
from telegram import Update, ChatAction
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
DOWNLOAD = 'downloads/'
DAYS = 1

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator

send_typing_action = send_action(ChatAction.TYPING)
send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)

def older(dir_path, n):
    all_files = os.listdir(dir_path)
    now = time.time()
    #max = n * 86400
    max = 240
    for f in all_files:
        file_path = os.path.join(dir_path, f)
        if not os.path.isfile(file_path):
            continue
        if os.stat(file_path).st_mtime < now - max:
            os.remove(file_path)
            print("Deleted ", f)

#@send_upload_video_action

def download(update: Update, context: CallbackContext):
    older(DOWNLOAD, DAYS)

    url = update.message.text

    messageId = update.message.message_id
    chatId = update.message.chat.id

    #context.bot.delete_message(chat_id=chatId, message_id=messageId)

    opts = {
        'format': 'best',
        'ignoreerrors': True,
        'nooverwrites': True,
        'continuedl': True,
        'youtube_include_dash_manifest': False,
        'socket_timeout': 10,
        'retries': 3,
        'quiet': False,
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
                #update.message.send_video(filename, supports_streaming=True, quote=True)
                #update.message.send_video(filename, supports_streaming=True)
                context.bot.send_video(filename, supports_streaming=True)
            except IOError:
                update.message.send_message("Impossível abrir o arquivo do vídeo.")
            finally:
                filename.close()

        except:
            update.message.reply_text('Um erro ocorreu, tente novamente.',quote=True)    

        #update.message.send_message(print(vars(downloading)))
        #context.bot.send_message(text=print(vars(downloading)))
        #update.message.reply_text(print(downloading),quote=True)    
        #context.bot.delete_message(downloading.message_id)
        #context.bot.delete_message(chat_id=update.message.chat_id, downloading.message_id)
        #context.bot.send_message(chat_id=print(vars(downloading)))

        context.bot.delete_message(chat_id=downloading.chat.id, message_id=downloading.message_id)
        context.bot.delete_message(chat_id=chatId, message_id=messageId)

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.entity('url'), download))

updater.start_polling()
updater.idle()