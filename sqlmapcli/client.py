#!/usr/bin/env python

"""
-----------------------------------------------------
@get('/task/new')
@get('/task/<taskid>/delete')
@get('/admin/<adminid>/list')
@get('/admin/<adminid>/flush')
@get('/download/<taskid>/target/filename')
-----------------------------------------------------
"""

from urllib.parse import urljoin

import requests

from .task import Task
from .logs import get_logger

logger = get_logger('sqlmapcli')


class Client(object):

    def __init__(self, admin_id, host='127.0.0.1', port=8775):
        """ Call remote api to create/delete/list/flush task.

        Args:
            admin_id (str): admin id for list & flush tasks, this admin id
                shows after starting a sqlmapapi server by `sqlmapapi -s`.
                If use [sqlmap-proxy](https://github.com/jetz/sqlmap-proxy),
                admin id is what you config.
            host (str): sqlmapapi server host
            port (int): sqlmapapi server port
        """

        self.admin_id = admin_id
        self.addr = 'http://%s:%d' % (host, port)

    def _get(self, path):
        """ utils function for request.

        Args:
            path (str): url path for request

        Returns:
            None if something wrong, dict otherwise
        """
        try:
            r = requests.get(urljoin(self.addr, path)).json()
        except requests.RequestException as e:
            logger.error('Fail to GET %s: %s' % (path, e))
            return None

        if r.get('success'):
            return r
        else:
            logger.error('Fail to GET %s: %s' % (path, r.get('message')))
            return None

    def create_task(self, options=None):
        """ Create a task by request remote api.

        This method will create a task object on client side, and request to
        create a task on remote server side.

        Args:
            options (Optional[dict]): options for running sqlmap, option
                list can be achieved by
                `curl http://<host>:<port>/option/<taskid>/list`. If None,
                can set options in task object later.

        Returns:
            Task: task object

        """
        r = self._get('/task/new')
        task = Task(r.get('taskid'), options, self.addr) if r else None
        return task

    def delete_task(self, taskid):
        """ Delete a remote task with it's taskid.

        Args:
            taskid (str): task id

        Returns:
            bool: True if successful, False otherwise
        """
        r = self._get('/task/%s/delete' % taskid)
        return bool(r)

    def list_tasks(self):
        """ List tasks's info of remote server side.

        Note:
            This method only request remote sqlmapapi server and get response,
            the tasks info are remote info, not local task objects created by
            `create_task` method.

        Returns:
            list: remote tasks info

        """

        r = self._get('/admin/%s/list' % self.admin_id)
        if r:
            return r.get('tasks')
        else:
            return []

    def flush_tasks(self):
        """ Flush remote sqlmapapi server's tasks.

        Returns:
            bool: True if flush successfully, False otherwise

        """
        r = self._get('/admin/%s/flush' % self.admin_id)
        return bool(r)

    def download_task(self, taskid, target, filename):
        """ Download a target file after sqlmap handle.

        Args:
            taskid (str): task id
            target (str): url domain name
            filename (str): file's name to download
        """
        raise NotImplementedError
