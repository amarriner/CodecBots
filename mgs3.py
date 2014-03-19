#!/usr/bin/python

import ConfigParser
import re
import string
import time
import twitter

INI_FILE = 'mgs3.ini'
Config = ConfigParser.ConfigParser()
Config.read(INI_FILE)

f = open('metal_gear_solid_3_sub_codec_script.txt', 'r')
lines = f.read().split('\n')
f.close()

characters = dict()

for key in Config.options('Names'):
   if (Config.get('Keys', key)):
      characters[key] = {'key': Config.get('Keys', key), 'secret': Config.get('Secrets', key), \
                         'twitter': twitter.Api(Config.get('Twitter', 'Consumer Key'),         \
                                                Config.get('Twitter', 'Consumer Secret'),      \
                                                Config.get('Keys', key),                       \
                                                Config.get('Secrets', key))}
      time.sleep(2)

def post_tweet(key, to, tweet, reply_id=None):
   l = 0
   t = 0
   dot = ''

   if reply_id:
      dot = '.'

   for i,c in enumerate(tweet):
      if ((t + (i - t)) - l) >= 140 - (len(to) + 2):
         while re.match(r'^([ \.,])', string.strip(tweet[l:t])):
            l = l + 1

         print dot + to + ' ' + string.strip(tweet[l:t]) + ' ' + str(t) + ' ' + str(l) + ' ' + str(len(to)) + ' ' + str(i)
         status = characters[key]['twitter'].PostUpdate(dot + to + ' ' + string.strip(tweet[l:t]), reply_id)
         time.sleep(5)

         l = t

      if not (re.match(r'([A-Za-z0-9])', c)):
         t = i

   while re.match(r'^([ \.,])', string.strip(tweet[l:])):
      l = l + 1

   if tweet[l:]:
      print dot + to + ' ' + string.strip(tweet[l:])
      status = characters[key]['twitter'].PostUpdate(dot + to + ' ' + string.strip(tweet[l:]), reply_id)

   return status

def process_conversation(conversation):
   print "\n================================================================================================\n"
   last_status = None

   for index, line in enumerate(conversation):
      if index == 0 and len(conversation) == 1:
         last_status = post_tweet(line['key'], '@' + Config.get('Usernames', 'snake'), line['text'])
      if index == 0 and len(conversation) > 1:
         last_status = post_tweet(line['key'], '@' + Config.get('Usernames', conversation[index + 1]['key']), line['text'])
      if index > 0:
         last_status = post_tweet(line['key'], '@' + Config.get('Usernames', conversation[index - 1]['key']), line['text'])

      time.sleep(60 * 10)

last_key = ''
conversation = []
for i, line in enumerate(lines):
   if i > int(Config.get('Script', 'Last Line')):
      Config.set('Script', 'Last Line', str(i))
      match = re.match(r'^.*: ', line)
      if (match):
         key = match.group().replace(': ', '').lower().replace(' ', '_')

         if key in Config.options('Names'):
            if last_key != key:
               conversation.append({'key': key, 'text': string.strip(string.strip(line.replace(Config.get('Names', key) + ': ', '')), '"')})

            last_key = key

      else:
         if line[:3] == '---' or line[:3] == '===' or line[:3] == '###':
            if len(conversation):
               print 'Processing conversation ... (Line ' + str(i) + ')'
               process_conversation(conversation)
               time.sleep(60 * 60 * 8)

            conversation = []
            last_key = ''

         if last_key in Config.options('Names'):
            if line[:5] == '     ':
               conversation[len(conversation) - 1]['text'] = conversation[len(conversation) - 1]['text'] + ' ' + string.strip(string.strip(line), '"')
