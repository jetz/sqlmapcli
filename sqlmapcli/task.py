#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-----------------------------------------------------
@post('/scan/<taskid>/start')
@get('/scan/<taskid>/stop')
@get('/scan/<taskid>/kill')
@get('/scan/<taskid>/status')
@get('/scan/<taskid>/data')
-----------------------------------------------------
"""

import time
from urlparse import urljoin

import requests

from .logs import get_logger
from .exceptions import TaskStatusError, TaskResultError, TaskLogError

logger = get_logger('sqlmapcli')


class TaskStatus(object):
    """ Task status constant """

    READY = 'not running'
    RUNNING = 'running'
    FINISHED = 'terminated'


class Task(object):

    def __init__(self, id, options, addr):
        """ Create a task object.

        Args:
            id (str): task id from remote sqlmapapi server.
            options (dict): options used to run task, see
                `curl http://<host>:<port>/option/<taskid>/list`.
            addr (str): remote sqlmapapi server address.
        """
        self.id = id
        self.addr = addr
        self.options = options or {}
        # always store url target in task object
        self.url = self.options.get('url', None)

    def __str__(self):
        return '<Task#%s>' % self.id

    def __repr__(self):
        return str(self)

    def _request(self, path, method='GET'):
        """ Used to request remote sqlmapapi server.

        Args:
            path (str): url path for request.
            method (str): GET or POST for different request.

        Returns:
            dict if successful, None otherwirse.
        """
        try:
            url, method = urljoin(self.addr, path), method.upper()
            if method == 'GET':
                r = requests.get(url).json()
            elif method == 'POST':
                r = requests.post(url, json=self.options).json()
        except requests.RequestException as e:
            logger.error('Fail to %s %s: %s' % (method, path, e))
            return None

        if r.get('success'):
            return r
        else:
            logger.error('Fail to %s %s: %s' % (method, path, r.get('message')))  # noqa
            return None

    def set_option(self, key, value):
        """ Set option for task.

        Options can be set when client create task, or call `set_option`
        after task is created but not start.

        Args:
            key (str): option name.
            value (str): option value.

        Returns:
            Task: for chained call, eg.
            `task.set_option(key, value).set_option(key, value)`.
        """
        self.options[key] = value
        if key == 'url':
            self.url = value
        return self

    def get_option(self, key):
        """ Get task option.

        Args:
            key (str): option name.

        Returns:
            str: option value.
        """
        return self.options.get(key)

    def update_options(self, options):
        """ Update some options at same time.

        Args:
            options (dict): options that to update.
        """
        self.options.update(options)
        if 'url' in options:
            self.url = options.get('url')

    def list_options(self):
        """ Get options that manually set.

        Returns:
            dict: options that user set.
        """
        return self.options

    def start(self, url=None, options=None):
        """ Task start to run.

        Args:
            url (str): target url to scan by sqlmap, this is a shorthand
                for set option with key `url`
            options (Optional[dict]): shorthand, set options for task,
                alternative to `set_option` or `update_options` or set
                options when create task.

        Returns:
            str: engineid, maybe useful in future.

        """
        if options:
            self.update_options(options)

        if url:
            self.url = url
            self.set_option('url', url)

        r = self._request('/scan/%s/start' % self.id, 'POST')
        self.engineid = r.get("engineid") if r else None
        return self.engineid

    def stop(self):
        """ Stop running task.

        Returns:
            bool: True if stop successfully, False otherwise.
        """
        r = self._request('/scan/%s/stop' % self.id)
        return bool(r)

    def kill(self):
        """ Kill running task unconditionally.

        Returns:
            bool: True if Kill successfully, False otherwise.
        """
        r = self._request('/scan/%s/kill' % self.id)
        return bool(r)

    def status(self):
        """ Task currenty status, ready, running or finished.

        Returns:
            dict: include status and retcode.

        Raises:
            TaskStatusError: status exception.
        """
        r = self._request('/scan/%s/status' % self.id)
        if r:
            status, retcode = r.get('status'), r.get('returncode')
            return {'status': status, 'retcode': retcode}
        else:
            raise TaskStatusError("Can't get status")

    @property
    def ready(self):
        """ shorthand for task status.

        Returns:
            bool: True if task is created but not start, False otherwise.
        """
        try:
            r = self.status()
            return r.get('status') == TaskStatus.READY
        except TaskStatusError as e:
            logger.error('Fail to GET task<%s> status: %s', self.id, e)
            return False

    @property
    def running(self):
        """ shorthand for task status.

        Returns:
            bool: True if task start but not finished, False otherwise.
        """
        try:
            r = self.status()
            return r.get('status') == TaskStatus.RUNNING
        except TaskStatusError as e:
            logger.error('Fail to GET task<%s> status: %s', self.id, e)
            return False

    @property
    def finished(self):
        """ shorthand for task status.

        Returns:
            bool: True if task is finished, False otherwise.
        """
        try:
            r = self.status()
            return r.get('status') == TaskStatus.FINISHED
        except TaskStatusError as e:
            logger.error('Fail to GET task<%s> status: %s', self.id, e)
            return False

    def get_result(self):
        """ Get task result.

        Returns:
           dict: task data.

        Raises:
            TaskResultError: task result exception.
        """
        r = self._request('/scan/%s/data' % self.id)
        if r:
            return r.get('data')
        else:
            raise TaskResultError("Can't get result")

    def get_log(self, start=None, end=None):
        """ Get task log.

        Args:
            start (int): start index of log list.
            end (int): end index of log list.

        Returns:
           dict: task log data.

        Raises:
            TaskLogError: task log exception.
        """
        if start and end:
            r = self._request('/scan/%s/log/%s/%s' % (self.id, start, end))
        else:
            r = self._request('/scan/%s/log' % self.id)

        if r:
            return r.get('log')
        else:
            raise TaskLogError("Can't get log")

    def run(self, url=None, options=None, interval=5):
        """ Shorthand for call `start`, `status` and `get_result`

        Args:
            url (str): target url to scan by sqlmap, this is a shorthand
                for set option with key `url`
            options (Optional[dict]): shorthand, set options for task,
                alternative to `set_option` or `update_options` or set
                options when create task.
            interval (int): interval time toquery task status, seconds default.

        Returns:
            dict if successfully, None otherwise.
        """
        self.start(url, options)

        while self.running:
            time.sleep(interval)

        try:
            r = self.get_result()
        except TaskResultError as e:
            logger.error('Fail to GET task<%s> result: %s', self.id, e)
            return None

        return r
