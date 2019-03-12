#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is a part of CostituzioneBot
#
# Copyright (c) 2019 The CostituzioneBot Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
CostituzioneBot - Read the Italian
constitution using a Telegram Bot!
"""

import argparse
import logging
import re
import ujson as json
from html import escape

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram import (InlineQueryResultArticle, ParseMode,
                      InputTextMessageContent)
from telegram.ext import Updater, InlineQueryHandler, MessageHandler, Filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

logger = logging.getLogger(__name__)

keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("📚 Inizia!", switch_inline_query_current_chat="Articolo 1")]]
)

with open("costituzione.json", "r") as file:
    constitution = json.load(file)


def inline_query(_, update: Update):
    """Retrieve an article using the user's inline query, then send it"""
    number = re.search(r'\d+[B]?', update.inline_query.query)

    if number and number.group() in constitution:
        update.inline_query.answer([
            InlineQueryResultArticle(
                id=number.group(),
                title="📘 Articolo " + number.group(),
                input_message_content=InputTextMessageContent(
                    (
                            "🇮🇹 <b>📘 Articolo " + number.group() +
                            "</b> della <i>Costituzione Italiana</i>\n\n" + constitution[number.group()] +
                            (
                                ("\n\n🇮🇹 <b>Continua</b> su <code>" +
                                 number.group() + "B</code>")
                                if number.group() + 'B' in constitution else ''
                            )
                    ), parse_mode=ParseMode.HTML))])

    roman = re.search(r'M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$', update.inline_query.query)

    if roman and roman.group() in constitution:
        update.inline_query.answer([
            InlineQueryResultArticle(
                id=roman.group(),
                title="📒 Transitoria " + roman.group(),
                input_message_content=InputTextMessageContent(
                    (
                            "🇮🇹 <b>📒 Transitoria " + roman.group() +
                            "</b> della <i>Costituzione Italiana</i>\n\n" + constitution[roman.group()]
                    ), parse_mode=ParseMode.HTML))])

    update.inline_query.answer([
        InlineQueryResultArticle(
            id="not_found",
            title="❗️ Non trovato!",
            input_message_content=InputTextMessageContent(
                "🇮🇹 <b>Viva</b> l'<b>Italia</b>!",
                parse_mode=ParseMode.HTML))])


def start(_, update: Update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        ('🇮🇹 <b>Benvenuto</b> <a href="tg://user?id={id}">{name}</a> ' +
         "su @CostituzioneBot!\n" +
         "Puoi utilizzarmi usando l'<b>Inline mode</b> offerta da " +
         "<i>Telegram</i> e digitando il <b>numero</b> dell'articolo " +
         "o della transitoria che stai cercando!").format(
            id=update.message.from_user.id,
            name=escape(
                update.message.from_user.first_name),
        ),
        parse_mode="HTML",
        reply_markup=keyboard)


def main():
    """Start the bot & the program"""
    parser = argparse.ArgumentParser(description=__doc__.rstrip())
    parser.add_argument("-t", "--token", help="The Telegram bot token",
                        required=True, type=str)
    parsed_arguments = parser.parse_args()

    logger.info(__doc__.rstrip())

    updater = Updater(parsed_arguments.token)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, start))
    updater.dispatcher.add_handler(InlineQueryHandler(inline_query))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
