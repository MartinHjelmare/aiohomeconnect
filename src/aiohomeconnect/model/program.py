"""Provide program models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.json import DataClassJSONMixin

from aiohomeconnect.const import LOGGER


@dataclass
class Program(DataClassJSONMixin):
    """Represent Program."""

    key: ProgramKey | None = None
    name: str | None = None
    options: list[Option] | None = None
    constraints: ProgramConstraints | None = None

    class Config(BaseConfig):
        """Config for mashumaro."""

        omit_none = True


@dataclass
class ProgramConstraints(DataClassJSONMixin):
    """Represent ProgramConstraints."""

    access: str | None = None


@dataclass
class ArrayOfAvailablePrograms(DataClassJSONMixin):
    """Represent ArrayOfAvailablePrograms."""

    programs: list[EnumerateAvailableProgram]


@dataclass
class EnumerateAvailableProgramConstraints(DataClassJSONMixin):
    """Represent EnumerateAvailableProgramConstraints."""

    execution: Execution | None = None


@dataclass
class EnumerateAvailableProgram(DataClassJSONMixin):
    """Represent EnumerateAvailableProgram."""

    key: ProgramKey
    raw_key: str = field(metadata=field_options(alias="key"))
    name: str | None = None
    constraints: EnumerateAvailableProgramConstraints | None = None


@dataclass
class ArrayOfPrograms(DataClassJSONMixin):
    """Represent ArrayOfPrograms."""

    programs: list[EnumerateProgram]
    active: Program | None = None
    selected: Program | None = None


@dataclass
class EnumerateProgramConstraints(DataClassJSONMixin):
    """Represent EnumerateProgramConstraints."""

    available: bool | None = None
    execution: Execution | None = None


@dataclass
class EnumerateProgram(DataClassJSONMixin):
    """Represent EnumerateProgram."""

    key: ProgramKey
    raw_key: str = field(metadata=field_options(alias="key"))
    name: str | None = None
    constraints: EnumerateProgramConstraints | None = None


class Execution(StrEnum):
    """Execution right of the program."""

    NONE = "none"
    SELECT_ONLY = "selectonly"
    START_ONLY = "startonly"
    SELECT_AND_START = "selectandstart"


@dataclass
class ProgramDefinition(DataClassJSONMixin):
    """Represent ProgramDefinition."""

    key: ProgramKey
    name: str | None = None
    options: list[ProgramDefinitionOption] | None = None


@dataclass
class ProgramDefinitionConstraints(DataClassJSONMixin):
    """Represent ProgramDefinitionConstraints."""

    min: int | None = None
    max: int | None = None
    step_size: int | None = field(
        default=None, metadata=field_options(alias="stepsize")
    )
    allowed_values: list[str | None] | None = field(
        default=None, metadata=field_options(alias="allowedvalues")
    )
    display_values: list[str | None] | None = field(
        default=None, metadata=field_options(alias="displayvalues")
    )
    default: Any | None = None
    live_update: bool | None = field(
        default=None, metadata=field_options(alias="liveupdate")
    )


@dataclass
class ProgramDefinitionOption(DataClassJSONMixin):
    """Represent ProgramDefinitionOption."""

    key: OptionKey
    type: str
    name: str | None = None
    unit: str | None = None
    constraints: ProgramDefinitionConstraints | None = None


@dataclass
class Option(DataClassJSONMixin):
    """Represent Option."""

    key: OptionKey
    value: Any
    name: str | None = None
    display_value: str | None = field(
        default=None, metadata=field_options(alias="displayvalue")
    )
    unit: str | None = None

    class Config(BaseConfig):
        """Config for mashumaro."""

        omit_none = True


@dataclass
class ArrayOfOptions(DataClassJSONMixin):
    """List of options."""

    options: list[Option]


class OptionKey(StrEnum):
    """Represent an option key."""

    @classmethod
    def _missing_(cls, value: object) -> OptionKey:
        """Return UNKNOWN for missing keys."""
        LOGGER.debug("Unknown option key: %s", value)
        return cls.UNKNOWN

    UNKNOWN = "unknown"
    BSH_COMMON_BASE_PROGRAM = "BSH.Common.Option.BaseProgram"
    BSH_COMMON_CURRENT_STEP_REMAINING_TIME = (
        "BSH.Common.Option.CurrentStepRemainingTime"
    )
    BSH_COMMON_DURATION = "BSH.Common.Option.Duration"
    BSH_COMMON_ELAPSED_PROGRAM_TIME = "BSH.Common.Option.ElapsedProgramTime"
    BSH_COMMON_ENERGY_FORECAST = "BSH.Common.Option.EnergyForecast"
    BSH_COMMON_ESTIMATED_TOTAL_PROGRAM_TIME = (
        "BSH.Common.Option.EstimatedTotalProgramTime"
    )
    BSH_COMMON_FINISH_IN_RELATIVE = "BSH.Common.Option.FinishInRelative"
    BSH_COMMON_PROGRAM_NAME = "BSH.Common.Option.ProgramName"
    BSH_COMMON_PROGRAM_PROGRESS = "BSH.Common.Option.ProgramProgress"
    BSH_COMMON_REMAINING_PROGRAM_TIME = "BSH.Common.Option.RemainingProgramTime"
    BSH_COMMON_REMAINING_PROGRAM_TIME_AUTO_COUNTING = (
        "BSH.Common.Option.RemainingProgramTime.AutoCounting"
    )
    BSH_COMMON_REMAINING_PROGRAM_TIME_ESTIMATION_STATE = (
        "BSH.Common.Option.RemainingProgramTimeEstimationState"
    )
    BSH_COMMON_REMAINING_PROGRAM_TIME_IS_ESTIMATED = (
        "BSH.Common.Option.RemainingProgramTimeIsEstimated"
    )
    BSH_COMMON_SMART_ENERGY_SERVICE_SMART_START_ENABLED = (
        "BSH.Common.Option.SmartEnergyService.SmartStartEnabled"
    )
    BSH_COMMON_START_IN_RELATIVE = "BSH.Common.Option.StartInRelative"
    BSH_COMMON_WATER_FORECAST = "BSH.Common.Option.WaterForecast"
    CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_MODE = (
        "ConsumerProducts.CleaningRobot.Option.CleaningMode"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_PROCESS_PHASE = (
        "ConsumerProducts.CleaningRobot.Option.ProcessPhase"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_REFERENCE_MAP_ID = (
        "ConsumerProducts.CleaningRobot.Option.ReferenceMapId"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SUCTION_POWER = (
        "ConsumerProducts.CleaningRobot.Option.SuctionPower"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_AROMA_SELECT = (
        "ConsumerProducts.CoffeeMaker.Option.AromaSelect"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEAN_AMOUNT = (
        "ConsumerProducts.CoffeeMaker.Option.BeanAmount"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEAN_CONTAINER_SELECTION = (
        "ConsumerProducts.CoffeeMaker.Option.BeanContainerSelection"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_SIZE = (
        "ConsumerProducts.CoffeeMaker.Option.BeverageSize"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGES_REMAINING = (
        "ConsumerProducts.CoffeeMaker.Option.BeveragesRemaining"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COARSNESS = (
        "ConsumerProducts.CoffeeMaker.Option.Coarsness"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COARSNESS_RECOMMENDATION = (
        "ConsumerProducts.CoffeeMaker.Option.Coarsness.Recommendation"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_MILK_RATIO = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeMilkRatio"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_STRENGTH = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeStrength"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_STRENGTH_RECOMMENDATION = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeStrength.Recommendation"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_TEMPERATURE = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeTemperature"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_TEMPERATURE_RECOMMENDATION = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeTemperature.Recommendation"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_FILL_QUANTITY = (
        "ConsumerProducts.CoffeeMaker.Option.FillQuantity"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_FILL_QUANTITY_RECOMMENDATION = (
        "ConsumerProducts.CoffeeMaker.Option.FillQuantity.Recommendation"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_FLOW_RATE = (
        "ConsumerProducts.CoffeeMaker.Option.FlowRate"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_FLOW_RATE_RECOMMENDATION = (
        "ConsumerProducts.CoffeeMaker.Option.FlowRate.Recommendation"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_HOT_WATER_TEMPERATURE = (
        "ConsumerProducts.CoffeeMaker.Option.HotWaterTemperature"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MULTIPLE_BEVERAGES = (
        "ConsumerProducts.CoffeeMaker.Option.MultipleBeverages"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_SHOT_COUNT = (
        "ConsumerProducts.CoffeeMaker.Option.Shot.Count"
    )
    COOKING_COMMON_HOOD_BOOST = "Cooking.Common.Option.Hood.Boost"
    COOKING_COMMON_HOOD_INTENSIVE_LEVEL = "Cooking.Common.Option.Hood.IntensiveLevel"
    COOKING_COMMON_HOOD_VENTING_LEVEL = "Cooking.Common.Option.Hood.VentingLevel"
    COOKING_OVEN_AIR_EXCHANGE = "Cooking.Oven.Option.AirExchange"
    COOKING_OVEN_CAVITY_SELECTOR = "Cooking.Oven.Option.CavitySelector"
    COOKING_OVEN_FAST_PRE_HEAT = "Cooking.Oven.Option.FastPreHeat"
    COOKING_OVEN_HEATUP_PROGRESS = "Cooking.Oven.Option.HeatupProgress"
    COOKING_OVEN_LEVEL = "Cooking.Oven.Option.Level"
    COOKING_OVEN_MEAT_PROBE_TEMPERATURE_V2 = (
        "Cooking.Oven.Option.MeatProbeTemperatureV2"
    )
    COOKING_OVEN_MICROWAVE_POWER = "Cooking.Oven.Option.MicrowavePower"
    COOKING_OVEN_PYROLYSIS_LEVEL = "Cooking.Oven.Option.PyrolysisLevel"
    COOKING_OVEN_SETPOINT_TEMPERATURE = "Cooking.Oven.Option.SetpointTemperature"
    COOKING_OVEN_STEAM_ASSIST_LEVEL = "Cooking.Oven.Option.SteamAssistLevel"
    COOKING_OVEN_STEAM_BOOST = "Cooking.Oven.Option.SteamBoost"
    COOKING_OVEN_WARMING_LEVEL = "Cooking.Oven.Option.WarmingLevel"
    DISHCARE_DISHWASHER_BRILLIANCE_DRY = "Dishcare.Dishwasher.Option.BrillianceDry"
    DISHCARE_DISHWASHER_DELICATE_BASKET = "Dishcare.Dishwasher.Option.DelicateBasket"
    DISHCARE_DISHWASHER_ECO_DRY = "Dishcare.Dishwasher.Option.EcoDry"
    DISHCARE_DISHWASHER_ENERGY_SAFE = "Dishcare.Dishwasher.Option.EnergySafe"
    DISHCARE_DISHWASHER_EXTRA_DRY = "Dishcare.Dishwasher.Option.ExtraDry"
    DISHCARE_DISHWASHER_EXTRA_RINSE = "Dishcare.Dishwasher.Option.ExtraRinse"
    DISHCARE_DISHWASHER_FLEX_SPRAY_BACK_LEFT = (
        "Dishcare.Dishwasher.Option.FlexSpray.BackLeft"
    )
    DISHCARE_DISHWASHER_FLEX_SPRAY_BACK_RIGHT = (
        "Dishcare.Dishwasher.Option.FlexSpray.BackRight"
    )
    DISHCARE_DISHWASHER_FLEX_SPRAY_FRONT_LEFT = (
        "Dishcare.Dishwasher.Option.FlexSpray.FrontLeft"
    )
    DISHCARE_DISHWASHER_FLEX_SPRAY_FRONT_RIGHT = (
        "Dishcare.Dishwasher.Option.FlexSpray.FrontRight"
    )
    DISHCARE_DISHWASHER_FLEX_SPRAY_TYPE = "Dishcare.Dishwasher.Option.FlexSpray.Type"
    DISHCARE_DISHWASHER_HALF_LOAD = "Dishcare.Dishwasher.Option.HalfLoad"
    DISHCARE_DISHWASHER_HOLIDAY_MODE = "Dishcare.Dishwasher.Option.HolidayMode"
    DISHCARE_DISHWASHER_HYGIENE_PLUS = "Dishcare.Dishwasher.Option.HygienePlus"
    DISHCARE_DISHWASHER_INTENSIV_ZONE = "Dishcare.Dishwasher.Option.IntensivZone"
    DISHCARE_DISHWASHER_LEARNING_DISHWASHER_CLEANING_LEVEL = (
        "Dishcare.Dishwasher.Option.LearningDishwasher.CleaningLevel"
    )
    DISHCARE_DISHWASHER_LEARNING_DISHWASHER_DRYING_LEVEL = (
        "Dishcare.Dishwasher.Option.LearningDishwasher.DryingLevel"
    )
    DISHCARE_DISHWASHER_LEARNING_DISHWASHER_DURATION_LEVEL = (
        "Dishcare.Dishwasher.Option.LearningDishwasher.DurationLevel"
    )
    DISHCARE_DISHWASHER_PRETREATMENT = "Dishcare.Dishwasher.Option.Pretreatment"
    DISHCARE_DISHWASHER_SANITATION_UC = "Dishcare.Dishwasher.Option.SanitationUC"
    DISHCARE_DISHWASHER_SILENCE_ON_DEMAND = "Dishcare.Dishwasher.Option.SilenceOnDemand"
    DISHCARE_DISHWASHER_STORAGE_FUNCTION = "Dishcare.Dishwasher.Option.StorageFunction"
    DISHCARE_DISHWASHER_TURBO = "Dishcare.Dishwasher.Option.Turbo"
    DISHCARE_DISHWASHER_VARIO_SPEED = "Dishcare.Dishwasher.Option.VarioSpeed"
    DISHCARE_DISHWASHER_VARIO_SPEED_PLUS = "Dishcare.Dishwasher.Option.VarioSpeedPlus"
    DISHCARE_DISHWASHER_ZEOLITE_DRY = "Dishcare.Dishwasher.Option.ZeoliteDry"
    HEATING_VENTILATION_AIR_CONDITIONING_AIR_CONDITIONER_FAN_SPEED_MODE = (
        "HeatingVentilationAirConditioning.AirConditioner.Option.FanSpeedMode"
    )
    HEATING_VENTILATION_AIR_CONDITIONING_AIR_CONDITIONER_FAN_SPEED_PERCENTAGE = (
        "HeatingVentilationAirConditioning.AirConditioner.Option.FanSpeedPercentage"
    )
    HEATING_VENTILATION_AIR_CONDITIONING_AIR_CONDITIONER_SETPOINT_TEMPERATURE = (
        "HeatingVentilationAirConditioning.AirConditioner.Option.SetpointTemperature"
    )
    LAUNDRY_CARE_COMMON_LOAD_RECOMMENDATION = (
        "LaundryCare.Common.Option.LoadRecommendation"
    )
    LAUNDRY_CARE_COMMON_LOW_TEMPERATURE_HYGIENE = (
        "LaundryCare.Common.Option.LowTemperatureHygiene"
    )
    LAUNDRY_CARE_COMMON_PROCESS_PHASE = "LaundryCare.Common.Option.ProcessPhase"
    LAUNDRY_CARE_COMMON_REFER_TO_PROGRAM = "LaundryCare.Common.Option.ReferToProgram"
    LAUNDRY_CARE_COMMON_SILENT_MODE = "LaundryCare.Common.Option.SilentMode"
    LAUNDRY_CARE_COMMON_SPEED_PERFECT = "LaundryCare.Common.Option.SpeedPerfect"
    LAUNDRY_CARE_COMMON_VARIO_PERFECT = "LaundryCare.Common.Option.VarioPerfect"
    LAUNDRY_CARE_DRYER_CONNECTED_DRY_ORIGINAL_PROGRAM_TIME = (
        "LaundryCare.Dryer.Option.ConnectedDry.OriginalProgramTime"
    )
    LAUNDRY_CARE_DRYER_DRYING_TARGET = "LaundryCare.Dryer.Option.DryingTarget"
    LAUNDRY_CARE_DRYER_DRYING_TARGET_ADJUSTMENT = (
        "LaundryCare.Dryer.Option.DryingTargetAdjustment"
    )
    LAUNDRY_CARE_DRYER_GENTLE = "LaundryCare.Dryer.Option.Gentle"
    LAUNDRY_CARE_DRYER_HALF_LOAD = "LaundryCare.Dryer.Option.HalfLoad"
    LAUNDRY_CARE_DRYER_PROCESS_PHASE = "LaundryCare.Dryer.Option.ProcessPhase"
    LAUNDRY_CARE_DRYER_REFRESHER = "LaundryCare.Dryer.Option.Refresher"
    LAUNDRY_CARE_DRYER_WRINKLE_GUARD = "LaundryCare.Dryer.Option.WrinkleGuard"
    LAUNDRY_CARE_WASHER_EISA = "LaundryCare.Washer.Option.EISA"
    LAUNDRY_CARE_WASHER_I_DOS_1_ACTIVE_ = "LaundryCare.Washer.Option.IDos1.Active"
    LAUNDRY_CARE_WASHER_I_DOS_1_ACTIVE = "LaundryCare.Washer.Option.IDos1Active"
    LAUNDRY_CARE_WASHER_I_DOS_1_DOSING_LEVEL = (
        "LaundryCare.Washer.Option.IDos1DosingLevel"
    )
    LAUNDRY_CARE_WASHER_I_DOS_2_ACTIVE_ = "LaundryCare.Washer.Option.IDos2.Active"
    LAUNDRY_CARE_WASHER_I_DOS_2_ACTIVE = "LaundryCare.Washer.Option.IDos2Active"
    LAUNDRY_CARE_WASHER_I_DOS_2_DOSING_LEVEL = (
        "LaundryCare.Washer.Option.IDos2DosingLevel"
    )
    LAUNDRY_CARE_WASHER_INTENSIVE_PLUS = "LaundryCare.Washer.Option.IntensivePlus"
    LAUNDRY_CARE_WASHER_LESS_IRONING = "LaundryCare.Washer.Option.LessIroning"
    LAUNDRY_CARE_WASHER_MINI_LOAD = "LaundryCare.Washer.Option.MiniLoad"
    LAUNDRY_CARE_WASHER_MULTIPLE_SOAK = "LaundryCare.Washer.Option.MultipleSoak"
    LAUNDRY_CARE_WASHER_PREWASH = "LaundryCare.Washer.Option.Prewash"
    LAUNDRY_CARE_WASHER_PROCESS_PHASE = "LaundryCare.Washer.Option.ProcessPhase"
    LAUNDRY_CARE_WASHER_RINSE_HOLD = "LaundryCare.Washer.Option.RinseHold"
    LAUNDRY_CARE_WASHER_RINSE_PLUS = "LaundryCare.Washer.Option.RinsePlus"
    LAUNDRY_CARE_WASHER_RINSE_PLUS_1 = "LaundryCare.Washer.Option.RinsePlus1"
    LAUNDRY_CARE_WASHER_SILENT_WASH = "LaundryCare.Washer.Option.SilentWash"
    LAUNDRY_CARE_WASHER_SOAK = "LaundryCare.Washer.Option.Soak"
    LAUNDRY_CARE_WASHER_SPEED_PERFECT = "LaundryCare.Washer.Option.SpeedPerfect"
    LAUNDRY_CARE_WASHER_SPIN_SPEED = "LaundryCare.Washer.Option.SpinSpeed"
    LAUNDRY_CARE_WASHER_STAINS = "LaundryCare.Washer.Option.Stains"
    LAUNDRY_CARE_WASHER_TEMPERATURE = "LaundryCare.Washer.Option.Temperature"
    LAUNDRY_CARE_WASHER_WATER_AND_RINSE_PLUS_1 = (
        "LaundryCare.Washer.Option.WaterAndRinsePlus1"
    )
    LAUNDRY_CARE_WASHER_WATER_PLUS = "LaundryCare.Washer.Option.WaterPlus"
    LAUNDRY_CARE_WASHER_DRYING_TARGET = "LaundryCare.WasherDryer.Option.DryingTarget"
    LAUNDRY_CARE_WASHER_LOW_TEMPERATURE_HYGIENE = (
        "LaundryCare.WasherDryer.Option.LowTemperatureHygiene"
    )
    LAUNDRY_CARE_WASHER_DRYER_PROGRAM_MODE = (
        "LaundryCare.WasherDryer.Option.ProgramMode"
    )
    LAUNDRY_CARE_WASHER_DRYER_WRINKLE_GUARD_BOOST = (
        "LaundryCare.WasherDryer.Option.WrinkleGuardBoost"
    )


class ProgramKey(StrEnum):
    """Represent a program key."""

    @classmethod
    def _missing_(cls, value: object) -> ProgramKey:
        """Return UNKNOWN or mapped ones for missing keys."""
        if isinstance(value, str) and value in _mapped_program_keys:
            return _mapped_program_keys[value]
        LOGGER.debug("Unknown program key: %s", value)
        return cls.UNKNOWN

    UNKNOWN = "unknown"
    BSH_COMMON_FAVORITE_001 = "BSH.Common.Program.Favorite.001"
    BSH_COMMON_FAVORITE_002 = "BSH.Common.Program.Favorite.002"
    BSH_COMMON_FAVORITE_003 = "BSH.Common.Program.Favorite.003"
    BSH_COMMON_FAVORITE_004 = "BSH.Common.Program.Favorite.004"
    BSH_COMMON_FAVORITE_005 = "BSH.Common.Program.Favorite.005"
    BSH_COMMON_FAVORITE_006 = "BSH.Common.Program.Favorite.006"
    BSH_COMMON_FAVORITE_007 = "BSH.Common.Program.Favorite.007"
    BSH_COMMON_FAVORITE_008 = "BSH.Common.Program.Favorite.008"
    BSH_COMMON_FAVORITE_009 = "BSH.Common.Program.Favorite.009"
    BSH_COMMON_FAVORITE_010 = "BSH.Common.Program.Favorite.010"
    BSH_COMMON_FAVORITE_011 = "BSH.Common.Program.Favorite.011"
    BSH_COMMON_FAVORITE_012 = "BSH.Common.Program.Favorite.012"
    BSH_COMMON_FAVORITE_013 = "BSH.Common.Program.Favorite.013"
    BSH_COMMON_FAVORITE_014 = "BSH.Common.Program.Favorite.014"
    BSH_COMMON_FAVORITE_015 = "BSH.Common.Program.Favorite.015"
    BSH_COMMON_FAVORITE_016 = "BSH.Common.Program.Favorite.016"
    BSH_COMMON_FAVORITE_017 = "BSH.Common.Program.Favorite.017"
    BSH_COMMON_FAVORITE_018 = "BSH.Common.Program.Favorite.018"
    BSH_COMMON_FAVORITE_019 = "BSH.Common.Program.Favorite.019"
    BSH_COMMON_FAVORITE_020 = "BSH.Common.Program.Favorite.020"
    CONSUMER_PRODUCTS_CLEANING_ROBOT_BASIC_GO_HOME = (
        "ConsumerProducts.CleaningRobot.Program.Basic.GoHome"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_CLEAN_ALL = (
        "ConsumerProducts.CleaningRobot.Program.Cleaning.CleanAll"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_CLEAN_MAP = (
        "ConsumerProducts.CleaningRobot.Program.Cleaning.CleanMap"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_CAFFE_GRANDE = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.CaffeGrande"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_CAFFE_LATTE = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.CaffeLatte"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_CAPPUCCINO = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.Cappuccino"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COFFEE = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.Coffee"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COFFEE_POT = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.CoffeePot"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_ESPRESSO = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.Espresso"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_ESPRESSO_DOPPIO = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.EspressoDoppio"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_ESPRESSO_MACCHIATO = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.EspressoMacchiato"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_HOT_WATER = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.HotWater"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_LATTE_MACCHIATO = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.LatteMacchiato"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_MILK_FROTH = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.MilkFroth"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_RISTRETTO = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.Ristretto"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_WARM_MILK = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.WarmMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_X_L_COFFEE = (
        "ConsumerProducts.CoffeeMaker.Program.Beverage.XLCoffee"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_APPLIANCE_OFF_RINSING = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.ApplianceOffRinsing"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_APPLIANCE_ON_RINSING = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.ApplianceOnRinsing"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_AUTO_CLEAN = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.AutoClean"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_AUTO_DESCALE = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.AutoDescale"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_CALC_N_CLEAN = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.CalcNClean"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_CLEAN = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.Clean"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_CLEAN_BREWING_UNIT_MANUALLY = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.CleanBrewingUnitManually"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_CLEAN_BREWING_UNIT_MANUALLY_DETAILED = (  # noqa: E501,
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.CleanBrewingUnitManuallyDetailed"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_CLEAN_OUTLET_MANUALLY = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.CleanOutletManually"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_DESCALE = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.Descale"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_FROST_PROTECTION = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.FrostProtection"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_REMOVE_WATER_FILTER = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.RemoveWaterFilter"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_REPLACE_WATER_FILTER = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.ReplaceWaterFilter"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEANING_MODES_RINSE_MILK_SYSTEM = (
        "ConsumerProducts.CoffeeMaker.Program.CleaningModes.RinseMilkSystem"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_AMERICANO = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.Americano"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_BLACK_EYE = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.BlackEye"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_CAFE_AU_LAIT = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.CafeAuLait"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_CAFE_CON_LECHE = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.CafeConLeche"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_CAFE_CORTADO = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.CafeCortado"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_COLD_BREW = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.ColdBrew"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_COLD_BREW_MACCHIATO = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.ColdBrewMacchiato"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_CORTADO = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.Cortado"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_DEAD_EYE = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.DeadEye"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_DOPPIO = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.Doppio"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_FLAT_WHITE = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.FlatWhite"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_GALAO = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.Galao"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_GAROTO = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.Garoto"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_GROSSER_BRAUNER = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.GrosserBrauner"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_KAAPI = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.Kaapi"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_KLEINER_BRAUNER = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.KleinerBrauner"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_KOFFIE_VERKEERD = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.KoffieVerkeerd"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_RED_EYE = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.RedEye"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_SLOW_BREW = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.SlowBrew"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_VERLAENGERTER = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.Verlaengerter"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_VERLAENGERTER_BRAUN = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.VerlaengerterBraun"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_WIENER_MELANGE = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.WienerMelange"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MY_COFFEE_MY_COFFEE_1 = (
        "ConsumerProducts.CoffeeMaker.Program.MyCoffee.MyCoffee1"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MY_COFFEE_MY_COFFEE_2 = (
        "ConsumerProducts.CoffeeMaker.Program.MyCoffee.MyCoffee2"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MY_COFFEE_MY_COFFEE_3 = (
        "ConsumerProducts.CoffeeMaker.Program.MyCoffee.MyCoffee3"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MY_COFFEE_MY_COFFEE_4 = (
        "ConsumerProducts.CoffeeMaker.Program.MyCoffee.MyCoffee4"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MY_COFFEE_MY_COFFEE_5 = (
        "ConsumerProducts.CoffeeMaker.Program.MyCoffee.MyCoffee5"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MY_COFFEE_MY_COFFEE_6 = (
        "ConsumerProducts.CoffeeMaker.Program.MyCoffee.MyCoffee6"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MY_COFFEE_MY_COFFEE_7 = (
        "ConsumerProducts.CoffeeMaker.Program.MyCoffee.MyCoffee7"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MY_COFFEE_MY_COFFEE_8 = (
        "ConsumerProducts.CoffeeMaker.Program.MyCoffee.MyCoffee8"
    )
    COOKING_COMMON_HOOD_AUTOMATIC = "Cooking.Common.Program.Hood.Automatic"
    COOKING_COMMON_HOOD_DELAYED_SHUT_OFF = "Cooking.Common.Program.Hood.DelayedShutOff"
    COOKING_COMMON_HOOD_INTERVAL = "Cooking.Common.Program.Hood.Interval"
    COOKING_COMMON_HOOD_VENTING = "Cooking.Common.Program.Hood.Venting"
    COOKING_HOB_FRYING_SENSOR_MODE = "Cooking.Hob.Program.FryingSensorMode"
    COOKING_HOB_POWER_LEVEL_MODE = "Cooking.Hob.Program.PowerLevelMode"
    COOKING_HOB_POWER_MOVE_MODE = "Cooking.Hob.Program.PowerMoveMode"
    COOKING_OVEN_CLEANING_DRAINING = "Cooking.Oven.Program.Cleaning.Draining"
    COOKING_OVEN_CLEANING_DRYING = "Cooking.Oven.Program.Cleaning.Drying"
    COOKING_OVEN_CLEANING_ECOLYSIS = "Cooking.Oven.Program.Cleaning.Ecolysis"
    COOKING_OVEN_CLEANING_PYROLYSIS = "Cooking.Oven.Program.Cleaning.Pyrolysis"
    COOKING_OVEN_CLEANING_MODES_AUTO_STEAM_CALIBRATION = (
        "Cooking.Oven.Program.CleaningModes.AutoSteamCalibration"
    )
    COOKING_OVEN_DISH_AUTOMATIC_CONV_STEAM_BONELESS_PORK_NECK_JOINT = (
        "Cooking.Oven.Program.Dish.Automatic.Conv.Steam.BonelessPorkNeckJoint"
    )
    COOKING_OVEN_DISH_AUTOMATIC_MICROWAVE_GEFLUEGELTEILE_AUFTAUEN = (
        "Cooking.Oven.Program.Dish.Automatic.Microwave.GefluegelteileAuftauen"
    )
    COOKING_OVEN_DISH_AUTOMATIC_MICROWAVE_HAEHNCHENTEILE = (
        "Cooking.Oven.Program.Dish.Automatic.Microwave.Haehnchenteile"
    )
    COOKING_OVEN_DISH_AUTOMATIC_MICROWAVE_POMMES_FRITES = (
        "Cooking.Oven.Program.Dish.Automatic.Microwave.PommesFrites"
    )
    COOKING_OVEN_DISH_RECOMMENDATION_CONV_MEAT_PROBE_GOOSE_BREAST = (
        "Cooking.Oven.Program.Dish.Recommendation.Conv.MeatProbe.GooseBreast"
    )
    COOKING_OVEN_DISH_RECOMMENDATION_CONV_STEAM_MEAT_PROBE_BONELESS_PORK_NECK_JOINT = (  # avoid ruff format issues  # noqa: E501
        "Cooking.Oven.Program.Dish.Recommendation.Conv.Steam.MeatProbe.BonelessPorkNeckJoint"
    )
    COOKING_OVEN_DISH_RECOMMENDATION_CONV_STEAM_MEAT_PROBE_TURKEY_BREAST = (
        "Cooking.Oven.Program.Dish.Recommendation.Conv.Steam.MeatProbe.TurkeyBreast"
    )
    COOKING_OVEN_DISH_RECOMMENDATION_CONV_STEAM_PART_COOKED_BREAD_ROLLS_OR_BAGUETTE = (  # avoid ruff format issues  # noqa: E501
        "Cooking.Oven.Program.Dish.Recommendation.Conv.Steam.PartCookedBreadRollsOrBaguette"
    )
    COOKING_OVEN_DISH_RECOMMENDATION_FULL_STEAM_BROCCOLI = (
        "Cooking.Oven.Program.Dish.Recommendation.FullSteam.Broccoli"
    )
    COOKING_OVEN_DISH_SUBSEQUENT_COOKING = "Cooking.Oven.Program.Dish.SubsequentCooking"
    COOKING_OVEN_HEATING_MODE_2_D_HOT_AIR = "Cooking.Oven.Program.HeatingMode.2DHotAir"
    COOKING_OVEN_HEATING_MODE_3D_HOT_AIR = "Cooking.Oven.Program.HeatingMode.3DHotAir"
    COOKING_OVEN_HEATING_MODE_AIR_FRY = "Cooking.Oven.Program.HeatingMode.AirFry"
    COOKING_OVEN_HEATING_MODE_BOTTOM_HEATING = (
        "Cooking.Oven.Program.HeatingMode.BottomHeating"
    )
    COOKING_OVEN_HEATING_MODE_BREAD_BAKING = (
        "Cooking.Oven.Program.HeatingMode.BreadBaking"
    )
    COOKING_OVEN_HEATING_MODE_DEFROST = "Cooking.Oven.Program.HeatingMode.Defrost"
    COOKING_OVEN_HEATING_MODE_DESICCATION = (
        "Cooking.Oven.Program.HeatingMode.Desiccation"
    )
    COOKING_OVEN_HEATING_MODE_DOUGH_PROVING = (
        "Cooking.Oven.Program.HeatingMode.DoughProving"
    )
    COOKING_OVEN_HEATING_MODE_FROZEN_HEATUP_SPECIAL = (
        "Cooking.Oven.Program.HeatingMode.FrozenHeatupSpecial"
    )
    COOKING_OVEN_HEATING_MODE_FULL_SURFACE_GRILL = (
        "Cooking.Oven.Program.HeatingMode.FullSurfaceGrill"
    )
    COOKING_OVEN_HEATING_MODE_GRILL_LARGE_AREA = (
        "Cooking.Oven.Program.HeatingMode.GrillLargeArea"
    )
    COOKING_OVEN_HEATING_MODE_GRILL_SMALL_AREA = (
        "Cooking.Oven.Program.HeatingMode.GrillSmallArea"
    )
    COOKING_OVEN_HEATING_MODE_HOT_AIR = "Cooking.Oven.Program.HeatingMode.HotAir"
    COOKING_OVEN_HEATING_MODE_HOT_AIR_100_STEAM = (
        "Cooking.Oven.Program.HeatingMode.HotAir100Steam"
    )
    COOKING_OVEN_HEATING_MODE_HOT_AIR_30_STEAM = (
        "Cooking.Oven.Program.HeatingMode.HotAir30Steam"
    )
    COOKING_OVEN_HEATING_MODE_HOT_AIR_60_STEAM = (
        "Cooking.Oven.Program.HeatingMode.HotAir60Steam"
    )
    COOKING_OVEN_HEATING_MODE_HOT_AIR_80_STEAM = (
        "Cooking.Oven.Program.HeatingMode.HotAir80Steam"
    )
    COOKING_OVEN_HEATING_MODE_HOT_AIR_ECO = "Cooking.Oven.Program.HeatingMode.HotAirEco"
    COOKING_OVEN_HEATING_MODE_HOT_AIR_GENTLE = (
        "Cooking.Oven.Program.HeatingMode.HotAirGentle"
    )
    COOKING_OVEN_HEATING_MODE_HOT_AIR_GRILLING = (
        "Cooking.Oven.Program.HeatingMode.HotAirGrilling"
    )
    COOKING_OVEN_HEATING_MODE_INTENSIVE_HEAT = (
        "Cooking.Oven.Program.HeatingMode.IntensiveHeat"
    )
    COOKING_OVEN_HEATING_MODE_KEEP_WARM = "Cooking.Oven.Program.HeatingMode.KeepWarm"
    COOKING_OVEN_HEATING_MODE_LET_REST = "Cooking.Oven.Program.HeatingMode.LetRest"
    COOKING_OVEN_HEATING_MODE_PIZZA_SETTING = (
        "Cooking.Oven.Program.HeatingMode.PizzaSetting"
    )
    COOKING_OVEN_HEATING_MODE_PRE_HEATING = (
        "Cooking.Oven.Program.HeatingMode.PreHeating"
    )
    COOKING_OVEN_HEATING_MODE_PREHEAT_OVENWARE = (
        "Cooking.Oven.Program.HeatingMode.PreheatOvenware"
    )
    COOKING_OVEN_HEATING_MODE_PROOF = "Cooking.Oven.Program.HeatingMode.Proof"
    COOKING_OVEN_HEATING_MODE_SABBATH_PROGRAMME = (
        "Cooking.Oven.Program.HeatingMode.SabbathProgramme"
    )
    COOKING_OVEN_HEATING_MODE_SLOW_COOK = "Cooking.Oven.Program.HeatingMode.SlowCook"
    COOKING_OVEN_HEATING_MODE_TOP_BOTTOM_HEATING = (
        "Cooking.Oven.Program.HeatingMode.TopBottomHeating"
    )
    COOKING_OVEN_HEATING_MODE_TOP_BOTTOM_HEATING_ECO = (
        "Cooking.Oven.Program.HeatingMode.TopBottomHeatingEco"
    )
    COOKING_OVEN_HEATING_MODE_WARMING_DRAWER = (
        "Cooking.Oven.Program.HeatingMode.WarmingDrawer"
    )
    COOKING_OVEN_MICROWAVE_1000_WATT = "Cooking.Oven.Program.Microwave.1000Watt"
    COOKING_OVEN_MICROWAVE_180_WATT = "Cooking.Oven.Program.Microwave.180Watt"
    COOKING_OVEN_MICROWAVE_360_WATT = "Cooking.Oven.Program.Microwave.360Watt"
    COOKING_OVEN_MICROWAVE_450_WATT = "Cooking.Oven.Program.Microwave.450Watt"
    COOKING_OVEN_MICROWAVE_600_WATT = "Cooking.Oven.Program.Microwave.600Watt"
    COOKING_OVEN_MICROWAVE_900_WATT = "Cooking.Oven.Program.Microwave.900Watt"
    COOKING_OVEN_MICROWAVE_90_WATT = "Cooking.Oven.Program.Microwave.90Watt"
    COOKING_OVEN_MICROWAVE_MAX = "Cooking.Oven.Program.Microwave.Max"
    COOKING_OVEN_STEAM_MODES_DOUGH_PROVING = (
        "Cooking.Oven.Program.SteamModes.DoughProving"
    )
    COOKING_OVEN_STEAM_MODES_REHEAT = "Cooking.Oven.Program.SteamModes.Reheat"
    COOKING_OVEN_STEAM_MODES_STEAM = "Cooking.Oven.Program.SteamModes.Steam"
    COOKING_OVEN_SUBSEQUENT_MODE_CONTINUE_COOKING = (
        "Cooking.Oven.Program.SubsequentMode.ContinueCooking"
    )
    COOKING_OVEN_SUBSEQUENT_MODE_KEEP_WARM = (
        "Cooking.Oven.Program.SubsequentMode.KeepWarm"
    )
    COOKING_OVEN_SUBSEQUENT_MODE_LEAVE_TO_REST = (
        "Cooking.Oven.Program.SubsequentMode.LeaveToRest"
    )
    COOKING_OVEN_SUBSEQUENT_MODE_MICROWAVE = (
        "Cooking.Oven.Program.SubsequentMode.Microwave"
    )
    DISHCARE_DISHWASHER_AUTO_1 = "Dishcare.Dishwasher.Program.Auto1"
    DISHCARE_DISHWASHER_AUTO_2 = "Dishcare.Dishwasher.Program.Auto2"
    DISHCARE_DISHWASHER_AUTO_3 = "Dishcare.Dishwasher.Program.Auto3"
    DISHCARE_DISHWASHER_AUTO_HALF_LOAD = "Dishcare.Dishwasher.Program.AutoHalfLoad"
    DISHCARE_DISHWASHER_ECO_50 = "Dishcare.Dishwasher.Program.Eco50"
    DISHCARE_DISHWASHER_EXPRESS_SPARKLE_65 = (
        "Dishcare.Dishwasher.Program.ExpressSparkle65"
    )
    DISHCARE_DISHWASHER_GLAS_40 = "Dishcare.Dishwasher.Program.Glas40"
    DISHCARE_DISHWASHER_GLASS_CARE = "Dishcare.Dishwasher.Program.GlassCare"
    DISHCARE_DISHWASHER_GLASS_SHINE = "Dishcare.Dishwasher.Program.GlassShine"
    DISHCARE_DISHWASHER_INTENSIV_45 = "Dishcare.Dishwasher.Program.Intensiv45"
    DISHCARE_DISHWASHER_INTENSIV_70 = "Dishcare.Dishwasher.Program.Intensiv70"
    DISHCARE_DISHWASHER_INTENSIV_POWER = "Dishcare.Dishwasher.Program.IntensivPower"
    DISHCARE_DISHWASHER_INTENSIVE_FIXED_ZONE = (
        "Dishcare.Dishwasher.Program.IntensiveFixedZone"
    )
    DISHCARE_DISHWASHER_KURZ_60 = "Dishcare.Dishwasher.Program.Kurz60"
    DISHCARE_DISHWASHER_LEARNING_DISHWASHER = (
        "Dishcare.Dishwasher.Program.LearningDishwasher"
    )
    DISHCARE_DISHWASHER_MACHINE_CARE = "Dishcare.Dishwasher.Program.MachineCare"
    DISHCARE_DISHWASHER_MAGIC_DAILY = "Dishcare.Dishwasher.Program.MagicDaily"
    DISHCARE_DISHWASHER_MAX_EFFICIENT = "Dishcare.Dishwasher.Program.MaxEfficient"
    DISHCARE_DISHWASHER_MAXIMUM_CLEANING = "Dishcare.Dishwasher.Program.MaximumCleaning"
    DISHCARE_DISHWASHER_MIXED_LOAD = "Dishcare.Dishwasher.Program.MixedLoad"
    DISHCARE_DISHWASHER_NIGHT_WASH = "Dishcare.Dishwasher.Program.NightWash"
    DISHCARE_DISHWASHER_NORMAL_45 = "Dishcare.Dishwasher.Program.Normal45"
    DISHCARE_DISHWASHER_NORMAL_65 = "Dishcare.Dishwasher.Program.Normal65"
    DISHCARE_DISHWASHER_PRE_RINSE = "Dishcare.Dishwasher.Program.PreRinse"
    DISHCARE_DISHWASHER_QUICK_45 = "Dishcare.Dishwasher.Program.Quick45"
    DISHCARE_DISHWASHER_QUICK_65 = "Dishcare.Dishwasher.Program.Quick65"
    DISHCARE_DISHWASHER_QUICK_D = "Dishcare.Dishwasher.Program.QuickD"
    DISHCARE_DISHWASHER_STEAM_FRESH = "Dishcare.Dishwasher.Program.SteamFresh"
    DISHCARE_DISHWASHER_SUPER_60 = "Dishcare.Dishwasher.Program.Super60"
    HEATING_VENTILATION_AIR_CONDITIONING_AIR_CONDITIONER_ACTIVE_CLEAN = (
        "HeatingVentilationAirConditioning.AirConditioner.Program.ActiveClean"
    )
    HEATING_VENTILATION_AIR_CONDITIONING_AIR_CONDITIONER_AUTO = (
        "HeatingVentilationAirConditioning.AirConditioner.Program.Auto"
    )
    HEATING_VENTILATION_AIR_CONDITIONING_AIR_CONDITIONER_COOL = (
        "HeatingVentilationAirConditioning.AirConditioner.Program.Cool"
    )
    HEATING_VENTILATION_AIR_CONDITIONING_AIR_CONDITIONER_DRY = (
        "HeatingVentilationAirConditioning.AirConditioner.Program.Dry"
    )
    HEATING_VENTILATION_AIR_CONDITIONING_AIR_CONDITIONER_FAN = (
        "HeatingVentilationAirConditioning.AirConditioner.Program.Fan"
    )
    HEATING_VENTILATION_AIR_CONDITIONING_AIR_CONDITIONER_HEAT = (
        "HeatingVentilationAirConditioning.AirConditioner.Program.Heat"
    )
    LAUNDRY_CARE_DRYER_ANTI_SHRINK = "LaundryCare.Dryer.Program.AntiShrink"
    LAUNDRY_CARE_DRYER_BEDLINENS = "LaundryCare.Dryer.Program.Bedlinens"
    LAUNDRY_CARE_DRYER_BLANKETS = "LaundryCare.Dryer.Program.Blankets"
    LAUNDRY_CARE_DRYER_BUSINESS_SHIRTS = "LaundryCare.Dryer.Program.BusinessShirts"
    LAUNDRY_CARE_DRYER_BUSINESS_SHIRTS_EASY_IRON = (
        "LaundryCare.Dryer.Program.BusinessShirts.EasyIron"
    )
    LAUNDRY_CARE_DRYER_COLD_REFRESH_1_PIECE = (
        "LaundryCare.Dryer.Program.ColdRefresh.1Piece"
    )
    LAUNDRY_CARE_DRYER_COLD_REFRESH_5_PIECE = (
        "LaundryCare.Dryer.Program.ColdRefresh.5Piece"
    )
    LAUNDRY_CARE_DRYER_COLD_REFRESH_BUSINESS = (
        "LaundryCare.Dryer.Program.ColdRefresh.Business"
    )
    LAUNDRY_CARE_DRYER_COLD_REFRESH_COLD_REFRESH_COLD_REFRESH = (
        "LaundryCare.Dryer.Program.ColdRefresh.ColdRefresh.ColdRefresh"
    )
    LAUNDRY_CARE_DRYER_CONNECTED_DRY = "LaundryCare.Dryer.Program.ConnectedDry"
    LAUNDRY_CARE_DRYER_COTTON = "LaundryCare.Dryer.Program.Cotton"
    LAUNDRY_CARE_DRYER_COTTON_COTTON_ECO = "LaundryCare.Dryer.Program.Cotton.CottonEco"
    LAUNDRY_CARE_DRYER_COTTON_ECO_4060 = "LaundryCare.Dryer.Program.Cotton.Eco4060"
    LAUNDRY_CARE_DRYER_DELICATES = "LaundryCare.Dryer.Program.Delicates"
    LAUNDRY_CARE_DRYER_DESSOUS = "LaundryCare.Dryer.Program.Dessous"
    LAUNDRY_CARE_DRYER_DOWN_FEATHERS = "LaundryCare.Dryer.Program.DownFeathers"
    LAUNDRY_CARE_DRYER_EASY_CARE_EASY_CARE = (
        "LaundryCare.Dryer.Program.EasyCare.EasyCare"
    )
    LAUNDRY_CARE_DRYER_HYGIENE = "LaundryCare.Dryer.Program.Hygiene"
    LAUNDRY_CARE_DRYER_IN_BASKET = "LaundryCare.Dryer.Program.InBasket"
    LAUNDRY_CARE_DRYER_IN_BASKET_WOOL_BASKET = (
        "LaundryCare.Dryer.Program.InBasket.WoolBasket"
    )
    LAUNDRY_CARE_DRYER_JEANS = "LaundryCare.Dryer.Program.Jeans"
    LAUNDRY_CARE_DRYER_MAINTENANCE_CARE_1_MAINTENANCE_CARE_1_QUICK_CARE = (
        "LaundryCare.Dryer.Program.MaintenanceCare1.MaintenanceCare1.QuickCare"
    )
    LAUNDRY_CARE_DRYER_MAINTENANCE_CARE_2_MAINTENANCE_CARE_2_DEPTH_CARE = (
        "LaundryCare.Dryer.Program.MaintenanceCare2.MaintenanceCare2.DepthCare"
    )
    LAUNDRY_CARE_DRYER_MIX = "LaundryCare.Dryer.Program.Mix"
    LAUNDRY_CARE_DRYER_MY_TIME_MY_DRYING_TIME = (
        "LaundryCare.Dryer.Program.MyTime.MyDryingTime"
    )
    LAUNDRY_CARE_DRYER_OUTDOOR = "LaundryCare.Dryer.Program.Outdoor"
    LAUNDRY_CARE_DRYER_OUTDOOR_SPORTSWEAR = (
        "LaundryCare.Dryer.Program.Outdoor.Sportswear"
    )
    LAUNDRY_CARE_DRYER_PILLOW = "LaundryCare.Dryer.Program.Pillow"
    LAUNDRY_CARE_DRYER_SHIRTS_15 = "LaundryCare.Dryer.Program.Shirts15"
    LAUNDRY_CARE_DRYER_SUPER_40 = "LaundryCare.Dryer.Program.Super40"
    LAUNDRY_CARE_DRYER_SYNTHETIC = "LaundryCare.Dryer.Program.Synthetic"
    LAUNDRY_CARE_DRYER_SYNTHETIC_REFRESH = "LaundryCare.Dryer.Program.SyntheticRefresh"
    LAUNDRY_CARE_DRYER_TIME_COLD = "LaundryCare.Dryer.Program.TimeCold"
    LAUNDRY_CARE_DRYER_TIME_COLD_AIR_FLUFF = (
        "LaundryCare.Dryer.Program.TimeCold.AirFluff"
    )
    LAUNDRY_CARE_DRYER_TIME_COLD_FIX_TIME_COLD_20 = (
        "LaundryCare.Dryer.Program.TimeColdFix.TimeCold20"
    )
    LAUNDRY_CARE_DRYER_TIME_COLD_FIX_TIME_COLD_30 = (
        "LaundryCare.Dryer.Program.TimeColdFix.TimeCold30"
    )
    LAUNDRY_CARE_DRYER_TIME_COLD_FIX_TIME_COLD_60 = (
        "LaundryCare.Dryer.Program.TimeColdFix.TimeCold60"
    )
    LAUNDRY_CARE_DRYER_TIME_WARM = "LaundryCare.Dryer.Program.TimeWarm"
    LAUNDRY_CARE_DRYER_TIME_WARM_FIX_TIME_WARM_30 = (
        "LaundryCare.Dryer.Program.TimeWarmFix.TimeWarm30"
    )
    LAUNDRY_CARE_DRYER_TIME_WARM_FIX_TIME_WARM_40 = (
        "LaundryCare.Dryer.Program.TimeWarmFix.TimeWarm40"
    )
    LAUNDRY_CARE_DRYER_TIME_WARM_FIX_TIME_WARM_60 = (
        "LaundryCare.Dryer.Program.TimeWarmFix.TimeWarm60"
    )
    LAUNDRY_CARE_DRYER_TOWELS = "LaundryCare.Dryer.Program.Towels"
    LAUNDRY_CARE_DRYER_WOOL_FINISH = "LaundryCare.Dryer.Program.WoolFinish"
    LAUNDRY_CARE_WASHER_AUTO_30 = "LaundryCare.Washer.Program.Auto30"
    LAUNDRY_CARE_WASHER_AUTO_40 = "LaundryCare.Washer.Program.Auto40"
    LAUNDRY_CARE_WASHER_AUTO_60 = "LaundryCare.Washer.Program.Auto60"
    LAUNDRY_CARE_WASHER_CHIFFON = "LaundryCare.Washer.Program.Chiffon"
    LAUNDRY_CARE_WASHER_COTTON = "LaundryCare.Washer.Program.Cotton"
    LAUNDRY_CARE_WASHER_COTTON_COLOUR = "LaundryCare.Washer.Program.Cotton.Colour"
    LAUNDRY_CARE_WASHER_COTTON_COTTON_ECO = (
        "LaundryCare.Washer.Program.Cotton.CottonEco"
    )
    LAUNDRY_CARE_WASHER_COTTON_ECO_4060 = "LaundryCare.Washer.Program.Cotton.Eco4060"
    LAUNDRY_CARE_WASHER_CURTAINS = "LaundryCare.Washer.Program.Curtains"
    LAUNDRY_CARE_WASHER_DARK_WASH = "LaundryCare.Washer.Program.DarkWash"
    LAUNDRY_CARE_WASHER_DELICATES_SILK = "LaundryCare.Washer.Program.DelicatesSilk"
    LAUNDRY_CARE_WASHER_DESSOUS = "LaundryCare.Washer.Program.Dessous"
    LAUNDRY_CARE_WASHER_DOWN_DUVET_DUVET = "LaundryCare.Washer.Program.DownDuvet.Duvet"
    LAUNDRY_CARE_WASHER_DRUM_CLEAN = "LaundryCare.Washer.Program.DrumClean"

    LAUNDRY_CARE_WASHER_EASY_CARE = "LaundryCare.Washer.Program.EasyCare"
    LAUNDRY_CARE_WASHER_HYGIENE_PLUS = "LaundryCare.Washer.Program.HygienePlus"
    LAUNDRY_CARE_WASHER_MIX = "LaundryCare.Washer.Program.Mix"
    LAUNDRY_CARE_WASHER_MIX_NIGHT_WASH = "LaundryCare.Washer.Program.Mix.NightWash"
    LAUNDRY_CARE_WASHER_MONSOON = "LaundryCare.Washer.Program.Monsoon"
    LAUNDRY_CARE_WASHER_MY_TIME = "LaundryCare.Washer.Program.MyTime"
    LAUNDRY_CARE_WASHER_OUTDOOR = "LaundryCare.Washer.Program.Outdoor"
    LAUNDRY_CARE_WASHER_PLUSH_TOY = "LaundryCare.Washer.Program.PlushToy"
    LAUNDRY_CARE_WASHER_POWER_SPEED_59 = "LaundryCare.Washer.Program.PowerSpeed59"
    LAUNDRY_CARE_WASHER_RINSE = "LaundryCare.Washer.Program.Rinse"
    LAUNDRY_CARE_WASHER_RINSE_RINSE_SPIN_DRAIN = (
        "LaundryCare.Washer.Program.Rinse.RinseSpinDrain"
    )
    LAUNDRY_CARE_WASHER_SENSITIVE = "LaundryCare.Washer.Program.Sensitive"
    LAUNDRY_CARE_WASHER_SHIRTS_BLOUSES = "LaundryCare.Washer.Program.ShirtsBlouses"
    LAUNDRY_CARE_WASHER_SPIN_SPIN_DRAIN = "LaundryCare.Washer.Program.Spin.SpinDrain"
    LAUNDRY_CARE_WASHER_SPORT_FITNESS = "LaundryCare.Washer.Program.SportFitness"
    LAUNDRY_CARE_WASHER_SPORT_SHOES = "LaundryCare.Washer.Program.SportShoes"
    LAUNDRY_CARE_WASHER_STEAMING_STEAMING = (
        "LaundryCare.Washer.Program.Steaming.Steaming"
    )
    LAUNDRY_CARE_WASHER_SUPER_153045_SUPER_15 = (
        "LaundryCare.Washer.Program.Super153045.Super15"
    )
    LAUNDRY_CARE_WASHER_SUPER_153045_SUPER_1530 = (
        "LaundryCare.Washer.Program.Super153045.Super1530"
    )
    LAUNDRY_CARE_WASHER_SUPER_153045_SUPER_30 = (
        "LaundryCare.Washer.Program.Super153045.Super30"
    )
    LAUNDRY_CARE_WASHER_TOWELS = "LaundryCare.Washer.Program.Towels"
    LAUNDRY_CARE_WASHER_WASH_AND_DRY_60 = "LaundryCare.Washer.Program.WashAndDry.60"
    LAUNDRY_CARE_WASHER_WASH_AND_DRY_90 = "LaundryCare.Washer.Program.WashAndDry.90"
    LAUNDRY_CARE_WASHER_WATER_PROOF = "LaundryCare.Washer.Program.WaterProof"
    LAUNDRY_CARE_WASHER_WOOL = "LaundryCare.Washer.Program.Wool"
    LAUNDRY_CARE_WASHER_DRYER_COTTON = "LaundryCare.WasherDryer.Program.Cotton"
    LAUNDRY_CARE_WASHER_DRYER_COTTON_ECO_4060 = (
        "LaundryCare.WasherDryer.Program.Cotton.Eco4060"
    )
    LAUNDRY_CARE_WASHER_DRYER_DELICATES_SILK = (
        "LaundryCare.WasherDryer.Program.DelicatesSilk"
    )
    LAUNDRY_CARE_WASHER_DRYER_DRUM_CLEAN_AND_DRY_DRUM_CARE = (
        "LaundryCare.WasherDryer.Program.DrumCleanAndDry.DrumCare"
    )
    LAUNDRY_CARE_WASHER_DRYER_EASY_CARE = "LaundryCare.WasherDryer.Program.EasyCare"
    LAUNDRY_CARE_WASHER_DRYER_MIX = "LaundryCare.WasherDryer.Program.Mix"
    LAUNDRY_CARE_WASHER_DRYER_RINSE = "LaundryCare.WasherDryer.Program.Rinse"
    LAUNDRY_CARE_WASHER_DRYER_SENSITIVE = "LaundryCare.WasherDryer.Program.Sensitive"
    LAUNDRY_CARE_WASHER_DRYER_SPIN = "LaundryCare.WasherDryer.Program.Spin"
    LAUNDRY_CARE_WASHER_DRYER_WASH_AND_DRY_60 = (
        "LaundryCare.WasherDryer.Program.WashAndDry.60"
    )
    LAUNDRY_CARE_WASHER_DRYER_WASH_AND_DRY_90 = (
        "LaundryCare.WasherDryer.Program.WashAndDry.90"
    )
    LAUNDRY_CARE_WASHER_DRYER_WOOL = "LaundryCare.WasherDryer.Program.Wool"


_mapped_program_keys = {
    "LaundryCare.WasherDryer.Program.Cotton.Cotton.Cotton": (
        ProgramKey.LAUNDRY_CARE_WASHER_DRYER_COTTON
    ),
    "LaundryCare.WasherDryer.Program.DelicatesSilk.DelicatesSilk.DelicatesSilk": (
        ProgramKey.LAUNDRY_CARE_WASHER_DRYER_DELICATES_SILK
    ),
    "LaundryCare.WasherDryer.Program.DrumCleanDry.DrumCare.DrumCare": (
        ProgramKey.LAUNDRY_CARE_WASHER_DRYER_DRUM_CLEAN_AND_DRY_DRUM_CARE
    ),
    "LaundryCare.WasherDryer.Program.Rinse.Rinse.Rinse": (
        ProgramKey.LAUNDRY_CARE_WASHER_DRYER_RINSE
    ),
    "LaundryCare.WasherDryer.Program.Sensitive.Sensitive.Sensitive": (
        ProgramKey.LAUNDRY_CARE_WASHER_DRYER_SENSITIVE
    ),
    "LaundryCare.WasherDryer.Program.Wool.Wool.Wool": (
        ProgramKey.LAUNDRY_CARE_WASHER_DRYER_WOOL
    ),
}
