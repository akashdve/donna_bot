from functools import wraps

from profanity_filter import ProfanityFilter
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, run_async

from constants import ON_DEMAND
from scrapers import get_centennial_updates

pf = ProfanityFilter()


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a smart, because I am Donna!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def button(update: Update, context: CallbackContext):
    query = update.callback_query

    likes = int(str(query.message.reply_markup.inline_keyboard[0][0]["text"])[-1])
    dislikes = abs(int(str(query.message.reply_markup.inline_keyboard[0][1]["text"])[-1]))
    spams = int(str(query.message.reply_markup.inline_keyboard[0][2]["text"])[-1])

    if query.data == "like":
        likes += 1
    elif query.data == "dislike":
        dislikes += 1
    elif query.data == "spam":
        spams += 1

    keyboard = [[InlineKeyboardButton("👍 {}".format(likes), callback_data='like'),
                 InlineKeyboardButton("👎 {}".format(dislikes), callback_data='dislike'),
                 InlineKeyboardButton("🚫 {}".format(spams), callback_data='spam')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_reply_markup(reply_markup)
    # query.edit_message_text(text="Thanks for your feedback!")
    return


def pollify(update: Update, context: CallbackContext):
    context.bot.send_poll(chat_id=update.effective_chat.id, question=" ".join(context.args), options=[":D", ":("],
                          is_anonymous=False)


def welcome(update: Update, context: CallbackContext, new_member):
    text = "Hello {}! Welcome to {}".format(new_member.first_name, update.message.chat.title)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

@run_async
@send_typing_action
def updates(update: Update, context: CallbackContext):
    n_updates = int(context.args[0]) if len(context.args) > 0 else 2
    if "centennial" in str(update.effective_chat.title).lower():
        reply = get_centennial_updates(n_updates)
        reply = ON_DEMAND.format("Centennial") + reply

        if len(reply) > 4096:
            for x in range(0, len(reply), 4096):
                update.message.reply_text(reply[x:x+4096])
        else:
            update.message.reply_text(reply)
    else:
        update.message.reply_text('Requested Resource is under construction. Sorry!')


@send_typing_action
def good_echo(update: Update, context: CallbackContext):
    text = update.message.text
    keyboard = [[InlineKeyboardButton("👍 0", callback_data='like'),
                 InlineKeyboardButton("👎 0", callback_data='dislike'),
                 InlineKeyboardButton("🚫 0", callback_data='spam')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if pf.is_profane(text):
        update.message.reply_text("Please be kind and respectful to others else you will be kicked.")
    else:
        if len(text) >= 250:
            update.message.reply_text(text="How cool is this reply?", reply_markup=reply_markup)
    return


@send_typing_action
def empty_message(update: Update, context: CallbackContext):
    if update.message.new_chat_members:
        for new_member in update.message.new_chat_members:
            return welcome(update, context, new_member)
