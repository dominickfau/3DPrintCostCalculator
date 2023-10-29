from datetime import datetime
from math import pi as PI
from typing import Optional, Tuple
import uuid

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint


class Base(SQLModel, table=False):
    """Base class for all models."""

    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    date_created: datetime = Field(nullable=False, default_factory=datetime.now)


class MaterialType(Base, table=True):
    """Material type model."""

    __table_args__ = (UniqueConstraint("code", "name"),)

    code: str = Field(nullable=False, min_length=2)
    name: str = Field(nullable=False)


class MaterialManufacturer(Base, table=True):
    """Material manufacturer model."""

    name: str = Field(nullable=False, unique=True)


class MaterialDiameter(Base, table=True):
    """Material diameter model."""

    diameter: float = Field(nullable=False, unique=True)
    """mm"""


class Material(Base, table=True):
    """Material model."""

    __table_args__ = (UniqueConstraint("manufacture_id", "color", "material_type_id"),)

    color_hex: str = Field(nullable=False, default="#000000")
    """Hexadecimal color code."""
    total_price: float = Field(nullable=False)
    """Total price per roll."""
    total_weight: float = Field(nullable=False)
    """kg"""
    density: float = Field(nullable=False)
    """g/cm³"""
    print_temperature: int = Field(nullable=False)
    """°C"""
    bed_temperature: int = Field(nullable=False)
    """°C"""
    material_type_id: int = Field(nullable=False, foreign_key="materialtype.id")
    manufacturer_id: int = Field(nullable=False, foreign_key="materialmanufacturer.id")
    diameter_id: int = Field(nullable=False, foreign_key="materialdiameter.id")

    # Relationships
    material_type: MaterialType = Relationship()
    manufacturer: MaterialManufacturer = Relationship()
    diameter: MaterialDiameter = Relationship()

    @property
    def length_per_roll(self) -> float:
        """Returns the estimated length in meters."""
        return (
            self.total_weight
            / self.density
            * 4
            / (PI * ((self.diameter / 100) * (self.diameter / 100)) / 10)
        )

    @property
    def price_per_kg(self) -> float:
        """Returns the price per kg."""
        return self.total_price / self.total_weight


class PrinterManufacturer(Base, table=True):
    """Printer manufacturer model."""

    name: str = Field(nullable=False, unique=True)


class Printer(Base, table=True):
    """Printer model."""

    __table_args__ = (UniqueConstraint("manufacturer_id", "name", "serial_number"),)

    name: str = Field(nullable=False)
    serial_number: str = Field(nullable=False, unique=True)
    material_size: float = Field(nullable=False)
    bed_size_x: float = Field(nullable=False)
    bed_size_y: float = Field(nullable=False)
    bed_size_z: float = Field(nullable=False)
    total_price: float = Field(nullable=False)
    depreciation_time: float = Field(nullable=False)
    """Minutes"""
    service_cost: float = Field(nullable=False)
    """Cost per minute"""
    electricity_cost: float = Field(nullable=False)
    """Cost per kWh"""
    manufacturer_id: int = Field(nullable=False, foreign_key="printermanufacturer.id")
    material_dimension_id: int = Field(
        nullable=False, foreign_key="materialdiameter.id"
    )

    # Relationships
    manufacturer: PrinterManufacturer = Relationship()
    material_dimension: MaterialDiameter = Relationship()

    @property
    def print_volume(self) -> float:
        """Returns the print volume in mm³."""
        return self.bed_size_x * self.bed_size_y * self.bed_size_z

    @property
    def depreciation_cost_per_minute(self) -> float:
        """Returns the depreciation cost per minute."""
        return self.total_price / self.depreciation_time

    def check_material_compatability(self, material: Material) -> bool:
        """Checks if the material is compatible with the printer."""
        return material.diameter.diameter == self.material_dimension.diameter

    def calculate_print_cost(
        self, print_time: float, print_weight: float, material: Material
    ) -> Tuple[float, float, float, float]:
        """Calculates the cost of a print.

        Args:
            print_time (float): Total print time in minutes.
            print_weight (float): Total print weight in g.
            material (Material): Material used for the print.

        Returns:
            float: Depreciation cost.
            float: Material cost.
            float: Service cost.
            float: Electricity cost.
        """
        if not self.check_material_compatability(material):
            raise ValueError("Material is not compatible with this printer.")

        depreciation_cost = self.depreciation_cost_per_minute * print_time
        material_cost = material.price_per_kg * (print_weight / 1000)
        service_cost = self.service_cost * print_time
        electricity_cost = self.electricity_cost * print_time
        return depreciation_cost, material_cost, service_cost, electricity_cost


class Print(Base, table=True):
    """Print model."""

    __table_args__ = (UniqueConstraint("printer_id", "material_id", "name"),)

    name: str = Field(nullable=False)
    print_time: float = Field(nullable=False)
    """Minutes"""
    print_weight: float = Field(nullable=False)
    """g"""
    printer_id: int = Field(nullable=False, foreign_key="printer.id")
    material_id: int = Field(nullable=False, foreign_key="material.id")

    # Relationships
    printer: Printer = Relationship()
    material: Material = Relationship()


class PrintJob(Base, table=True):
    """Print job model."""

    __table_args__ = (UniqueConstraint("print_id", "uuid"),)

    uuid: str = Field(nullable=False, unique=True)
    print_id: int = Field(nullable=False, foreign_key="print.id")
    date_started: Optional[datetime] = Field(nullable=True)
    date_finished: Optional[datetime] = Field(nullable=True)
    preparation_time: float = Field(nullable=False, default=0.00)
    slice_time: float = Field(nullable=False, default=0.00)
    transfer_time: float = Field(nullable=False, default=0.00)
    post_processing_time: float = Field(nullable=False, default=0.00)
    support_removal_time: float = Field(nullable=False, default=0.00)
    packaging_time: float = Field(nullable=False, default=0.00)
    additional_time: float = Field(nullable=False, default=0.00)
    cost_per_minute: float = Field(nullable=False)
    """This is the hourly rate divided by 60."""

    # Relationships
    print: Print = Relationship()

    @property
    def total_time(self) -> float:
        """Returns the total time in minutes."""
        return (
            self.preparation_time
            + self.slice_time
            + self.transfer_time
            + self.post_processing_time
            + self.support_removal_time
            + self.packaging_time
            + self.additional_time
        )

    @property
    def preparation_cost(self) -> float:
        """Returns the preparation cost."""
        return self.preparation_time * self.cost_per_minute

    @property
    def slice_cost(self) -> float:
        """Returns the slice cost."""
        return self.slice_time * self.cost_per_minute

    @property
    def transfer_cost(self) -> float:
        """Returns the transfer cost."""
        return self.transfer_time * self.cost_per_minute

    @property
    def post_processing_cost(self) -> float:
        """Returns the post processing cost."""
        return self.post_processing_time * self.cost_per_minute

    @property
    def support_removal_cost(self) -> float:
        """Returns the support removal cost."""
        return self.support_removal_time * self.cost_per_minute

    @property
    def packaging_cost(self) -> float:
        """Returns the packaging cost."""
        return self.packaging_time * self.cost_per_minute

    @property
    def additional_cost(self) -> float:
        """Returns the additional cost."""
        return self.additional_time * self.cost_per_minute

    @property
    def total_cost(self) -> float:
        """Returns the total cost."""
        return (
            self.preparation_cost
            + self.slice_cost
            + self.transfer_cost
            + self.post_processing_cost
            + self.support_removal_cost
            + self.packaging_cost
            + self.additional_cost
        )

    def start(self):
        """Starts the print job."""
        self.date_started = datetime.now()

    def finish(self):
        """Finishes the print job."""
        self.date_finished = datetime.now()


class JobQuote(Base, table=True):
    """Job quote model."""

    __table_args__ = (UniqueConstraint("id", "print_job_id", "customer_name"),)

    customer_name: str = Field(nullable=False)
    print_job_id: int = Field(nullable=False, foreign_key="printjob.id")
    date_created: datetime = Field(nullable=False, default_factory=datetime.now)
    date_valid_until: datetime = Field(nullable=False)
    total_cost: float = Field(nullable=False)

    # Relationships
    print_job: PrintJob = Relationship()