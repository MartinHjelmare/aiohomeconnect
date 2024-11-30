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
    name: str | None
    options: list[Option] | None
    constraints: ProgramConstraints | None


@dataclass
class ProgramConstraints(DataClassJSONMixin):
    """Represent ProgramConstraints."""

    access: str | None


@dataclass
class ArrayOfAvailablePrograms(DataClassJSONMixin):
    """Represent ArrayOfAvailablePrograms."""

    programs: list[EnumerateAvailableProgram]


@dataclass
class EnumerateAvailableProgramConstraints(DataClassJSONMixin):
    """Represent EnumerateAvailableProgramConstraints."""

    execution: Execution | None


@dataclass
class EnumerateAvailableProgram(DataClassJSONMixin):
    """Represent EnumerateAvailableProgram."""

    key: ProgramKey
    name: str | None
    constraints: EnumerateAvailableProgramConstraints | None


@dataclass
class ArrayOfPrograms(DataClassJSONMixin):
    """Represent ArrayOfPrograms."""

    programs: list[EnumerateProgram]
    active: Program | None
    selected: Program | None


@dataclass
class EnumerateProgramConstraints(DataClassJSONMixin):
    """Represent EnumerateProgramConstraints."""

    available: bool | None
    execution: Execution | None


@dataclass
class EnumerateProgram(DataClassJSONMixin):
    """Represent EnumerateProgram."""

    key: ProgramKey
    name: str | None
    constraints: EnumerateProgramConstraints | None


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
    name: str | None
    options: list[ProgramDefinitionOption] | None


@dataclass
class ProgramDefinitionConstraints(DataClassJSONMixin):
    """Represent ProgramDefinitionConstraints."""

    min: int | None
    max: int | None
    step_size: int | None = field(metadata=field_options(alias="stepsize"))
    allowed_values: list[str | None] | None = field(
        metadata=field_options(alias="allowedvalues")
    )
    display_values: list[str | None] | None = field(
        metadata=field_options(alias="displayvalues")
    )
    default: Any | None
    live_update: bool | None = field(metadata=field_options(alias="liveupdate"))


@dataclass
class ProgramDefinitionOption(DataClassJSONMixin):
    """Represent ProgramDefinitionOption."""

    key: OptionKey
    name: str | None
    type: str
    unit: str | None
    constraints: ProgramDefinitionConstraints | None


@dataclass
class Option(DataClassJSONMixin):
    """Represent Option."""

    key: OptionKey
    name: str | None
    value: Any
    display_value: str | None = field(metadata=field_options(alias="displayvalue"))
    unit: str | None


@dataclass
class ArrayOfOptions(DataClassJSONMixin):
    """List of options."""

    options: list[Option]


class OptionKey(StrEnum):
    """Represent an option key."""

    # TODO(Martin Hjelmare): Add all option keys  # noqa: FIX002
    # https://github.com/MartinHjelmare/aiohomeconnect/issues/22
    # Missing option categories still to be added 20241129:
    # Dryer, Hood, Oven, Warming Drawer, Washer

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
    DISHCARE_DISHWASHER_BRILLIANCE_DRY = "Dishcare.Dishwasher.Option.BrillianceDry"
    DISHCARE_DISHWASHER_ECO_DRY = "Dishcare.Dishwasher.Option.EcoDry"
    DISHCARE_DISHWASHER_EXTRA_DRY = "Dishcare.Dishwasher.Option.ExtraDry"
    DISHCARE_DISHWASHER_HALF_LOAD = "Dishcare.Dishwasher.Option.HalfLoad"
    DISHCARE_DISHWASHER_HYGIENE_PLUS = "Dishcare.Dishwasher.Option.HygienePlus"
    DISHCARE_DISHWASHER_INTENSIV_ZONE = "Dishcare.Dishwasher.Option.IntensivZone"
    DISHCARE_DISHWASHER_SILENCE_ON_DEMAND = "Dishcare.Dishwasher.Option.SilenceOnDemand"
    DISHCARE_DISHWASHER_VARIO_SPEED_PLUS = "Dishcare.Dishwasher.Option.VarioSpeedPlus"
    DISHCARE_DISHWASHER_ZEOLITE_DRY = "Dishcare.Dishwasher.Option.ZeoliteDry"


class ProgramKey(StrEnum):
    """Represent a program key."""

    # TODO(Martin Hjelmare): Add all program keys  # noqa: FIX002
    # https://github.com/MartinHjelmare/aiohomeconnect/issues/23
    # Missing program categories still to be added 20241129:
    # Dryer, Hood, Oven, Warming Drawer, Washer, Washer Dryer

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
