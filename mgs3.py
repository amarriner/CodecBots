#!/usr/bin/python

import ConfigParser
import re
import string

INI_FILE = 'mgs3.ini'
Config = ConfigParser.ConfigParser()
Config.read(INI_FILE)

f = open('metal_gear_solid_3_sub_codec_script.txt', 'r')
lines = f.read().split('\n')
f.close()

def post_tweet(key, to, tweet):
   l = 0
   t = 0
   for i,c in enumerate(tweet):
      if not (re.match(r'([A-Za-z0-9])', c)):
         t = i

      if (t - l) > 140 - len(to) + 1:
         while re.match(r'^([ \.,])', string.strip(tweet[l:t])):
            l = l + 1

         print Config.get('Name', key) + ': ' + to + ' ' + string.strip(tweet[l:t])

         l = t

   while re.match(r'^([ \.,])', string.strip(tweet[l:])):
      l = l + 1

   if tweet[l:]:
      print Config.get('Name', key) + ': ' + to + ' ' + string.strip(tweet[l:])

def process_conversation(conversation):
   print '\n================================================================================================\n'

   
   for index, line in enumerate(conversation):
      if index == 0 and len(conversation) == 1:
         post_tweet(line['key'], '@snake', line['text'])
      if index == 0 and len(conversation) > 1:
         post_tweet(line['key'], '@' + conversation[index + 1]['key'], line['text'])
      if index > 0:
         post_tweet(line['key'], '@' + conversation[index - 1]['key'], line['text'])

last_key = ''
num_convos = 0
conversation = []
for i, line in enumerate(lines):
   if num_convos == 3:
      break

   if i > int(Config.get('Script', 'Last Line')):
      Config.set('Script', 'Last Line', str(i))
      match = re.match(r'^.*: ', line)
      if (match):
         key = match.group().replace(': ', '').lower().replace(' ', '_')

         if key in Config.options('Name'):
            if last_key != key:
               conversation.append({'key': key, 'text': string.strip(string.strip(line.replace(Config.get('Name', key) + ': ', '')), '"')})

            last_key = key

      else:
         if line[:3] == '---' or line[:3] == '===' or line[:3] == '###':
            if len(conversation):
               num_convos = num_convos + 1
               process_conversation(conversation)

            conversation = []
            last_key = ''

         if last_key in Config.options('Name'):
            if line[:5] == '     ':
               conversation[len(conversation) - 1]['text'] = conversation[len(conversation) - 1]['text'] + ' ' + string.strip(string.strip(line), '"')

print '\n================================================================================================\n'
