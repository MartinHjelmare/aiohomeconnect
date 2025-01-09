"""Provide event models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
import json

from httpx_sse import ServerSentEvent
from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin


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
    BSH_COMMON_OPTION_DURATION = "BSH.Common.Option.Duration"
    BSH_COMMON_OPTION_ELAPSED_PROGRAM_TIME = "BSH.Common.Option.ElapsedProgramTime"
    BSH_COMMON_OPTION_ESTIMATED_TOTAL_PROGRAM_TIME = (
        "BSH.Common.Option.EstimatedTotalProgramTime"
    )
    BSH_COMMON_OPTION_FINISH_IN_RELATIVE = "BSH.Common.Option.FinishInRelative"
    BSH_COMMON_OPTION_PROGRAM_PROGRESS = "BSH.Common.Option.ProgramProgress"
    BSH_COMMON_OPTION_REMAINING_PROGRAM_TIME = "BSH.Common.Option.RemainingProgramTime"
    BSH_COMMON_OPTION_REMAINING_PROGRAM_TIME_IS_ESTIMATED = (
        "BSH.Common.Option.RemainingProgramTimeIsEstimated"
    )
    BSH_COMMON_OPTION_START_IN_RELATIVE = "BSH.Common.Option.StartInRelative"
    BSH_COMMON_ROOT_ACTIVE_PROGRAM = "BSH.Common.Root.ActiveProgram"
    BSH_COMMON_ROOT_SELECTED_PROGRAM = "BSH.Common.Root.SelectedProgram"
    BSH_COMMON_SETTING_ALARM_CLOCK = "BSH.Common.Setting.AlarmClock"
    BSH_COMMON_SETTING_AMBIENT_LIGHT_BRIGHTNESS = (
        "BSH.Common.Setting.AmbientLightBrightness"
    )
    BSH_COMMON_SETTING_AMBIENT_LIGHT_COLOR = "BSH.Common.Setting.AmbientLightColor"
    BSH_COMMON_SETTING_AMBIENT_LIGHT_CUSTOM_COLOR = (
        "BSH.Common.Setting.AmbientLightCustomColor"
    )
    BSH_COMMON_SETTING_AMBIENT_LIGHT_ENABLED = "BSH.Common.Setting.AmbientLightEnabled"
    BSH_COMMON_SETTING_CHILD_LOCK = "BSH.Common.Setting.ChildLock"
    BSH_COMMON_SETTING_LIQUID_VOLUME_UNIT = "BSH.Common.Setting.LiquidVolumeUnit"
    BSH_COMMON_SETTING_POWER_STATE = "BSH.Common.Setting.PowerState"
    BSH_COMMON_SETTING_TEMPERATURE_UNIT = "BSH.Common.Setting.TemperatureUnit"
    BSH_COMMON_STATUS_BATTERY_CHARGING_STATE = "BSH.Common.Status.BatteryChargingState"
    BSH_COMMON_STATUS_BATTERY_LEVEL = "BSH.Common.Status.BatteryLevel"
    BSH_COMMON_STATUS_CHARGING_CONNECTION = "BSH.Common.Status.ChargingConnection"
    BSH_COMMON_STATUS_DOOR_STATE = "BSH.Common.Status.DoorState"
    BSH_COMMON_STATUS_LOCAL_CONTROL_ACTIVE = "BSH.Common.Status.LocalControlActive"
    BSH_COMMON_STATUS_OPERATION_STATE = "BSH.Common.Status.OperationState"
    BSH_COMMON_STATUS_REMOTE_CONTROL_ACTIVE = "BSH.Common.Status.RemoteControlActive"
    BSH_COMMON_STATUS_REMOTE_CONTROL_START_ALLOWED = (
        "BSH.Common.Status.RemoteControlStartAllowed"
    )
    BSH_COMMON_STATUS_VIDEO_CAMERA_STATE = "BSH.Common.Status.Video.CameraState"
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
        "ConsumerProducts.CleaningRobot.Option.CleaningMode"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_OPTION_PROCESS_PHASE = (
        "ConsumerProducts.CleaningRobot.Option.ProcessPhase"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_OPTION_REFERENCE_MAP_ID = (
        "ConsumerProducts.CleaningRobot.Option.ReferenceMapId"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_CURRENT_MAP = (
        "ConsumerProducts.CleaningRobot.Setting.CurrentMap"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_NAME_OF_MAP_1 = (
        "ConsumerProducts.CleaningRobot.Setting.NameOfMap1"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_NAME_OF_MAP_2 = (
        "ConsumerProducts.CleaningRobot.Setting.NameOfMap2"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_NAME_OF_MAP_3 = (
        "ConsumerProducts.CleaningRobot.Setting.NameOfMap3"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_NAME_OF_MAP_4 = (
        "ConsumerProducts.CleaningRobot.Setting.NameOfMap4"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SETTING_NAME_OF_MAP_5 = (
        "ConsumerProducts.CleaningRobot.Setting.NameOfMap5"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_STATUS_DUST_BOX_INSERTED = (
        "ConsumerProducts.CleaningRobot.Status.DustBoxInserted"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_STATUS_LAST_SELECTED_MAP = (
        "ConsumerProducts.CleaningRobot.Status.LastSelectedMap"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_STATUS_LIFTED = (
        "ConsumerProducts.CleaningRobot.Status.Lifted"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_STATUS_LOST = (
        "ConsumerProducts.CleaningRobot.Status.Lost"
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
        "ConsumerProducts.CoffeeMaker.Option.BeanAmount"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_BEAN_CONTAINER_SELECTION = (
        "ConsumerProducts.CoffeeMaker.Option.BeanContainerSelection"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_COFFEE_MILK_RATIO = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeMilkRatio"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_COFFEE_TEMPERATURE = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeTemperature"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_FILL_QUANTITY = (
        "ConsumerProducts.CoffeeMaker.Option.FillQuantity"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_FLOW_RATE = (
        "ConsumerProducts.CoffeeMaker.Option.FlowRate"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_HOT_WATER_TEMPERATURE = (
        "ConsumerProducts.CoffeeMaker.Option.HotWaterTemperature"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_OPTION_MULTIPLE_BEVERAGES = (
        "ConsumerProducts.CoffeeMaker.Option.MultipleBeverages"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_SETTING_CUP_WARMER = (
        "ConsumerProducts.CoffeeMaker.Setting.CupWarmer"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_COFFEE = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterCoffee"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_COFFEE_AND_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterCoffeeAndMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_FROTHY_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterFrothyMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_HOT_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_HOT_WATER = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotWater"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_HOT_WATER_CUPS = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotWaterCups"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_POWDER_COFFEE = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterPowderCoffee"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_STATUS_BEVERAGE_COUNTER_RISTRETTO_ESPRESSO = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterRistrettoEspresso"
    )
    COOKING_COMMON_EVENT_HOOD_GREASE_FILTER_MAX_SATURATION_NEARLY_REACHED = (
        "Cooking.Common.Event.Hood.GreaseFilterMaxSaturationNearlyReached"
    )
    COOKING_COMMON_EVENT_HOOD_GREASE_FILTER_MAX_SATURATION_REACHED = (
        "Cooking.Common.Event.Hood.GreaseFilterMaxSaturationReached"
    )
    COOKING_COMMON_OPTION_HOOD_INTENSIVE_LEVEL = (
        "Cooking.Common.Option.Hood.IntensiveLevel"
    )
    COOKING_COMMON_OPTION_HOOD_VENTING_LEVEL = "Cooking.Common.Option.Hood.VentingLevel"
    COOKING_COMMON_SETTING_LIGHTING = "Cooking.Common.Setting.Lighting"
    COOKING_COMMON_SETTING_LIGHTING_BRIGHTNESS = (
        "Cooking.Common.Setting.LightingBrightness"
    )
    COOKING_HOOD_SETTING_COLOR_TEMPERATURE = "Cooking.Hood.Setting.ColorTemperature"
    COOKING_HOOD_SETTING_COLOR_TEMPERATURE_PERCENT = (
        "Cooking.Hood.Setting.ColorTemperaturePercent"
    )
    COOKING_OVEN_EVENT_PREHEAT_FINISHED = "Cooking.Oven.Event.PreheatFinished"
    COOKING_OVEN_EVENT_REGULAR_PREHEAT_FINISHED = (
        "Cooking.Oven.Event.RegularPreheatFinished"
    )
    COOKING_OVEN_OPTION_FAST_PRE_HEAT = "Cooking.Oven.Option.FastPreHeat"
    COOKING_OVEN_OPTION_SETPOINT_TEMPERATURE = "Cooking.Oven.Option.SetpointTemperature"
    COOKING_OVEN_OPTION_WARMING_LEVEL = "Cooking.Oven.Option.WarmingLevel"
    COOKING_OVEN_SETTING_SABBATH_MODE = "Cooking.Oven.Setting.SabbathMode"
    DISHCARE_DISHWASHER_EVENT_RINSE_AID_NEARLY_EMPTY = (
        "Dishcare.Dishwasher.Event.RinseAidNearlyEmpty"
    )
    DISHCARE_DISHWASHER_EVENT_SALT_NEARLY_EMPTY = (
        "Dishcare.Dishwasher.Event.SaltNearlyEmpty"
    )
    DISHCARE_DISHWASHER_OPTION_BRILLIANCE_DRY = (
        "Dishcare.Dishwasher.Option.BrillianceDry"
    )
    DISHCARE_DISHWASHER_OPTION_ECO_DRY = "Dishcare.Dishwasher.Option.EcoDry"
    DISHCARE_DISHWASHER_OPTION_EXTRA_DRY = "Dishcare.Dishwasher.Option.ExtraDry"
    DISHCARE_DISHWASHER_OPTION_HALF_LOAD = "Dishcare.Dishwasher.Option.HalfLoad"
    DISHCARE_DISHWASHER_OPTION_HYGIENE_PLUS = "Dishcare.Dishwasher.Option.HygienePlus"
    DISHCARE_DISHWASHER_OPTION_INTENSIV_ZONE = "Dishcare.Dishwasher.Option.IntensivZone"
    DISHCARE_DISHWASHER_OPTION_SILENCE_ON_DEMAND = (
        "Dishcare.Dishwasher.Option.SilenceOnDemand"
    )
    DISHCARE_DISHWASHER_OPTION_VARIO_SPEED_PLUS = (
        "Dishcare.Dishwasher.Option.VarioSpeedPlus"
    )
    DISHCARE_DISHWASHER_OPTION_ZEOLITE_DRY = "Dishcare.Dishwasher.Option.ZeoliteDry"
    LAUNDRY_CARE_COMMON_OPTION_VARIO_PERFECT = "LaundryCare.Common.Option.VarioPerfect"
    LAUNDRY_CARE_DRYER_EVENT_DRYING_PROCESS_FINISHED = (
        "LaundryCare.Dryer.Event.DryingProcessFinished"
    )
    LAUNDRY_CARE_DRYER_OPTION_DRYING_TARGET = "LaundryCare.Dryer.Option.DryingTarget"
    LAUNDRY_CARE_WASHER_EVENT_I_DOS_1_FILL_LEVEL_POOR = (
        "LaundryCare.Washer.Event.IDos1FillLevelPoor"
    )
    LAUNDRY_CARE_WASHER_EVENT_I_DOS_2_FILL_LEVEL_POOR = (
        "LaundryCare.Washer.Event.IDos2FillLevelPoor"
    )
    LAUNDRY_CARE_WASHER_OPTION_I_DOS_1_ACTIVE = "LaundryCare.Washer.Option.IDos1Active"
    LAUNDRY_CARE_WASHER_OPTION_I_DOS_2_ACTIVE = "LaundryCare.Washer.Option.IDos2Active"
    LAUNDRY_CARE_WASHER_OPTION_SPIN_SPEED = "LaundryCare.Washer.Option.SpinSpeed"
    LAUNDRY_CARE_WASHER_OPTION_TEMPERATURE = "LaundryCare.Washer.Option.Temperature"
    LAUNDRY_CARE_WASHER_SETTING_I_DOS_1_BASE_LEVEL = (
        "LaundryCare.Washer.Setting.IDos1BaseLevel"
    )
    LAUNDRY_CARE_WASHER_SETTING_I_DOS_2_BASE_LEVEL = (
        "LaundryCare.Washer.Setting.IDos2BaseLevel"
    )
    REFRIGERATION_COMMON_SETTING_BOTTLE_COOLER_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.BottleCooler.SetpointTemperature"
    )
    REFRIGERATION_COMMON_SETTING_CHILLER_COMMON_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.ChillerCommon.SetpointTemperature"
    )
    REFRIGERATION_COMMON_SETTING_CHILLER_LEFT_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.ChillerLeft.SetpointTemperature"
    )
    REFRIGERATION_COMMON_SETTING_CHILLER_RIGHT_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.ChillerRight.SetpointTemperature"
    )
    REFRIGERATION_COMMON_SETTING_DISPENSER_ENABLED = (
        "Refrigeration.Common.Setting.Dispenser.Enabled"
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_FORCE_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantForceFreezer"
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_FORCE_FRIDGE = (
        "Refrigeration.Common.Setting.Door.AssistantForceFridge"
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantFreezer"
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_FRIDGE = (
        "Refrigeration.Common.Setting.Door.AssistantFridge"
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_TIMEOUT_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantTimeoutFreezer"
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_TIMEOUT_FRIDGE = (
        "Refrigeration.Common.Setting.Door.AssistantTimeoutFridge"
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_TRIGGER_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantTriggerFreezer"
    )
    REFRIGERATION_COMMON_SETTING_DOOR_ASSISTANT_TRIGGER_FRIDGE = (
        "Refrigeration.Common.Setting.Door.AssistantTriggerFridge"
    )
    REFRIGERATION_COMMON_SETTING_ECO_MODE = "Refrigeration.Common.Setting.EcoMode"
    REFRIGERATION_COMMON_SETTING_FRESH_MODE = "Refrigeration.Common.Setting.FreshMode"
    REFRIGERATION_COMMON_SETTING_LIGHT_EXTERNAL_BRIGHTNESS = (
        "Refrigeration.Common.Setting.Light.External.Brightness"
    )
    REFRIGERATION_COMMON_SETTING_LIGHT_EXTERNAL_POWER = (
        "Refrigeration.Common.Setting.Light.External.Power"
    )
    REFRIGERATION_COMMON_SETTING_LIGHT_INTERNAL_BRIGHTNESS = (
        "Refrigeration.Common.Setting.Light.Internal.Brightness"
    )
    REFRIGERATION_COMMON_SETTING_LIGHT_INTERNAL_POWER = (
        "Refrigeration.Common.Setting.Light.Internal.Power"
    )
    REFRIGERATION_COMMON_SETTING_SABBATH_MODE = (
        "Refrigeration.Common.Setting.SabbathMode"
    )
    REFRIGERATION_COMMON_SETTING_VACATION_MODE = (
        "Refrigeration.Common.Setting.VacationMode"
    )
    REFRIGERATION_COMMON_SETTING_WINE_COMPARTMENT_2_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.WineCompartment2.SetpointTemperature"
    )
    REFRIGERATION_COMMON_SETTING_WINE_COMPARTMENT_3_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.WineCompartment3.SetpointTemperature"
    )
    REFRIGERATION_COMMON_SETTING_WINE_COMPARTMENT_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.WineCompartment.SetpointTemperature"
    )
    REFRIGERATION_COMMON_STATUS_DOOR_BOTTLE_COOLER = (
        "Refrigeration.Common.Status.Door.BottleCooler"
    )
    REFRIGERATION_COMMON_STATUS_DOOR_CHILLER = (
        "Refrigeration.Common.Status.Door.Chiller"
    )
    REFRIGERATION_COMMON_STATUS_DOOR_CHILLER_COMMON = (
        "Refrigeration.Common.Status.Door.ChillerCommon"
    )
    REFRIGERATION_COMMON_STATUS_DOOR_CHILLER_LEFT = (
        "Refrigeration.Common.Status.Door.ChillerLeft"
    )
    REFRIGERATION_COMMON_STATUS_DOOR_CHILLER_RIGHT = (
        "Refrigeration.Common.Status.Door.ChillerRight"
    )
    REFRIGERATION_COMMON_STATUS_DOOR_FLEX_COMPARTMENT = (
        "Refrigeration.Common.Status.Door.FlexCompartment"
    )
    REFRIGERATION_COMMON_STATUS_DOOR_FREEZER = (
        "Refrigeration.Common.Status.Door.Freezer"
    )
    REFRIGERATION_COMMON_STATUS_DOOR_REFRIGERATOR = (
        "Refrigeration.Common.Status.Door.Refrigerator"
    )
    REFRIGERATION_COMMON_STATUS_DOOR_REFRIGERATOR2 = (
        "Refrigeration.Common.Status.Door.Refrigerator2"
    )
    REFRIGERATION_COMMON_STATUS_DOOR_REFRIGERATOR3 = (
        "Refrigeration.Common.Status.Door.Refrigerator3"
    )
    REFRIGERATION_COMMON_STATUS_DOOR_WINE_COMPARTMENT = (
        "Refrigeration.Common.Status.Door.WineCompartment"
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
        "Refrigeration.FridgeFreezer.Setting.SetpointTemperatureFreezer"
    )
    REFRIGERATION_FRIDGE_FREEZER_SETTING_SETPOINT_TEMPERATURE_REFRIGERATOR = (
        "Refrigeration.FridgeFreezer.Setting.SetpointTemperatureRefrigerator"
    )
    REFRIGERATION_FRIDGE_FREEZER_SETTING_SUPER_MODE_FREEZER = (
        "Refrigeration.FridgeFreezer.Setting.SuperModeFreezer"
    )
    REFRIGERATION_FRIDGE_FREEZER_SETTING_SUPER_MODE_REFRIGERATOR = (
        "Refrigeration.FridgeFreezer.Setting.SuperModeRefrigerator"
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
