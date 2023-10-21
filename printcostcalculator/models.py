from datetime import datetime
from math import pi as PI
from typing import Optional, List

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint


class Base(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    date_created: datetime = Field(nullable=False, default_factory=datetime.now)


class MaterialType(Base, table=True):
    __table_args__ = (UniqueConstraint("code", "name"),)

    code: str = Field(nullable=False, min_length=2)
    name: str = Field(nullable=False)


class MaterialManufacturer(Base, table=True):
    __table_args__ = (UniqueConstraint("name"),)

    name: str = Field(nullable=False)


class Material(Base, table=True):
    __table_args__ = (UniqueConstraint("manufacture_id", "color", "material_type_id"),)

    color: str = Field(nullable=False)
    color_hex: str = Field(nullable=True)
    diameter: float = Field(nullable=False)
    """mm"""
    price: float = Field(nullable=False)
    weight: float = Field(nullable=False)
    """kg"""
    density: float = Field(nullable=False)
    """g/cm³"""
    print_temperature: int = Field(nullable=False)
    """°C"""
    bed_temperature: int = Field(nullable=False)
    """°C"""
    material_type_id: int = Field(nullable=False, foreign_key="materialtype.id")
    manufacturer_id: int = Field(nullable=False, foreign_key="materialmanufacturer.id")

    # Relationships
    material_type: MaterialType = Relationship()
    manufacturer: MaterialManufacturer = Relationship()
    properties: List["MaterialProperty"] = Relationship(back_populates="material")

    def properties_dict(self) -> dict:
        return {p.name: p.value for p in self.properties}

    @property
    def length_per_roll(self) -> int:
        """Returns the estimated length in meters."""
        return (
            self.weight
            / self.density
            * 4
            / (PI * ((self.diameter / 100) * (self.diameter / 100)) / 10)
        )

    @property
    def price_per_kg(self) -> float:
        return self.price / self.weight


class MaterialProperty(Base, table=True):
    __table_args__ = (UniqueConstraint("name", "material_id"),)

    name: str = Field(nullable=False)
    _value: float = Field(nullable=False)
    _type: str = Field(nullable=False)
    material_id: int = Field(nullable=False, foreign_key="material.id")

    # Relationships
    material: Material = Relationship(back_populates="properties")

    @property
    def value(self) -> float:
        return eval(f"{self._value}{self._type}")


class PrinterManufacturer(Base, table=True):
    __table_args__ = (UniqueConstraint("name"),)

    name: str = Field(nullable=False)


class Printer(Base, table=True):
    __table_args__ = (UniqueConstraint("serial_number", "name"),)

    name: str = Field(nullable=False)
    serial_number: str = Field(nullable=True)
    material_diameter: float = Field(nullable=False)
    """mm"""
    price: float = Field(nullable=False)
    deprecation_time: int = Field(nullable=False)
    service_cost_per_life: int = Field(nullable=False)
    energy_consumption: float = Field(nullable=False)
    """kWh/h"""
    manufacturer_id: int = Field(nullable=False, foreign_key="printermanufacturer.id")

    # Relationships
    manufacturer: PrinterManufacturer = Relationship()

    @property
    def deprecation_per_hour(self) -> float:
        """Returns the total deprecation cost per hour."""
        return (self.price + self.service_cost_per_life) / self.deprecation_time


class Quote(Base, table=True):
    customer_name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    printer_id: Optional[int] = Field(default=None, foreign_key="printer.id")
    material_id: Optional[int] = Field(default=None, foreign_key="material.id")
    weight: int = Field(nullable=False)
    print_time_minutes: int = Field(nullable=False)
    model_prep_time_minutes: int = Field(nullable=False)
    slicing_time_minutes: int = Field(nullable=False)
    material_change_time_minutes: int = Field(nullable=False)
    transfer_start_time_minutes: int = Field(nullable=False)
    print_removal_time_minutes: int = Field(nullable=False)
    support_removal_time_minutes: int = Field(nullable=False)
    additional_work_time_minutes: int = Field(nullable=False)
    consumables: float = Field(nullable=False)
    markup: int = Field(nullable=False)
    quoted_price: float = Field(nullable=False)

    # Relationships
    printer: Optional[Printer] = Relationship()
    material: Optional[Material] = Relationship()

    @property
    def total_prep_time_minutes(self) -> float:
        return (
            self.model_prep_time_minutes
            + self.slicing_time_minutes
            + self.material_change_time_minutes
            + self.transfer_start_time_minutes
        )

    @property
    def total_post_processing_time_minutes(self) -> float:
        return (
            self.print_removal_time_minutes
            + self.support_removal_time_minutes
            + self.additional_work_time_minutes
        )

    @property
    def print_time_hours(self) -> float:
        return self.print_time_minutes / 60

    @property
    def material_cost(self) -> float:
        return (self.weight / 1000) * self.material.price_per_kg

    @property
    def electricity_cost(self) -> float:
        # TODO: Store electricity cost.
        return self.print_time_hours * self.printer.energy_consumption * 0.15

    @property
    def printer_deprecation_cost(self) -> float:
        return self.print_time_hours * self.printer.deprecation_per_hour

    @property
    def preparation_cost(self) -> float:
        # TODO: Add labor cost.
        return self.total_prep_time_minutes / 60 * 30

    @property
    def post_processing_cost(self) -> float:
        # TODO: Add labor cost.
        return self.total_post_processing_time_minutes / 60 * 30

    @property
    def consumables_cost(self) -> float:
        return self.consumables

    @property
    def subtotal(self) -> float:
        return (
            self.material_cost
            + self.electricity_cost
            + self.printer_deprecation_cost
            + self.preparation_cost
            + self.post_processing_cost
            + self.consumables_cost
        )

    @property
    def subtotal_with_failures(self) -> float:
        # TODO: Add failure 10%.
        return self.subtotal * (10 / 100 + 1)

    @property
    def suggested_price(self) -> float:
        return self.subtotal_with_failures * (self.markup / 100)
