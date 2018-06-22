#!bin/bash/python3
# -*- coding: utf-8 -*-
import time
from threading import Thread
from datetime import datetime
from zipfile import ZipFile
import subprocess
import sys

import telepot

from Handle import user_commands
from PyMyAdmin import Database as db

group_id = str(-1001166468779)
bot = telepot.Bot(sys.argv[1])

def add_group(idU,chatT,chatId):
    bot.sendMessage(group_id,'`{}` Added me to the group `{}` : `{}`'.format(idU,chatT,chatId),parse_mode="Markdown")
    db(chatId,chatT,idU).add_groups()
def del_group(idU,chatT,chatId):
    bot.sendMessage(group_id,'`{}` Removed me from the group `{}` : `{}`'.format(idU,chatT,chatId),parse_mode="Markdown")
    db(chatId,chatT,idU).remove_groups()

def check(func):
    commands = (
        '/start','/sql', '/xss',
        '/lfi', '/bing', '/dork',
        '/ch', '/help','$statist',
        '/decrypt','/encrypt','/bkp',
        '/file'
    )
    def inner(msg):
        if msg.get('text'):
            cmd = msg.get('text').split()[0].lower()
            msg['command'] = {
                'check': cmd in commands,
                'cmd': cmd
            }
        try:
            if msg['new_chat_participant']['username'] == 'ScrutinBot':
                add_group(msg['from']['id'],str(msg['chat']['title']),str(msg['chat']['id']))
            elif msg['left_chat_participant']['username'] == 'ScrutinBot':
                del_group(msg['from']['id'],str(msg['chat']['title']),str(msg['chat']['id']))
        except:
            pass
        func(msg)
    
    return inner

@check
def control(msg):
    try:
        handle = user_commands(bot,msg)

        user_command = {
            '/start': handle.welcome,
            '/sql': handle.sqli,
            '/xss': handle.xss,
            '/lfi': handle.lfi,
            '/bing': handle.bing,
            '/dork': handle.gen_dork,
            '/help': handle.help_users,
            '/encrypt': handle._Encrypt,
            '/decrypt': handle._Decrypt,
            '/ch': handle.changelog_for_users,
            '/bkp': handle.manual_bkp,
            '/file': handle.sendFile,
            '$statist': handle.statistcs
        }

        if msg['command']['check']:
            user_command[msg['command']['cmd']]()
        else:
            pass
    except:
        pass

time.sleep(2)
bot.message_loop(control)
print("[+] Scrutin Iniciado [+]\n")
while 1:
    time.sleep(10)