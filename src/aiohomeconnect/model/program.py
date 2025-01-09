"""Provide program models for the Home Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class Program(DataClassJSONMixin):
    """Represent Program."""

    key: ProgramKey
    name: str | None = None
    options: list[Option] | None = None
    constraints: ProgramConstraints | None = None


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


@dataclass
class ArrayOfOptions(DataClassJSONMixin):
    """List of options."""

    options: list[Option]


class OptionKey(StrEnum):
    """Represent an option key."""

    BSH_COMMON_DURATION = "BSH.Common.Option.Duration"
    BSH_COMMON_FINISH_IN_RELATIVE = "BSH.Common.Option.FinishInRelative"
    BSH_COMMON_START_IN_RELATIVE = "BSH.Common.Option.StartInRelative"
    CONSUMER_PRODUCTS_CLEANING_ROBOT_CLEANING_MODE = (
        "ConsumerProducts.CleaningRobot.Option.CleaningMode"
    )
    CONSUMER_PRODUCTS_CLEANING_ROBOT_REFERENCE_MAP_ID = (
        "ConsumerProducts.CleaningRobot.Option.ReferenceMapId"
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
    LAUNDRY_CARE_COMMON_VARIO_PERFECT = "LaundryCare.Common.Option.VarioPerfect"
    LAUNDRY_CARE_DRYER_DRYING_TARGET = "LaundryCare.Dryer.Option.DryingTarget"
    LAUNDRY_CARE_WASHER_I_DOS_1_ACTIVE = "LaundryCare.Washer.Option.IDos1Active"
    LAUNDRY_CARE_WASHER_I_DOS_2_ACTIVE = "LaundryCare.Washer.Option.IDos2Active"
    LAUNDRY_CARE_WASHER_SPIN_SPEED = "LaundryCare.Washer.Option.SpinSpeed"
    LAUNDRY_CARE_WASHER_TEMPERATURE = "LaundryCare.Washer.Option.Temperature"


class ProgramKey(StrEnum):
    """Represent a program key."""

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
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_XL_COFFEE = (
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
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_CAFE_CONLECHE = (
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
    CONSUMER_PRODUCTS_COFFEE_MAKE_COFFEE_WORLD_VERLAENGERTER_BRAUN = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.VerlaengerterBraun"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_WORLD_WIENER_MELANGE = (
        "ConsumerProducts.CoffeeMaker.Program.CoffeeWorld.WienerMelange"
    )
    COOKING_COMMON_PROGRAM_HOOD_AUTOMATIC = "Cooking.Common.Program.Hood.Automatic"
    COOKING_COMMON_PROGRAM_HOOD_DELAYEDSHUTOFF = (
        "Cooking.Common.Program.Hood.DelayedShutOff"
    )
    COOKING_COMMON_PROGRAM_HOOD_VENTING = "Cooking.Common.Program.Hood.Venting"
    COOKING_OVEN_PROGRAM_HEATINGMODE_BOTTOMHEATING = (
        "Cooking.Oven.Program.HeatingMode.BottomHeating"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_DEFROST = (
        "Cooking.Oven.Program.HeatingMode.Defrost"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_DESICCATION = (
        "Cooking.Oven.Program.HeatingMode.Desiccation"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_FROZENHEATUPSPECIAL = (
        "Cooking.Oven.Program.HeatingMode.FrozenHeatupSpecial"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_HOTAIR = "Cooking.Oven.Program.HeatingMode.HotAir"
    COOKING_OVEN_PROGRAM_HEATINGMODE_HOTAIR100STEAM = (
        "Cooking.Oven.Program.HeatingMode.HotAir100Steam"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_HOTAIR30STEAM = (
        "Cooking.Oven.Program.HeatingMode.HotAir30Steam"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_HOTAIR60STEAM = (
        "Cooking.Oven.Program.HeatingMode.HotAir60Steam"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_HOTAIR80STEAM = (
        "Cooking.Oven.Program.HeatingMode.HotAir80Steam"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_HOTAIRECO = (
        "Cooking.Oven.Program.HeatingMode.HotAirEco"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_HOTAIRGRILLING = (
        "Cooking.Oven.Program.HeatingMode.HotAirGrilling"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_INTENSIVEHEAT = (
        "Cooking.Oven.Program.HeatingMode.IntensiveHeat"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_KEEPWARM = (
        "Cooking.Oven.Program.HeatingMode.KeepWarm"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_PIZZASETTING = (
        "Cooking.Oven.Program.HeatingMode.PizzaSetting"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_PREHEATING = (
        "Cooking.Oven.Program.HeatingMode.PreHeating"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_PREHEATOVENWARE = (
        "Cooking.Oven.Program.HeatingMode.PreheatOvenware"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_PROOF = "Cooking.Oven.Program.HeatingMode.Proof"
    COOKING_OVEN_PROGRAM_HEATINGMODE_SABBATHPROGRAMME = (
        "Cooking.Oven.Program.HeatingMode.SabbathProgramme"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_SLOWCOOK = (
        "Cooking.Oven.Program.HeatingMode.SlowCook"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_TOPBOTTOMHEATING = (
        "Cooking.Oven.Program.HeatingMode.TopBottomHeating"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_TOPBOTTOMHEATINGECO = (
        "Cooking.Oven.Program.HeatingMode.TopBottomHeatingEco"
    )
    COOKING_OVEN_PROGRAM_HEATINGMODE_WARMINGDRAWER = (
        "Cooking.Oven.Program.HeatingMode.WarmingDrawer"
    )
    COOKING_OVEN_PROGRAM_MICROWAVE_1000WATT = "Cooking.Oven.Program.Microwave.1000Watt"
    COOKING_OVEN_PROGRAM_MICROWAVE_180WATT = "Cooking.Oven.Program.Microwave.180Watt"
    COOKING_OVEN_PROGRAM_MICROWAVE_360WATT = "Cooking.Oven.Program.Microwave.360Watt"
    COOKING_OVEN_PROGRAM_MICROWAVE_600WATT = "Cooking.Oven.Program.Microwave.600Watt"
    COOKING_OVEN_PROGRAM_MICROWAVE_900WATT = "Cooking.Oven.Program.Microwave.900Watt"
    COOKING_OVEN_PROGRAM_MICROWAVE_90WATT = "Cooking.Oven.Program.Microwave.90Watt"
    COOKING_OVEN_PROGRAM_MICROWAVE_MAX = "Cooking.Oven.Program.Microwave.Max"
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
    LAUNDRYCARE_DRYER_PROGRAM_ANTISHRINK = "LaundryCare.Dryer.Program.AntiShrink"
    LAUNDRYCARE_DRYER_PROGRAM_BLANKETS = "LaundryCare.Dryer.Program.Blankets"
    LAUNDRYCARE_DRYER_PROGRAM_BUSINESSSHIRTS = (
        "LaundryCare.Dryer.Program.BusinessShirts"
    )
    LAUNDRYCARE_DRYER_PROGRAM_COTTON = "LaundryCare.Dryer.Program.Cotton"
    LAUNDRYCARE_DRYER_PROGRAM_DELICATES = "LaundryCare.Dryer.Program.Delicates"
    LAUNDRYCARE_DRYER_PROGRAM_DESSOUS = "LaundryCare.Dryer.Program.Dessous"
    LAUNDRYCARE_DRYER_PROGRAM_DOWNFEATHERS = "LaundryCare.Dryer.Program.DownFeathers"
    LAUNDRYCARE_DRYER_PROGRAM_HYGIENE = "LaundryCare.Dryer.Program.Hygiene"
    LAUNDRYCARE_DRYER_PROGRAM_INBASKET = "LaundryCare.Dryer.Program.InBasket"
    LAUNDRYCARE_DRYER_PROGRAM_JEANS = "LaundryCare.Dryer.Program.Jeans"
    LAUNDRYCARE_DRYER_PROGRAM_MIX = "LaundryCare.Dryer.Program.Mix"
    LAUNDRYCARE_DRYER_PROGRAM_MYTIME_MYDRYINGTIME = (
        "LaundryCare.Dryer.Program.MyTime.MyDryingTime"
    )
    LAUNDRYCARE_DRYER_PROGRAM_OUTDOOR = "LaundryCare.Dryer.Program.Outdoor"
    LAUNDRYCARE_DRYER_PROGRAM_PILLOW = "LaundryCare.Dryer.Program.Pillow"
    LAUNDRYCARE_DRYER_PROGRAM_SHIRTS15 = "LaundryCare.Dryer.Program.Shirts15"
    LAUNDRYCARE_DRYER_PROGRAM_SUPER40 = "LaundryCare.Dryer.Program.Super40"
    LAUNDRYCARE_DRYER_PROGRAM_SYNTHETIC = "LaundryCare.Dryer.Program.Synthetic"
    LAUNDRYCARE_DRYER_PROGRAM_SYNTHETICREFRESH = (
        "LaundryCare.Dryer.Program.SyntheticRefresh"
    )
    LAUNDRYCARE_DRYER_PROGRAM_TIMECOLD = "LaundryCare.Dryer.Program.TimeCold"
    LAUNDRYCARE_DRYER_PROGRAM_TIMECOLDFIX_TIMECOLD20 = (
        "LaundryCare.Dryer.Program.TimeColdFix.TimeCold20"
    )
    LAUNDRYCARE_DRYER_PROGRAM_TIMECOLDFIX_TIMECOLD30 = (
        "LaundryCare.Dryer.Program.TimeColdFix.TimeCold30"
    )
    LAUNDRYCARE_DRYER_PROGRAM_TIMECOLDFIX_TIMECOLD60 = (
        "LaundryCare.Dryer.Program.TimeColdFix.TimeCold60"
    )
    LAUNDRYCARE_DRYER_PROGRAM_TIMEWARM = "LaundryCare.Dryer.Program.TimeWarm"
    LAUNDRYCARE_DRYER_PROGRAM_TIMEWARMFIX_TIMEWARM30 = (
        "LaundryCare.Dryer.Program.TimeWarmFix.TimeWarm30"
    )
    LAUNDRYCARE_DRYER_PROGRAM_TIMEWARMFIX_TIMEWARM40 = (
        "LaundryCare.Dryer.Program.TimeWarmFix.TimeWarm40"
    )
    LAUNDRYCARE_DRYER_PROGRAM_TIMEWARMFIX_TIMEWARM60 = (
        "LaundryCare.Dryer.Program.TimeWarmFix.TimeWarm60"
    )
    LAUNDRYCARE_DRYER_PROGRAM_TOWELS = "LaundryCare.Dryer.Program.Towels"
    LAUNDRYCARE_WASHER_PROGRAM_AUTO30 = "LaundryCare.Washer.Program.Auto30"
    LAUNDRYCARE_WASHER_PROGRAM_AUTO40 = "LaundryCare.Washer.Program.Auto40"
    LAUNDRYCARE_WASHER_PROGRAM_AUTO60 = "LaundryCare.Washer.Program.Auto60"
    LAUNDRYCARE_WASHER_PROGRAM_CHIFFON = "LaundryCare.Washer.Program.Chiffon"
    LAUNDRYCARE_WASHER_PROGRAM_COTTON = "LaundryCare.Washer.Program.Cotton"
    LAUNDRYCARE_WASHER_PROGRAM_COTTON_COLOUR = (
        "LaundryCare.Washer.Program.Cotton.Colour"
    )
    LAUNDRYCARE_WASHER_PROGRAM_COTTON_COTTONECO = (
        "LaundryCare.Washer.Program.Cotton.CottonEco"
    )
    LAUNDRYCARE_WASHER_PROGRAM_COTTON_ECO4060 = (
        "LaundryCare.Washer.Program.Cotton.Eco4060"
    )
    LAUNDRYCARE_WASHER_PROGRAM_CURTAINS = "LaundryCare.Washer.Program.Curtains"
    LAUNDRYCARE_WASHER_PROGRAM_DARKWASH = "LaundryCare.Washer.Program.DarkWash"
    LAUNDRYCARE_WASHER_PROGRAM_DELICATESSILK = (
        "LaundryCare.Washer.Program.DelicatesSilk"
    )
    LAUNDRYCARE_WASHER_PROGRAM_DESSOUS = "LaundryCare.Washer.Program.Dessous"
    LAUNDRYCARE_WASHER_PROGRAM_DOWNDUVET_DUVET = (
        "LaundryCare.Washer.Program.DownDuvet.Duvet"
    )
    LAUNDRYCARE_WASHER_PROGRAM_DRUMCLEAN = "LaundryCare.Washer.Program.DrumClean"
    LAUNDRYCARE_WASHER_PROGRAM_EASYCARE = "LaundryCare.Washer.Program.EasyCare"
    LAUNDRYCARE_WASHER_PROGRAM_MIX = "LaundryCare.Washer.Program.Mix"
    LAUNDRYCARE_WASHER_PROGRAM_MIX_NIGHTWASH = (
        "LaundryCare.Washer.Program.Mix.NightWash"
    )
    LAUNDRYCARE_WASHER_PROGRAM_MONSOON = "LaundryCare.Washer.Program.Monsoon"
    LAUNDRYCARE_WASHER_PROGRAM_OUTDOOR = "LaundryCare.Washer.Program.Outdoor"
    LAUNDRYCARE_WASHER_PROGRAM_PLUSHTOY = "LaundryCare.Washer.Program.PlushToy"
    LAUNDRYCARE_WASHER_PROGRAM_POWERSPEED59 = "LaundryCare.Washer.Program.PowerSpeed59"
    LAUNDRYCARE_WASHER_PROGRAM_RINSE_RINSESPINDRAIN = (
        "LaundryCare.Washer.Program.Rinse.RinseSpinDrain"
    )
    LAUNDRYCARE_WASHER_PROGRAM_SENSITIVE = "LaundryCare.Washer.Program.Sensitive"
    LAUNDRYCARE_WASHER_PROGRAM_SHIRTSBLOUSES = (
        "LaundryCare.Washer.Program.ShirtsBlouses"
    )
    LAUNDRYCARE_WASHER_PROGRAM_SPORTFITNESS = "LaundryCare.Washer.Program.SportFitness"
    LAUNDRYCARE_WASHER_PROGRAM_SUPER153045_SUPER15 = (
        "LaundryCare.Washer.Program.Super153045.Super15"
    )
    LAUNDRYCARE_WASHER_PROGRAM_SUPER153045_SUPER1530 = (
        "LaundryCare.Washer.Program.Super153045.Super1530"
    )
    LAUNDRYCARE_WASHER_PROGRAM_TOWELS = "LaundryCare.Washer.Program.Towels"
    LAUNDRYCARE_WASHER_PROGRAM_WATERPROOF = "LaundryCare.Washer.Program.WaterProof"
    LAUNDRYCARE_WASHER_PROGRAM_WOOL = "LaundryCare.Washer.Program.Wool"
    LAUNDRYCARE_WASHERDRYER_PROGRAM_COTTON = "LaundryCare.WasherDryer.Program.Cotton"
    LAUNDRYCARE_WASHERDRYER_PROGRAM_COTTON_ECO4060 = (
        "LaundryCare.WasherDryer.Program.Cotton.Eco4060"
    )
    LAUNDRYCARE_WASHERDRYER_PROGRAM_EASYCARE = (
        "LaundryCare.WasherDryer.Program.EasyCare"
    )
    LAUNDRYCARE_WASHERDRYER_PROGRAM_MIX = "LaundryCare.WasherDryer.Program.Mix"
    LAUNDRYCARE_WASHERDRYER_PROGRAM_WASHANDDRY60 = (
        "LaundryCare.WasherDryer.Program.WashAndDry.60"
    )
    LAUNDRYCARE_WASHERDRYER_PROGRAM_WASHANDDRY90 = (
        "LaundryCare.WasherDryer.Program.WashAndDry.90"
    )
