import asyncio
import pytest

from pyopensprinkler.const import (
    STATION_STATUS_IDLE,
    STATION_STATUS_MANUAL,
    STATION_TYPE_STANDARD,
)
from const import FIRMWARE_VERSION


class TestStation:
    @pytest.mark.asyncio
    async def test_index(self, controller):
        await controller.refresh()
        assert controller.stations[0].index == 0

    @pytest.mark.asyncio
    async def test_is_master(self, controller):
        await controller.refresh()
        assert controller.stations[0].is_master == False

    @pytest.mark.skipif(FIRMWARE_VERSION > 215, reason="only for version 215 and below")
    @pytest.mark.asyncio
    async def test_max_name_length(self, controller):
        await controller.refresh()
        assert controller.stations[0].max_name_length == 16

    @pytest.mark.skipif(
        FIRMWARE_VERSION < 216 and FIRMWARE_VERSION > 218,
        reason="only for version 216 to 218",
    )
    @pytest.mark.asyncio
    async def test_max_name_length(self, controller):
        await controller.refresh()
        assert controller.stations[0].max_name_length == 24

    @pytest.mark.skipif(FIRMWARE_VERSION < 219, reason="only for version 219 and above")
    @pytest.mark.asyncio
    async def test_max_name_length(self, controller):
        await controller.refresh()
        assert controller.stations[0].max_name_length == 32

    @pytest.mark.skipif(FIRMWARE_VERSION < 216, reason="only for version 216 and above")
    @pytest.mark.asyncio
    async def test_special(self, controller):
        await controller.refresh()
        assert controller.stations[0].special == False

    @pytest.mark.skipif(FIRMWARE_VERSION < 216, reason="only for version 216 and above")
    @pytest.mark.asyncio
    async def test_station_type(self, controller):
        await controller.refresh()
        assert controller.stations[0].station_type == STATION_TYPE_STANDARD

    @pytest.mark.asyncio
    async def test_toggle(self, controller):
        await controller.refresh()
        assert controller.stations[0].is_running == False
        assert controller.stations[0].start_time == 0
        assert controller.stations[0].end_time == 0

        await controller.stations[0].toggle()
        assert controller.stations[0].is_running == True
        assert controller.stations[0].status == STATION_STATUS_MANUAL
        assert controller.stations[0].start_time > 0
        assert controller.stations[0].end_time > 0
        assert controller.stations[0].seconds_remaining > 0
        assert controller.stations[0].end_time > controller.stations[0].start_time

        await controller.stations[0].toggle()
        assert controller.stations[0].is_running == False
        assert controller.stations[0].status == STATION_STATUS_IDLE
        assert controller.stations[0].start_time == 0
        assert controller.stations[0].end_time == 0

    @pytest.mark.asyncio
    async def test_enable_disable(self, controller):
        await controller.refresh()
        assert controller.stations[0].enabled == True

        await controller.stations[0].disable()
        assert controller.stations[0].enabled == False

        await controller.stations[0].enable()
        assert controller.stations[0].enabled == True

    @pytest.mark.asyncio
    async def test_set_name(self, controller):
        await controller.refresh()
        await controller.stations[0].set_name("new name")
        assert controller.stations[0].name == "new name"

    @pytest.mark.asyncio
    async def test_set_master_1_operation_enabled(self, controller):
        await controller.refresh()
        await controller.stations[0].set_master_1_operation_enabled(True)
        assert controller.stations[0].master_1_operation_enabled == True

        await controller.stations[0].set_master_1_operation_enabled(False)
        assert controller.stations[0].master_1_operation_enabled == False

    @pytest.mark.asyncio
    async def test_set_master_2_operation_enabled(self, controller):
        await controller.refresh()
        await controller.stations[0].set_master_2_operation_enabled(True)
        assert controller.stations[0].master_2_operation_enabled == True

        await controller.stations[0].set_master_2_operation_enabled(False)
        assert controller.stations[0].master_2_operation_enabled == False

    @pytest.mark.skipif(FIRMWARE_VERSION < 219, reason="only for version 219 and above")
    @pytest.mark.asyncio
    async def test_set_sensor_1_ignored(self, controller):
        await controller.refresh()
        await controller.stations[0].set_sensor_1_ignored(True)
        assert controller.stations[0].sensor_1_ignored == True

        await controller.stations[0].set_sensor_1_ignored(False)
        assert controller.stations[0].sensor_1_ignored == False

    @pytest.mark.skipif(FIRMWARE_VERSION < 219, reason="only for version 219 and above")
    @pytest.mark.asyncio
    async def test_set_sensor_2_ignored(self, controller):
        await controller.refresh()
        await controller.stations[0].set_sensor_2_ignored(True)
        assert controller.stations[0].sensor_2_ignored == True

        await controller.stations[0].set_sensor_2_ignored(False)
        assert controller.stations[0].sensor_2_ignored == False

    @pytest.mark.asyncio
    async def test_set_rain_delay_ignored(self, controller):
        await controller.refresh()
        await controller.stations[0].set_rain_delay_ignored(True)
        assert controller.stations[0].rain_delay_ignored == True

        await controller.stations[0].set_rain_delay_ignored(False)
        assert controller.stations[0].rain_delay_ignored == False

    @pytest.mark.asyncio
    async def test_set_sequential_operation(self, controller):
        await controller.refresh()
        await controller.stations[0].set_sequential_operation(True)
        assert controller.stations[0].sequential_operation == True

        await controller.stations[0].set_sequential_operation(False)
        assert controller.stations[0].sequential_operation == False
