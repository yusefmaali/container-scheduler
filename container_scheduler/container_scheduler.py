import logging
import time
import timeit
from datetime import datetime, timezone

import docker
import schedule

from container_scheduler.graceful_halt_signal_receiver import GracefulHaltSignalReceiver


class ContainerScheduler:
    """
    schedules structure
    [
        {
            "container": "container_name_1",
            "crontab": "*/1 * * * *"
        }
    ]
    """
    def __init__(self):
        self.logger = logging.getLogger("container_scheduler")
        self.docker_client = docker.from_env()
        self.halt_receiver = GracefulHaltSignalReceiver()

    def add_schedules(self, schedules: list) -> list[str]:
        containers = self.docker_client.containers.list(all=True)

        available_containers = list[str]()
        for c in containers:
            available_containers.append(c.name)

        scheduled_containers = []

        schedule.clear()
        for s in schedules:
            schedule_container = s['container']
            if schedule_container in available_containers:
                self._add_schedule_job(schedule_container, s['crontab'])
                scheduled_containers.append(schedule_container)

        self.logger.info("Scheduled containers: %s", ",".join(scheduled_containers))
        return scheduled_containers

    def _add_schedule_job(self, container_name: str, crontab: str):
        schedule.every().crontab_expression(crontab).do(self.schedule_job, container_name)

    def schedule_job(self, container_name: str):
        self.logger.info("Triggered job for container '%s' at time %s",
                         container_name, datetime.now(tz=timezone.utc).isoformat())

        containers = self.docker_client.containers.list(all=True)
        for c in containers:
            if c.name != container_name:
                continue

            if c.status != "exited":
                self.logger.warning("Should start the container '%s' but its state is invalid (%s). "
                                    "Skipping the current scheduled run", c.name, c.status)
                continue

            timer_start = timeit.default_timer()

            self.logger.info("Starting the container '%s'", c.name)
            c.start()

            self.logger.info("Container '%s' started. Waiting for completion", c.name)
            container_rv = c.wait()

            timer_stop = timeit.default_timer()
            elapsed_time = timer_stop - timer_start

            container_status = container_rv["StatusCode"] if "StatusCode" in container_rv else None
            if container_status == 0:
                self.logger.info("Container '%s' completed its job in %f secs", c.name, elapsed_time)
            else:
                self.logger.warning("Container '%s' failed its job after %f secs with status '%d'",
                                    c.name, elapsed_time, container_status)

    def run(self) -> None:
        self.logger.info("Starting the container scheduler")
        while not self.halt_receiver.graceful_halt_requested:
            schedule.run_pending()
            time.sleep(1)
        self.logger.info("Stopped the container scheduler")

    @classmethod
    def start(cls, schedules: list) -> bool:
        container_scheduler = ContainerScheduler()
        container_scheduler.add_schedules(schedules)
        container_scheduler.run()
        return True


start = ContainerScheduler.start
