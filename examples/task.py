#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '..')

import time
from pprint import pprint

from sqlmapcli import client

if __name__ == "__main__":
    admin_id = '10af2eefc9606577bccb75ced1fa74db'
    c = client.Client(admin_id)
    """
    task = c.create_task()
    r = task.run(url='http://testphp.vulnweb.com/artists.php?artist=1')
    pprint(r)
    r = c.list_tasks()
    pprint(r)
    c.delete_task(task.id)
    c.flush_tasks()
    """

    ###################################################

    task = c.create_task()
    task.set_option('url', 'http://testphp.vulnweb.com/artists.php?artist=1')
    task.start()
    r = task.get_result()
    pprint(r)
    while task.running:
        time.sleep(1)
    r = task.get_result()
    pprint(r)
    r = c.list_tasks()
    pprint(r)
    c.delete_task(task.id)
    c.flush_tasks()
