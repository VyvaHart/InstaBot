from pathlib import Path
from instaloader import *
import time
import instaloader
from telebot import types
from telebot.types import CallbackQuery, InputMediaPhoto, InputMediaVideo, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import Constants
import telebot
import os
from os import listdir
from os.path import isfile, join
from telegram.ext import *
import random
import translation
import data_handler
import json


bot = telebot.TeleBot(Constants.API_KEY)
ig = instaloader.Instaloader(save_metadata=False, post_metadata_txt_pattern='', download_video_thumbnails=False, max_connection_attempts=1)

username = [Constants.login_1, Constants.login_2, Constants.login_3]
password = [Constants.password_1, Constants.password_2, Constants.password_3]
whichPrf = random.randrange(0,3)

emoji = [u"\U0001F44B", u"\u23F3", u"\u270F",
         u"\u0031\uFE0F\u20E3", u"\u0032\u20E3", u"\u0033\u20E3",
         u"\u0034\u20E3", u"\u0035\u20E3", u"\u0036\u20E3",
         u"\U0001F633", u"\U0001F447", u"\U0001F4CE",
         u"\U0001F6CE", u"\U0001F197", u"\u2B07\uFE0F",
         u"\u2705", u"\U0001F1F7\U0001F1FA", u"\U0001F1FA\U0001F1F8",
         u"\U0001F501"]

@bot.message_handler(commands=['start'])
def language(message):
    mark = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item_1 = types.KeyboardButton(text= emoji[16] + ' Russian')#, callback_data="ru")
    item_2 = types.KeyboardButton(text=emoji[17]+ ' English')#, callback_data='uk')
    mark.add(item_1, item_2)
    bot.send_message(message.chat.id, "Choose the language/Выбери язык:", reply_markup=mark)

#@bot.message_handler(commands=['option'])
#def retry_after_no(message):
#    option(message)

def start_text(message):
    lang = WhatLanguage(message)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_0 = types.InlineKeyboardButton(text=emoji[15], callback_data='ok')
    markup.add(item_0)

    if(lang == emoji[16] + ' Russian'): 
        data_handler.Base(message.chat.id, lang, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
        bot.send_message(message.chat.id, 
            "Привет, <b>{.first_name}</b>! {}\n\nЯ помогаю анонимно <u>просматривать</u> и <u>скачивать</u> <b>истории</b>(<b>посты</b>, <b>фото профиля</b>, <b>reels</b>, <b>IGTV</b>) из <b>Instagram</b> без необходимости входа в систему или наличия учетной записи"
                .format(message.from_user, emoji[0]),
                parse_mode='html',
                reply_markup=markup,
        )
    else:
        data_handler.Base(message.chat.id, lang, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
        bot.send_message(message.chat.id, 
            "Hi, <b>{.first_name}</b>! {}\n\nI am created for reading of public Instagram profiles(<b>stories</b>, <b>posts</b>, <b>profile photos</b>, <b>reels</b>, <b>IGTV</b>). You can watch Instagram stories <u>anonymously</u> and <u>quickly</u> without the need to log in or having account"
                .format(message.from_user, emoji[0]),
                parse_mode='html',
                reply_markup=markup
        )         

#@bot.message_handler(content_types=['text'])
#def get_text(message):
#    if message.text == 'окей':
#        bot.register_next_step_handler(message, option)

def WhatLanguage(message):
    with open(data_handler.path, 'r', encoding= 'utf-8') as file:
       data = json.load(file)

    for info in data["People"]:
        if info["id"] == message.chat.id:
            return info["language"]

def option(message):
    time.sleep(.5)
    lang = WhatLanguage(message)
    butt_txt = translation.funk_butts_ru if lang == emoji[16] + ' Russian' else translation.funk_butts_eng

    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton(text= butt_txt[0], callback_data='story')
    item_2 = types.InlineKeyboardButton(text= butt_txt[1], callback_data='profile_pic')
    item_3 = types.InlineKeyboardButton(text= butt_txt[2], callback_data='post')
    item_4 = types.InlineKeyboardButton(text= butt_txt[3], switch_inline_query='')

    #item_6 = types.InlineKeyboardButton(text='Фото профиля', callback_data='profile_pic')

    markup_inline.add(item_1, item_2, item_3, item_4)

    funk_txt = translation.funk_select_ru if lang == emoji[16] + ' Russian' else translation.funk_select_eng

    bot.send_message(message.chat.id, "{} {}".format(funk_txt, emoji[10]),
        parse_mode='html',
        reply_markup=markup_inline
        )

#@bot.callback_query_handler(func= lambda call: call.data == 'ru' or call.data == 'uk')
def lang_choice(message):
    global lang
    lang = message.text
    print(message.text)
    remove_butt = telebot.types.ReplyKeyboardRemove()
    data_handler.Base(message.chat.id, lang, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    if(lang == emoji[16] + ' Russian'): 
        bot.send_message(chat_id=message.chat.id, text="Выбранный язык: {}".format(emoji[16]), reply_markup=remove_butt)
    if(lang == emoji[17]+ ' English'): 
        bot.send_message(chat_id=message.chat.id, text="Chosen language: {}".format(emoji[17]), reply_markup=remove_butt)
    start_text(message)

@bot.message_handler(content_types=['text'])
def get_text(message):
    if(message.text == 'restart'):
        remove_butt = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "..." , reply_markup=remove_butt)
        bot.delete_message(message.chat.id, message.message_id)
        start_text(message)
    if(message.text == emoji[16] + ' Russian'):
        lang_choice(message)
    if(message.text == emoji[17]+ ' English'):
        lang_choice(message)
    #if(message.text == 'yes' or message.text == 'да'):
    #    option(message)
    #if(message.text == 'no' or message.text == 'нет'):
    #    lang = WhatLanguage(message)
    #    endPhrase = translation.end_phrase_ru if lang == emoji[16] + ' Russian' else translation.end_phrase_eng
    #    retry_mark = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    #    retry_butt = types.KeyboardButton('restart')
    #    retry_mark.add(retry_butt)
    #    bot.send_message(message.chat.id, "{} {}".format(endPhrase, emoji[12]),
    #                parse_mode='html',
    #                reply_markup=retry_mark
    #       )

@bot.callback_query_handler(func= lambda call: call.data == 'ok')
def send_ok(call):
    option(call.message)
    bot.answer_callback_query(callback_query_id=call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func= lambda call: call.data == 'yes' )
def send_yes(call):
    option(call.message)
    bot.answer_callback_query(callback_query_id=call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func= lambda call: call.data == 'no')
def send_no(call):
    lang = WhatLanguage(call.message)
    endPhrase = translation.end_phrase_ru if lang == emoji[16] + ' Russian' else translation.end_phrase_eng
    retry_mark = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    retry_butt = types.KeyboardButton('restart')
    retry_mark.add(retry_butt)
    bot.send_message(call.message.chat.id, "{} {}".format(endPhrase, emoji[12]),
                parse_mode='html',
                reply_markup=retry_mark
            )
    
        
    bot.answer_callback_query(callback_query_id=call.id)

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    lang = WhatLanguage(call.message)
    operations = translation.operations_ru if lang == emoji[16] + ' Russian' else translation.operations_eng
    butt_txt = translation.funk_butts_ru if lang == emoji[16] + ' Russian' else translation.funk_butts_eng

    data_handler.Stats(call.data)
    i = 0 #just to know button txt

    if(call.data == 'story'):
        i=0
        bot.send_message(call.message.chat.id, "{} {}".format(operations[0] ,emoji[2]), parse_mode='html')
        bot.register_next_step_handler(call.message, story_pics)

    if(call.data == 'profile_pic'):
        i=1
        bot.send_message(call.message.chat.id, "{} {}".format(operations[0], emoji[2]), parse_mode='html')
        bot.register_next_step_handler(call.message, profile_pic)
        
    if(call.data == 'post'):
        i=2
        bot.send_message(call.message.chat.id, "{} {}".format(operations[1], emoji[11]), parse_mode='html')
        bot.register_next_step_handler(call.message, ig_post)
    
    bot.answer_callback_query(callback_query_id=call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, 
            message_id=call.message.message_id, text="{} {}".format(operations[2], '<b>'+butt_txt[i]+'</b>'), parse_mode='html')

    #if(str(message.text).lower() == "6"):
    #    bot.send_message(message.chat.id, "Для начала работы введите название профиля {}:".format(emoji[2]), parse_mode='html')
    #    bot.register_next_step_handler(message, high_story_cover)

def short_id(message):
    s = '' 
    if(message[26] == 'p'): 
        for x in range(28,39): s+=message[x]
    if(message[26] == 'r'): 
        for x in range(31,42): s+=message[x]
    if(message[26] == 't'): 
        for x in range(29,40): s+=message[x]
    return s

def story_pics(message):

    lang = WhatLanguage(message)
    story_feedback = translation.operations_feedback_ru if lang == emoji[16] + ' Russian' else translation.operations_feedback_eng
    bot.send_message(message.chat.id, "{}".format(story_feedback[0]) + emoji[1])
    global nick
    nick = message.text
    global profile
    whichPrf = random.randrange(0,3)

    try:
        profile = Profile.from_username(ig.context, username=nick) #ProfileNotExistsException
    except(ProfileNotExistsException, QueryReturnedNotFoundException):
        bot.send_message(message.from_user.id, "{}".format(story_feedback[1]))
        option(message)
    else:
        time.sleep(random.randrange(1, 5))
        print(username[whichPrf])
        ig.login(username[whichPrf], password[whichPrf])

        if(profile.has_public_story==False):
            bot.send_message(message.from_user.id, "{}".format(story_feedback[2]))
        elif(profile.is_private==True):
            bot.send_message(message.from_user.id, "{}".format(story_feedback[3]))
        else:
            path = '/home/admin/TeleNinja/ig_ninja/downloads/' + profile.username + '_stories'
            #path = 'C:/Users/KillerVyva/source/repos/Python/tg_bots/ig_ninja/downloads/' + profile.username + '_stories'
            ig.dirname_pattern = path
            ig.download_stories(userids=[profile.userid],filename_target='/tg_bots/ig_ninja/downloads/{}_stories'.format(profile.username))
            files = []
            # r=root, d=directories, f = files
            for r, d, f in os.walk(path):
                for file in f:
                    if '.jpg' in file:
                        files.append(os.path.join(r, file))
                    if '.mp4' in file:
                        files.append(os.path.join(r, file))

            for f in files:
                if '.mp4' in f:
                    bot.send_document(chat_id = message.from_user.id, data=open(f, 'rb'))
                if '.jpg' in f:
                    bot.send_photo(chat_id = message.from_user.id, photo=open(f, 'rb'))
        retry_1(message)

def profile_pic(message):
    lang = WhatLanguage(message)
    pic_feedback = translation.operations_feedback_ru if lang == emoji[16] + ' Russian' else translation.operations_feedback_eng
    bot.send_message(message.chat.id, "{}".format(pic_feedback[0]) + emoji[1])

    global nick
    nick = message.text
    global profile
    
    try:
        profile = Profile.from_username(ig.context, username=nick)
    except(ProfileNotExistsException):
        bot.send_message(message.from_user.id, "{}".format(pic_feedback[1]))
        option(message)
    else:

        path = '/home/admin/TeleNinja/ig_ninja/downloads/' + profile.username
        #path = 'C:/Users/KillerVyva/source/repos/Python/tg_bots/ig_ninja/downloads/' + profile.username
        ig.dirname_pattern = path
        ig.download_profile(profile.username, profile_pic_only=True)
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.jpg' in file:
                    files.append(os.path.join(r, file))
        for f in files:
            if '.jpg' in f:
                bot.send_photo(chat_id = message.from_user.id, photo=open(f, 'rb'))
        retry_1(message)

def ig_post(message):
    lang = WhatLanguage(message)
    post_feedback = translation.operations_feedback_ru if lang == emoji[16] + ' Russian' else translation.operations_feedback_eng

    try:
        short_code = short_id(message.text)
        path = '/home/admin/TeleNinja/ig_ninja/downloads/post_{}'.format(short_code)
        #path = 'C:/Users/KillerVyva/source/repos/Python/tg_bots/ig_ninja/downloads/post_{}'.format(short_code)
        ig.dirname_pattern = path
        time.sleep(random.randrange(1, 5))
        print(username[whichPrf])
        ig.login(username[whichPrf], password[whichPrf])
        post = Post.from_shortcode(ig.context, short_code)
    except(BadResponseException, IndexError):
        bot.send_message(message.from_user.id, "{}".format(post_feedback[4]))
        option(message)
    else:
        bot.send_message(message.chat.id, "{}".format(post_feedback[5]) + emoji[14])
        ig.download_post(post, target='post_{}'.format(short_code))
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.jpg' in file:
                    files.append(os.path.join(r, file))
                if '.mp4' in file:
                    files.append(os.path.join(r, file))
        media_group = []
        for f in files:

                if '.jpg' in f:
                    media_group.append(InputMediaPhoto(media=open(f, 'rb')))
                if '.mp4' in f:
                    media_group.append(InputMediaVideo(media=open(f, 'rb')))
        bot.send_media_group(chat_id = message.from_user.id, media=media_group)
        time.sleep(1)
        retry_1(message)


#def high_story_cover(message):
#    bot.send_message(message.chat.id, "Подождите, это может занять некоторое время... " + emoji[1])
#    global nick
#    nick = message.text
#    global profile
#    profile = Profile.from_username(ig.context, username=nick)
#    #logIn.LogIn
#    path = 'C:/Users/KillerVyva/source/repos/Python/' + profile.username + '_high_cover'

    #for highlight in ig.get_highlights(profile):
    #    if(highlight == '.'):
    #for item in highlight.get_items():
    #    ig.download_storyitem(item, '{}/{}'.format(highlight.owner_username, highlight.title))

    #ig.download_highlight_cover('https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTYwODQyMjM0MDU3MDMy?story_media_id=1822042916351041126&utm_medium=copy_link','{}_high_cover'.format(profile.username))
    #files = []
    ## r=root, d=directories, f = files
    #for r, d, f in os.walk(path):
    #    for file in f:
    #        if '.jpg' in file:
    #            files.append(os.path.join(r, file))
    #        if '.mp4' in file:
    #            files.append(os.path.join(r, file))
    #for f in files:
    #    if '.mp4' in f:
    #        bot.send_document(chat_id = message.from_user.id, data=open(f, 'rb'))
    #    if '.jpg' in f:
    #        bot.send_photo(chat_id = message.from_user.id, photo=open(f, 'rb'))
    #bot.register_next_step_handler(message, retry_1)


def retry_1(message):
    lang = WhatLanguage(message)
    retry_txt = translation.retry_ru if lang == emoji[16] + ' Russian' else translation.retry_eng

    #retry_butt = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    #butt_yes = types.InlineKeyboardButton(text= retry_txt[1])
    #butt_no = types.InlineKeyboardButton(text=retry_txt[2])

    retry_butt = types.InlineKeyboardMarkup(row_width=2)
    butt_yes = types.InlineKeyboardButton(text= retry_txt[1], callback_data= 'yes')
    butt_no = types.InlineKeyboardButton(text=retry_txt[2], callback_data= 'no')
    retry_butt.add(butt_yes, butt_no)
    bot.send_message(message.chat.id, "{}".format(retry_txt[0]), reply_markup=retry_butt)


bot.polling()