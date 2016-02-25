#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# simagin.mail@yandex.ru


import collections
import html.parser
import os.path
import re
import threading
import urllib.request


import log
import parser


WIKI_ROOT = 'http://simple.wikipedia.org/wiki/'
HTML_PATH = 'html/'
TEXT_PATH = 'text/'
KB_SIZE = 1024


def extractName(url):
    return url.replace(WIKI_ROOT, '')


def namesToUrls(names):
    return list(
        map(lambda name: WIKI_ROOT + name, names)
    )


def load(url):
    response = urllib.request.urlopen(url)
    page = str(response.read(), encoding='utf-8')
    log.debug('Load "%s"... %s %s', url, response.reason, response.getcode())
    return page


def store(lines, path, url):
    with open(path, 'w') as out:
        print(lines, file=out)
    log.debug('Store %s to %s... %i KB', url, path, round(os.path.getsize(path) // KB_SIZE))


def create(master, n):
    return tuple(Slave(master) for i in range(n))


class Slave(threading.Thread):

    def __init__(self, master):
        self._master = master
        threading.Thread.__init__(self, daemon=False)
        log.debug('Create slave thread "%s"', self.name)


    def work(self):
        while True:
            try:
                url = self._master.getTask()
                if not url:
                    break

                page = load(url)
                text, names = parser.parse(page)
                name = extractName(url)
                store(page, HTML_PATH + name, url)
                store(text, TEXT_PATH + name, url)
                self._master.report(url)
                self._master.pushUrls(namesToUrls(names))

            except (urllib.error.URLError, urllib.error.HTTPError) as exception:
                log.error('Load "%s"... %s %s', url, exception.reason, exception.code)

        log.debug('Shutdown thread "%s"...', self.name)


    def run(self):
        try:
            self.work()
        except Exception:
            log.critical('Thread "%s": %s', self.name, exception)
            log.critical(sys.exc_info())
            log.critical('Thread "%s" is forced to terminate...', self.name)
