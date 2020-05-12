#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging


def get_logger(name):
    """ config logger

    Args:
        name (str): logger name

    Returns:
        object: logger
    """
    # suppress requests library's log
    logging.getLogger("requests").setLevel(logging.WARNING)

    log_fmt = '[%(asctime)s @%(filename)s:%(lineno)d <%(levelname)s>] %(message)s'  # noqa

    logging.basicConfig(
        level=logging.INFO,
        format=log_fmt,
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout
    )

    return logging.getLogger(name)
