#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '..')

from sqlmapcli import client

if __name__ == "__main__":
    admin_id = '10af2eefc9606577bccb75ced1fa74db'
    c = client.Client(admin_id)
    task = c.create_task({'url': 'http://testphp.vulnweb.com/artists.php?artist=1'})  # noqa
    r = c.list_tasks()
    print(r)
    c.delete_task(task.id)
    c.flush_tasks()
