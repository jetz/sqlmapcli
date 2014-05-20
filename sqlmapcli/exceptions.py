#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TaskError(Exception):
    pass


class TaskStatusError(TaskError):
    pass


class TaskResultError(TaskError):
    pass


class TaskLogError(TaskError):
    pass
