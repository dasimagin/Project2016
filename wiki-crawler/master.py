#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# simagin.mail@yandex.ru


import time
import threading
import os.path

import log
import slave


INDEX_PATH = '.index'
QUEUE_PATH = '.queue'


def load(name, path):
    if not os.path.isfile(path):
        log.debug('Create empty %s', name)
        return set()
    with open(path, 'r') as lines:
        urls = set(map(lambda line: line.strip(), lines))
        log.debug("Create %s, size = %s", name, len(urls))
        return urls


def store(name, path, urls):
    with open(path, 'w') as out:
        for url in urls:
            print(url, file=out)
    log.debug('Store %s, size = %s', name, len(urls))


class Master():

    def __init__(self, thread_n):
        self._index = load('index', INDEX_PATH)
        self._queue = load('queue', QUEUE_PATH)

        self._slaves = slave.create(self, thread_n)
        self._lock = threading.Lock()

        self._in_progress = set()
        self._shutdown = False
        self._wait_for_task = 1.0


    def run(self):
        log.debug('Starting wiki-crawler...')
        for slave in self._slaves:
            slave.start()

        for slave in self._slaves:
            slave.join()


    def getTask(self):
        while not self._shutdown:
            self._lock.acquire()
            if not self._queue:
                if not self._in_progress:
                    self._lock.release()
                    return
                self._lock.release()
                time.sleep(self._wait_for_task)
                continue
            url = self._queue.pop()
            self._in_progress.add(url)
            self._lock.release()
            return url


    def report(self, url):
        self._lock.acquire()
        self._in_progress.remove(url)
        self._index.add(url)
        self._lock.release()


    def pushUrls(self, urls):
        self._lock.acquire()
        for url in urls:
            if url not in self._index and url not in self._in_progress:
                self._queue.add(url)
        self._lock.release()


    def shutdown(self):
        self._shutdown = True
        log.debug('Shutdown wiki-crawler...')
        for slave in self._slaves:
            slave.join()

        store('idnex', INDEX_PATH, self._index)
        store('queue', QUEUE_PATH, self._queue)
