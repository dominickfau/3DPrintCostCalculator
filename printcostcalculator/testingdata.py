from sqlmodel import Session

from printcostcalculator import models


MATERIAL_TYPES = {
    "PLA": models.MaterialType(code="PLA", name="Polylactic Acid"),
    "ABS": models.MaterialType(code="ABS", name="Acrylonitrile Butadiene Styrene"),
    "PC": models.MaterialType(code="PC", name="Polycarbonate"),
    "Nylon": models.MaterialType(code="Nylon", name="Nylon"),
    "PETG": models.MaterialType(
        code="PETG", name="Polyethylene Terephthalate Glycol-modified"
    ),
    "PETG-CF": models.MaterialType(code="PETG-CF", name="Carbon Fiber Reinforced PETG"),
}


MATERIAL_MANUFACTURERS = {
    "HatchBox": models.MaterialManufacturer(name="HatchBox"),
    "Bambu Lab": models.MaterialManufacturer(name="Bambu Lab"),
}


MATERIALS = [
    models.Material(
        manufacturer=MATERIAL_MANUFACTURERS["HatchBox"],
        color="Black",
        color_hex="#000000",
        diameter=1.75,
        price=25.0,
        weight=1.0,
        density=1.24,
        print_temperature=200,
        bed_temperature=40,
        material_type_id=1,
    ),
    models.Material(
        manufacture=MATERIAL_MANUFACTURERS["Bambu Lab"],
        color="Matte Ash Gray",
        color_hex="#9B9EA0",
        diameter=1.75,
        price=28.0,
        weight=1.0,
        density=1.31,
        print_temperature=200,
        bed_temperature=40,
        material_type_id=1,
    ),
    models.Material(
        manufacturer=MATERIAL_MANUFACTURERS["Bambu Lab"],
        color="Alpine Green Sparkle",
        color_hex="#3F5443",
        diameter=1.75,
        price=30.0,
        weight=1.0,
        density=1.26,
        print_temperature=200,
        bed_temperature=40,
        material_type_id=1,
    ),
    models.Material(
        manufacturer=MATERIAL_MANUFACTURERS["Bambu Lab"],
        color="Black",
        color_hex="#000000",
        diameter=1.75,
        price=35.0,
        weight=1.0,
        density=1.25,
        print_temperature=250,
        bed_temperature=70,
        material_type_id=6,
    ),
]


PRINTER_MANUFACTURERS = {"Bambu Lab": models.PrinterManufacturer(name="Bambu Lab")}


PRINTERS = [
    models.Printer(
        manufacturer=PRINTER_MANUFACTURERS["Bambu Lab"],
        name="X1 Carbon",
        serial_number="123456789",
        material_diameter=1.75,
        price=1700,
        deprecation_time=5000,
        service_cost_per_life=850,
        energy_consumption=0.4,
    )
]


def create_test_data(session: Session) -> None:
    session.add_all([item for _, item in MATERIAL_TYPES.items()])
    session.add_all(MATERIALS)
    session.add_all(PRINTERS)
