#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Updated: 
#  1. 使用async来update lastname，更加稳定

import time
import os
import sys
import logging
import asyncio
from time import strftime
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest

# Function to convert integer to Roman numeral, using ' ' for 0
def int_to_roman(num):
    if num == 0:
        return ' '  # Use ' ' to represent zero
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

# Function to convert time into Roman numerals
def time_to_roman(hour, minute):
    hour_roman = int_to_roman(int(hour))
    minute_roman = int_to_roman(int(minute))
    return f"{hour_roman}:{minute_roman}"

api_auth_file = 'api_auth'
if not os.path.exists(api_auth_file + '.session'):
    api_id = input('api_id: ')
    api_hash = input('api_hash: ')
else:
    api_id = 123456
    api_hash = '00000000000000000000000000000000'

client1 = TelegramClient(api_auth_file, api_id, api_hash)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Async function to update the last name every 10 seconds with Roman numerals
async def change_name_auto():
    print('will change name')

    while True:
        try:
            time_cur = strftime("%H:%M:%S:%p:%a", time.localtime())
            hour, minu, seco, p, abbwn = time_cur.split(':')

            # Update at 00 or 30 seconds
            if seco == '00' or seco == '30':
                # Convert current time to Roman numerals
                last_name = '⌛%s⌛' % time_to_roman(hour, minu)

                await client1(UpdateProfileRequest(last_name=last_name))
                logger.info('Updated -> %s' % last_name)
        
        except KeyboardInterrupt:
            print('\nwill reset last name\n')
            await client1(UpdateProfileRequest(last_name=''))
            sys.exit()

        except Exception as e:
            print('%s: %s' % (type(e), e))

        await asyncio.sleep(1)

# Main function to handle the Telegram client
async def main(loop):
    await client1.start()

    # Create a new task
    print('creating task')
    task = loop.create_task(change_name_auto())
    await task
     
    print('It works.')
    await client1.run_until_disconnected()
    task.cancel()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
