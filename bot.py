#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is a part of CostituzioneBot
#
# Copyright (c) 2017 The CostituzioneBot Authors (see AUTHORS)
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

import logging
import argparse

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

logger.info(__doc__.rstrip())

parser = argparse.ArgumentParser(description=__doc__.rstrip())
parser.add_argument('token',
                    help='The Telegram bot token')
parsed_arguments = parser.parse_args()

if not parsed_arguments.token:
    logger.error('No Bot Token found')


articles = {}
last_number, last_string = '', ''
transitorie = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII',
               'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII']


def get_article(article: str) -> str:
    """It adjusts the given line
    to create the final string.
    It deletes useless space and it sums
    words split in two lines.

    Args:
        article (str): The given article you would like to adjust

    Returns:
        str: The adjusted string
    """

    final_string, current_string, complete_word = '', [], ''
    completing_word = False

    for word in [line.strip() for line in article.split()]:
        print(repr(word))
        if completing_word:
            current_string.append(complete_word + word)
            completing_word, complete_word = False, ''
        elif word.endswith('-'):
            completing_word = True
            complete_word = word.replace('-', '')
        elif (not word.endswith('.') and not word.endswith(';') and not word.endswith(':')) or word == 'n.':
            current_string.append(word)
        else:
            current_string.append(word)
            final_string += ' '.join(current_string) + '\n'
            current_string.clear()

    return final_string.rstrip()


logger.info('Opening \'costituzione.txt\'')
with open('costituzione.txt', 'r') as costituzione:
    logger.info('Starting reading lines...')
    for riga in costituzione.readlines():
        if riga.startswith('ART. ') or riga.rstrip().replace('.', '') in transitorie:
            articles[last_number] = last_string[1:].rstrip()
            logger.info('Added Article/Transitoria %s' % last_number)
            last_number = riga.replace('ART. ', '').replace('.', '').replace('\n', '').rstrip().rstrip('-')
            last_string = ''
        elif str(riga) != '':
            last_string += riga

logger.info('Added Article/Transitoria XVIII')
articles['XVIII'] = last_string
logger.info('Finished creating Articles dictionary!')

del last_number, last_string