from robophery.interface.gpio import GpioModule


class SwitchModule(GpioModule):
    """
    Module for generic GPIO switch.
    """
    DEVICE_NAME = 'switch'

    def __init__(self, *args, **kwargs):
        super(SwitchModule, self).__init__(*args, **kwargs)
        self._pin = self._normalize_pin(kwargs.get('data_pin'))
        self.setup_pin(self._pin, self.GPIO_MODE_IN)
        self._turn_on_count = 0
        self._turn_off_count = 0
        self._runtime = 0
        both_edge = self._interface.GPIO_EVENT_BOTH
        self.add_event_detect(self._pin, both_edge,
                              callback=self._process_event)
        if self.is_high(self._pin):
            self._runtime_start = self._get_time()
            self._state = 1
        else:
            self._runtime_start = None
            self._state = 0

    def _normalize_pin(self, pin):
        value = pin
        return value

    def _process_event(self, pin):
        if self.is_high(pin):
            self._state = 1
            self._turn_on_count += 1
            self._runtime_start = self._get_time()
        else:
            self._update_runtime()
            self._state = 0
            self._turn_off_count += 1
            self._runtime_start = None

    def _update_runtime(self):
        if self._runtime_start is not None:
            now = self._get_time()
            self._runtime = self._runtime + (now - self._runtime_start)
            self._runtime_start = now

    def commit_action(self, action):
        if action == 'read_data':
            return self.read_data()

    def read_data(self):
        """
        Switch status readings.
        """
        read_start = self._get_time()
        self._update_runtime()
        read_stop = self._get_time()
        read_time = (read_stop - read_start) / 4
        data = [
            (self._name, 'state', self._state, read_time),
            (self._name, 'runtime', self._runtime, read_time),
            (self._name, 'turned_on', self._turn_on_count, read_time),
            (self._name, 'turned_off', self._turn_off_count, read_time),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'state': {
                'type': 'gauge',
                'unit': '',
                'range_low': 0,
                'range_high': 1,
                'sensor': self.DEVICE_NAME
            },
            'runtime': {
                'type': 'counter',
                'unit': 's',
                'range_low': 0,
                'range_high': None,
                'sensor': self.DEVICE_NAME
            },
            'turned_on': {
                'type': 'counter',
                'unit': 'times',
                'range_low': 0,
                'range_high': None,
                'sensor': self.DEVICE_NAME
            },
            'turned_off': {
                'type': 'counter',
                'unit': 'times',
                'range_low': 0,
                'range_high': None,
                'sensor': self.DEVICE_NAME
            },
        }
