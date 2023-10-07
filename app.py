from printcostcalculator import models
from printcostcalculator.database import DBContext, create_db_and_tables
from printcostcalculator.testingdata import create_test_data


def init_db():
    create_db_and_tables()

    with DBContext() as session:
        create_test_data(session)
        session.commit()

# init_db()

with DBContext() as session:
    printer = session.query(models.Printer).filter(models.Printer.name == "X1 Carbon").first() # type: models.Printer
    petg_cf = session.query(models.MaterialType).filter(models.MaterialType.code == "PETG-CF").first() # type: models.MaterialType
    material = session.query(models.Material).filter(
        models.Material.manufacture == "Bambu Lab",
        models.Material.color == "Black",
        models.Material.material_type == petg_cf
        ).first()

