
from flask import Flask, request
import telegram.ext
from telebot.credentials import bot_token
from transformers import AutoTokenizer, AutoModelWithLMHead, SummarizationPipeline
from transformers import pipeline
from transformers import BartTokenizer, BartForConditionalGeneration
import torch



# with open("telebot/credentials.py","r") as f:
#     TOKEN= f.read()

def start(update,context):
    update.message.reply_text("hello")

def help(update,context):
    update.message.reply_text("help")

def handle_message(update,context):
    usertext=update.message.text
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    inputs = tokenizer(usertext, return_tensors="pt")

    
    summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=200)
    x=tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    update.message.reply_text(x)


updater = telegram.ext.Updater(bot_token, use_context=True)
disp= updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start",start))
disp.add_handler(telegram.ext.CommandHandler("help",help))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text,handle_message))

updater.start_polling()
updater.idle()

