container-scheduler
===================

A scheduler for docker containers, made easy. Configure the desired schedule per each container and the library ensures
the container will be running at the correct timing.

Usage
-----

To start the scheduler, run the command below

.. code-block:: python

    import container_scheduler

    schedules = [
        {"container": "container_name_1", "crontab": "*/1 * * * *"},
        {"container": "container_name_2", "crontab": "0 4 * * *"}
    ]

    container_scheduler.start(schedules)

The function ``start`` is synchronous and will not return until the scheduler is running. To stop the scheduler
gracefully, you can send a ``SIGTERM`` or a ``SIGKILL`` signal.

The library was originally developed to work in a docker container, acting as a scheduler container for other
containers (take a look at `docker-container-scheduler <https://github.com/yusefmaali/docker-container-scheduler>`_)

Meta
----

Yusef Maali - contact@yusefmaali.net

The scheduling is executed by the `schedule-cronjob <https://github.com/yusefmaali/schedule-cronjob>`_ library, a fork of the
excellent `schedule <https://github.com/dbader/schedule>`_ from Daniel Bader.

Distributed under the MIT license. See `LICENSE.txt <https://github.com/yusefmaali/container-scheduler/blob/master/LICENSE.txt>`_ for more information.

https://github.com/yusefmaali/container-scheduler
