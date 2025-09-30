"""Karrio universal data types and units definitions"""

from ctypes import util
import attr
import typing
import numbers
import pathlib
import functools
import phonenumbers
import karrio.core.utils as utils
import karrio.core.models as models
import karrio.core.errors as errors


@attr.s(auto_attribs=True)
class PackagePreset:
    width: float = None
    height: float = None
    length: float = None
    weight: float = None
    volume: float = None
    thickness: float = None
    weight_unit: str = "LB"
    dimension_unit: str = "IN"
    packaging_type: str = None


class LabelType(utils.StrEnum):
    PDF = "PDF"
    ZPL = "ZPL"
    PNG = "PNG"


class DocFormat(utils.StrEnum):
    gif = "GIF"
    jpg = "JPG"
    pdf = "PDF"
    png = "PNG"


class PackagingUnit(utils.StrEnum):
    envelope = "Small Envelope"
    pak = "Pak"
    tube = "Tube"
    pallet = "Pallet"
    small_box = "Small Box"
    medium_box = "Medium Box"
    your_packaging = "Your Packaging"


class PaymentType(utils.StrEnum):
    sender = "SENDER"
    recipient = "RECIPIENT"
    third_party = "THIRD_PARTY"


class CreditCardType(utils.StrEnum):
    visa = "Visa"
    mastercard = "Mastercard"
    american_express = "AmericanExpress"


class CustomsContentType(utils.StrEnum):
    documents = "DOCUMENTS"
    gift = "GIFT"
    sample = "SAMPLE"
    merchandise = "MERCHANDISE"
    return_merchandise = "RETURN_MERCHANDISE"
    other = "OTHER"


class Incoterm(utils.StrEnum):
    """universal international shipment incoterm (term of trades)"""

    CFR = "Cost and Freight"
    CIF = "Cost Insurance and Freight"
    CIP = "Carriage and Insurance Paid"
    CPT = "Carriage Paid To"
    DAP = "Delivery at Place"
    DAF = "Delivered at Frontier"
    DDP = "Delivery Duty Paid"
    DDU = "Delivery Duty Unpaid"
    DEQ = "Delivered Ex Quay"
    DES = "Delivered Ex Ship"
    EXW = "Ex Works"
    FAS = "Free Alongside Ship"
    FCA = "Free Carrier"
    FOB = "Free On Board"


class WeightUnit(utils.StrEnum):
    """universal weight units"""

    KG = "KG"
    LB = "LB"
    OZ = "OZ"
    G = "G"


class DimensionUnit(utils.StrEnum):
    """universal dimension units"""

    CM = "CM"
    IN = "IN"


class VolumeUnit(utils.StrEnum):
    """universal dimension units"""

    l = "l"
    m3 = "m3"
    i3 = "i3"
    ft3 = "ft3"
    cm3 = "cm3"

    """ mapping from dimension units to volume units """
    CM = "cm3"
    IN = "i3"


class FreightClass(utils.Enum):
    """universal freight_class units"""

    freight_class_50 = 50
    freight_class_55 = 55
    freight_class_60 = 60
    freight_class_65 = 65
    freight_class_70 = 70
    freight_class_77 = 77
    freight_class_77_5 = 77.5
    freight_class_85 = 85
    freight_class_92_5 = 92.5
    freight_class_100 = 100
    freight_class_110 = 110
    freight_class_125 = 125
    freight_class_150 = 150
    freight_class_175 = 175
    freight_class_200 = 200
    freight_class_250 = 250
    freight_class_300 = 300
    freight_class_400 = 400


class UploadDocumentType(utils.StrEnum):
    """universal upload document types"""

    certificate_of_origin = "certificate_of_origin"
    commercial_invoice = "commercial_invoice"
    pro_forma_invoice = "pro_forma_invoice"
    packing_list = "packing_list"
    other = "other"


class MeasurementOptionsType(typing.NamedTuple):
    quant: typing.Optional[float] = None

    min_in: typing.Optional[float] = None
    min_cm: typing.Optional[float] = None
    min_lb: typing.Optional[float] = None
    min_kg: typing.Optional[float] = None
    min_oz: typing.Optional[float] = None
    min_g: typing.Optional[float] = None
    max_in: typing.Optional[float] = None
    max_cm: typing.Optional[float] = None
    max_lb: typing.Optional[float] = None
    max_kg: typing.Optional[float] = None
    max_oz: typing.Optional[float] = None
    max_g: typing.Optional[float] = None

    min_volume: typing.Optional[float] = None
    max_volume: typing.Optional[float] = None


class CarrierCapabilities(utils.Enum):
    pickup = "pickup"
    rating = "rating"
    shipping = "shipping"
    tracking = "tracking"
    paperless = "paperless"
    manifest = "manifest"

    @classmethod
    def get_capabilities(cls):
        return [c.name for c in list(cls)]

    @classmethod
    def map_capability(cls, method_name: str):
        if "rate" in method_name:
            return "rating"
        elif "tracking" in method_name:
            return "tracking"
        elif "shipment" in method_name:
            return "shipping"
        elif "pickup" in method_name:
            return "pickup"
        elif "address" in method_name:
            return "shipping"
        elif "document" in method_name:
            return "paperless"
        elif "manifest" in method_name:
            return "manifest"

        return None


class Dimension:
    """The dimension common processing helper"""

    def __init__(
        self,
        value: float,
        unit: typing.Union[DimensionUnit, str] = DimensionUnit.CM,
        options: MeasurementOptionsType = MeasurementOptionsType(),
    ):
        self._value = value
        self._unit = DimensionUnit[unit] if isinstance(unit, str) else unit

        # Options mapping
        self._min_in = options.min_in
        self._min_cm = options.min_cm
        self._quant = options.quant

    def __getitem__(self, item):
        return getattr(self, item)

    def _compute(self, value: float, min_value: float = None):
        below_min = min_value is not None and value < min_value
        return utils.NF.decimal(
            value=(min_value if below_min else value), quant=self._quant
        )

    @property
    def unit(self) -> str:
        if self._unit is None:
            return None

        return self._unit.value

    @property
    def value(self):
        if self._unit is None or self._value is None:
            return None

        return self.__getattribute__(str(self._unit.name))

    @property
    def CM(self):
        if self._unit is None or self._value is None:
            return None
        if self._unit == DimensionUnit.IN:
            return self._compute(self._value * 2.54, self._min_cm)
        else:
            return self._compute(self._value, self._min_cm)

    @property
    def IN(self):
        if self._unit is None or self._value is None:
            return None
        if self._unit == DimensionUnit.CM:
            return self._compute(self._value / 2.54, self._min_in)
        else:
            return self._compute(self._value, self._min_in)

    @property
    def M(self):
        if self._unit is None or self._value is None:
            return None
        else:
            return self._compute(self.CM / 100)

    @property
    def MM(self):
        if self._unit is None or self._value is None:
            return None
        else:
            return self._compute(self.CM * 10)

    def map(self, options: MeasurementOptionsType):
        return Dimension(value=self._value, unit=self._unit, options=options)


class Volume:
    """The volume common processing helper"""

    def __init__(
        self,
        side1: Dimension = None,
        side2: Dimension = None,
        side3: Dimension = None,
        value: float = None,
        unit: typing.Union[VolumeUnit, str] = VolumeUnit.cm3,
        options: MeasurementOptionsType = MeasurementOptionsType(),
    ):
        self._side1 = side1
        self._side2 = side2
        self._side3 = side3

        self._value = value
        self._unit = VolumeUnit[unit] if isinstance(unit, str) else unit

        self._quant = 0.01
        self._min_volume = options.min_volume

    def __getitem__(self, item):
        return getattr(self, item)

    def _compute(self, value: float):
        below_min = self._min_volume is not None and value < self._min_volume
        return utils.NF.decimal(
            value=(self._min_volume if below_min else value),
            quant=self._quant,
        )

    @property
    def unit(self) -> str:
        if self._unit is None:
            return None

        return self._unit.value

    @property
    def value(self):
        missing_side_value = not all(
            [
                getattr(self._side1, "value", None),
                getattr(self._side2, "value", None),
                getattr(self._side3, "value", None),
            ]
        )
        missing_value = self._unit is None or self._value is None

        if missing_side_value and missing_value:
            return None

        if not missing_value:
            return self._value

        return self._compute(self._side1.value * self._side2.value * self._side3.value)

    @property
    def l(self):
        if self.value is None:
            return None
        if self._unit == VolumeUnit.m3:
            return self._compute(self.value * 1000)
        elif self._unit == VolumeUnit.i3:
            return self._compute(self.value / 61.024)
        elif self._unit == VolumeUnit.ft3:
            return self._compute(self.value * 28.317)
        if self._unit == VolumeUnit.cm3:
            return self._compute(self.value / 1000)
        else:
            return self.value

    @property
    def m3(self):
        if self.value is None:
            return None
        if self._unit == VolumeUnit.l:
            return self._compute(self.value / 1000)
        if self._unit == VolumeUnit.cm3:
            return self._compute(self.value / 1e6)
        elif self._unit == VolumeUnit.i3:
            return self._compute(self.value / 61020)
        elif self._unit == VolumeUnit.ft3:
            return self._compute(self.value / 35.315)
        else:
            return self.value

    @property
    def i3(self):
        if self.value is None:
            return None
        if self._unit == VolumeUnit.l:
            return self._compute(self.value * 61.024)
        if self._unit == VolumeUnit.m3:
            return self._compute(self.value * 1000000)
        elif self._unit == VolumeUnit.cm3:
            return self._compute(self.value / 16.387)
        elif self._unit == VolumeUnit.ft3:
            return self._compute(self.value * 1728)
        else:
            return self.value

    @property
    def ft3(self):
        if self.value is None:
            return None
        if self._unit == VolumeUnit.l:
            return self._compute(self.value / 28.317)
        if self._unit == VolumeUnit.m3:
            return self._compute(self.value * 35.315)
        elif self._unit == VolumeUnit.i3:
            return self._compute(self.value / 1728)
        elif self._unit == VolumeUnit.cm3:
            return self._compute(self.value / 28320)
        else:
            return self.value

    @property
    def cm3(self):
        if self.value is None:
            return None
        if self._unit == VolumeUnit.l:
            return self._compute(self.value * 1000)
        if self._unit == VolumeUnit.m3:
            return self._compute(self.value * 1e6)
        elif self._unit == VolumeUnit.i3:
            return self._compute(self.value * 16.387)
        elif self._unit == VolumeUnit.ft3:
            return self._compute(self.value * 28320)
        else:
            return self.value

    @property
    def cubic_meter(self):
        return self.m3

    def map(self, options: MeasurementOptionsType):
        return Volume(
            side1=self._side1,
            side2=self._side2,
            side3=self._side3,
            value=self._value,
            unit=self._unit,
            options=options,
        )


class Girth:
    """The girth common processing helper"""

    def __init__(
        self, side1: Dimension = None, side2: Dimension = None, side3: Dimension = None
    ):
        self._side1 = side1
        self._side2 = side2
        self._side3 = side3

    @property
    def value(self):
        sides = [self._side1.CM, self._side2.CM, self._side3.CM]
        if not any(sides):
            return None

        sides.sort()
        small_side1, small_side2, _ = sides
        return utils.NF.decimal((small_side1 + small_side2) * 2)


class Weight:
    """The weight common processing helper"""

    def __init__(
        self,
        value: float,
        unit: typing.Union[WeightUnit, str] = WeightUnit.KG,
        options: MeasurementOptionsType = MeasurementOptionsType(),
    ):
        self._value = value
        self._unit = WeightUnit[unit] if isinstance(unit, str) else unit

        # Options mapping
        self._min_lb = options.min_lb
        self._min_kg = options.min_kg
        self._min_oz = options.min_oz
        self._min_g = options.min_g
        self._quant = options.quant

    def __getitem__(self, item):
        return getattr(self, item)

    def _compute(self, value: float, min_value: float = None) -> typing.Optional[float]:
        below_min = min_value is not None and value < min_value
        return utils.NF.decimal(
            value=(min_value if below_min else value), quant=self._quant
        )

    @property
    def unit(self) -> str:
        if self._unit is None:
            return None

        return self._unit.value

    @property
    def value(self) -> typing.Optional[float]:
        if self._unit is None or self._value is None:
            return None

        return self.__getattribute__(str(self._unit.name))

    @property
    def KG(self) -> typing.Optional[float]:
        if self._unit is None or self._value is None:
            return None
        if self._unit == WeightUnit.KG:
            return self._compute(self._value, self._min_kg)
        elif self._unit == WeightUnit.LB:
            return self._compute(self._value / 2.205, self._min_kg)
        elif self._unit == WeightUnit.OZ:
            return self._compute(self._value / 35.274, self._min_kg)
        elif self._unit == WeightUnit.G:
            return self._compute(self._value / 1000, self._min_kg)

        return None

    @property
    def LB(self) -> typing.Optional[float]:
        if self._unit is None or self._value is None:
            return None
        if self._unit == WeightUnit.LB:
            return self._compute(self._value, self._min_lb)
        elif self._unit == WeightUnit.KG:
            return self._compute(self._value * 2.205, self._min_lb)
        elif self._unit == WeightUnit.OZ:
            return self._compute(self._value / 16, self._min_lb)
        elif self._unit == WeightUnit.G:
            return self._compute(self._value / 453.6, self._min_lb)

        return None

    @property
    def OZ(self) -> typing.Optional[float]:
        if self._unit is None or self._value is None:
            return None
        elif self._unit == WeightUnit.OZ:
            return self._compute(self._value, self._min_oz)
        if self._unit == WeightUnit.LB:
            return self._compute(self._value * 16, self._min_oz)
        elif self._unit == WeightUnit.KG:
            return self._compute(self._value * 35.274, self._min_oz)
        elif self._unit == WeightUnit.G:
            return self._compute(self._value / 28.35, self._min_oz)

        return None

    @property
    def G(self) -> typing.Optional[float]:
        if self._unit is None or self._value is None:
            return None
        elif self._unit == WeightUnit.G:
            return self._compute(self._value, self._min_g)
        if self._unit == WeightUnit.LB:
            return self._compute(self._value * 453.6, self._min_g)
        elif self._unit == WeightUnit.KG:
            return self._compute(self._value * 1000, self._min_g)
        elif self._unit == WeightUnit.OZ:
            return self._compute(self._value * 28.35, self._min_g)

        return None

    def map(self, options: MeasurementOptionsType):
        return Weight(value=self._value, unit=self._unit, options=options)


class Product(models.Commodity):
    """The item common processing helper"""

    def __init__(
        self,
        item: models.Commodity,
        weight_unit: str = None,
    ):
        self.item = item
        self._weight_unit: str = weight_unit or item.weight_unit or "LB"

    def __getitem__(self, item):
        return getattr(self.item, item, None)

    def __getattr__(self, item):
        return self[item]

    @property
    def weight_unit(self):
        return self._weight_unit

    @property
    def weight(self):
        if self.item.weight is None:
            return None

        _weight_value = Weight(
            self.item.weight,
            self.item.weight_unit or self._weight_unit,
        )

        return typing.cast(float, _weight_value[self._weight_unit])

    @property
    def quantity(self) -> int:  # type: ignore
        _quantity = utils.NF.integer(self.item.quantity)
        if _quantity is None:
            return 1

        return _quantity


class Products(typing.Iterable[Product]):
    """The commoditiy/item collection common processing helper"""

    def __init__(
        self,
        items: typing.List[models.Commodity],
        weight_unit: str = None,
    ):
        self._items = [Product(item, weight_unit=weight_unit) for item in items]
        self._weight_unit = (
            weight_unit or self._items[0].weight_unit if any(self._items) else None
        )

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> Product:
        return self._items[index]

    def __iter__(self) -> typing.Iterator[Product]:
        return iter(self._items)

    @property
    def quantity(self):
        return sum((item.quantity for item in self._items), 0)

    @property
    def value_amount(self):
        return sum(
            (
                item.value_amount * item.quantity
                for item in self._items
                if utils.NF.decimal(item.value_amount) is not None
            ),
            0.0,
        )

    @property
    def weight(self) -> Weight:
        return Weight(
            sum([item.weight * item.quantity for item in self._items], 0.0),
            self._weight_unit,
        )

    @property
    def description(self) -> typing.Optional[str]:
        descriptions = set([item.description for item in self._items])
        description: typing.Optional[str] = utils.SF.concat_str(
            *list(descriptions), join=True
        )  # type:ignore

        return description


class Package:
    """The parcel common processing helper"""

    def __init__(
        self,
        parcel: models.Parcel,
        template: PackagePreset = None,
        options: "ShippingOptions" = None,
        package_option_type: typing.Type[utils.Enum] = utils.Enum,
        weight_unit: str = None,
        dimension_unit: str = None,
        shipping_options_initializer: typing.Callable = None,
    ):
        self.parcel: models.Parcel = parcel
        self.preset: PackagePreset = template or PackagePreset()

        _options = {**parcel.options, **getattr(options, "content", {})}
        self._options: "ShippingOptions" = (
            shipping_options_initializer(_options)
            if shipping_options_initializer is not None
            else ShippingOptions(_options, package_option_type)
        )
        self._dimension_unit = (
            dimension_unit or self.parcel.dimension_unit or self.preset.dimension_unit
        )
        self._weight_unit = (
            weight_unit or self.parcel.weight_unit or self.preset.weight_unit
        )

    def _compute_dimension(self, value):
        _dimension_unit = (
            self.parcel.dimension_unit or self._dimension_unit
            if self.preset.width is None
            else self.preset.dimension_unit
        )
        _dimension = Dimension(value, DimensionUnit[_dimension_unit])

        if _dimension_unit == self.dimension_unit.value:
            return _dimension

        return Dimension(_dimension[self.dimension_unit.value], self.dimension_unit)

    def _compute_weight(self, value):
        _weight_unit = self.parcel.weight_unit or self._weight_unit
        _weight = Weight(value, _weight_unit)

        if _weight_unit == self.weight_unit.value:
            return _weight

        return Weight(_weight[self.weight_unit.value], self.weight_unit)

    @property
    def dimension_unit(self) -> DimensionUnit:
        if self.weight_unit == WeightUnit.KG:
            return DimensionUnit.CM

        return DimensionUnit.IN

    @property
    def weight_unit(self) -> WeightUnit:
        return WeightUnit[self._weight_unit]

    @property
    def packaging_type(self):
        return self.parcel.packaging_type or self.preset.packaging_type

    @property
    def weight(self) -> Weight:
        return self._compute_weight(self.parcel.weight or self.preset.weight)

    @property
    def width(self) -> Dimension:
        return self._compute_dimension(self.preset.width or self.parcel.width)

    @property
    def height(self) -> Dimension:
        return self._compute_dimension(self.preset.height or self.parcel.height)

    @property
    def length(self) -> Dimension:
        return self._compute_dimension(self.preset.length or self.parcel.length)

    @property
    def girth(self) -> Girth:
        return Girth(self.width, self.length, self.height)

    @property
    def volume(self) -> Volume:
        return Volume(
            self.width, self.length, self.height, unit=self.dimension_unit.value
        )

    @property
    def thickness(self) -> Dimension:
        return self._compute_dimension(self.preset.thickness)

    @property
    def description(self) -> typing.Optional[str]:
        if any(self.parcel.description or ""):
            return self.parcel.description

        descriptions = [item.title or item.description for item in self.items]
        description: typing.Optional[str] = utils.SF.concat_str(
            *descriptions, join=True
        )  # type:ignore

        return description

    @property
    def has_dimensions(self) -> bool:
        return any(
            [
                self.length.value,
                self.width.value,
                self.height.value,
            ]
        )

    @property
    def options(self) -> "ShippingOptions":
        return self._options

    @property
    def items(self) -> Products:
        _items = self.parcel.items or []

        return Products(_items, self.weight_unit.value)

    @property
    def total_value(self) -> typing.Optional[float]:
        if not any(self.parcel.items or []):
            return None

        return self.items.value_amount

    @property
    def reference_number(self) -> typing.Optional[str]:
        return self.parcel.reference_number


class Packages(typing.Iterable[Package]):
    """The parcel collection common processing helper"""

    def __init__(
        self,
        parcels: typing.List[models.Parcel],
        presets: typing.Type[utils.Enum] = None,
        required: typing.List[str] = None,
        max_weight: Weight = None,
        options: "ShippingOptions" = None,
        package_option_type: typing.Type[utils.Enum] = utils.Enum,
        shipping_options_initializer: typing.Callable = None,
    ):
        self._compatible_units = self._compute_compatible_units(parcels, presets)
        self._options = options or ShippingOptions({}, package_option_type)
        self._items = [
            Package(
                parcel,
                self._compute_preset(parcel, presets),
                options=self._options,
                package_option_type=package_option_type,
                weight_unit=self._compatible_units[0].value,
                dimension_unit=self._compatible_units[1].value,
                shipping_options_initializer=shipping_options_initializer,
            )
            for parcel in parcels
        ]
        self._required = required
        self._max_weight = max_weight
        self._package_option_type = package_option_type
        self._shipping_options_initializer = shipping_options_initializer

        self.validate()

    def __getitem__(self, index: int) -> Package:
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> typing.Iterator[Package]:
        return iter(self._items)

    @property
    def single(self) -> Package:
        if len(self._items) > 1:
            raise errors.MultiParcelNotSupportedError()
        return self._items[0]

    def _compute_compatible_units(
        self,
        parcels: typing.List[models.Parcel],
        presets: typing.Type[utils.Enum],
    ):
        master_weight_unit = next(
            (
                p.weight_unit
                or getattr(self._compute_preset(p, presets), "weight_unit", None)
                for p in parcels
            ),
            None,
        )

        if master_weight_unit == WeightUnit.KG.value:
            return (WeightUnit.KG, DimensionUnit.CM)

        return (WeightUnit.LB, DimensionUnit.IN)

    def _compute_preset(self, parcel: models.Parcel, presets: typing.Type[utils.Enum]):
        if (presets is None) | (
            presets is not None and parcel.package_preset not in presets
        ):
            return None

        return presets[parcel.package_preset].value

    @property
    def weight(self) -> Weight:
        unit, _ = self.compatible_units
        value = sum(
            pkg.weight[unit.name]
            for pkg in self._items
            if pkg.weight[unit.name] is not None
        )

        if value is None or not any(self._items):
            return Weight(None, None)

        return Weight(unit=unit, value=value)

    @property
    def volume(self) -> Volume:
        if not any([pkg.volume.value for pkg in self._items]):
            return Volume(value=None)

        _, _dimension_unit = self._compatible_units
        _volume_unit = VolumeUnit[_dimension_unit.name]
        _total_volume = sum(
            [
                pkg.volume[_volume_unit.name]
                for pkg in self._items
                if pkg.volume is not None
            ],
            0.0,
        )

        return Volume(value=_total_volume, unit=_volume_unit)

    @property
    def package_type(self) -> str:
        return (
            (self._items[0].packaging_type or "your_packaging")
            if len(self._items) == 1
            else None
        )

    @property
    def is_document(self) -> bool:
        return all([pkg.parcel.is_document for pkg in self._items])

    @property
    def description(self) -> typing.Optional[str]:
        descriptions = set([item.description for item in self._items])
        description: typing.Optional[str] = utils.SF.concat_str(
            *list(descriptions), join=True
        )  # type:ignore

        return description

    @property
    def content(self) -> typing.Optional[str]:
        contents = set([item.parcel.content for item in self._items])
        content: typing.Optional[str] = utils.SF.concat_str(
            *list(contents), join=True
        )  # type:ignore

        return content

    @property
    def options(self) -> "ShippingOptions":
        def merge_options(acc, pkg) -> dict:
            """Merge package options into one
            if an item exists in one and is of type int or float,
            add them up.
            """
            return {
                **acc,
                **{
                    key: (
                        (val + acc[key])
                        if (
                            key in acc
                            and isinstance(val, numbers.Number)
                            and not isinstance(val, bool)
                        )
                        else val
                    )
                    for key, val in pkg.options.content.items()
                },
            }

        options: dict = functools.reduce(
            merge_options,
            self._items,
            self._options.content,
        )

        if self._shipping_options_initializer is not None:
            return self._shipping_options_initializer(options)

        return ShippingOptions(options, self._package_option_type)

    @property
    def compatible_units(self) -> typing.Tuple[WeightUnit, DimensionUnit]:
        return self._compatible_units

    @property
    def weight_unit(self) -> str:
        _weight_unit, _ = self._compatible_units
        return _weight_unit.value

    @property
    def items(self) -> Products:
        _weight_unit, _ = self.compatible_units
        _items: typing.List[models.Commodity] = functools.reduce(
            lambda acc, pkg: [*acc, *[p.item for p in pkg.items]],
            self._items,
            [],
        )

        return Products(_items, _weight_unit.value)

    @property
    def total_value(self) -> typing.Optional[float]:
        if not any([_.total_value for _ in self._items]):
            return None

        return sum(
            [pkg.total_value for pkg in self._items if pkg.total_value is not None], 0.0
        )

    def validate(self, required: typing.List[str] = None, max_weight: Weight = None):
        required = required or self._required
        max_weight = max_weight or self._max_weight

        if any(check is not None for check in [required, max_weight]):
            validation_errors = {}
            for index, package in enumerate(self._items):
                if required is not None:
                    for field in required:
                        prop = getattr(package, field)

                        if prop is None or (
                            hasattr(prop, "value") and prop.value is None
                        ):
                            validation_errors.update(
                                {
                                    f"parcel[{index}].{field}": errors.FieldErrorCode.required
                                }
                            )

                if (
                    max_weight is not None
                    and (package.weight.LB or 0.0) > max_weight.LB
                ):
                    validation_errors.update(
                        {f"parcel[{index}].weight": errors.FieldErrorCode.exceeds}
                    )

            if any(validation_errors.items()):
                raise errors.FieldError(validation_errors)

    @staticmethod
    def map(
        parcels: typing.List[models.Parcel],
        presets: typing.Type[utils.Enum] = None,
        required: typing.List[str] = None,
        max_weight: Weight = None,
        options: "ShippingOptions" = None,
        package_option_type: typing.Type[utils.Enum] = utils.Enum,
        shipping_options_initializer: typing.Callable = None,
    ) -> typing.Union[typing.List[Package], "Packages"]:
        return typing.cast(
            typing.Union[typing.List[Package], Packages],
            Packages(
                parcels,
                presets,
                required,
                max_weight,
                options,
                package_option_type,
                shipping_options_initializer,
            ),
        )


class Options:
    """The options common processing helper"""

    def __init__(
        self,
        options: dict,
        option_type: typing.Type[utils.Enum] = utils.Enum,
        items_filter: typing.Callable[[str], bool] = None,
        base_option_type: typing.Type[utils.Enum] = utils.Enum,
    ):
        option_values: typing.Dict[str, utils.OptionEnum] = {}

        for key, val in options.items():
            if option_type is not None and key in option_type:
                _val = option_type[key].value(val)
                _key = option_type[key].name
                option_values[_key] = _val
            elif key in base_option_type and key:
                _val = base_option_type[key].value(val)
                _key = key
                option_values[key] = _val

        self._raw_options = options
        self._options = option_values
        self._option_list = self._filter(
            option_values, (items_filter or utils.identity)
        )

    def __getitem__(self, item):
        return self._options.get(item) or utils.OptionEnum("")

    def __getattr__(self, item):
        return self[item]

    def __contains__(self, item) -> bool:
        return item in self._options

    def __len__(self) -> int:
        return len(self._options.items())

    def __iter__(self) -> typing.Iterator[typing.Tuple[str, typing.Any]]:
        return iter(self._options.items())

    def _filter(self, option_values, items_filter):
        return [
            (key, option) for key, option in option_values.items() if items_filter(key)
        ]

    def items(self) -> typing.List[typing.Tuple[str, typing.Optional[str], typing.Any]]:
        return self._option_list

    @property
    def content(self) -> dict:
        return {key: option.state for key, option in self._options.items()}

    @property
    def has_content(self) -> bool:
        return any(o for o in self._options)


class ShippingOption(utils.Enum):
    """universal shipment options (special services)"""

    currency = utils.OptionEnum("currency")
    is_return = utils.OptionEnum("is_return", bool)
    insurance = utils.OptionEnum("insurance", float)
    cash_on_delivery = utils.OptionEnum("COD", float)
    shipment_note = utils.OptionEnum("shipment_note")
    dangerous_good = utils.OptionEnum("dangerous_good", bool)
    declared_value = utils.OptionEnum("declared_value", float)
    paperless_trade = utils.OptionEnum("paperless_trade", bool)
    sms_notification = utils.OptionEnum("sms_notification", bool)
    email_notification = utils.OptionEnum("email_notification", bool)
    email_notification_to = utils.OptionEnum("email_notification_to")
    signature_confirmation = utils.OptionEnum("signature_confirmation", bool)
    saturday_delivery = utils.OptionEnum("saturday_delivery", bool)
    sunday_delivery = utils.OptionEnum("sunday_delivery", bool)
    doc_files = utils.OptionEnum("doc_files", utils.DP.to_dict)
    doc_references = utils.OptionEnum("doc_references", utils.DP.to_dict)
    hold_at_location = utils.OptionEnum("hold_at_location", bool)
    hold_at_location_address = utils.OptionEnum(
        "hold_at_location_address",
        functools.partial(utils.DP.to_object, models.Address),
    )
    shipper_instructions = utils.OptionEnum("shipper_instructions")
    recipient_instructions = utils.OptionEnum("recipient_instructions")

    """TODO: dreprecate these"""
    shipment_date = utils.OptionEnum("shipment_date")

    """TODO: standardize to these"""
    shipping_date = utils.OptionEnum("shipping_date")  # format: %Y-%m-%dT%H:%M

    invoice_number = utils.OptionEnum("invoice_number")
    invoice_date = utils.OptionEnum("invoice_date")


class ShippingOptions(Options):
    """The options common processing helper"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, base_option_type=ShippingOption)

    @property
    def cash_on_delivery(self) -> utils.OptionEnum:
        return self[ShippingOption.cash_on_delivery.name]

    @property
    def currency(self) -> utils.OptionEnum:
        return self[ShippingOption.currency.name]

    @property
    def insurance(self) -> utils.OptionEnum:
        return self[ShippingOption.insurance.name]

    @property
    def declared_value(self) -> utils.OptionEnum:
        return self[ShippingOption.declared_value.name]

    @property
    def dangerous_good(self) -> utils.OptionEnum:
        return self[ShippingOption.dangerous_good.name]

    @property
    def email_notification(self) -> utils.OptionEnum:
        if ShippingOption.email_notification.name in self:
            return self[ShippingOption.email_notification.name]

        return ShippingOption.email_notification.value(True)

    @property
    def sms_notification(self) -> utils.OptionEnum:
        return self[ShippingOption.sms_notification.name]

    @property
    def email_notification_to(self) -> utils.OptionEnum:
        return self[ShippingOption.email_notification_to.name]

    @property
    def shipment_date(self) -> utils.OptionEnum:
        # Check if shipment_date is not defined and fallback to shipping_date
        if not self[ShippingOption.shipment_date.name].state:
            return utils.OptionEnum(
                "shipment_date",
                str,
                utils.DF.fdate(
                    self._raw_options.get("shipping_date"), "%Y-%m-%dT%H:%M"
                ),
            )

        return self[ShippingOption.shipment_date.name]

    @property
    def shipping_date(self) -> utils.OptionEnum:
        return self[ShippingOption.shipping_date.name]

    @property
    def signature_confirmation(self) -> utils.OptionEnum:
        return self[ShippingOption.signature_confirmation.name]

    @property
    def hold_at_location(self) -> utils.OptionEnum:
        return self[ShippingOption.hold_at_location.name]

    @property
    def paperless_trade(self) -> utils.OptionEnum:
        return self[ShippingOption.paperless_trade.name]

    @property
    def doc_files(self) -> utils.OptionEnum:
        return self[ShippingOption.doc_files.name]

    @property
    def doc_references(self) -> utils.OptionEnum:
        return self[ShippingOption.doc_references.name]

    @property
    def shipment_note(self) -> utils.OptionEnum:
        return self[ShippingOption.shipment_note.name]

    @property
    def shipper_instructions(self) -> utils.OptionEnum:
        return self[ShippingOption.shipper_instructions.name]

    @property
    def recipient_instructions(self) -> utils.OptionEnum:
        return self[ShippingOption.recipient_instructions.name]

    @property
    def invoice_number(self) -> utils.OptionEnum:
        return self[ShippingOption.invoice_number.name]

    @property
    def invoice_date(self) -> utils.OptionEnum:
        return self[ShippingOption.invoice_date.name]


class CustomsOption(utils.Enum):
    """common shipment customs identifiers"""

    aes = utils.OptionEnum("aes")
    ioss = utils.OptionEnum("ioss")
    eel_pfc = utils.OptionEnum("eel_pfc")
    nip_number = utils.OptionEnum("nip_number")
    eori_number = utils.OptionEnum("eori_number")
    license_number = utils.OptionEnum("license_number")
    certificate_number = utils.OptionEnum("certificate_number")
    vat_registration_number = utils.OptionEnum("vat_registration_number")


class CustomsOptions(Options):
    """The options common processing helper"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, base_option_type=CustomsOption)

    @property
    def aes(self) -> utils.OptionEnum:
        return self[CustomsOption.aes.name]

    @property
    def eel_pfc(self) -> utils.OptionEnum:
        return self[CustomsOption.eel_pfc.name]

    @property
    def nip_number(self) -> utils.OptionEnum:
        return self[CustomsOption.nip_number.name]

    @property
    def eori_number(self) -> utils.OptionEnum:
        return self[CustomsOption.eori_number.name]

    @property
    def license_number(self) -> utils.OptionEnum:
        return self[CustomsOption.license_number.name]

    @property
    def certificate_number(self) -> utils.OptionEnum:
        return self[CustomsOption.certificate_number.name]

    @property
    def vat_registration_number(self) -> utils.OptionEnum:
        return self[CustomsOption.vat_registration_number.name]


class CustomsInfo(models.Customs):
    """The customs info processing helper"""

    def __init__(
        self,
        customs: models.Customs = None,
        option_type: typing.Type[utils.Enum] = utils.Enum,
        weight_unit: str = None,
        default_to: typing.Optional[models.Customs] = None,
        shipper: typing.Optional[models.Address] = None,
        recipient: typing.Optional[models.Address] = None,
    ):
        _customs = customs or default_to
        options = CustomsOptions(
            getattr(_customs, "options", None) or {},
            option_type=option_type,
        )

        self._customs = _customs
        self._options = options
        self._weight_unit = weight_unit
        self._shipper = shipper
        self._recipient = recipient

    def __getitem__(self, item):
        return getattr(self._customs, item, None)

    def __getattr__(self, item):
        return self[item]

    def __contains__(self, item) -> bool:
        return item in self._options or hasattr(self._customs, item)

    @property
    def is_defined(self) -> bool:
        return self._customs is not None

    @property
    def duty(self) -> models.Duty:  # type:ignore
        return getattr(self._customs, "duty", None) or models.Duty()

    @property
    def duty_billing_address(self) -> "ComputedAddress":  # type:ignore
        paid_by = getattr(self.duty, "paid_by", "sender")
        billing_address = getattr(self._customs, "duty_billing_address", None)

        if billing_address is not None:
            return ComputedAddress(billing_address)

        if paid_by == "sender":
            return ComputedAddress(self._shipper)

        elif paid_by == "recipient":
            return ComputedAddress(self._recipient)

        return ComputedAddress(billing_address)

    @property
    def commodities(self) -> Products:  # type:ignore
        _commodities = getattr(self._customs, "commodities", None) or []

        return Products(_commodities, self._weight_unit)

    @property
    def options(self):
        return self._options


class DocumentUploadOption(utils.Enum):
    """common shipment document upload options"""

    origin_postal_code = utils.OptionEnum("origin_postal_code")
    origin_country_code = utils.OptionEnum("origin_country_code")
    destination_postal_code = utils.OptionEnum("destination_postal_code")
    destination_country_code = utils.OptionEnum("destination_country_code")


class ConnectionConfigOption(utils.Enum):
    """common shipment document upload options"""

    label_type = utils.OptionEnum("label_type")
    language_code = utils.OptionEnum("language_code")
    default_currency = utils.OptionEnum("default_currency")
    shipping_options = utils.OptionEnum("shipping_options", list)
    shipping_services = utils.OptionEnum("shipping_services", list)


class ConnectionConfigOptions(Options):
    """The options common processing helper"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, base_option_type=ConnectionConfigOption)

    @property
    def label_type(self) -> utils.OptionEnum:
        return self[ConnectionConfigOption.label_type.name]

    @property
    def language_code(self) -> utils.OptionEnum:
        return self[ConnectionConfigOption.language_code.name]

    @property
    def default_currency(self) -> utils.OptionEnum:
        return self[ConnectionConfigOption.default_currency.name]

    @property
    def shipping_options(self) -> utils.OptionEnum:
        return self[ConnectionConfigOption.shipping_options.name]

    @property
    def shipping_services(self) -> utils.OptionEnum:
        return self[ConnectionConfigOption.shipping_services.name]


class Services:
    """The services common processing helper"""

    def __init__(
        self, services: typing.Iterable, service_type: typing.Type[utils.Enum]
    ):
        self._services = [service_type[s] for s in services if s in service_type]

    def __len__(self) -> int:
        return len(self._services)

    def __iter__(self) -> typing.Iterator[utils.Enum]:
        return iter(self._services)

    def __contains__(self, item) -> bool:
        return item in [s.name for s in self._services]

    @property
    def first(self) -> utils.Enum:
        return next(iter(self._services), None)


class Phone:
    def __init__(self, phone_number: str = None, country_code: str = None):
        try:
            self.number = phonenumbers.parse(phone_number, country_code)
        except Exception:
            self.number = None

    @property
    def country_code(self):
        if self.number is None:
            return None

        return self.number.country_code

    @property
    def area_code(self):
        if self.number is None:
            return None

        return str(self.number.national_number)[0:3]

    @property
    def phone(self):
        if self.number is None:
            return None

        return str(self.number.national_number)[3:]


class ComputedAddress(models.Address):
    def __init__(self, address: typing.Optional[models.Address]):
        self.address = address

    def __getattr__(self, item):
        if item == "street_number":
            return self._compute_street_number()

        if hasattr(self.address, item):
            return getattr(self.address, item)

        return getattr(getattr(self.address, "extra", None), item, None)

    @property
    def country_name(self):
        return Country.map(self.address.country_code).value

    @property
    def address_line(self) -> str:
        return self._compute_address_line()

    @property
    def address_lines(self) -> str:
        return self._compute_address_line(join=False)

    @property
    def street(self) -> typing.Optional[str]:
        return typing.cast(
            str,
            utils.SF.concat_str(
                self.street_number,
                self.street_name,
                join=True,
            ),
        )

    @property
    def street_name(self) -> typing.Optional[str]:
        """The address line 1 without the street number"""
        return typing.cast(
            str,
            utils.SF.concat_str(
                *[
                    _
                    for _ in self.address.address_line1.split(" ")
                    if _ != self.street_number
                ],
                join=True,
            ),
        )

    @property
    def tax_id(self) -> typing.Optional[str]:
        return self.address.federal_tax_id or self.address.state_tax_id

    @property
    def taxes(self) -> typing.List[str]:
        return utils.SF.concat_str(
            self.address.federal_tax_id, self.address.state_tax_id
        )  # type:ignore

    @property
    def has_contact_info(self) -> bool:
        return any(
            [
                self.address.company_name,
                self.address.phone_number,
                self.address.person_name,
                self.address.email,
            ]
        )

    @property
    def has_tax_info(self) -> bool:
        return any([self.address.federal_tax_id, self.address.state_tax_id])

    @property
    def contact(self) -> typing.Optional[str]:
        return getattr(self.address, "person_name", None) or getattr(
            self.address, "company_name", None
        )

    @property
    def first_name(self) -> typing.Optional[str]:
        if self.address.person_name is None:
            return None

        return self.address.person_name.split(" ")[0]

    @property
    def last_name(self) -> typing.Optional[str]:
        if self.address.person_name is None:
            return None

        return self.address.person_name.split(" ")[-1]

    def _compute_address_line(self, join: bool = True) -> typing.Optional[str]:
        if any(
            [
                self.street,
                self.address_line2,
            ]
        ):
            return utils.SF.concat_str(
                self.street,
                self.address_line2,
                join=join,
            )  # type:ignore

        return None

    def _compute_street_number(self):
        _value = getattr(self.address, "street_number", None)

        if _value is None and self.address:
            words = self.address.address_line1.split(" ")

            if any(_.isdigit() for _ in words[0]):
                return words[0]

            if any(_.isdigit() for _ in words[-1]):
                return words[-1]

        return _value


class ComputedDocumentFile(models.DocumentFile):
    def __init__(self, document: typing.Optional[models.DocumentFile]):
        self.document = document

    def __getattr__(self, item):
        return getattr(self.document, item, None)

    @property
    def doc_format(self):
        return getattr(self.document, "doc_format", self.doc_file_extension)

    @property
    def doc_file_extension(self) -> typing.Optional[str]:
        return pathlib.Path(self.doc_name or "").suffix


class TrackingStatus(utils.Enum):
    pending = ["pending"]
    on_hold = ["on_hold"]
    cancelled = ["cancelled"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]
    return_to_sender = ["return_to_sender"]
    unknown = ["unknown"]


def create_enum(name, values) -> utils.Enum:
    return utils.Enum(name, values)  # type: ignore


class Currency(utils.Enum):
    EUR = "Euro"
    AED = "UAE Dirham"
    USD = "US Dollar"
    XCD = "East Caribbean Dollar"
    AMD = "Dran"
    ANG = "Netherlands Antilles Guilder"
    AOA = "Kwanza"
    ARS = "Argentine Peso"
    AUD = "Australian Dollar"
    AWG = "Aruba Guilder"
    AZN = "Manat"
    BAM = "Convertible Marks"
    BBD = "Barbadian Dollar"
    BDT = "Taka"
    XOF = "CFA Franc West Africa"
    BGN = "Bulgarian Lev"
    BHD = "Bahraini Dinar"
    BIF = "Burundese Franc"
    BMD = "Bermudian Dollar"
    BND = "Brunei Dollar"
    BOB = "Boliviano"
    BRL = "Real"
    BSD = "Bahamian Dollar"
    BTN = "Ngultrum"
    BWP = "Pula"
    BYN = "Belarussian Ruble"
    BZD = "Belize Dollar"
    CAD = "Canadian Dollar"
    CDF = "Franc Congolais"
    XAF = "CFA Franc Central Africa"
    CHF = "Swiss Franc"
    NZD = "New Zealand Dollar"
    CLP = "New Chile Peso"
    CNY = "Yuan (Ren Min Bi)"
    COP = "Colombian Peso"
    CRC = "Costa Rican Colon"
    CUC = "Peso Convertible"
    CVE = "Cape Verde Escudo"
    CZK = "Czech Koruna"
    DJF = "Djibouti Franc"
    DKK = "Danish Krone"
    DOP = "Dominican Republic Peso"
    DZD = "Algerian Dinar"
    EGP = "Egyptian Pound"
    ERN = "Nakfa"
    ETB = "Birr"
    FJD = "Fijian Dollar"
    GBP = "Pound Sterling"
    GEL = "Georgian Lari"
    GHS = "Cedi"
    GMD = "Dalasi"
    GNF = "Guinea Franc"
    GTQ = "Quetzal"
    GYD = "Guyanan Dollar"
    HKD = "Hong Kong Dollar"
    HNL = "Lempira"
    HRK = "Croatian Kuna"
    HTG = "Gourde"
    HUF = "Forint"
    IDR = "Rupiah"
    ILS = "New Israeli Shekel"
    INR = "Indian Rupee"
    IRR = "Iranian Rial"
    ISK = "Icelandic Krona"
    JMD = "Jamaican Dollar"
    JOD = "Jordanian Dinar"
    JPY = "Yen"
    KES = "Kenyan Shilling"
    KGS = "Som"
    KHR = "Khmer Rial"
    KMF = "Comoros Franc"
    KPW = "North Korean Won"
    KRW = "Won"
    KWD = "Kuwaiti Dinar"
    KYD = "Cayman Islands Dollar"
    KZT = "Tenge"
    LAK = "Kip"
    LKR = "Sri Lankan Rupee"
    LRD = "Liberian Dollar"
    LSL = "Loti"
    LYD = "Libyan Dinar"
    MAD = "Moroccan Dirham"
    MDL = "Moldovan Leu"
    MGA = "Ariary"
    MKD = "Denar"
    MMK = "Kyat"
    MNT = "Tugrik"
    MOP = "Pataca"
    MRO = "Ouguiya"
    MUR = "Mauritius Rupee"
    MVR = "Rufiyaa"
    MWK = "Kwacha"
    MXN = "Mexican Nuevo Peso"
    MYR = "Ringgit"
    MZN = "Mozambique Metical"
    NAD = "Namibian Dollar"
    XPF = "CFP Franc"
    NGN = "Naira"
    NIO = "Cordoba Oro"
    NOK = "Norwegian Krone"
    NPR = "Nepalese Rupee"
    OMR = "Omani Rial"
    PEN = "Nuevo Sol"
    PGK = "Kina"
    PHP = "Phillipines Peso"
    PKR = "Pakistani Rupee"
    PLN = "Zloty"
    PYG = "Guarani"
    QAR = "Qatar Rial"
    RON = "Romanian Leu"
    RSD = "Serbia, Dinars"
    RUB = "Russian Ruble"
    RWF = "Rwanda Franc"
    SAR = "Saudi Riyal"
    SBD = "Solomon Islands Dollar"
    SCR = "Seychelles Rupee"
    SDG = "Sudanese Pound"
    SEK = "Swedish Krona"
    SGD = "Singapore Dollar"
    SHP = "St. Helena Pound"
    SLL = "Leone"
    SOS = "Somali Shilling"
    SRD = "Suriname Dollar"
    SSP = "South Sudanese pound"
    STD = "Dobra"
    SYP = "Syrian Pound"
    SZL = "Lilangeni"
    THB = "Baht"
    TJS = "Somoni"
    TND = "Tunisian Dinar"
    TOP = "Pa'anga"
    TRY = "New Turkish Lira"
    TTD = "Trinidad and Tobago Dollar"
    TWD = "New Taiwan Dollar"
    TZS = "Tanzanian Shilling"
    UAH = "Hryvna"
    UYU = "Peso Uruguayo"
    UZS = "Sum"
    VEF = "Bolivar Fuerte"
    VND = "Dong"
    VUV = "Vanuatu Vatu"
    WST = "Tala"
    YER = "Yemeni Riyal"
    ZAR = "South African Rand"
    ZMW = "Kwacha"


class Country(utils.Enum):
    AC = "Ascension Island"
    AD = "Andorra"
    AE = "United Arab Emirates"
    AF = "Afghanistan"
    AG = "Antigua"
    AI = "Anguilla"
    AL = "Albania"
    AM = "Armenia"
    AN = "Netherlands Antilles"
    AO = "Angola"
    AR = "Argentina"
    AS = "American Samoa"
    AT = "Austria"
    AU = "Australia"
    AW = "Aruba"
    AZ = "Azerbaijan"
    BA = "Bosnia And Herzegovina"
    BB = "Barbados"
    BD = "Bangladesh"
    BE = "Belgium"
    BF = "Burkina Faso"
    BG = "Bulgaria"
    BH = "Bahrain"
    BI = "Burundi"
    BJ = "Benin"
    BM = "Bermuda"
    BN = "Brunei"
    BO = "Bolivia"
    BR = "Brazil"
    BS = "Bahamas"
    BT = "Bhutan"
    BW = "Botswana"
    BY = "Belarus"
    BZ = "Belize"
    CA = "Canada"
    CD = "Congo, Democratic Republic of the"
    CF = "Central African Republic"
    CG = "Congo"
    CH = "Switzerland"
    CI = "Cote D Ivoire"
    CK = "Cook Islands"
    CL = "Chile"
    CM = "Cameroon"
    CN = "China"
    CO = "Colombia"
    CR = "Costa Rica"
    CU = "Cuba"
    CV = "Cape Verde"
    CY = "Cyprus"
    CZ = "Czech Republic"
    DE = "Germany"
    DJ = "Djibouti"
    DK = "Denmark"
    DM = "Dominica"
    DO = "Dominican Republic"
    DZ = "Algeria"
    EC = "Ecuador"
    EE = "Estonia"
    EG = "Egypt"
    ER = "Eritrea"
    ES = "Spain"
    ET = "Ethiopia"
    FI = "Finland"
    FJ = "Fiji"
    FK = "Falkland Islands"
    FM = "Micronesia, Federated States Of"
    FO = "Faroe Islands"
    FR = "France"
    GA = "Gabon"
    GB = "United Kingdom"
    GD = "Grenada"
    GE = "Georgia"
    GF = "French Guyana"
    GG = "Guernsey"
    GH = "Ghana"
    GI = "Gibraltar"
    GL = "Greenland"
    GM = "Gambia"
    GN = "Guinea Republic"
    GP = "Guadeloupe"
    GQ = "Guinea-equatorial"
    GR = "Greece"
    GT = "Guatemala"
    GU = "Guam"
    GW = "Guinea-bissau"
    GY = "Guyana (british)"
    HK = "Hong Kong"
    HN = "Honduras"
    HR = "Croatia"
    HT = "Haiti"
    HU = "Hungary"
    IC = "Canary Islands"
    ID = "Indonesia"
    IE = "Ireland"
    IL = "Israel"
    IN = "India"
    IQ = "Iraq"
    IR = "Iran"
    IS = "Iceland"
    IT = "Italy"
    JE = "Jersey"
    JM = "Jamaica"
    JO = "Jordan"
    JP = "Japan"
    KE = "Kenya"
    KG = "Kyrgyzstan"
    KH = "Cambodia"
    KI = "Kiribati"
    KM = "Comoros"
    KN = "St. Kitts"
    KP = "Korea, The D.p.r Of (north K.)"
    KR = "Korea, Republic of (South Korea)"
    KV = "Kosovo"
    KW = "Kuwait"
    KY = "Cayman Islands"
    KZ = "Kazakhstan"
    LA = "Lao Peoples Democratic Republic"
    LB = "Lebanon"
    LC = "St. Lucia"
    LI = "Liechtenstein"
    LK = "Sri Lanka"
    LR = "Liberia"
    LS = "Lesotho"
    LT = "Lithuania"
    LU = "Luxembourg"
    LV = "Latvia"
    LY = "Libya"
    MA = "Morocco"
    MC = "Monaco"
    MD = "Moldova"
    ME = "Montenegro"
    MG = "Madagascar"
    MH = "Marshall Islands"
    MK = "Macedonia"
    ML = "Mali"
    MM = "Myanmar"
    MN = "Mongolia"
    MO = "Macau"
    MP = "Nothern Mariana Islands, Commonwealth of"
    MQ = "Martinique"
    MR = "Mauritania"
    MS = "Montserrat"
    MT = "Malta"
    MU = "Mauritius"
    MV = "Maldives"
    MW = "Malawi"
    MX = "Mexico"
    MY = "Malaysia"
    MZ = "Mozambique"
    NA = "Namibia"
    NC = "New Caledonia"
    NE = "Niger"
    NG = "Nigeria"
    NI = "Nicaragua"
    NL = "Netherlands"
    NO = "Norway"
    NP = "Nepal"
    NR = "Nauru"
    NU = "Niue"
    NZ = "New Zealand"
    OM = "Oman"
    PA = "Panama"
    PE = "Peru"
    PF = "Tahiti"
    PG = "Papua New Guinea"
    PH = "Philippines"
    PK = "Pakistan"
    PL = "Poland"
    PR = "Puerto Rico"
    PT = "Portugal"
    PW = "Palau"
    PY = "Paraguay"
    QA = "Qatar"
    RE = "Reunion"
    RO = "Romania"
    RS = "Serbia"
    RU = "Russia"
    RW = "Rwanda"
    SA = "Saudi Arabia"
    SB = "Solomon Islands"
    SC = "Seychelles"
    SD = "Sudan"
    SE = "Sweden"
    SG = "Singapore"
    SH = "Saint Helena"
    SI = "Slovenia"
    SK = "Slovakia"
    SL = "Sierra Leone"
    SM = "San Marino"
    SN = "Senegal"
    SO = "Somalia"
    SR = "Suriname"
    SS = "South Sudan"
    ST = "Sao Tome And Principe"
    SV = "El Salvador"
    SY = "Syria"
    SZ = "Swaziland"
    TC = "Turks And Caicos Islands"
    TD = "Chad"
    TG = "Togo"
    TH = "Thailand"
    TJ = "Tajikistan"
    TL = "Timor Leste"
    TN = "Tunisia"
    TO = "Tonga"
    TR = "Turkey"
    TT = "Trinidad And Tobago"
    TV = "Tuvalu"
    TW = "Taiwan"
    TZ = "Tanzania"
    UA = "Ukraine"
    UG = "Uganda"
    US = "United States"
    UY = "Uruguay"
    UZ = "Uzbekistan"
    VA = "Vatican City"
    VC = "St. Vincent"
    VE = "Venezuela"
    VG = "British Virgin Islands"
    VI = "U.S. Virgin Islands"
    VN = "Vietnam"
    VU = "Vanuatu"
    WS = "Samoa"
    XB = "Bonaire"
    XC = "Curacao"
    XE = "St. Eustatius"
    XM = "St. Maarten"
    XN = "Nevis"
    XS = "Somaliland, Rep Of (north Somalia)"
    XY = "St. Barthelemy"
    YE = "Yemen"
    YT = "Mayotte"
    ZA = "South Africa"
    ZM = "Zambia"
    ZW = "Zimbabwe"
    # Adding missing country codes
    EH = "Western Sahara"
    IM = "Isle of Man"
    BL = "Saint Barthelemy"
    MF = "Saint Martin"
    SX = "Sint Maarten"
    XK = "Kosovo"


class CountryCurrency(utils.Enum):
    AC = "USD"
    AD = "EUR"
    AE = "AED"
    AF = "USD"
    AG = "XCD"
    AI = "XCD"
    AL = "EUR"
    AM = "AMD"
    AN = "ANG"
    AO = "AOA"
    AR = "ARS"
    AS = "USD"
    AT = "EUR"
    AU = "AUD"
    AW = "AWG"
    AZ = "AZN"
    BA = "BAM"
    BB = "BBD"
    BD = "BDT"
    BE = "EUR"
    BF = "XOF"
    BG = "BGN"
    BH = "BHD"
    BI = "BIF"
    BJ = "XOF"
    BM = "BMD"
    BN = "BND"
    BO = "BOB"
    BR = "BRL"
    BS = "BSD"
    BT = "BTN"
    BW = "BWP"
    BY = "BYN"
    BZ = "BZD"
    CA = "CAD"
    CD = "CDF"
    CF = "XAF"
    CG = "XAF"
    CH = "CHF"
    CI = "XOF"
    CK = "NZD"
    CL = "CLP"
    CM = "XAF"
    CN = "CNY"
    CO = "COP"
    CR = "CRC"
    CU = "CUC"
    CV = "CVE"
    CY = "EUR"
    CZ = "CZK"
    DE = "EUR"
    DJ = "DJF"
    DK = "DKK"
    DM = "XCD"
    DO = "DOP"
    DZ = "DZD"
    EC = "USD"
    EE = "EUR"
    EG = "EGP"
    ER = "ERN"
    ES = "EUR"
    ET = "ETB"
    FI = "EUR"
    FJ = "FJD"
    FK = "GBP"
    FM = "USD"
    FO = "DKK"
    FR = "EUR"
    GA = "XAF"
    GB = "GBP"
    GD = "XCD"
    GE = "GEL"
    GF = "EUR"
    GG = "GBP"
    GH = "GHS"
    GI = "GBP"
    GL = "DKK"
    GM = "GMD"
    GN = "GNF"
    GP = "EUR"
    GQ = "XAF"
    GR = "EUR"
    GT = "GTQ"
    GU = "USD"
    GW = "XOF"
    GY = "GYD"
    HK = "HKD"
    HN = "HNL"
    HR = "HRK"
    HT = "HTG"
    HU = "HUF"
    IC = "EUR"
    ID = "IDR"
    IE = "EUR"
    IL = "ILS"
    IN = "INR"
    IQ = "USD"
    IR = "IRR"
    IS = "ISK"
    IT = "EUR"
    JE = "GBP"
    JM = "JMD"
    JO = "JOD"
    JP = "JPY"
    KE = "KES"
    KG = "KGS"
    KH = "KHR"
    KI = "AUD"
    KM = "KMF"
    KN = "XCD"
    KP = "KPW"
    KR = "KRW"
    KV = "EUR"
    KW = "KWD"
    KY = "KYD"
    KZ = "KZT"
    LA = "LAK"
    LB = "USD"
    LC = "XCD"
    LI = "CHF"
    LK = "LKR"
    LR = "LRD"
    LS = "LSL"
    LT = "EUR"
    LU = "EUR"
    LV = "EUR"
    LY = "LYD"
    MA = "MAD"
    MC = "EUR"
    MD = "MDL"
    ME = "EUR"
    MG = "MGA"
    MH = "USD"
    MK = "MKD"
    ML = "XOF"
    MM = "MMK"
    MN = "MNT"
    MO = "MOP"
    MP = "USD"
    MQ = "EUR"
    MR = "MRO"
    MS = "XCD"
    MT = "EUR"
    MU = "MUR"
    MV = "MVR"
    MW = "MWK"
    MX = "MXN"
    MY = "MYR"
    MZ = "MZN"
    NA = "NAD"
    NC = "XPF"
    NE = "XOF"
    NG = "NGN"
    NI = "NIO"
    NL = "EUR"
    NO = "NOK"
    NP = "NPR"
    NR = "AUD"
    NU = "NZD"
    NZ = "NZD"
    OM = "OMR"
    PA = "USD"
    PE = "PEN"
    PF = "XPF"
    PG = "PGK"
    PH = "PHP"
    PK = "PKR"
    PL = "PLN"
    PR = "USD"
    PT = "EUR"
    PW = "USD"
    PY = "PYG"
    QA = "QAR"
    RE = "EUR"
    RO = "RON"
    RS = "RSD"
    RU = "RUB"
    RW = "RWF"
    SA = "SAR"
    SB = "SBD"
    SC = "SCR"
    SD = "SDG"
    SE = "SEK"
    SG = "SGD"
    SH = "SHP"
    SI = "EUR"
    SK = "EUR"
    SL = "SLL"
    SM = "EUR"
    SN = "XOF"
    SO = "SOS"
    SR = "SRD"
    SS = "SSP"
    ST = "STD"
    SV = "USD"
    SY = "SYP"
    SZ = "SZL"
    TC = "USD"
    TD = "XAF"
    TG = "XOF"
    TH = "THB"
    TJ = "TJS"
    TL = "USD"
    TN = "TND"
    TO = "TOP"
    TR = "TRY"
    TT = "TTD"
    TV = "AUD"
    TW = "TWD"
    TZ = "TZS"
    UA = "UAH"
    UG = "USD"
    US = "USD"
    UY = "UYU"
    UZ = "UZS"
    VA = "EUR"
    VC = "XCD"
    VE = "VEF"
    VG = "USD"
    VI = "USD"
    VN = "VND"
    VU = "VUV"
    WS = "WST"
    XB = "EUR"
    XC = "EUR"
    XE = "ANG"
    XM = "EUR"
    XN = "XCD"
    XS = "USD"
    XY = "ANG"
    YE = "YER"
    YT = "EUR"
    ZA = "ZAR"
    ZM = "ZMW"
    ZW = "USD"


class CountryState(utils.Enum):
    AE = create_enum(
        "State",
        {
            "AB": "Abu Dhabi",
            "AJ": "Ajman",
            "DU": "Dubai",
            "FU": "Fujairah",
            "RA": "Ras al-Khaimah",
            "SH": "Sharjah",
            "UM": "Umm al-Qaiwain",
        },
    )
    AU = create_enum(
        "State",
        {
            "NSW": "New South Wales",
            "VIC": "Victoria",
            "QLD": "Queensland",
            "WA": "Western Australia",
            "SA": "South Australia",
            "TAS": "Tasmania",
        },
    )
    CA = create_enum(
        "State",
        {
            "AB": "Alberta",
            "BC": "British Columbia",
            "MB": "Manitoba",
            "NB": "New Brunswick",
            "NL": "Newfoundland",
            "NT": "Northwest Territories",
            "NS": "Nova Scotia",
            "NU": "Nunavut",
            "ON": "Ontario",
            "PE": "Prince Edward Island",
            "QC": "Quebec",
            "SK": "Saskatchewan",
            "YT": "Yukon",
        },
    )
    CN = create_enum(
        "State",
        {
            "anhui": "Anhui",
            "hainan": "Hainan",
            "jiangxi": "Jiangxi",
            "shanghai": "Shanghai",
            "beijing": "Beijing",
            "hebei": "Hebei",
            "jilin": "Jilin",
            "shanxi": "Shanxi",
            "chongqing": "Chongqing",
            "heilongjiang": "Heilongjiang",
            "liaoning": "Liaoning",
            "sichuan": "Sichuan",
            "fujian": "Fujian",
            "henan": "Henan",
            "nei_mongol": "Nei Mongol",
            "tianjin": "Tianjin",
            "gansu": "Gansu",
            "hubei": "Hubei",
            "qinghai": "Qinghai",
            "xinjiang": "Xinjiang",
            "guangdong": "Guangdong",
            "hunan": "Hunan",
            "shaanxi": "Shaanxi",
            "yunnan": "Yunnan",
            "guizhou": "Guizhou",
            "jiangsu": "Jiangsu",
            "shandong": "Shandong",
            "zhejiang": "Zhejiang",
        },
    )
    IN = create_enum(
        "State",
        {
            "AN": "Andaman & Nicobar (U.T)",
            "AP": "Andhra Pradesh",
            "AR": "Arunachal Pradesh",
            "AS": "Assam",
            "BR": "Bihar",
            "CG": "Chattisgarh",
            "CH": "Chandigarh (U.T.)",
            "DD": "Daman & Diu (U.T.)",
            "DL": "Delhi (U.T.)",
            "DN": "Dadra and Nagar Haveli (U.T.)",
            "GA": "Goa",
            "GJ": "Gujarat",
            "HP": "Himachal Pradesh",
            "HR": "Haryana",
            "JH": "Jharkhand",
            "JK": "Jammu & Kashmir",
            "KA": "Karnataka",
            "KL": "Kerala",
            "LD": "Lakshadweep (U.T)",
            "MH": "Maharashtra",
            "ML": "Meghalaya",
            "MN": "Manipur",
            "MP": "Madhya Pradesh",
            "MZ": "Mizoram",
            "NL": "Nagaland",
            "OR": "Orissa",
            "PB": "Punjab",
            "PY": "Puducherry (U.T.)",
            "RJ": "Rajasthan",
            "SK": "Sikkim",
            "TN": "Tamil Nadu",
            "TR": "Tripura",
            "UA": "Uttaranchal",
            "UP": "Uttar Pradesh",
            "WB": "West Bengal",
        },
    )
    MX = create_enum(
        "State",
        {
            "AG": "Aguascalientes",
            "BC": "Baja California",
            "BS": "Baja California Sur",
            "CM": "Campeche",
            "CS": "Chiapas",
            "CH": "Chihuahua",
            "CO": "Coahuila",
            "CL": "Colima",
            "DF": "Ciudad de México",
            "DG": "Durango",
            "GT": "Guanajuato",
            "GR": "Guerrero",
            "HG": "Hidalgo",
            "JA": "Jalisco",
            "EM": "Estado de México",
            "MI": "Michoacán",
            "MO": "Morelos",
            "NA": "Nayarit",
            "NL": "Nuevo León",
            "OA": "Oaxaca",
            "PU": "Puebla",
            "QE": "Querétaro",
            "QR": "Quintana Roo",
            "SL": "San Luis Potosí",
            "SI": "Sinaloa",
            "SO": "Sonora",
            "TB": "Tabasco",
            "TM": "Tamaulipas",
            "TL": "Tlaxcala",
            "VE": "Veracruz",
            "YU": "Yucatán",
            "ZA": "Zacatecas",
        },
    )
    US = create_enum(
        "State",
        {
            "AL": "Alabama",
            "AK": "Alaska",
            "AZ": "Arizona",
            "AR": "Arkansas",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "DC": "District of Columbia",
            "FL": "Florida",
            "GA": "Georgia",
            "HI": "Hawaii",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "IA": "Iowa",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "ME": "Maine",
            "MD": "Maryland",
            "MA": "Massachusetts",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MS": "Mississippi",
            "MO": "Missouri",
            "MT": "Montana",
            "NE": "Nebraska",
            "NV": "Nevada",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NY": "New York",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VT": "Vermont",
            "VA": "Virginia",
            "WA": "Washington State",
            "WV": "West Virginia",
            "WI": "Wisconsin",
            "WY": "Wyoming",
            "PR": "Puerto Rico",
        },
    )


class CountryISO(utils.Enum):
    AF = 4
    AX = 248
    AL = 8
    DZ = 12
    AS = 16
    AD = 20
    AO = 24
    AI = 660
    AQ = 10
    AG = 28
    AR = 32
    AM = 51
    AW = 533
    AU = 36
    AT = 40
    AZ = 31
    BS = 44
    BH = 48
    BD = 50
    BB = 52
    BY = 112
    BE = 56
    BZ = 84
    BJ = 204
    BM = 60
    BT = 64
    BO = 68
    BQ = 535
    BA = 70
    BW = 72
    BV = 74
    BR = 76
    IO = 86
    BN = 96
    BG = 100
    BF = 854
    BI = 108
    CV = 132
    KH = 116
    CM = 120
    CA = 124
    KY = 136
    CF = 140
    TD = 148
    CL = 152
    CN = 156
    CX = 162
    CC = 166
    CO = 170
    KM = 174
    CG = 178
    CD = 180
    CK = 184
    CR = 188
    CI = 384
    HR = 191
    CU = 192
    CW = 531
    CY = 196
    CZ = 203
    DK = 208
    DJ = 262
    DM = 212
    DO = 214
    EC = 218
    EG = 818
    SV = 222
    GQ = 226
    ER = 232
    EE = 233
    SZ = 748
    ET = 231
    FK = 238
    FO = 234
    FJ = 242
    FI = 246
    FR = 250
    GF = 254
    PF = 258
    TF = 260
    GA = 266
    GM = 270
    GE = 268
    DE = 276
    GH = 288
    GI = 292
    GR = 300
    GL = 304
    GD = 308
    GP = 312
    GU = 316
    GT = 320
    GG = 831
    GN = 324
    GW = 624
    GY = 328
    HT = 332
    HM = 334
    VA = 336
    HN = 340
    HK = 344
    HU = 348
    IS = 352
    IN = 356
    ID = 360
    IR = 364
    IQ = 368
    IE = 372
    IM = 833
    IL = 376
    IT = 380
    JM = 388
    JP = 392
    JE = 832
    JO = 400
    KZ = 398
    KE = 404
    KI = 296
    KP = 408
    KR = 410
    KW = 414
    KG = 417
    LA = 418
    LV = 428
    LB = 422
    LS = 426
    LR = 430
    LY = 434
    LI = 438
    LT = 440
    LU = 442
    MO = 446
    MG = 450
    MW = 454
    MY = 458
    MV = 462
    ML = 466
    MT = 470
    MH = 584
    MQ = 474
    MR = 478
    MU = 480
    YT = 175
    MX = 484
    FM = 583
    MD = 498
    MC = 492
    MN = 496
    ME = 499
    MS = 500
    MA = 504
    MZ = 508
    MM = 104
    NA = 516
    NR = 520
    NP = 524
    NL = 528
    NC = 540
    NZ = 554
    NI = 558
    NE = 562
    NG = 566
    NU = 570
    NF = 574
    MK = 807
    MP = 580
    NO = 578
    OM = 512
    PK = 586
    PW = 585
    PS = 275
    PA = 591
    PG = 598
    PY = 600
    PE = 604
    PH = 608
    PN = 612
    PL = 616
    PT = 620
    PR = 630
    QA = 634
    RE = 638
    RO = 642
    RU = 643
    RW = 646
    BL = 652
    SH = 654
    KN = 659
    LC = 662
    MF = 663
    PM = 666
    VC = 670
    WS = 882
    SM = 674
    ST = 678
    SA = 682
    SN = 686
    RS = 688
    SC = 690
    SL = 694
    SG = 702
    SX = 534
    SK = 703
    SI = 705
    SB = 90
    SO = 706
    ZA = 710
    GS = 239
    SS = 728
    ES = 724
    LK = 144
    SD = 729
    SR = 740
    SJ = 744
    SE = 752
    CH = 756
    SY = 760
    TW = 158
    TJ = 762
    TZ = 834
    TH = 764
    TL = 626
    TG = 768
    TK = 772
    TO = 776
    TT = 780
    TN = 788
    TR = 792
    TM = 795
    TC = 796
    TV = 798
    UG = 800
    UA = 804
    AE = 784
    GB = 826
    US = 840
    UM = 581
    UY = 858
    UZ = 860
    VU = 548
    VE = 862
    VN = 704
    VG = 92
    VI = 850
    WF = 876
    EH = 732
    YE = 887
    ZM = 894
    ZW = 716


class EUCountry(utils.Enum):
    AT = "Austria"
    BE = "Belgium"
    BG = "Bulgaria"
    HR = "Croatia"
    CY = "Cyprus"
    CZ = "Czech Republic"
    DK = "Denmark"
    EE = "Estonia"
    FI = "Finland"
    FR = "France"
    DE = "Germany"
    EL = "Greece"
    HU = "Hungary"
    IE = "Ireland"
    IT = "Italy"
    LV = "Latvia"
    LT = "Lithuania"
    LU = "Luxembourg"
    MT = "Malta"
    NL = "Netherlands"
    PL = "Poland"
    PT = "Portugal"
    RO = "Romania"
    SI = "Slovenia"
    SK = "Slovakia"
    ES = "Spain"
    SE = "Sweden"


class CountryCode(utils.Enum):
    AD = "AND"  # Andorra
    AE = "ARE"  # United Arab Emirates
    AF = "AFG"  # Afghanistan
    AG = "ATG"  # Antigua
    AI = "AIA"  # Anguilla
    AL = "ALB"  # Albania
    AM = "ARM"  # Armenia
    AN = "ANT"  # Netherlands Antilles
    AO = "AGO"  # Angola
    AR = "ARG"  # Argentina
    AS = "ASM"  # American Samoa
    AT = "AUT"  # Austria
    AU = "AUS"  # Australia
    AW = "ABW"  # Aruba
    AZ = "AZE"  # Azerbaijan
    BA = "BIH"  # Bosnia And Herzegovina
    BB = "BRB"  # Barbados
    BD = "BGD"  # Bangladesh
    BE = "BEL"  # Belgium
    BF = "BFA"  # Burkina Faso
    BG = "BGR"  # Bulgaria
    BH = "BHR"  # Bahrain
    BI = "BDI"  # Burundi
    BJ = "BEN"  # Benin
    BM = "BMU"  # Bermuda
    BN = "BRN"  # Brunei
    BO = "BOL"  # Bolivia
    BR = "BRA"  # Brazil
    BS = "BHS"  # Bahamas
    BT = "BTN"  # Bhutan
    BW = "BWA"  # Botswana
    BY = "BLR"  # Belarus
    BZ = "BLZ"  # Belize
    CA = "CAN"  # Canada
    CD = "COD"  # Congo, Democratic Republic of the
    CF = "CAF"  # Central African Republic
    CG = "COG"  # Congo
    CH = "CHE"  # Switzerland
    CI = "CIV"  # Cote D Ivoire
    CK = "COK"  # Cook Islands
    CL = "CHL"  # Chile
    CM = "CMR"  # Cameroon
    CN = "CHN"  # China
    CO = "COL"  # Colombia
    CR = "CRI"  # Costa Rica
    CU = "CUB"  # Cuba
    CV = "CPV"  # Cape Verde
    CY = "CYP"  # Cyprus
    CZ = "CZE"  # Czech Republic
    DE = "DEU"  # Germany
    DJ = "DJI"  # Djibouti
    DK = "DNK"  # Denmark
    DM = "DMA"  # Dominica
    DO = "DOM"  # Dominican Republic
    DZ = "DZA"  # Algeria
    EC = "ECU"  # Ecuador
    EE = "EST"  # Estonia
    EG = "EGY"  # Egypt
    ER = "ERI"  # Eritrea
    ES = "ESP"  # Spain
    ET = "ETH"  # Ethiopia
    FI = "FIN"  # Finland
    FJ = "FJI"  # Fiji
    FK = "FLK"  # Falkland Islands
    FM = "FSM"  # Micronesia, Federated States Of
    FO = "FRO"  # Faroe Islands
    FR = "FRA"  # France
    GA = "GAB"  # Gabon
    GB = "GBR"  # United Kingdom
    GD = "GRD"  # Grenada
    GE = "GEO"  # Georgia
    GF = "GUF"  # French Guyana
    GG = "GGY"  # Guernsey
    GH = "GHA"  # Ghana
    GI = "GIB"  # Gibraltar
    GL = "GRL"  # Greenland
    GM = "GMB"  # Gambia
    GN = "GIN"  # Guinea Republic
    GP = "GLP"  # Guadeloupe
    GQ = "GNQ"  # Guinea-equatorial
    GR = "GRC"  # Greece
    GT = "GTM"  # Guatemala
    GU = "GUM"  # Guam
    GW = "GNB"  # Guinea-bissau
    GY = "GUY"  # Guyana (british)
    HK = "HKG"  # Hong Kong
    HN = "HND"  # Honduras
    HR = "HRV"  # Croatia
    HT = "HTI"  # Haiti
    HU = "HUN"  # Hungary
    IC = "ICA"  # Canary Islands
    ID = "IDN"  # Indonesia
    IE = "IRL"  # Ireland
    IL = "ISR"  # Israel
    IN = "IND"  # India
    IQ = "IRQ"  # Iraq
    IR = "IRN"  # Iran
    IS = "ISL"  # Iceland
    IT = "ITA"  # Italy
    JE = "JEY"  # Jersey
    JM = "JAM"  # Jamaica
    JO = "JOR"  # Jordan
    JP = "JPN"  # Japan
    KE = "KEN"  # Kenya
    KG = "KGZ"  # Kyrgyzstan
    KH = "KHM"  # Cambodia
    KI = "KIR"  # Kiribati
    KM = "COM"  # Comoros
    KN = "KNA"  # St. Kitts
    KP = "PRK"  # Korea, The D.p.r Of (north K.)
    KR = "KOR"  # Korea, Republic of (South Korea)
    KV = "XKX"  # Kosovo
    KW = "KWT"  # Kuwait
    KY = "CYM"  # Cayman Islands
    KZ = "KAZ"  # Kazakhstan
    LA = "LAO"  # Lao Peoples Democratic Republic
    LB = "LBN"  # Lebanon
    LC = "LCA"  # St. Lucia
    LI = "LIE"  # Liechtenstein
    LK = "LKA"  # Sri Lanka
    LR = "LBR"  # Liberia
    LS = "LSO"  # Lesotho
    LT = "LTU"  # Lithuania
    LU = "LUX"  # Luxembourg
    LV = "LVA"  # Latvia
    LY = "LBY"  # Libya
    MA = "MAR"  # Morocco
    MC = "MCO"  # Monaco
    MD = "MDA"  # Moldova
    ME = "MNE"  # Montenegro
    MG = "MDG"  # Madagascar
    MH = "MHL"  # Marshall Islands
    MK = "MKD"  # Macedonia
    ML = "MLI"  # Mali
    MM = "MMR"  # Myanmar
    MN = "MNG"  # Mongolia
    MO = "MAC"  # Macau
    MP = "MNP"  # Nothern Mariana Islands, Commonwealth of
    MQ = "MTQ"  # Martinique
    MR = "MRT"  # Mauritania
    MS = "MSR"  # Montserrat
    MT = "MLT"  # Malta
    MU = "MUS"  # Mauritius
    MV = "MDV"  # Maldives
    MW = "MWI"  # Malawi
    MX = "MEX"  # Mexico
    MY = "MYS"  # Malaysia
    MZ = "MOZ"  # Mozambique
    NA = "NAM"  # Namibia
    NC = "NCL"  # New Caledonia
    NE = "NER"  # Niger
    NG = "NGA"  # Nigeria
    NI = "NIC"  # Nicaragua
    NL = "NLD"  # Netherlands
    NO = "NOR"  # Norway
    NP = "NPL"  # Nepal
    NR = "NRU"  # Nauru
    NU = "NIU"  # Niue
    NZ = "NZL"  # New Zealand
    OM = "OMN"  # Oman
    PA = "PAN"  # Panama
    PE = "PER"  # Peru
    PF = "PYF"  # Tahiti
    PG = "PNG"  # Papua New Guinea
    PH = "PHL"  # Philippines
    PK = "PAK"  # Pakistan
    PL = "POL"  # Poland
    PR = "PRI"  # Puerto Rico
    PT = "PRT"  # Portugal
    PW = "PLW"  # Palau
    PY = "PRY"  # Paraguay
    QA = "QAT"  # Qatar
    RE = "REU"  # Reunion
    RO = "ROU"  # Romania
    RS = "SRB"  # Serbia
    RU = "RUS"  # Russia
    RW = "RWA"  # Rwanda
    SA = "SAU"  # Saudi Arabia
    SB = "SLB"  # Solomon Islands
    SC = "SYC"  # Seychelles
    SD = "SDN"  # Sudan
    SE = "SWE"  # Sweden
    SG = "SGP"  # Singapore
    SH = "SHN"  # Saint Helena
    SI = "SVN"  # Slovenia
    SK = "SVK"  # Slovakia
    SL = "SLE"  # Sierra Leone
    SM = "SMR"  # San Marino
    SN = "SEN"  # Senegal
    SO = "SOM"  # Somalia
    SR = "SUR"  # Suriname
    SS = "SSD"  # South Sudan
    ST = "STP"  # Sao Tome And Principe
    SV = "SLV"  # El Salvador
    SY = "SYR"  # Syria
    SZ = "SWZ"  # Swaziland
    TC = "TCA"  # Turks And Caicos Islands
    TD = "TCD"  # Chad
    TG = "TGO"  # Togo
    TH = "THA"  # Thailand
    TJ = "TJK"  # Tajikistan
    TL = "TLS"  # Timor Leste
    TN = "TUN"  # Tunisia
    TO = "TON"  # Tonga
    TR = "TUR"  # Turkey
    TT = "TTO"  # Trinidad And Tobago
    TV = "TUV"  # Tuvalu
    TW = "TWN"  # Taiwan
    TZ = "TZA"  # Tanzania
    UA = "UKR"  # Ukraine
    UG = "UGA"  # Uganda
    US = "USA"  # United States
    UY = "URY"  # Uruguay
    UZ = "UZB"  # Uzbekistan
    VA = "VAT"  # Vatican City
    VC = "VCT"  # St. Vincent
    VE = "VEN"  # Venezuela
    VG = "VGB"  # British Virgin Islands
    VI = "VIR"  # U.S. Virgin Islands
    VN = "VNM"  # Vietnam
    VU = "VUT"  # Vanuatu
    WS = "WSM"  # Samoa
    XB = "BES"  # Bonaire
    XC = "CUW"  # Curacao
    XE = "EUX"  # St. Eustatius
    XM = "SXM"  # St. Maarten
    XN = "KNA"  # Nevis
    XS = "SOM"  # Somaliland, Rep Of (north Somalia)
    XY = "BLM"  # St. Barthelemy
    YE = "YEM"  # Yemen
    YT = "MYT"  # Mayotte
    ZA = "ZAF"  # South Africa
    ZM = "ZMB"  # Zambia
    ZW = "ZWE"  # Zimbabwe
