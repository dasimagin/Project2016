#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# simagin.mail@yandex.ru


import argparse
import sys

import log
import master


def parse_argument(argv):
    parser = argparse.ArgumentParser(
        prog = 'wiki-crawler',
        usage = 'wiki-crawler [-h] [--thread-n n] urls...',
        description = 'Download pages from simple english wikipedia.'
    )
    parser.add_argument(
        '--thread-n',
        type = int,
        default = 4,
        help = 'number of threads',
        dest = 'thread_n'
    )
    parser.add_argument(
        '--log',
        default = 'critical',
        help = 'log level',
        choices = ['silence', 'critical', 'error',  'debug'],
        dest = 'log_level'
    )
    parser.add_argument(
        'urls',
        nargs = '*',
        help = 'urls to download'
    )
    return parser.parse_args()


def main():
    args = parse_argument(sys.argv)
    log.config(log.level(args.log_level))

    crawler = master.Master(args.thread_n)
    try:
        crawler.pushUrls(args.urls)
        crawler.run()
    except KeyboardInterrupt:
        log.debug('Force wiki-crawler to stop...')
    except Exception as exception:
        log.critical(exception)
        log.critical(sys.exc_info())
    finally:
        crawler.shutdown()


if __name__ == '__main__':
    main()
