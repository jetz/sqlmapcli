#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
[{u'status': 1,
  u'type': 0,
  u'value': [{u'dbms': u'MySQL',
              u'suffix': u'',
              u'clause': [1],
              u'ptype': 1,
              u'dbms_version': [u'> 5.0.11'],
              u'prefix': u'',
              u'place': u'GET',
              u'data': {u'1': {u'comment': u'',
                               u'matchRatio': None,
                               u'title': u'AND boolean-based blind - WHERE or HAVING clause',
                               u'templatePayload': None,
                               u'vector': u'AND [INFERENCE]',
                               u'where': 1,
                               u'payload': u'id=1 AND 6981=6981'},
                        u'3': {u'comment': u'#',
                               u'matchRatio': None,
                               u'title': u'MySQL UNION query (NULL) - 1 to 20 columns',
                               u'templatePayload': None, u'vector': [0, 1, u'#', u'', u'', u'NULL', 1, False],
                               u'where': 1,
                               u'payload': u'id=1 UNION ALL SELECT CONCAT(0x716b726771,0x54577443486b6268564d,0x7165697971)#'},
                        u'5': {u'comment': u'',
                               u'matchRatio': None,
                               u'title': u'MySQL > 5.0.11 AND time-based blind',
                               u'templatePayload': None,
                               u'vector': u'AND [RANDNUM]=IF(([INFERENCE]),SLEEP([SLEEPTIME]),[RANDNUM])',
                               u'where': 1,
                               u'payload': u'id=1 AND SLEEP([SLEEPTIME])'}
                         },
               u'conf': {u'string': None,
                         u'notString': None,
                         u'titles': False,
                         u'regexp': None,
                         u'textOnly': False,
                         u'optimize': False},
               u'parameter': u'id',
               u'os': None}]
}] '''

class Value(object):
    def __init__(self):
        pass

class Data(object):
    def __init__(self):
        pass

class Report(object):
    def __init__(self, r_data):
        raw_data = r_data[0] if r_data else None
        if raw_data:
            self.status = raw_data['status']
            self.type = raw_data['type']
            self.value = Value(raw_data['value'])

    def __str__(self):
        return "<status:%s,type:%s,value:%s>"% (self.status,self.type,type(self.value))
