#!/usr/bin/python

# ------------------------------------------------------------------------------------------------
# Twitter bots that have Metal Gear Solid codec conversations with each other
# Author: Aaron Marriner (https://twitter.com/amarriner)
# https://github.com/amarriner/CodecBots
# ------------------------------------------------------------------------------------------------

import ConfigParser
import re
import string
import time
import twitter

# Configuration file that contains various bot information such as their names and twitter accounts (and keys)
INI_FILE = 'mgs3.ini'
Config = ConfigParser.ConfigParser()
Config.read(INI_FILE)

# Read in the transcript file
# Downloaded from http://www.gamefaqs.com/ps2/914828-metal-gear-solid-3-snake-eater/faqs/43456
f = open('metal_gear_solid_3_sub_codec_script.txt', 'r')
lines = f.read().split('\n')
f.close()

# Find all the character data in the config file and put it into a dictionary for lookup
# Also instantiates and connects to a twitter object for each character
characters = dict()
for key in Config.options('Names'):
   if (Config.get('Keys', key)):
      characters[key] = {'key': Config.get('Keys', key), 'secret': Config.get('Secrets', key), \
                         'twitter': twitter.Api(Config.get('Twitter', 'Consumer Key'),         \
                                                Config.get('Twitter', 'Consumer Secret'),      \
                                                Config.get('Keys', key),                       \
                                                Config.get('Secrets', key))}

      # Pausing so we don't run into any usage errors for twitter
      time.sleep(2)


# ------------------------------------------------------------------------------------------------
# This function tweets a line of conversation for a particular bot.
# If the line is longer than 140 characters, the function will split it into several tweets until
# it has exhausted the line. It will generally tweet at another bot and will sometimes be in reply
# to a previous tweet in the conversation if there is one.
# ------------------------------------------------------------------------------------------------
def post_tweet(key, to, tweet, last_status=twitter.Status):
   l = 0
   t = 0
   dot = ''

   # Set up status object in case something goes wrong
   status = twitter.Status
   status.id = None

   # Use .@ replies to make sure non-followers see it
   if last_status.id:
      dot = '.'

   # If the to variable is not Snake, add him because everyone is always talking to him
   # Don't add it if it's Snake who is talking, natch...
   if to != '@' + Config.get('Usernames', 'snake') and key != 'snake':
      to = '@' + Config.get('Usernames', 'snake') + ' ' + to

   # Step through each character in the text to be tweeted
   for i,c in enumerate(tweet):

      # If we've reached our character limit before the end of the string, split it up and
      # post an interim tweet.
      #   * t represents the last good break where we can tweet without splitting a word up and
      #     still be under 140 characters
      #   * l represents the last t value we used to tweet
      if ((t + (i - t)) - l) >= 140 - (len(to) + 3):

         # This is a kludgey way of stripping out "bad" characters at the beginning of a tweet
         # Mainly to make the tweet look nicer so it doesn't start with periods, commas, etc.
         # Snake says '...' a lot so make a special case for that. Sometimes characters prefix
         # lines with '...', but also say something. The prefix will be stripped which should 
         # probably be fixed. Like I said...kludgey
         if (string.strip(tweet[l:t]) != '...'):
            while re.match(r'^([ \.,])', string.strip(tweet[l:t])):
               l = l + 1

         # Post the tweet to twitter and retain the resulting status object, print out a debug line and wait 
         # five seconds before continuing
         status = characters[key]['twitter'].PostUpdate(dot + to + ' ' + string.strip(tweet[l:t]), last_status.id)
         print dot + to + ' ' + string.strip(tweet[l:t]) + ' (' + str(status.id) + ')'
         time.sleep(5)

         # Update l because we posted a tweet
         l = t

      # Update t because we found a good break point (i.e., we're in between words)
      if not (re.match(r'([A-Za-z0-9])', c)):
         t = i

   # Again, stripping out "bad" characters"
   if (string.strip(tweet[l:]) != '...'):
      while re.match(r'^([ \.,])', string.strip(tweet[l:])):
         l = l + 1

   # If there are characters left (most likely there ar), tweet the rest
   if tweet[l:]:
      status = characters[key]['twitter'].PostUpdate(dot + to + ' ' + string.strip(tweet[l:]), last_status.id)
      print dot + to + ' ' + string.strip(tweet[l:]) + ' (' + str(status.id) + ')'

   # Return the resulting status object so it can be passed back in and used for its reply id
   return status


# ------------------------------------------------------------------------------------------------
# This function merely loops through a list of conversation lines between characters
# ------------------------------------------------------------------------------------------------
def process_conversation(conversation):

   # Set up the last_status variable which will affect whether a tweet is in response to a previous tweet or not
   last_status = twitter.Status
   last_status.id = None

   for index, line in enumerate(conversation):
      # This is the case where there is only one line of dialog in a given conversation, assume Snake is the recipient
      if index == 0 and len(conversation) == 1:
         last_status = post_tweet(line['key'], '@' + Config.get('Usernames', 'snake'), line['text'], last_status)

      # This is the case where we're on the first line of the conversation, but there are more than one total
      # Check the next line to see who this tweet should be directed at
      if index == 0 and len(conversation) > 1:
         last_status = post_tweet(line['key'], '@' + Config.get('Usernames', conversation[index + 1]['key']), line['text'], last_status)

      # Now we're past the first line so check the previous line to see who to reply to
      if index > 0:
         last_status = post_tweet(line['key'], '@' + Config.get('Usernames', conversation[index - 1]['key']), line['text'], last_status)

      # Wait 10 minutes before tweeting the next line of dialog
      time.sleep(60 * 3)


# ------------------------------------------------------------------------------------------------
# Main logic flow
# ------------------------------------------------------------------------------------------------
last_key = ''
conversation = []
for i, line in enumerate(lines):

   # On startup, skip a certain number of lines as determined by a config value. 
   if i > int(Config.get('Script', 'Last Line')):

      # Update the config file with the last line read 
      Config.set('Script', 'Last Line', str(i))
      f = open(INI_FILE, 'w')
      Config.write(f)
      f.close()

      # Determine if the line starts with some characters and a colon
      match = re.match(r'^.*: ', line)

      # If it does, make the regex match look like a potential character key (from the config file)
      # These should be lower case and replace spaces with underscores
      if (match):
         key = match.group().replace(': ', '').lower().replace(' ', '_')

         # If the key found is one of the keys from the config file, update the conversation if we're
         # on to a new character. Generally the second IF is superfluous given the layout of the 
         # transcript, but as a double-check I put it in
         if key in Config.options('Names'):
            if last_key != key:
               conversation.append({'key': key, 'text': string.strip(string.strip(line.replace(Config.get('Names', key) + ': ', '')), '"')})

            # Keep track of the last good key that was found
            last_key = key

      # Else there was no potential key match
      else:

         # These three circumstances denote the end of a conversation
         if line[:3] == '---' or line[:3] == '===' or line[:3] == '###':

            # So if we have any lines of dialog to tweet, process them then wait a period of time before 
            # looking for a new conversation to process
            if len(conversation):
               print "\n================================================================================================\n"
               print 'Processing conversation ... (Line ' + str(i) + ')'
               print "\n------------------------------------------------------------------------------------------------\n"
               process_conversation(conversation)
               time.sleep(60 * 60 * 8)

            conversation = []
            last_key = ''

         # This is a continuation of a line of dialog. The last_key variable holds the last character who
         # was talking and appends this text onto their last line.
         if last_key in Config.options('Names'):
            if line[:5] == '     ':
               conversation[len(conversation) - 1]['text'] = conversation[len(conversation) - 1]['text'] + ' ' + string.strip(string.strip(line), '"')
