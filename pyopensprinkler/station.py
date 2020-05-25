"""Station module handling /station/ API calls."""

import math


class Station(object):
    """Station class with /station/ API calls."""

    def __init__(self, controller, index):
        """Station class initializer."""
        self._controller = controller
        self._index = index

    def _get_status_variable(self, statusIndex):
        """
        Retrieve station variable
        
        Program status data: each element is a 3-field array that stores the [pid,rem,start] of a station, where
        pid is the program index (0 means none), rem is the remaining water time (in seconds), start is the start time.
        If a station is not running (sbit is 0) but has a non-zero pid, that means the station is in the queue waiting to run.
        """
        return self._controller._state["settings"]["ps"][self._index][statusIndex]

    def _manual_run(self, params=None):
        """Manual station run"""
        if params is None:
            params = {}
        params["sid"] = self._index
        (_, content) = self._controller.request("/cm", params)
        return content["result"]

    def _bit_check(self, bit_property):
        # [254, 255, 255]
        # 254 = all but first station in the first block of 8 have master1 enabled
        # each entry is for next block of 8 stations
        bits = self._controller._state["stations"][bit_property]
        bank = math.floor(self._index / 8)
        bits = list(reversed([int(x) for x in list("{0:08b}".format(bits[bank]))]))
        position = self._index % 8

        return bool(bits[position])

    def run(self, seconds=60):
        """Run station"""
        params = {"en": 1, "t": seconds}
        return self._manual_run(params)

    def stop(self):
        """Stop station"""
        params = {"en": 0}
        return self._manual_run(params)

    def toggle(self):
        """Toggle station"""
        self._controller.refresh()
        if self.is_running:
            return self.stop()
        else:
            return self.run()

    @property
    def name(self):
        """Station name"""
        return self._controller._state["stations"]["snames"][self._index]

    @property
    def index(self):
        """Station index"""
        return self._index

    @property
    def is_running(self):
        """Retrieve is running flag"""
        return bool(self._controller._state["status"]["sn"][self._index])

    @property
    def running_program_id(self):
        """Retrieve seconds remaining"""
        return self._get_status_variable(0)

    @property
    def seconds_remaining(self):
        """Retrieve seconds remaining"""
        return self._get_status_variable(1)

    @property
    def start_time(self):
        """Retrieve start time"""
        return self._get_status_variable(2)

    @property
    def max_name_length(self):
        return self._controller._state["stations"]["maxlen"]

    @property
    def master_1_operation(self):
        return self._bit_check("masop")

    @property
    def master_2_operation(self):
        return self._bit_check("masop2")

    @property
    def rain_delay_ignored(self):
        return self._bit_check("ignore_rain")

    @property
    def sensor_1_ignored(self):
        return self._bit_check("ignore_sn1")

    @property
    def sensor_2_ignored(self):
        return self._bit_check("ignore_sn2")

    @property
    def disabled(self):
        return self._bit_check("stn_dis")

    @property
    def sequential_operation(self):
        return self._bit_check("stn_seq")

    @property
    def special(self):
        return self._bit_check("stn_spe")

    @property
    def station_type(self):
        if not self.special:
            return "standard"

        # TODO: fetch the /je endpoint and return as appropriate

    # TODO: implement setting station options /cs endpoint

    @property
    def status(self):
        """Retrieve status"""
        is_running = self.is_running
        pid = self.running_program_id

        if is_running:
            if pid == 99:
                state = "manual"
            elif pid == 254:
                state = "once_program"
            elif pid == 0:
                state = "idle"
            else:
                state = "program"
        else:
            if pid > 0:
                state = "waiting"
            else:
                state = "idle"

        return state
