#Ahsoka_Tano_Bot
#Not intended to be used abusively on reddit

#Color Code
#Title = Purple
#Ignore stuff = Yellow
#Dice Rolls = Blue
#Describers = Green
#Everything pulled = White
#Spacers = White
#General Messages = Cyan


from googletrans import Translator, constants
from pprint import pprint
translator = Translator()

import os




from gingerit.gingerit import GingerIt






import praw
import os
import csv
from replit import db
from keep_alive import keep_alive
import re
import random
import time
import numpy as np

from our_colors import COL

from datetime import datetime

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

nltk.download('omw-1.4')
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

grammar=GingerIt()

langs=[
"af",
"ga",
"sq",
"it",
"ar",
"ja",
"az",
"kn",
"eu",
"ko",
"bn",
"la",
"be",
"lv",
"bg",
"lt",
"ca",
"mk",
"zh-CN",
"ms",
"zh-TW",
"mt",
"hr",
"no",
"cs",
"fa",
"da",
"pl",
"nl",
"pt",
"en",
"ro",
"eo",
"ru",
"et",
"sr",
"tl",
"sk",
"fi",
"sl",
"fr",
"es",
"gl",
"sw",
"ka",
"sv",
"de",
"ta",
"el",
"te",
"gu",
"th",
"ht",
"tr",
"iw",
"uk",
"hi",
"ur",
"hu",
"vi",
"is",
"cy",
"id",
"yi",
]
phlangs=[
"af",
"ga",
"sq",
"it",


"az",

"eu",


"la",

"lv",

"lt",
"ca",


"ms",

"mt",
"hr",
"no",
"cs",

"da",
"pl",
"nl",
"pt",
"en",
"ro",
"eo",

"et",

"tl",
"sk",
"fi",
"sl",
"fr",
"es",
"gl",
"sw",

"sv",
"de",





"ht",
"tr",




"hu",
"vi",
"is",
"cy",
"id",

]

#translate the text into random languages and then back to english effectively paraphrasing or changing the meaning
def lang_rotate(txt):
  lis=[random.choice(langs),random.choice(langs),random.choice(langs),random.choice(langs),random.choice(langs)]
  translation = translator.translate(txt, src="en",dest=lis[0]).text
  translation = translator.translate(translation, src=lis[0],dest=lis[1]).text
  translation = translator.translate(translation, src=lis[1],dest=lis[2]).text
  translation = translator.translate(translation, src=lis[2],dest=lis[3]).text
  translation = translator.translate(translation, src=lis[3],dest=lis[4]).text
  translation = translator.translate(translation, src=lis[4],dest="en").text
  print(translation)
  return translation
  
#translate a single word into a random language that uses the phoenician alphabet
def rand_lang_word(txt):
  return translator.translate(txt, src="en",dest=random.choice(phlangs)).text

# get all the synonyms for a word
def get_all_synonyms(word):
    synonyms = []
    for ss in wn.synsets(word):
        synonyms.extend(ss.lemma_names())
        for sim in ss.similar_tos():
            synonyms_batch = sim.lemma_names()
            synonyms.extend(synonyms_batch)
    synonyms = set(synonyms)
    if word in synonyms:
        synonyms.remove(word)
    synonyms = [synonym.replace('_', ' ') for synonym in synonyms]
    return synonyms

#get all the synonyms/antonyms/hypernyms/pertainyms etc for a word
def get_all_nyms(word):
    nyms = []
    for ss in wn.synsets(word):
        nyms.extend(ss.lemma_names())
        for sim in ss.similar_tos():
            nyms_batch = sim.lemma_names()
            nyms.extend(nyms_batch)
            for s in sim.lemmas():
                lnyms=s.antonyms()
                lnyms.extend(s.pertainyms())
                lnyms.extend(s.derivationally_related_forms())
                for anm in lnyms:
                    nyms.append(str(anm.name()))
        for sim in ss.hypernyms():
            nyms_batch = sim.lemma_names()
            nyms.extend(nyms_batch)
            for s in sim.lemmas():
                lnyms=s.antonyms()
                lnyms.extend(s.pertainyms())
                lnyms.extend(s.derivationally_related_forms())
                for anm in lnyms:
                    nyms.append(str(anm.name()))
        for sim in ss.hyponyms():
            nyms_batch = sim.lemma_names()
            nyms.extend(nyms_batch)
            for s in sim.lemmas():
                lnyms=s.antonyms()
                lnyms.extend(s.pertainyms())
                lnyms.extend(s.derivationally_related_forms())
                for anm in lnyms:
                    nyms.append(str(anm.name()))
        for sim in ss.member_holonyms():
            nyms_batch = sim.lemma_names()
            nyms.extend(nyms_batch)
            for s in sim.lemmas():
                lnyms=s.antonyms()
                lnyms.extend(s.pertainyms())
                lnyms.extend(s.derivationally_related_forms())
                for anm in lnyms:
                    nyms.append(str(anm.name()))
        for sim in ss.root_hypernyms():
            nyms_batch = sim.lemma_names()
            nyms.extend(nyms_batch)
            for s in sim.lemmas():
                lnyms=s.antonyms()
                lnyms.extend(s.pertainyms())
                lnyms.extend(s.derivationally_related_forms())
                for anm in lnyms:
                    nyms.append(str(anm.name()))
        for s in ss.lemmas():
            lnyms=s.antonyms()
            lnyms.extend(s.pertainyms())
            lnyms.extend(s.derivationally_related_forms())
            for anm in lnyms:
              nyms.append(str(anm.name()))      
    nyms = set(nyms)
    if word in nyms:
        nyms.remove(word)
    nyms = [nym.replace('_', ' ') for nym in nyms]
    return nyms


# get all the synonyms and pick one at random
def get_rand_syn(word):
  wrds=get_all_synonyms(word)
  if len(wrds) < 1:
    return word
  return random.choice(wrds)

#get all the *nyms and pick one at random
def get_rand_nym(word):
  try:
    wrds=get_all_nyms(word)
    if len(wrds) < 1:
      return word
    return random.choice(wrds)
  except:
    return word

#for each word in the sentence swap a word with a similar word 50% of the time
def randomize_nyms(word):
  ri=word.split(" ")
  res=""
  for r in ri:
    rt=word_tokenize(r)
    tes=""
    for t in rt:
      if len(t) > 3 and random.choice([True,False]):
        t=get_rand_nym(t)
      tes=tes+t
    res=res+tes+" "
  word=res
  return word

#for each word in the sentence swap a word with that word from another language 50% of the time
def randomize_langs(word):
  ri=word.split(" ")
  res=""
  for r in ri:
    rt=word_tokenize(r)
    tes=""
    for t in rt:
      if len(t) > 3 and random.choice([True,False]):
        t=rand_lang_word(t)
      tes=tes+t
    res=res+tes+" "
  word=res
  return word
#swap a vowel for another vowel randomly
def swap_vowel(ch):
  if ch == "a":
    return random.choice(["e","i","o","u"])
  if ch == "e":
    return random.choice(["a","i","o","u"])
  if ch == "i":
    return random.choice(["e","a","o","u"])
  if ch == "o":
    return random.choice(["e","i","a","u"])
  if ch == "u":
    return random.choice(["e","i","o","a"])
  return ch
#replace each vowel in a word with another vowel 1/3 of the time
def randomize_vowels(word):
  w=""
  for ch in word:
    if random.choice([False,True,False]):
      w=w+swap_vowel(ch)
    else:w=w+ch
  return w
  
def list_content(filepath):
    items = []
    with open(filepath, 'r') as rf:
        items = rf.read().split("\n")
    while "" in items:
        items.pop(items.index(""))
    return items


adverbs=list_content("lists/words/adverbs.txt")

def sent_split(sent):
  ss=sent.split(' ')
  ss[(len(ss)/2)]=ss[(len(ss)/2)]+' '+random.choice(adverbs)
  sent=ss.join(' ')
  return sent

def add_adverbs(word):
  wres=""
  words=word.split(".")
  if len(words)==1:
    return sent_split(words[0])+"."
  for w in words:
    if len(w) > 2:
      wres=wres+sent_split(w)+"."
  return wres
  
#run all intended sentence and word mutations on reddit comment
def process_output(repli):
  if repli.count("*") > 0:
    return alt_chars(repli.replace("*"," "))
    
  swich=random.choice([0,1,2,3])
  if(swich==0):
    repli=randomize_nyms(repli)
  if(swich==1):
    repli=randomize_vowels(repli)
  if(swich==2):
    repli=lang_rotate(repli)
  if(swich==3):
    repli=randomize_langs(repli)
  repli=add_adverbs(repli)
  ct=grammar.parse(repli)
  print(ct)
  repli=ct.get('result')
  repli=pad_string(alt_chars(repli))
  return repli

#process sentence and word mutations on input triggers
def process_trigger(trig):
  if trig.count("*") > 0:
    return trig.split("*")[0]
  return randomize_nyms(trig.split("*")[0])


#directories
IGNORE_LIST = "lists/ignore_list.txt"
GENERAL_REPLIES = "lists/general_replies.txt"
REPLIES = "lists/replies.txt"
GENERAL_TRIGGERS = "lists/general_triggers.txt"
GRAY_LIST = "lists/gray_list.txt"
GRAY_LIST_REPLIES = "lists/gray_list_replies.txt"
CAKE_DAY_LIST = "lists/cake_day_list.txt"
RESPONSE_REPLIES = "lists/response_replies.txt"
CAKE_DAY_REPLIES = "lists/cake_day_replies.txt"


#special number amounts or something
DASH_AMOUNT = 5
NEWLINE_AMOUNT = 1

#The time in seconds between posts
COOLDOWN = 600
COOLDOWN = 30



#Change some letters with alternates to avoid triggering other bots
def alt_chars(word):
  word=word.replace("a","а")
  word=word.replace("e","е")
  word=word.replace("p","р")
  word=word.replace("c","с")
  word=word.replace("s","ѕ")
  word=word.replace("y","у")
  word=word.replace("x","х")
  word=word.replace("o","о")
  word=word.replace("w","ԝ")
  return word
  
# pad strings with zero-width joiners to prevent triggering other bots
def pad_string(str):
    padded = ""
    for ch in str:
        padded = padded + ch + "‍"
    return padded


#Initalizers
def clean_string(raw_string):
    cleaned_string = raw_string.lower()
    cleaned_string = re.sub(r'[^A-Za-z0-9 ]+', '', cleaned_string)
    return cleaned_string




response_list = []

# Bots user id
bot_id = 'swuxogqb'

#Sign into Reddit Account
reddit = praw.Reddit(client_id=os.environ['client_id'],
                     client_secret=os.environ['client_secret'],
                     username=os.environ['username'],
                     password=os.environ['password'],
                     user_agent="<AshokaBot123>")

# print(reddit.auth.url(["identity"], "...", "permanent"))
print(reddit.user.me())

keep_alive()

while True:
    try:
        # Begins the comment stream, scans for new comments
        for comment in reddit.subreddit('prequelmemes').stream.comments(
                skip_existing=True):

            author_name = str(comment.author.name)  # Fetch author name
            author_id = str(comment.author.id)  # Fetch author id
            comment_lower = comment.body.lower(
            )  # Fetch comment body and convert to lowercase

            #ignore list stuff
            with open(IGNORE_LIST,
                      'r') as rf:  # Opens ignore_list in read only mode

                rf_contents = rf.read()  # Reads the contents of ignore list

                if author_id not in rf_contents and author_id != bot_id:  #Checks comment against ignore list and bot id
                    with open(GRAY_LIST, 'r') as gl:

                        gray_list = gl.read(
                        )  # Reads the contents of gray list

                        if author_name in gray_list:  #determines if user is in graylist

                            is_graylisted = "yes"
                            # print("gray_list is yes")

                        else:

                            is_graylisted = "no"
                            # print("gray_list is no")

                    if "!ignore" in comment_lower and len(
                            comment_lower
                    ) < 8:  # Looks for the word "ignore" in the comment and checks length of comment to prevent misfire.
                        print(COL.WHITE + "-" * DASH_AMOUNT)
                        print(COL.PURPLE + "Ignore Found")
                        print(COL.YELLOW + "Checking if reply")

                        if comment.parent(
                        ).author.id == bot_id:  # Checks if comment is a reply to your bot

                            with open(
                                    IGNORE_LIST, 'a'
                            ) as f:  # Opens ignore list in append mode

                                print(COL.YELLOW + "New Ignore")
                                print(COL.GREEN + "User: " + COL.WHITE,
                                      comment.author.name)
                                print(COL.GREEN + "User ID: " + COL.WHITE,
                                      comment.author.id)
                                print(COL.GREEN + "Comment: " + COL.WHITE,
                                      comment.body.lower())

                                # Writes Username and ID of user to the ignore list
                                f.write(author_name)
                                f.write("\n")
                                f.write(author_id)
                                f.write("\n")
                                f.write("\n")

                                print(COL.YELLOW + "User Added to Ignore List")
                                print(COL.WHITE + "-" * DASH_AMOUNT)

                                # Replies to user comment
                                comment.reply(
                                    process_output(
                                        "If it isn’t the hairless harpy. How nice of you. Tell you what, I’ll give you a merciful death. User Added to Ignore List."
                                    ))

                                time.sleep(COOLDOWN)
                                print(COL.CYAN + "Cooldown Over")
                                print(COL.WHITE + "-" * DASH_AMOUNT)

                        else:  # if ignore is not in response to your bot, prints a false alarm message and does not add name to ignore list

                            print(COL.YELLOW +
                                  "Ignore not a reply. Not adding to list.")
                            print(COL.WHITE + "-" * DASH_AMOUNT)

#Reply Area
                    else:

                        proceed_to_comment = True

                        #list_content(REPLIES)

                        #For Normal Replies
                        rep_triggers = []
                        rep_responses = []
                        for item in list_content(REPLIES):
                            rep_triggers.append(item.split(":")[0])
                            rep_responses.append(item.split(":")[1])

                        word = "not a keyword"
                        for item in rep_triggers:
                            if not (word in rep_triggers):
                                if process_trigger(item) in clean_string(comment.body):
                                    word = item

#For Gray List Replies
                        gray_triggers = []
                        gray_responses = []
                        for item in list_content(GRAY_LIST_REPLIES):
                            gray_triggers.append(item.split(":")[0])
                            gray_responses.append(item.split(":")[1])

                        gray_word = "not a keyword"
                        for item in gray_triggers:
                            if not (gray_word in gray_triggers):
                                if item in clean_string(comment.body):
                                    gray_word = item

#For Response Replies
                        response_triggers = []
                        response_responses = []
                        for item in list_content(RESPONSE_REPLIES):
                            response_triggers.append(item.split(":")[0])
                            response_responses.append(item.split(":")[1])

                        response_word = "not a keyword"
                        for item in response_triggers:
                            if not (response_word in response_triggers):
                                if process_trigger(item) in clean_string(comment.body):
                                    response_word = item

#Normal Reply Stuff
                        if word in rep_triggers and is_graylisted == "no":

                            if word == "kill count" and comment.parent(
                            ).author.name == "clone_trooper_bot":

                                print(COL.CYAN + "Clone Kill Count")

                            else:

                                #print( COL.LIGHT_GRAY + "'Rep' Trigger Called. Line end at 1.")
                                if proceed_to_comment:
                                    print(COL.WHITE + "-" * DASH_AMOUNT)
                                    print(COL.PURPLE + "Normal Reply")
                                    generated_reply = rep_responses[
                                        rep_triggers.index(word)]
                                    comment.reply(
                                        process_output(generated_reply)
                                    )  # Replies to comment with quote
                                    print(COL.GREEN + "User: " + COL.WHITE,
                                          comment.author)
                                    print(COL.GREEN + "User ID: " + COL.WHITE,
                                          comment.author.id)
                                    print(COL.GREEN + "Comment: " + COL.WHITE,
                                          comment.body.lower())
                                    print(COL.GREEN + "Keyword: " + COL.WHITE,
                                          word)
                                    print(COL.GREEN + "Reply: " + COL.WHITE,
                                          str(generated_reply)
                                          )  # Prints random quote from reply
                                    print(
                                        COL.GREEN + "Subreddit: " + COL.WHITE,
                                        comment.subreddit)
                                    print("-" * DASH_AMOUNT)
                                    time.sleep(COOLDOWN)
                                    print(COL.CYAN + "Cooldown Over")
                                    print(COL.WHITE + "-" * DASH_AMOUNT)

#General Reply Stuff
                        elif any(word in comment_lower
                                 for word in list_content(GENERAL_TRIGGERS)
                                 ) and is_graylisted == "no":
                            #print( COL.LIGHT_GRAY + "General Trigger Called. Line end at 2.")
                            # This function rolls a die and returns true on 1
                            print(COL.WHITE + "-" * DASH_AMOUNT)
                            roll_die = random.randint(1, 1)
                            print(COL.BLUE + "Dice Roll: ", roll_die)
                            roll_die_string = str(roll_die)
                            if roll_die_string == "1":

                                with open(GENERAL_REPLIES,
                                          'r',
                                          encoding='utf-8') as tf:

                                    quote_selection = tf.read().splitlines()

                                    print(COL.WHITE + "-" * DASH_AMOUNT)
                                    print(COL.PURPLE + "General Reply")
                                    generated_reply_unadjusted = random.choice(
                                        quote_selection
                                    )  # Fetch random quote from list
                                    #generated_reply = generated_reply_unadjusted.replace("username", author_name)
                                    generated_reply = generated_reply_unadjusted
                                    comment.reply(
                                        process_output(generated_reply)
                                    )  # Replies to comment with random quote
                                    print(COL.GREEN + "User: " + COL.WHITE,
                                          comment.author)
                                    print(COL.GREEN + "User ID: " + COL.WHITE,
                                          comment.author.id)
                                    print(COL.GREEN + "Comment: " + COL.WHITE,
                                          comment.body.lower())
                                    print(COL.GREEN + "Reply: " + COL.WHITE,
                                          str(generated_reply)
                                          )  # Prints random quote from reply
                                    print(
                                        COL.GREEN + "Subreddit: " + COL.WHITE,
                                        comment.subreddit)
                                    print("-" * DASH_AMOUNT)
                                    time.sleep(COOLDOWN)  # Cooldown in seconds
                                    print(COL.CYAN + "Cooldown Over")
                                    print(COL.WHITE + "-" * DASH_AMOUNT)

                            else:  # on a failed die roll, the comment is ignored.
                                print(COL.BLUE + "Roll failed, not replying")
                                print(COL.WHITE + "-" * DASH_AMOUNT)

#Gray List Reply Stuff
                        elif gray_word in gray_triggers and is_graylisted == "yes":
                            #print( COL.LIGHT_GRAY + "Graylist Trigger Called. Line end at 3.")
                            if is_graylisted == "yes":

                                # This function rolls a die and returns true on 1
                                print(COL.WHITE + "-" * DASH_AMOUNT)
                                roll_die = random.randint(1, 10)
                                print(COL.BLUE + "Dice Roll: ", roll_die)
                                roll_die_string = str(roll_die)
                                if roll_die_string == "1":

                                    if gray_word in gray_triggers:
                                        if proceed_to_comment:
                                            print(COL.WHITE +
                                                  "-" * DASH_AMOUNT)
                                            print(COL.PURPLE +
                                                  "Gray List Reply")
                                            generated_reply = gray_responses[
                                                gray_triggers.index(gray_word)]
                                            comment.reply(
                                                process_output(generated_reply)
                                            )  # Replies to comment with quote
                                            print(
                                                COL.GREEN + "User: " +
                                                COL.WHITE, comment.author)
                                            print(
                                                COL.GREEN + "User ID: " +
                                                COL.WHITE, comment.author.id)
                                            print(
                                                COL.GREEN +
                                                "Comment: " + COL.WHITE,
                                                comment.body.lower())
                                            print(
                                                COL.GREEN + "Keyword: " +
                                                COL.WHITE, gray_word)
                                            print(
                                                COL.GREEN + "Reply: " +
                                                COL.WHITE, str(generated_reply)
                                            )  # Prints random quote from reply
                                            print(
                                                COL.GREEN + "Subreddit: " +
                                                COL.WHITE, comment.subreddit)
                                            print("-" * DASH_AMOUNT)
                                            time.sleep(COOLDOWN)
                                            print(COL.CYAN + "Cooldown Over")
                                            print(COL.WHITE +
                                                  "-" * DASH_AMOUNT)

                                else:  # on a failed die roll, the comment is ignored.
                                    print(COL.BLUE +
                                          "Roll failed, not replying")
                                    print(COL.WHITE + "-" * DASH_AMOUNT)

#Response Reply
                        elif comment.parent().author.id == bot_id:
                            if response_word in response_triggers:
                                #print( COL.LIGHT_GRAY + "Responce Trigger Called. Line end at 4.")
                                # This function rolls a die and returns true on 1
                                print(COL.WHITE + "-" * DASH_AMOUNT)
                                roll_die = random.randint(1, 1)
                                print(COL.BLUE + "Dice Roll: ", roll_die)
                                roll_die_string = str(roll_die)
                                if roll_die_string == "1":

                                    if response_word in response_triggers:
                                        if proceed_to_comment:
                                            print(COL.WHITE +
                                                  "-" * DASH_AMOUNT)
                                            print(COL.PURPLE +
                                                  "Response Reply")
                                            generated_reply = response_responses[
                                                response_triggers.index(
                                                    response_word)]
                                            comment.reply(
                                                process_output(generated_reply)
                                            )  # Replies to comment with quote
                                            print(
                                                COL.GREEN + "User: " +
                                                COL.WHITE, comment.author)
                                            print(
                                                COL.GREEN + "User ID: " +
                                                COL.WHITE, comment.author.id)
                                            print(
                                                COL.GREEN +
                                                "Comment: " + COL.WHITE,
                                                comment.body.lower())
                                            print(
                                                COL.GREEN + "Keyword: " +
                                                COL.WHITE, response_word)
                                            print(
                                                COL.GREEN + "Reply: " +
                                                COL.WHITE, str(generated_reply)
                                            )  # Prints random quote from reply
                                            print(
                                                COL.GREEN + "Subreddit: " +
                                                COL.WHITE, comment.subreddit)
                                            print("-" * DASH_AMOUNT)
                                            time.sleep(COOLDOWN)
                                            print(COL.CYAN + "Cooldown Over")
                                            print(COL.WHITE +
                                                  "-" * DASH_AMOUNT)

                                else:  # on a failed die roll, the comment is ignored.
                                    print(COL.BLUE +
                                          "Roll failed, not replying")
                                    print(COL.WHITE + "-" * DASH_AMOUNT)

#On Ignore List
                else:  # If user on ignore list, prints User Ignored, and does not reply to comment
                    if comment.author.id != bot_id:

                        print(COL.WHITE + "-" * DASH_AMOUNT)
                        print(COL.PURPLE + "Ignored Comment")
                        print(COL.GREEN + "User: " + COL.WHITE, comment.author)
                        print(COL.YELLOW + "User ignored")
                        print(COL.WHITE + "-" * DASH_AMOUNT)
                    #else:
                    #print(COL.CYAN + "I don't reply to myself.")

#Failer to reply message and passthrough
    except Exception as e:  #IndexError as i
        print(COL.WHITE + "=" * DASH_AMOUNT)
        print(COL.PURPLE + COL.NEGATIVE + "Reply failed! Passing.", COL.END)
        print("Error: " + COL.RED, e)
        print(COL.WHITE + "=" * DASH_AMOUNT)
        pass
