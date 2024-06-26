import logging
from datetime import datetime, timezone


log = logging.getLogger(__name__)


class Timer(object):
    def __init__(
        self,
        name: str,
        in_millis: bool = True,
        init_message: str = '',
        log_warning_step_threshold: int = -1,
        log_warning_total_threshold: int = -1,
    ):
        
        super(Timer, self).__init__()
        self.name = name
        self.init_time = datetime.now(timezone.utc)
        self.prev_time = self.init_time
        self.in_millis = in_millis
        self.log_warning_step_threshold = log_warning_step_threshold
        self.log_warning_total_threshold = log_warning_total_threshold
        self.unit_symbol = 'ms' if in_millis else 's'

        log.info('Started timer "{}" - {}'.format(self.name, init_message))

    def next(self, msg: str):
        current = datetime.now(timezone.utc)
        delta_init = current - self.init_time
        delta_prev = current - self.prev_time

        log_level = logging.INFO
        step_delta = self.__get_time_period(delta_prev)
        if 0 < self.log_warning_step_threshold < step_delta:
            log_level = logging.WARNING

        total_delta = self.__get_time_period(delta_init)
        if 0 < self.log_warning_total_threshold < total_delta:
            log_level = logging.WARNING

        log.log(
            log_level,
            'Timer "{}" , step "{}" - total: {}{} | step: {}{}'.format(
                self.name, msg, total_delta, self.unit_symbol, step_delta, self.unit_symbol
            ),
        )

        self.prev_time = current

    def __get_time_period(self, delta) -> int:
        if self.in_millis:
            return self.__compute_millis(delta)
        else:
            return delta.seconds

    @staticmethod
    def __compute_millis(delta) -> int:
        return int(delta.seconds * 1000 + delta.microseconds / 1000)
