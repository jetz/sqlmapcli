.. image:: https://img.shields.io/pypi/v/sqlmapcli.svg
    :target:  https://pypi.python.org/pypi/sqlmapcli

.. image:: https://img.shields.io/github/release/jetz/sqlmapcli.svg
    :target: http://www.github.com/jetz/sqlmapcli

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://github.com/jetz/sqlmapcli/blob/master/LICENSE


Simplify Your Operations For SqlmapAPI

~~~~~

Intro
======

This is a library used to simplify operations for sqlmapapi, you needn't
manually request remote sqlmapapi server to create task, run task or others 
by HTTP, just a few steps as follow:

.. code:: python

    def test():
        admin_id = '10af2eefc9606577bccb75ced1fa74db'
        c = client.Client(admin_id)
        task = c.create_task()
        r = task.run(url='http://testphp.vulnweb.com/artists.php?artist=1')
        print(r)
        c.delete_task(task.id)


Installation
============

.. code:: bash

    pip install sqlmapcli

or

.. code:: bash
    
    git clone https://www.github.com/jetz/sqlmapapi
    cd sqlmapcli && python setup.py install
    

API
====

Client
------

**class sqlmapcli.Client(admin_id, host='127.0.0.1', port=8775)**

    Call remote api to create/delete/list/flush task. 
    
    ``admin_id`` is used to list & flush tasks, it can be obtained after starting
    a sqlmapapi server by ``sqlmapapi -s``. If use `sqlmap-proxy <https://github.com/jetz/sqlmap-proxy>`_, admin id is what you config.

    
Methods
+++++++

`Client.create_task(options=None)`

    Returns task object. This method will create a task object on client side, and request to 
    create a task on remote server side. 
    
    ``options`` can be achieved by ``curl http://<host>:<port>/option/<taskid>/list``, 
    alternatively, can set options in task object later.


`Client.delete_task(self, taskid)`

    Returns True if successful, False otherwise

    Delete a remote task with it's taskid.


`Client.list_tasks(self)`

    Returns remote tasks info as dict.

    List tasks's info of remote server side. It only requests remote
    sqlmapapi server and gets response, the tasks info are remote info, not 
    local task objects created by ``Client.create_task`` method.


`Client.flush_tasks(self)`

    Returns True if flush successfully, False otherwise

    Flush remote sqlmapapi server's tasks.



Task
------

**class sqlmapcli.Task(id, options, addr)**

    Returns a task object. Generally, ``Client.create_task`` do it for you.
    
    Task id comes from remote sqlmapapi server. 

    All optional ``options`` can list by ``curl http://<host>:<port>/option/<taskid>/list``.

    ``addr`` is remote sqlmapapi server address. 



Attributes
++++++++++

`Task.ready`

    It's True If task is created but not start, False otherwise.


`Task.running`

    It's True if task start but not finished, False otherwise.


`Task.finished`

    It's True if task is finished, False otherwise.


Methods
+++++++

`Task.set_option(key, value)`

    Returns task object for chained call.

    Set option for task. Options can be set when client create task, or call
    ``set_option`` after task is created but not start. This method can be 
    chain-called, like:

    Example:

    .. code:: python

        task.set_option('url', 'http://testphp.vulnweb.com/artists.php?artist=1').set_option('dbms', 'mysql')


`Task.get_option(key)`

    Returns option value.

    If key is not set, raise error


`Task.update_options(options)`
    
    Update bulk options at same time. ``options`` is a dict contains some
    valid values as ``set_option``.


`Task.list_options()`

    Returns all options that you have set.

    NOTICE: not option list in remote server.


`Task.start(url=None, options=None)`

    Returns engineid, maybe useful in future.

    ``url`` is the target to scan by sqlmap, it's a shorthand for setting option
    with key `url`.

    You can pass options here directly or `set_option` or `update_options` in task 
    or pass options when create task, choose one way as you like.

    Example:

    .. code:: python

        def test(admin_id):
            c = client.Client(admin_id)
            try:
                task = c.create_task()
            except:
                return
            task.set_option('url', 'http://testphp.vulnweb.com/artists.php?artist=1')
            task.start()
            while task.running:
                time.sleep(2)
            r = task.get_result()
            pprint(r)
            c.delete_task(task.id)


`Task.stop()`

    Returns True if stop successfully, False otherwise.

    Stop running task.


`Task.kill()`

    Returns True if Kill successfully, False otherwise.

    Kill running task unconditionally.


`Task.status()`

    Returns a dict contains `status` and `retcode`. It may raise TaskStatusError.

    Task's current status, `not running`, `running`, `terminated`.


`Task.get_result()`

    Returns task data as dict. It may raise TaskResultError.


`Task.get_log(start=None, end=None)`

    Returns task log data as dict. It may raise TaskLogError.

    If start & end is None, return all logs, otherwise return logs between start and end index. 


`Task.run(url=None, options=None, interval=5)`

    Returns task result dict if successfully, None otherwise.

    This method is shorthand for call ``start``, ``status`` and ``get_result``.

    ``url`` and ``options`` is same as ``start`` method. 
    
    ``interval`` poll to check task status.

    Example:

    .. code:: python

        def test(admin_id):
            c = client.Client(admin_id)
            try:
                task = c.create_task(options={'url':'http://testphp.vulnweb.com/artists.php?artist=1'})
                task.run()
            except:
                return
            print(r)
            r = c.list_tasks()
            print(r)
            c.delete_task(task.id)
            c.flush_tasks()


TODO
====

- more examples
- download interface
