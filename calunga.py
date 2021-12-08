#!/usr/bin/env python3
# coding: utf-8

import os, sys, time
import youtube_dl
from threading import Thread
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackContext, Filters
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
DOWNLOAD = 'downloads/'
DAYS = 1

def stop_and_restart():
    """Gracefully stop the Updater and replace the current process with a new one"""
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)

def restart(update, context):
    context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id)
    #update.message.reply_text('Estou reiniciando...')
    #context.bot.send_message(update.message.chat_id, 'Estou reiniciando...')
    Thread(target=stop_and_restart).start()

def older(dir_path, n):
    allFiles = os.listdir(dir_path)
    now = time.time()
    maxSize = n * 86400
    
    for f in allFiles:
        file_path = os.path.join(dir_path, f)
        if not os.path.isfile(file_path):
            continue
        elif file_path.endswith(".gitkeep"):
            continue
        if os.stat(file_path).st_mtime < now - maxSize:
            os.remove(file_path)

def download2(update: Update, context: CallbackContext):
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
        'socket_timeout': 120,
        'retries': 7,
        'quiet': False,
        'outtmpl': DOWNLOAD + '%(title)s-%(id)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(opts) as ydl:
        downloading = update.message.reply_text('Baixando...', quote=True, disable_web_page_preview=True)
        
        result = ydl.extract_info(url, download=False)

        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result

        print(video)

        ydl.download([url])

        if os.path.isfile(ydl.prepare_filename(video)):
            try:
                videoFile = open(ydl.prepare_filename(video), 'rb')
                
                documento = context.bot.send_document(timeout=10000, chat_id=chatId, document=open(videoFile, 'rb'))
                fileId = documento.document.file_id

                context.bot.send_document(timeout=10000, chat_id=chatId, document=fileId)
                
                #update.message.reply_video(filename, supports_streaming=True)

                context.bot.delete_message(chat_id=downloading.chat.id, message_id=downloading.message_id)
            except IOError:
                update.message.send_message('Impossível abrir o arquivo do vídeo.')
        else:
            update.message.send_message('Impossível abrir o arquivo do vídeo.')

def notify(message, update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def my_hook(d):
    if d['status'] == 'finished':
        notify('finished:\n' + d['filename'] + '\nsize: ' + str(round(d['total_bytes'] / 1024 / 1024,1)) + 'MB')
    if d['status'] == 'error':
        notify('error:\n' + d['filename'])

def download(update: Update):
    #older(DOWNLOAD, DAYS)

    url = update.message.text

    opts = {
        'format': 'best',
        'progress_hooks': [my_hook],
        'ignoreerrors': True,
        'nooverwrites': True,
        'continuedl': True,
        'youtube_include_dash_manifest': False,
        'socket_timeout': 8,
        'retries': 3,
        'outtmpl': DOWNLOAD + '%(title)s-%(id)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(opts) as ydl:
        update.message.reply_text('format:' + opts['format'] + '\ndownloading',quote=True)
        try:
            ydl.download([url])
        except:
            update.message.reply_text('Unexpected error occurred',quote=True)

updater = Updater(TOKEN, request_kwargs={'read_timeout': 60, 'connect_timeout': 120}, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.entity('url'), download, run_async=True))
updater.dispatcher.add_handler(CommandHandler('r', restart, filters=Filters.user(username='@sistematico')))

updater.start_polling()
updater.idle()