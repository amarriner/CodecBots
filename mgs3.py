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

      if (t - l) > 140:
         while re.match(r'^([ \.,])', string.strip(tweet[l:t])):
            l = l + 1

         print Config.get('Name', key) + ': @' + to  + ' ' + string.strip(tweet[l:t])

         l = t

   while re.match(r'^([ \.,])', string.strip(tweet[l:])):
      l = l + 1

   if tweet[l:]:
      print Config.get('Name', key) + ': @' + to + ' ' + string.strip(tweet[l:])

last_tweet = ''
last_to = ''
last_key = ''
tweet = ''
num_convos = 0
for i, line in enumerate(lines):
   if num_convos == 2:
      break

   if i > int(Config.get('Script', 'Last Line')):
      Config.set('Script', 'Last Line', str(i))
      match = re.match(r'^.*: ', line)
      if (match):
         key = match.group().replace(': ', '').lower().replace(' ', '_')

         if key in Config.options('Name'):
            if last_key != key:
               last_to = key
               if (last_tweet):
                  post_tweet(last_key, last_to, last_tweet)

               tweet = ''

            last_key = key
            tweet = string.strip(string.strip(line.replace(Config.get('Name', key) + ': ', '')), '"')
            last_tweet = tweet

      else:
         if line[:3] == '---' or line[:3] == '===' or line[:3] == '###':
            if (last_tweet):
               post_tweet(last_key, last_to, last_tweet)
               num_convos = num_convos + 1

            last_tweet = ''
            last_to = last_key
            tweet = ''
            last_key = ''

         if last_key in Config.options('Name'):
            if line[:5] == '     ':
               tweet = tweet + ' ' + string.strip(string.strip(line), '"')
               last_tweet = tweet
