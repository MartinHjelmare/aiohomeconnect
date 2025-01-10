"""Provide event models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
import json

from httpx_sse import ServerSentEvent
from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin

from aiohomeconnect.model.program import OptionKey
from aiohomeconnect.model.setting import SettingKey
from aiohomeconnect.model.status import StatusKey


@dataclass
class ArrayOfEvents(DataClassJSONMixin):
    """Represent ArrayOfEvents."""

    items: list[Event]


@dataclass
class Event(DataClassJSONMixin):
    """Represent Event."""

    key: EventKey
    timestamp: int
    level: str
    handling: str
    value: str | int | float | bool
    name: str | None = None
    uri: str | None = None
    display_value: str | None = field(
        default=None, metadata=field_options(alias="displayvalue")
    )
    unit: str | None = None


@dataclass
class EventMessage:
    """Represent a server sent event message sent from the Home Connect API."""

    ha_id: str
    type: EventType
    data: ArrayOfEvents

    @classmethod
    def from_server_sent_event(cls, sse: ServerSentEvent) -> EventMessage:
        """Create an EventMessage instance from a server sent event."""
        if not sse.data:
            return cls(
                ha_id=sse.id,
                type=EventType(sse.event),
                data=ArrayOfEvents([]),
            )
        data = json.loads(sse.data)
        if "items" in data:
            events = ArrayOfEvents.from_dict(data)
        else:
            events = ArrayOfEvents([Event.from_dict(data)])
        return cls(
            ha_id=sse.id,
            type=EventType(sse.event),
            data=events,
        )


class EventKey(StrEnum):
    """Represent an event key."""

    @classmethod
    def _missing_(cls, _: object) -> EventKey:
        """Return UNKNOWN for missing keys."""
        return cls.UNKNOWN

    UNKNOWN = "unknown"
    BSH_COMMON_APPLIANCE_CONNECTED = "BSH.Common.Appliance.Connected"
    BSH_COMMON_APPLIANCE_DEPAIRED = "BSH.Common.Appliance.Depaired"
    BSH_COMMON_APPLIANCE_DISCONNECTED = "BSH.Common.Appliance.Disconnected"
    BSH_COMMON_APPLIANCE_PAIRED = "BSH.Common.Appliance.Paired"
    BSH_COMMON_EVENT_ALARM_CLOCK_ELAPSED = "BSH.Common.Event.AlarmClockElapsed"
    BSH_COMMON_EVENT_PROGRAM_ABORTED = "BSH.Common.Event.ProgramAborted"
    BSH_COMMON_EVENT_PROGRAM_FINISHED = "BSH.Common.Event.ProgramFinished"
    BSH_COMMON_OPTION_DURATION = OptionKey.BSH_COMMON_DURATION
    BSH_COMMON_OPTION_ELAPSED_PROGRAM_TIME = "BSH.Common.Option.ElapsedProgramTime"
    BSH_COMMON_OPTION_ESTIMATED_TOTAL_PROGRAM_TIME = (
        "BSH.Common.Option.EstimatedTotalProgramTime"
    )
    BSH_COMMON_OPTION_FINISH_IN_RELATIVE = OptionKey.BSH_COMMON_FINISH_IN_RELATIVE
    BSH_COMMON_OPTION_PROGRAM_PROGRESS = "BSH.Common.Option.ProgramProgress"
    BSH_COMMON_OPTION_REMAINING_PROGRAM_TIME = "BSH.Common.Option.RemainingProgramTime"
    BSH_COMMON_OPTION_REMAINING_PROGRAM_TIME_IS_ESTIMATED = (
        "BSH.Common.Option.RemainingProgramTimeIsEstimated"
    )
    BSH_COMMON_OPTION_START_IN_RELATIVE = OptionKey.BSH_COMMON_START_IN_RELATIVE
    BSH_COMMON_ROOT_ACTIVE_PROGRAM = "BSH.Common.Root.ActiveProgram"
    BSH_COMMON_ROOT_SELECTED_PROGRAM = "BSH.Common.Root.SelectedProgram"
    BSH_COMMON_SETTING_ALARM_CLOCK = SettingKey.BSH_COMMON_ALARM_CLOCK
    BSH_COMMON_SETTING_AMBIENT_LIGHT_BRIGHTNESS = (
        SettingKey.BSH_COMMON_AMBIENT_LIGHT_BRIGHTNESS
    )
    BSH_COMMON_SETTING_AMBIENT_LIGHT_COLOR = SettingKey.BSH_COMMON_AMBIENT_LIGHT_COLOR
    BSH_COMMON_SETTING_AMBIENT_LIGHT_CUSTOM_COLOR = (
        SettingKey.BSH_COMMON_AMBIENT_LIGHT_CUSTOM_COLOR
    )
    BSH_COMMON_SETTING_AMBIENT_LIGHT_ENABLED = (
        SettingKey.BSH_COMMON_AMBIENT_LIGHT_ENABLED
    )
    BSH_COMMON_SETTING_CHILD_LOCK = SettingKey.BSH_COMMON_CHILD_LOCK
    BSH_COMMON_SETTING_LIQUID_VOLUME_UNIT = SettingKey.BSH_COMMON_LIQUID_VOLUME_UNIT
    BSH_COMMON_SETTING_POWER_STATE = SettingKey.BSH_COMMON_POWER_STATE
    BSH_COMMON_SETTING_TEMPERATURE_UNIT = SettingKey.BSH_COMMON_TEMPERATURE_UNIT
    BSH_COMMON_STATUS_BATTERY_CHARGING_STATE = (
        StatusKey.BSH_COMMON_BATTERY_CHARGING_STATE
    )
    BSH_COMMON_STATUS_BATTERY_LEVEL = StatusKey.BSH_COMMON_BATTERY_LEVEL
    BSH_COMMON_STATUS_CHARGING_CONNECTION = StatusKey.BSH_COMMON_CHARGING_CONNECTION
    BSH_COMMON_STATUS_DOOR_STATE = StatusKey.BSH_COMMON_DOOR_STATE
    BSH_COMMON_STATUS_LOCAL_CONTROL_ACTIVE = StatusKey.BSH_COMMON_LOCAL_CONTROL_ACTIVE
    BSH_COMMON_STATUS_OPERATION_STATE = StatusKey.BSH_COMMON_OPERATION_STATE
    BSH_COMMON_STATUS_REMOTE_CONTROL_ACTIVE = StatusKey.BSH_COMMON_REMOTE_CONTROL_ACTIVE
    BSH_COMMON_STATUS_REMOTE_CONTROL_START_ALLOWED = (
        StatusKey.BSH_COMMON_REMOTE_CONTROL_START_ALLOWED
    )
    BSH_COMMON_STATUS_VIDEO_CAMERA_STATE = StatusKey.BSH_COMMON_VIDEO_CAMERA_STATE
    CONSUMER_PRODUCTS_CLEANING_ROBOT_EVENT_DOCKING_STATION_NOT_FOUND = (
        "ConsumerProducts.CleaningRobot.Event.DockingStationNotFound"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_EVENT_EMPTY_DUST_BOX_AND_CLEAN_FILTER = (
        "ConsumerProducts.CleaningRobot.Event.EmptyDustBoxAndCleanFilter"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_EVENT_ROBOT_IS_STUCK = (
        "ConsumerProducts.CleaningRobot.Event.RobotIsStuck"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_OPTION_CLEANING_MODE = (
        OptionKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_MODE
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_OPTION_PROCESS_PHASE = (
        "ConsumerProducts.CleaningRobot.Option.ProcessPhase"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_OPTION_REFERENCE_MAP_ID = (
        OptionKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_REFERENCE_MAP_ID
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_CURRENT_MAP = (
        SettingKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_CURRENT_MAP
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_NAME_OF_MAP_1 = (
        SettingKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_NAME_OF_MAP_1
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_NAME_OF_MAP_2 = (
        SettingKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_NAME_OF_MAP_2
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_NAME_OF_MAP_3 = (
        SettingKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_NAME_OF_MAP_3
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_NAME_OF_MAP_4 = (
        SettingKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_NAME_OF_MAP_4
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_NAME_OF_MAP_5 = (
        SettingKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_NAME_OF_MAP_5
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_STATUS_DUST_BOX_INSERTED = (
        StatusKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_DUST_BOX_INSERTED
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_STATUS_LAST_SELECTED_MAP = (
        StatusKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_LAST_SELECTED_MAP
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_STATUS_LIFTED = (
        StatusKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_LIFTED
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_STATUS_LOST = (
        StatusKey.CONSUMER_PRODUCTS_CLEANING_ROBOT_LOST
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_BEAN_CONTAINER_EMPTY = (
        "ConsumerProducts.CoffeeMaker.Event.BeanContainerEmpty"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_CALC_N_CLEAN_IN10CUPS = (
        "ConsumerProducts.CoffeeMaker.Event.CalcNCleanIn10Cups"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_CALC_N_CLEAN_IN15CUPS = (
        "ConsumerProducts.CoffeeMaker.Event.CalcNCleanIn15Cups"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_CALC_N_CLEAN_IN20CUPS = (
        "ConsumerProducts.CoffeeMaker.Event.CalcNCleanIn20Cups"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_CALC_N_CLEAN_IN5CUPS = (
        "ConsumerProducts.CoffeeMaker.Event.CalcNCleanIn5Cup"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DESCALING_IN_10_CUPS = (
        "ConsumerProducts.CoffeeMaker.Event.DescalingIn10Cups"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DESCALING_IN_15_CUPS = (
        "ConsumerProducts.CoffeeMaker.Event.DescalingIn15Cups"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DESCALING_IN_20_CUPS = (
        "ConsumerProducts.CoffeeMaker.Event.DescalingIn20Cups"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DESCALING_IN_5_CUPS = (
        "ConsumerProducts.CoffeeMaker.Event.DescalingIn5Cups"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DEVICE_CALC_N_CLEAN_BLOCKAGE = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceCalcNCleanBlockage"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DEVICE_CALC_N_CLEAN_OVERDUE = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceCalcNCleanOverdue"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DEVICE_CLEANING_OVERDUE = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceCleaningOverdue"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DEVICE_DESCALING_BLOCKAGE = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceDescalingBlockage"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DEVICE_DESCALING_OVERDUE = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceDescalingOverdue"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DEVICE_SHOULD_BE_CALC_N_CLEANED = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceShouldBeCalcNCleaned"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DEVICE_SHOULD_BE_CLEANED = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceShouldBeCleaned"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DEVICE_SHOULD_BE_DESCALED = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceShouldBeDescaled"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_DRIP_TRAY_FULL = (
        "ConsumerProducts.CoffeeMaker.Event.DripTrayFull"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_KEEP_MILK_TANK_COOL = (
        "ConsumerProducts.CoffeeMaker.Event.KeepMilkTankCool"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EVENT_WATER_TANK_EMPTY = (
        "ConsumerProducts.CoffeeMaker.Event.WaterTankEmpty"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_BEAN_AMOUNT = (
        OptionKey.CONSUMER_PRODUCTS_COFFEE_MAKER_BEAN_AMOUNT
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_BEAN_CONTAINER_SELECTION = (
        OptionKey.CONSUMER_PRODUCTS_COFFEE_MAKER_BEAN_CONTAINER_SELECTION
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_COFFEE_MILK_RATIO = (
        OptionKey.CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_MILK_RATIO
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_COFFEE_TEMPERATURE = (
        OptionKey.CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_TEMPERATURE
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_FILL_QUANTITY = (
        OptionKey.CONSUMER_PRODUCTS_COFFEE_MAKER_FILL_QUANTITY
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_FLOW_RATE = (
        OptionKey.CONSUMER_PRODUCTS_COFFEE_MAKER_FLOW_RATE
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_HOT_WATER_TEMPERATURE = (
        OptionKey.CONSUMER_PRODUCTS_COFFEE_MAKER_HOT_WATER_TEMPERATURE
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_MULTIPLE_BEVERAGES = (
        OptionKey.CONSUMER_PRODUCTS_COFFEE_MAKER_MULTIPLE_BEVERAGES
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_SETTING_CUP_WARMER = (
        SettingKey.CONSUMER_PRODUCTS_COFFEE_MAKER_CUP_WARMER
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_COFFEE = (
        StatusKey.CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_COFFEE
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_COFFEE_AND_MILK = (
        StatusKey.CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_COFFEE_AND_MILK
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_FROTHY_MILK = (
        StatusKey.CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_FROTHY_MILK
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_HOT_MILK = (
        StatusKey.CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_HOT_MILK
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_HOT_WATER = (
        StatusKey.CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_HOT_WATER
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_HOT_WATER_CUPS = (
        StatusKey.CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_HOT_WATER_CUPS
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_MILK = (
        StatusKey.CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_MILK
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_POWDER_COFFEE = (
        StatusKey.CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_POWDER_COFFEE
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_RISTRETTO_ESPRESSO = (
        StatusKey.CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_RISTRETTO_ESPRESSO
    )
    COOKING_COMMON_EVENT_HOOD_GREASE_FILTER_MAX_SATURATION_NEARLY_REACHED = (
        "Cooking.Common.Event.Hood.GreaseFilterMaxSaturationNearlyReached"
    )
    COOKING_COMMON_EVENT_HOOD_GREASE_FILTER_MAX_SATURATION_REACHED = (
        "Cooking.Common.Event.Hood.GreaseFilterMaxSaturationReached"
    )
    COOKING_COMMON_OPTION_HOOD_INTENSIVE_LEVEL = (
        OptionKey.COOKING_COMMON_HOOD_INTENSIVE_LEVEL
    )
    COOKING_COMMON_OPTION_HOOD_VENTING_LEVEL = (
        OptionKey.COOKING_COMMON_HOOD_VENTING_LEVEL
    )
    COOKING_COMMON_SETTING_LIGHTING = SettingKey.COOKING_COMMON_LIGHTING
    COOKING_COMMON_SETTING_LIGHTING_BRIGHTNESS = (
        SettingKey.COOKING_COMMON_LIGHTING_BRIGHTNESS
    )
    COOKING_HOOD_SETTING_COLOR_TEMPERATURE = SettingKey.COOKING_HOOD_COLOR_TEMPERATURE
    COOKING_HOOD_SETTING_COLOR_TEMPERATURE_PERCENT = (
        SettingKey.COOKING_HOOD_COLOR_TEMPERATURE_PERCENT
    )
    COOKING_OVEN_EVENT_PREHEAT_FINISHED = "Cooking.Oven.Event.PreheatFinished"
    COOKING_OVEN_EVENT_REGULAR_PREHEAT_FINISHED = (
        "Cooking.Oven.Event.RegularPreheatFinished"
    )
    COOKING_OVEN_OPTION_FAST_PRE_HEAT = OptionKey.COOKING_OVEN_FAST_PRE_HEAT
    COOKING_OVEN_OPTION_SETPOINT_TEMPERATURE = (
        OptionKey.COOKING_OVEN_SETPOINT_TEMPERATURE
    )
    COOKING_OVEN_OPTION_WARMING_LEVEL = OptionKey.COOKING_OVEN_WARMING_LEVEL
    COOKING_OVEN_SETTING_SABBATH_MODE = SettingKey.COOKING_OVEN_SABBATH_MODE
    DISHCARE_DISHWASHER_EVENT_RINSE_AID_NEARLY_EMPTY = (
        "Dishcare.Dishwasher.Event.RinseAidNearlyEmpty"
    )
    DISHCARE_DISHWASHER_EVENT_SALT_NEARLY_EMPTY = (
        "Dishcare.Dishwasher.Event.SaltNearlyEmpty"
    )
    DISHCARE_DISHWASHER_OPTION_BRILLIANCE_DRY = (
        OptionKey.DISHCARE_DISHWASHER_BRILLIANCE_DRY
    )
    DISHCARE_DISHWASHER_OPTION_ECO_DRY = OptionKey.DISHCARE_DISHWASHER_ECO_DRY
    DISHCARE_DISHWASHER_OPTION_EXTRA_DRY = OptionKey.DISHCARE_DISHWASHER_EXTRA_DRY
    DISHCARE_DISHWASHER_OPTION_HALF_LOAD = OptionKey.DISHCARE_DISHWASHER_HALF_LOAD
    DISHCARE_DISHWASHER_OPTION_HYGIENE_PLUS = OptionKey.DISHCARE_DISHWASHER_HYGIENE_PLUS
    DISHCARE_DISHWASHER_OPTION_INTENSIV_ZONE = (
        OptionKey.DISHCARE_DISHWASHER_INTENSIV_ZONE
    )
    DISHCARE_DISHWASHER_OPTION_SILENCE_ON_DEMAND = (
        OptionKey.DISHCARE_DISHWASHER_SILENCE_ON_DEMAND
    )
    DISHCARE_DISHWASHER_OPTION_VARIO_SPEED_PLUS = (
        OptionKey.DISHCARE_DISHWASHER_VARIO_SPEED_PLUS
    )
    DISHCARE_DISHWASHER_OPTION_ZEOLITE_DRY = OptionKey.DISHCARE_DISHWASHER_ZEOLITE_DRY
    LAUNDRY_CARE_COMMON_OPTION_VARIO_PERFECT = (
        OptionKey.LAUNDRY_CARE_COMMON_VARIO_PERFECT
    )
    LAUNDRY_CARE_DRYER_EVENT_DRYING_PROCESS_FINISHED = (
        "LaundryCare.Dryer.Event.DryingProcessFinished"
    )
    LAUNDRY_CARE_DRYER_OPTION_DRYING_TARGET = OptionKey.LAUNDRY_CARE_DRYER_DRYING_TARGET
    LAUNDRY_CARE_WASHER_EVENT_I_DOS_1_FILL_LEVEL_POOR = (
        "LaundryCare.Washer.Event.IDos1FillLevelPoor"
    )
    LAUNDRY_CARE_WASHER_EVENT_I_DOS_2_FILL_LEVEL_POOR = (
        "LaundryCare.Washer.Event.IDos2FillLevelPoor"
    )
    LAUNDRY_CARE_WASHER_OPTION_I_DOS_1_ACTIVE = (
        OptionKey.LAUNDRY_CARE_WASHER_I_DOS_1_ACTIVE
    )
    LAUNDRY_CARE_WASHER_OPTION_I_DOS_2_ACTIVE = (
        OptionKey.LAUNDRY_CARE_WASHER_I_DOS_2_ACTIVE
    )
    LAUNDRY_CARE_WASHER_OPTION_SPIN_SPEED = OptionKey.LAUNDRY_CARE_WASHER_SPIN_SPEED
    LAUNDRY_CARE_WASHER_OPTION_TEMPERATURE = OptionKey.LAUNDRY_CARE_WASHER_TEMPERATURE
    LAUNDRY_CARE_WASHER_SETTING_I_DOS_1_BASE_LEVEL = (
        SettingKey.LAUNDRY_CARE_WASHER_I_DOS_1_BASE_LEVEL
    )
    LAUNDRY_CARE_WASHER_SETTING_I_DOS_2_BASE_LEVEL = (
        SettingKey.LAUNDRY_CARE_WASHER_I_DOS_2_BASE_LEVEL
    )
    REFRIGERATION_COMMON_SETTING_BOTTLE_COOLER_SETPOINT_TEMPERATURE = (
        SettingKey.REFRIGERATION_COMMON_BOTTLE_COOLER_SETPOINT_TEMPERATURE
    )
    REFRIGERATION_COMMON_SETTING_CHILLER_COMMON_SETPOINT_TEMPERATURE = (
        SettingKey.REFRIGERATION_COMMON_CHILLER_COMMON_SETPOINT_TEMPERATURE
    )
    REFRIGERATION_COMMON_SETTING_CHILLER_LEFT_SETPOINT_TEMPERATURE = (
        SettingKey.REFRIGERATION_COMMON_CHILLER_LEFT_SETPOINT_TEMPERATURE
    )
    REFRIGERATION_COMMON_SETTING_CHILLER_RIGHT_SETPOINT_TEMPERATURE = (
        SettingKey.REFRIGERATION_COMMON_CHILLER_RIGHT_SETPOINT_TEMPERATURE
    )
    REFRIGERATION_COMMON_SETTING_DISPENSER_ENABLED = (
        SettingKey.REFRIGERATION_COMMON_DISPENSER_ENABLED
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_FORCE_FREEZER = (
        SettingKey.REFRIGERATION_COMMON_DOOR_ASSISTANT_FORCE_FREEZER
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_FORCE_FRIDGE = (
        SettingKey.REFRIGERATION_COMMON_DOOR_ASSISTANT_FORCE_FRIDGE
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_FREEZER = (
        SettingKey.REFRIGERATION_COMMON_DOOR_ASSISTANT_FREEZER
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_FRIDGE = (
        SettingKey.REFRIGERATION_COMMON_DOOR_ASSISTANT_FRIDGE
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_TIMEOUT_FREEZER = (
        SettingKey.REFRIGERATION_COMMON_DOOR_ASSISTANT_TIMEOUT_FREEZER
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_TIMEOUT_FRIDGE = (
        SettingKey.REFRIGERATION_COMMON_DOOR_ASSISTANT_TIMEOUT_FRIDGE
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_TRIGGER_FREEZER = (
        SettingKey.REFRIGERATION_COMMON_DOOR_ASSISTANT_TRIGGER_FREEZER
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_TRIGGER_FRIDGE = (
        SettingKey.REFRIGERATION_COMMON_DOOR_ASSISTANT_TRIGGER_FRIDGE
    )
    REFRIGERATION_COMMON_SETTING_ECO_MODE = SettingKey.REFRIGERATION_COMMON_ECO_MODE
    REFRIGERATION_COMMON_SETTING_FRESH_MODE = SettingKey.REFRIGERATION_COMMON_FRESH_MODE
    REFRIGERATION_COMMON_SETTING_LIGHT_EXTERNAL_BRIGHTNESS = (
        SettingKey.REFRIGERATION_COMMON_LIGHT_EXTERNAL_BRIGHTNESS
    )
    REFRIGERATION_COMMON_SETTING_LIGHT_EXTERNAL_POWER = (
        SettingKey.REFRIGERATION_COMMON_LIGHT_EXTERNAL_POWER
    )
    REFRIGERATION_COMMON_SETTING_LIGHT_INTERNAL_BRIGHTNESS = (
        SettingKey.REFRIGERATION_COMMON_LIGHT_INTERNAL_BRIGHTNESS
    )
    REFRIGERATION_COMMON_SETTING_LIGHT_INTERNAL_POWER = (
        SettingKey.REFRIGERATION_COMMON_LIGHT_INTERNAL_POWER
    )
    REFRIGERATION_COMMON_SETTING_SABBATH_MODE = (
        SettingKey.REFRIGERATION_COMMON_SABBATH_MODE
    )
    REFRIGERATION_COMMON_SETTING_VACATION_MODE = (
        SettingKey.REFRIGERATION_COMMON_VACATION_MODE
    )
    REFRIGERATION_COMMON_SETTING_WINE_COMPARTMENT_2_SETPOINT_TEMPERATURE = (
        SettingKey.REFRIGERATION_COMMON_WINE_COMPARTMENT_2_SETPOINT_TEMPERATURE
    )
    REFRIGERATION_COMMON_SETTING_WINE_COMPARTMENT_3_SETPOINT_TEMPERATURE = (
        SettingKey.REFRIGERATION_COMMON_WINE_COMPARTMENT_3_SETPOINT_TEMPERATURE
    )
    REFRIGERATION_COMMON_SETTING_WINE_COMPARTMENT_SETPOINT_TEMPERATURE = (
        SettingKey.REFRIGERATION_COMMON_WINE_COMPARTMENT_SETPOINT_TEMPERATURE
    )
    REFRIGERATION_COMMON_STATUS_DOOR_BOTTLE_COOLER = (
        StatusKey.REFRIGERATION_COMMON_DOOR_BOTTLE_COOLER
    )
    REFRIGERATION_COMMON_STATUS_DOOR_CHILLER = (
        StatusKey.REFRIGERATION_COMMON_DOOR_CHILLER
    )
    REFRIGERATION_COMMON_STATUS_DOOR_CHILLER_COMMON = (
        StatusKey.REFRIGERATION_COMMON_DOOR_CHILLER_COMMON
    )
    REFRIGERATION_COMMON_STATUS_DOOR_CHILLER_LEFT = (
        StatusKey.REFRIGERATION_COMMON_DOOR_CHILLER_LEFT
    )
    REFRIGERATION_COMMON_STATUS_DOOR_CHILLER_RIGHT = (
        StatusKey.REFRIGERATION_COMMON_DOOR_CHILLER_RIGHT
    )
    REFRIGERATION_COMMON_STATUS_DOOR_FLEX_COMPARTMENT = (
        StatusKey.REFRIGERATION_COMMON_DOOR_FLEX_COMPARTMENT
    )
    REFRIGERATION_COMMON_STATUS_DOOR_FREEZER = (
        StatusKey.REFRIGERATION_COMMON_DOOR_FREEZER
    )
    REFRIGERATION_COMMON_STATUS_DOOR_REFRIGERATOR = (
        StatusKey.REFRIGERATION_COMMON_DOOR_REFRIGERATOR
    )
    REFRIGERATION_COMMON_STATUS_DOOR_REFRIGERATOR2 = (
        StatusKey.REFRIGERATION_COMMON_DOOR_REFRIGERATOR_2
    )
    REFRIGERATION_COMMON_STATUS_DOOR_REFRIGERATOR3 = (
        StatusKey.REFRIGERATION_COMMON_DOOR_REFRIGERATOR_3
    )
    REFRIGERATION_COMMON_STATUS_DOOR_WINE_COMPARTMENT = (
        StatusKey.REFRIGERATION_COMMON_DOOR_WINE_COMPARTMENT
    )
    REFRIGERATION_FRIDGE_FREEZER_EVENT_DOOR_ALARM_FREEZER = (
        "Refrigeration.FridgeFreezer.Event.DoorAlarmFreezer"
    )
    REFRIGERATION_FRIDGE_FREEZER_EVENT_DOOR_ALARM_REFRIGERATOR = (
        "Refrigeration.FridgeFreezer.Event.DoorAlarmRefrigerator"
    )
    REFRIGERATION_FRIDGE_FREEZER_EVENT_TEMPERATURE_ALARM_FREEZER = (
        "Refrigeration.FridgeFreezer.Event.TemperatureAlarmFreezer"
    )
    REFRIGERATION_FRIDGE_FREEZER_SETTING_SETPOINT_TEMPERATURE_FREEZER = (
        SettingKey.REFRIGERATION_FRIDGE_FREEZER_SETPOINT_TEMPERATURE_FREEZER
    )
    REFRIGERATION_FRIDGE_FREEZER_SETTING_SETPOINT_TEMPERATURE_REFRIGERATOR = (
        SettingKey.REFRIGERATION_FRIDGE_FREEZER_SETPOINT_TEMPERATURE_REFRIGERATOR
    )
    REFRIGERATION_FRIDGE_FREEZER_SETTING_SUPER_MODE_FREEZER = (
        SettingKey.REFRIGERATION_FRIDGE_FREEZER_SUPER_MODE_FREEZER
    )
    REFRIGERATION_FRIDGE_FREEZER_SETTING_SUPER_MODE_REFRIGERATOR = (
        SettingKey.REFRIGERATION_FRIDGE_FREEZER_SUPER_MODE_REFRIGERATOR
    )


class EventType(StrEnum):
    """Represent an event type."""

    KEEP_ALIVE = "KEEP-ALIVE"
    STATUS = "STATUS"
    EVENT = "EVENT"
    NOTIFY = "NOTIFY"
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    PAIRED = "PAIRED"
    DEPAIRED = "DEPAIRED"
