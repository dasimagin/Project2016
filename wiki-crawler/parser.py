#!/usr/bin/python3
# -*- coding: utf-8 -*-
# simagin.mail@yandex.ru - CS


import html.parser
import io
import re
import sys


SPACE_CLEAN_PATTERN = re.compile(r'(\s)(\s+)')

def clean_spaces(text):
    return SPACE_CLEAN_PATTERN.sub(r'\1', text)


WIKI_ARTICLE_URL_PATTERN = re.compile(
  '''^/wiki/[a-zA-Z0-9_\%\.\-\,\']+$'''
)


def is_wiki_article(url):
    return bool(WIKI_ARTICLE_URL_PATTERN.match(url))


class Parser(html.parser.HTMLParser):

    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self._out = io.StringIO()
        self._articles = set()
        self._text_tags = {'p', 'ul'}
        self._content_depth = 0
        self._main_text_tag_depth = 0


    def handle_starttag(self, tag, attrs):
        attrs  = dict(attrs)

        if tag == 'a' and 'href' in attrs:
            url = attrs['href']
            if is_wiki_article(url):
                name = url.strip().replace('/wiki/', '')
                self._articles.add(name)

        if self._content_depth:
            self._content_depth += 1
            if self._main_text_tag_depth or tag in self._text_tags:
                self._main_text_tag_depth += 1
        else:
            if tag == 'div' and 'id' in attrs and attrs['id'] == 'mw-content-text':
                self._content_depth = 1


    def handle_endtag(self, tag):
        if self._content_depth:
            self._content_depth -= 1
        if self._main_text_tag_depth:
            if self._main_text_tag_depth == 1:
                self._out.write('\n')
            self._main_text_tag_depth -= 1


    def handle_data(self, data):
        if self._main_text_tag_depth:
            self._out.write(data)


    def parse(self, page):
        self.feed(page)
        return (
            clean_spaces(self._out.getvalue()),
            list(self._articles)
        )


def parse(page):
    return Parser().parse(page)
