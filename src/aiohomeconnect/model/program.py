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
    BSH_COMMON_DURATION = "BSH.Common.Option.Duration"
    BSH_COMMON_FINISH_IN_RELATIVE = "BSH.Common.Option.FinishInRelative"
    BSH_COMMON_START_IN_RELATIVE = "BSH.Common.Option.StartInRelative"
    CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_MODE = (
        "ConsumerProducts.CleaningRobot.Option.CleaningMode"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_REFERENCE_MAP_ID = (
        "ConsumerProducts.CleaningRobot.Option.ReferenceMapId"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_SUCTION_POWER = (
        "ConsumerProducts.CleaningRobot.Option.SuctionPower"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEAN_AMOUNT = (
        "ConsumerProducts.CoffeeMaker.Option.BeanAmount"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEAN_CONTAINER_SELECTION = (
        "ConsumerProducts.CoffeeMaker.Option.BeanContainerSelection"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_MILK_RATIO = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeMilkRatio"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_TEMPERATURE = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeTemperature"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_FILL_QUANTITY = (
        "ConsumerProducts.CoffeeMaker.Option.FillQuantity"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_FLOW_RATE = (
        "ConsumerProducts.CoffeeMaker.Option.FlowRate"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_HOT_WATER_TEMPERATURE = (
        "ConsumerProducts.CoffeeMaker.Option.HotWaterTemperature"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MULTIPLE_BEVERAGES = (
        "ConsumerProducts.CoffeeMaker.Option.MultipleBeverages"
    )
    COOKING_COMMON_HOOD_INTENSIVE_LEVEL = "Cooking.Common.Option.Hood.IntensiveLevel"
    COOKING_COMMON_HOOD_VENTING_LEVEL = "Cooking.Common.Option.Hood.VentingLevel"
    COOKING_OVEN_FAST_PRE_HEAT = "Cooking.Oven.Option.FastPreHeat"
    COOKING_OVEN_SETPOINT_TEMPERATURE = "Cooking.Oven.Option.SetpointTemperature"
    COOKING_OVEN_WARMING_LEVEL = "Cooking.Oven.Option.WarmingLevel"
    DISHCARE_DISHWASHER_BRILLIANCE_DRY = "Dishcare.Dishwasher.Option.BrillianceDry"
    DISHCARE_DISHWASHER_ECO_DRY = "Dishcare.Dishwasher.Option.EcoDry"
    DISHCARE_DISHWASHER_EXTRA_DRY = "Dishcare.Dishwasher.Option.ExtraDry"
    DISHCARE_DISHWASHER_HALF_LOAD = "Dishcare.Dishwasher.Option.HalfLoad"
    DISHCARE_DISHWASHER_HYGIENE_PLUS = "Dishcare.Dishwasher.Option.HygienePlus"
    DISHCARE_DISHWASHER_INTENSIV_ZONE = "Dishcare.Dishwasher.Option.IntensivZone"
    DISHCARE_DISHWASHER_SILENCE_ON_DEMAND = "Dishcare.Dishwasher.Option.SilenceOnDemand"
    DISHCARE_DISHWASHER_VARIO_SPEED_PLUS = "Dishcare.Dishwasher.Option.VarioSpeedPlus"
    DISHCARE_DISHWASHER_ZEOLITE_DRY = "Dishcare.Dishwasher.Option.ZeoliteDry"
    HEATING_VENTILATION_AIR_CONDITIONING_AIR_CONDITIONER_FAN_SPEED_MODE = (
        "HeatingVentilationAirConditioning.AirConditioner.Option.FanSpeedMode"
    )
    HEATING_VENTILATION_AIR_CONDITIONING_AIR_CONDITIONER_FAN_SPEED_PERCENTAGE = (
        "HeatingVentilationAirConditioning.AirConditioner.Option.FanSpeedPercentage"
    )
    LAUNDRY_CARE_COMMON_VARIO_PERFECT = "LaundryCare.Common.Option.VarioPerfect"
    LAUNDRY_CARE_DRYER_DRYING_TARGET = "LaundryCare.Dryer.Option.DryingTarget"
    LAUNDRY_CARE_WASHER_I_DOS_1_ACTIVE = "LaundryCare.Washer.Option.IDos1Active"
    LAUNDRY_CARE_WASHER_I_DOS_2_ACTIVE = "LaundryCare.Washer.Option.IDos2Active"
    LAUNDRY_CARE_WASHER_SPIN_SPEED = "LaundryCare.Washer.Option.SpinSpeed"
    LAUNDRY_CARE_WASHER_TEMPERATURE = "LaundryCare.Washer.Option.Temperature"


class ProgramKey(StrEnum):
    """Represent a program key."""

    @classmethod
    def _missing_(cls, value: object) -> ProgramKey:
        """Return UNKNOWN for missing keys."""
        LOGGER.debug("Unknown program key: %s", value)
        return cls.UNKNOWN

    UNKNOWN = "unknown"
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
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_VERLAENGERTER = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.Verlaengerter"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_VERLAENGERTER_BRAUN = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.VerlaengerterBraun"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_WIENER_MELANGE = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.WienerMelange"
    )
    COOKING_COMMON_HOOD_AUTOMATIC = "Cooking.Common.Program.Hood.Automatic"
    COOKING_COMMON_HOOD_DELAYED_SHUT_OFF = "Cooking.Common.Program.Hood.DelayedShutOff"
    COOKING_COMMON_HOOD_VENTING = "Cooking.Common.Program.Hood.Venting"
    COOKING_OVEN_HEATING_MODE_BOTTOM_HEATING = (
        "Cooking.Oven.Program.HeatingMode.BottomHeating"
    )
    COOKING_OVEN_HEATING_MODE_DEFROST = "Cooking.Oven.Program.HeatingMode.Defrost"
    COOKING_OVEN_HEATING_MODE_DESICCATION = (
        "Cooking.Oven.Program.HeatingMode.Desiccation"
    )
    COOKING_OVEN_HEATING_MODE_FROZEN_HEATUP_SPECIAL = (
        "Cooking.Oven.Program.HeatingMode.FrozenHeatupSpecial"
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
    COOKING_OVEN_HEATING_MODE_HOT_AIR_GRILLING = (
        "Cooking.Oven.Program.HeatingMode.HotAirGrilling"
    )
    COOKING_OVEN_HEATING_MODE_INTENSIVE_HEAT = (
        "Cooking.Oven.Program.HeatingMode.IntensiveHeat"
    )
    COOKING_OVEN_HEATING_MODE_KEEP_WARM = "Cooking.Oven.Program.HeatingMode.KeepWarm"
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
    DISHCARE_DISHWASHER_INTENSIV_45 = "Dishcare.Dishwasher.Program.Intensiv45"
    DISHCARE_DISHWASHER_INTENSIV_70 = "Dishcare.Dishwasher.Program.Intensiv70"
    DISHCARE_DISHWASHER_INTENSIV_POWER = "Dishcare.Dishwasher.Program.IntensivPower"
    DISHCARE_DISHWASHER_KURZ_60 = "Dishcare.Dishwasher.Program.Kurz60"
    DISHCARE_DISHWASHER_MACHINE_CARE = "Dishcare.Dishwasher.Program.MachineCare"
    DISHCARE_DISHWASHER_MAGIC_DAILY = "Dishcare.Dishwasher.Program.MagicDaily"
    DISHCARE_DISHWASHER_MAXIMUM_CLEANING = "Dishcare.Dishwasher.Program.MaximumCleaning"
    DISHCARE_DISHWASHER_MIXED_LOAD = "Dishcare.Dishwasher.Program.MixedLoad"
    DISHCARE_DISHWASHER_NIGHT_WASH = "Dishcare.Dishwasher.Program.NightWash"
    DISHCARE_DISHWASHER_NORMAL_45 = "Dishcare.Dishwasher.Program.Normal45"
    DISHCARE_DISHWASHER_NORMAL_65 = "Dishcare.Dishwasher.Program.Normal65"
    DISHCARE_DISHWASHER_PRE_RINSE = "Dishcare.Dishwasher.Program.PreRinse"
    DISHCARE_DISHWASHER_QUICK_45 = "Dishcare.Dishwasher.Program.Quick45"
    DISHCARE_DISHWASHER_QUICK_65 = "Dishcare.Dishwasher.Program.Quick65"
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
    LAUNDRY_CARE_DRYER_BLANKETS = "LaundryCare.Dryer.Program.Blankets"
    LAUNDRY_CARE_DRYER_BUSINESS_SHIRTS = "LaundryCare.Dryer.Program.BusinessShirts"
    LAUNDRY_CARE_DRYER_COTTON = "LaundryCare.Dryer.Program.Cotton"
    LAUNDRY_CARE_DRYER_DELICATES = "LaundryCare.Dryer.Program.Delicates"
    LAUNDRY_CARE_DRYER_DESSOUS = "LaundryCare.Dryer.Program.Dessous"
    LAUNDRY_CARE_DRYER_DOWN_FEATHERS = "LaundryCare.Dryer.Program.DownFeathers"
    LAUNDRY_CARE_DRYER_HYGIENE = "LaundryCare.Dryer.Program.Hygiene"
    LAUNDRY_CARE_DRYER_IN_BASKET = "LaundryCare.Dryer.Program.InBasket"
    LAUNDRY_CARE_DRYER_JEANS = "LaundryCare.Dryer.Program.Jeans"
    LAUNDRY_CARE_DRYER_MIX = "LaundryCare.Dryer.Program.Mix"
    LAUNDRY_CARE_DRYER_MY_TIME_MY_DRYING_TIME = (
        "LaundryCare.Dryer.Program.MyTime.MyDryingTime"
    )
    LAUNDRY_CARE_DRYER_OUTDOOR = "LaundryCare.Dryer.Program.Outdoor"
    LAUNDRY_CARE_DRYER_PILLOW = "LaundryCare.Dryer.Program.Pillow"
    LAUNDRY_CARE_DRYER_SHIRTS_15 = "LaundryCare.Dryer.Program.Shirts15"
    LAUNDRY_CARE_DRYER_SUPER_40 = "LaundryCare.Dryer.Program.Super40"
    LAUNDRY_CARE_DRYER_SYNTHETIC = "LaundryCare.Dryer.Program.Synthetic"
    LAUNDRY_CARE_DRYER_SYNTHETIC_REFRESH = "LaundryCare.Dryer.Program.SyntheticRefresh"
    LAUNDRY_CARE_DRYER_TIME_COLD = "LaundryCare.Dryer.Program.TimeCold"
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
    LAUNDRY_CARE_WASHER_MIX = "LaundryCare.Washer.Program.Mix"
    LAUNDRY_CARE_WASHER_MIX_NIGHT_WASH = "LaundryCare.Washer.Program.Mix.NightWash"
    LAUNDRY_CARE_WASHER_MONSOON = "LaundryCare.Washer.Program.Monsoon"
    LAUNDRY_CARE_WASHER_OUTDOOR = "LaundryCare.Washer.Program.Outdoor"
    LAUNDRY_CARE_WASHER_PLUSH_TOY = "LaundryCare.Washer.Program.PlushToy"
    LAUNDRY_CARE_WASHER_POWER_SPEED_59 = "LaundryCare.Washer.Program.PowerSpeed59"
    LAUNDRY_CARE_WASHER_RINSE_RINSE_SPIN_DRAIN = (
        "LaundryCare.Washer.Program.Rinse.RinseSpinDrain"
    )
    LAUNDRY_CARE_WASHER_SENSITIVE = "LaundryCare.Washer.Program.Sensitive"
    LAUNDRY_CARE_WASHER_SHIRTS_BLOUSES = "LaundryCare.Washer.Program.ShirtsBlouses"
    LAUNDRY_CARE_WASHER_SPORT_FITNESS = "LaundryCare.Washer.Program.SportFitness"
    LAUNDRY_CARE_WASHER_SUPER_153045_SUPER_15 = (
        "LaundryCare.Washer.Program.Super153045.Super15"
    )
    LAUNDRY_CARE_WASHER_SUPER_153045_SUPER_1530 = (
        "LaundryCare.Washer.Program.Super153045.Super1530"
    )
    LAUNDRY_CARE_WASHER_TOWELS = "LaundryCare.Washer.Program.Towels"
    LAUNDRY_CARE_WASHER_WATER_PROOF = "LaundryCare.Washer.Program.WaterProof"
    LAUNDRY_CARE_WASHER_WOOL = "LaundryCare.Washer.Program.Wool"
    LAUNDRY_CARE_WASHER_DRYER_COTTON = "LaundryCare.WasherDryer.Program.Cotton"
    LAUNDRY_CARE_WASHER_DRYER_COTTON_ECO_4060 = (
        "LaundryCare.WasherDryer.Program.Cotton.Eco4060"
    )
    LAUNDRY_CARE_WASHER_DRYER_EASY_CARE = "LaundryCare.WasherDryer.Program.EasyCare"
    LAUNDRY_CARE_WASHER_DRYER_MIX = "LaundryCare.WasherDryer.Program.Mix"
    LAUNDRY_CARE_WASHER_DRYER_WASH_AND_DRY_60 = (
        "LaundryCare.WasherDryer.Program.WashAndDry.60"
    )
    LAUNDRY_CARE_WASHER_DRYER_WASH_AND_DRY_90 = (
        "LaundryCare.WasherDryer.Program.WashAndDry.90"
    )
