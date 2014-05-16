#!/usr/bin/env python

# RESTful API for sqlmap server
# ---------------------------------------------------------------
#   @get("/task/new")
#   @get("/task/<taskid>/delete")

#   @get("/admin/<taskid>/list")
#   @get("/admin/<taskid>/flush")

#   @post("/scan/<taskid>/start")
#   @get("/scan/<taskid>/stop")
#   @get("/scan/<taskid>/kill")
#   @get("/scan/<taskid>/status")
#   @get("/scan/<taskid>/data")

#   @get("/scan/<taskid>/log/<start>/<end>")
#   @get("/scan/<taskid>/log")

#   @get("/option/<taskid>/list")
#   @post("/option/<taskid>/get")
#   @post("/option/<taskid>/set")

#   @get("/download/<taskid>/<target>/<filename:path>")
# ---------------------------------------------------------------

import sys
import time
import json
import logging
import requests
from report import Report
from threading import Timer
from urlparse import urljoin

logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

RESTAPI_SERVER_HOST = "127.0.0.1"
RESTAPI_SERVER_PORT = 8775


class OperationFailed(Exception):
    def __init__(self, msg="???"):
        self.msg = msg

    def __str__(self):
        return "<OperationFailed:%s>" % self.msg


class SqlmapClient(object):
    """
    Sqlmap REST-JSON API client
    """
    def __init__(self, host=RESTAPI_SERVER_HOST, port=RESTAPI_SERVER_PORT):
        self.addr = "http://%s:%d" % (host, port)
        self.options = dict()
        logger.info("Starting REST-JSON API client to '%s'...\n", self.addr)

    def create_task(self):
        try:
            resp = requests.get(urljoin(self.addr, "/task/new"))
        except requests.RequestException, e:
            raise e
        if resp.status_code == 200:
            r = resp.json()
            if r.get("success", False):
                taskid = r.get("taskid", None)
                logger.info(">>> Create task<%s>", taskid)
                return taskid
            else:
                raise OperationFailed("Failed to create task")
        else:
            raise OperationFailed("Failed to create task, Response<%d>" % resp.status_code)

    def delete_task(self, taskid):
        uri = "".join(["/task/", taskid, "/delete"])
        try:
            resp = requests.get(urljoin(self.addr, uri))
        except requests.RequestException, e:
            raise e
        if resp.status_code == 200:
            r = resp.json()
            if r.get("success", False):
                logger.info(">>> Delete task<%s>", taskid)
                return True
            else:
                raise OperationFailed("Failed to delete task<%s>:%s" % (taskid, r.get("message")))
        else:
            raise OperationFailed("Failed to delete task<%s>, Response<%s>" % (taskid, resp.status_code))

    def admin_list(self, taskid, action):
        uri = "".join(["/admin/", taskid, "/list"])
        try:
            resp = requests.get(urljoin(self.addr, uri))
        except requests.RequestException, e:
            raise e
        if resp.status_code == 200:
            r = resp.json()
            if r.get("success", False):
                ntask, tasks = r.get("tasks_num"), r.get("tasks")
                logger.info("Admin list %d tasks:%s", ntask, tasks)
                return ntask, tasks
            else:
                raise OperationFailed("Failed to list tasks:%s" % r.get("message"))
        else:
            raise OperationFailed("Failed to list tasks, Response<%s>" % resp.status_code)

    def admin_flush(self, taskid):
        uri = "".join(["/admin/", taskid, "/flush"])
        try:
            resp = requests.get(urljoin(self.addr, uri))
        except requests.RequestException, e:
            raise e
        if resp.status_code == 200:
            r = resp.json()
            if r.get("success", False):
                logger.info("Admin flush tasks Success")
                return True
            else:
                raise OperationFailed("Admin flush tasks Failed: %s" % r.get("message"))
        else:
            raise OperationFailed("Admin flush tasks Failed, Response<%s>" % resp.status_code)


    def start_scan(self, taskid):
        uri = "".join(["/scan/", taskid, "/start"])
        headers = {"content-type":"application/json"}

        try:
            resp = requests.post(urljoin(self.addr, uri),
                                 data=json.dumps(self.options),
                                 headers=headers)
        except requests.RequestException, e:
            raise e
        if resp.status_code == 200:
            r = resp.json()
            if r.get("success", False):
                engineid = r.get("engineid")
                logger.info("Start task<%s>, EngineID:%s", taskid, engineid)
                return engineid
            else:
                raise OperationFailed("Failed to start task<%s>:%s" % (taskid, r.get("message")))
        else:
            raise OperationFailed("Failed to start task<%s>,Response<%s>" % (taskid, resp.status_code))

    def stop_scan(self, taskid):
        uri = "".join(["/scan/", taskid, "/stop"])
        try:
            resp = requests.get(urljoin(self.addr, uri))
        except requests.RequestException, e:
            raise e
        if resp.status_code == 200:
            r = resp.json()
            if r.get("success", False):
                logger.info("Stop task<%s>", taskid)
                return True
            else:
                raise OperationFailed("Failed to stop task<%s>:%s" % (taskid, r.get("message")))
        else:
            raise OperationFailed("Failed to stop task<%s>,Response<%s>" % (taskid, resp.status_code))

    def kill_scan(self, taskid):
        uri = "".join(["/scan/", taskid, "/kill"])
        try:
            resp = requests.get(urljoin(self.addr, uri))
        except requests.RequestException, e:
            raise e
        if resp.status_code == 200:
            r = resp.json()
            if r.get("success", False):
                logger.info("Kill task<%s>", taskid)
                return True
            else:
                raise OperationFailed("Failed to kill task<%s>:%s" % (taskid, r.get("message")))
        else:
            raise OperationFailed("Failed to kill task<%s>,Response<%s>" % (taskid, resp.status_code))


    def get_scan_status(self, taskid):
        uri = "".join(["/scan/", taskid, "/status"])
        try:
            resp = requests.get(urljoin(self.addr, uri))
        except requests.RequestException, e:
            raise e
        if resp.status_code == 200:
            r = resp.json()
            if r.get("success", False):
                status, retcode = r.get("status"), r.get("returncode")
                logger.info("Task<%s> status: %s", taskid, status)
                return retcode
            else:
                raise OperationFailed("Failed to get task<%s> status:%s" % (taskid, r.get("message")))
        else:
            raise OperationFailed("Failed to get task<%s> status,Response<%s>" % (taskid, resp.status_code))

    def get_scan_report(self, taskid):
        uri = "".join(["/scan/", taskid, "/status"])
        try:
            resp = requests.get(urljoin(self.addr, uri))
        except requests.RequestException, e:
            raise e
        if resp.status_code == 200:
            r = resp.json()
            if r.get("success", False):
                data, error = r.get("data"), r.get("error")
                logger.info("Get task<%s> report, error: %s", taskid, error)
                return data, error
            else:
                raise OperationFailed("Failed to get task<%s> report:%s" % (taskid, r.get("message")))
        else:
            raise OperationFailed("Failed to get task<%s> report,Response<%s>" % (taskid, resp.status_code))

    def get_scan_log(self, taskid, start=None, end=None):
        raise NotImplementedError()

    def set_option(self, key, value):
        self.options[key] = value
        return self

    def get_option(self, key):
        raise NotImplementedError()

    def list_option(self):
        raise NotImplementedError()

    def download(self):
        raise NotImplementedError()

    def run(self, taskid, url=None, timeout=None):

        if url is not None:
            self.set_option("url", url)

        if timeout:
            timer = Timer(timeout, self.ontimeout, (taskid,))
            timer.start()
        try:
            self.start_scan(taskid)
            retcode = self.get_scan_status(taskid)
            while retcode is None:
                time.sleep(5)
                retcode = self.get_scan_status(taskid)

            if retcode == 0:
                data = self.get_scan_report(taskid)
            else:
                data = None
            if timeout:
                timer.cancel()
        except OperationFailed, e:
            if timeout:
                timer.cancel()
            raise e
        return Report(data)

    def ontimeout(self, taskid):
        if self.get_scan_status(taskid) is None:
            self.kill_scan(taskid)

#######################################################################
if __name__ == '__main__':

    filepath = "result_test.txt"
    f = open(filepath, "r")

    client = SqlmapClient()
    try:
        taskid = client.create_task()
    except Exception, e:
        logger.error("Failed to create task: %s",e)
        sys.exit(1)
    client.set_option("dbms", "mysql")  # .set_option("bulkFile", filepath)
    for url in f.readlines():
        try:
            res = client.run(taskid, url, 20)
        except Exception, e:
            logger.error(e)
            continue

    client.delete_task(taskid)

    f.close()
