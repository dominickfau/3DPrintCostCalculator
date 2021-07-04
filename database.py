import sqlite3

connection = sqlite3.connect("test.db")

cursor = connection.cursor()

def create_blank_database():
    cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS "setting" (
                "id"	INTEGER NOT NULL,
                "name"	TEXT NOT NULL,
                "value"	REAL NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
                );
            """
    )
    
    cursor.execute(
        """
            INSERT INTO setting ("name", "value")
            VALUES("Energy Cost", 0.15),
                ("Labor Rate", 30.00),
                ("Failure Rate", 10.00)
        """
    )
    
    cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS "materialType" (
                "id"	INTEGER NOT NULL,
                "name"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
    )
    
    cursor.execute(
        """
            INSERT INTO materialType (id, name)
            VALUES(10, "Fused Deposition Modeling (FDM)"),
                (20, "Stereolithography (SLA)"),
                (30, "Masked Stereolithography (MSLA)"),
                (40, "Direct Light Processing (DLP)"),
                (50, "Selective Laser Sintering (SLS)"),
                (60, "Material Jetting (MJ)"),
                (70, "Drop on Demand (DOD)"),
                (80, "Binder Jetting (BJ)"),
                (90, "Direct Metal Laser Sintering (DMLS)"),
                (100, "Selective Laser Melting (SLM)"),
                (110, "Electron Beam Melting (EBM)")
        """
    )

    cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS "printer" (
                "id"	INTEGER NOT NULL,
                "bedSizeHeight"	REAL NOT NULL DEFAULT 0.00,
                "bedSizeLength"	REAL NOT NULL DEFAULT 0.00,
                "bedSizeWidth"	REAL NOT NULL DEFAULT 0.00,
                "deprecationPerHour"	REAL NOT NULL DEFAULT 0.00,
                "deprecationTime"	REAL NOT NULL DEFAULT 0.00,
                "energyConsumption"	REAL NOT NULL DEFAULT 0.00,
                "materialTypeId" INTEGER NOT NULL,
                "name"	TEXT NOT NULL UNIQUE,
                "price"	REAL NOT NULL DEFAULT 0.00,
                "totalServiceCost"	REAL NOT NULL DEFAULT 0.00,
                CONSTRAINT "FK_printerMaterialTypeId" FOREIGN KEY("materialTypeId") REFERENCES materialType(id),
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
    )

    cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS "serviceCostCalcRow" (
                "id"	INTEGER NOT NULL,
                "lifeInterval"	REAL NOT NULL,
                "name"	TEXT NOT NULL,
                "price"	REAL NOT NULL,
                "printerId"	INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT),
                CONSTRAINT "FK_printerId" FOREIGN KEY("printerId") REFERENCES printer(id)
            );
            """
    )

    cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS "material" (
                "id"	INTEGER NOT NULL,
                "description"	TEXT NOT NULL,
                "materialTypeId" INTEGER NOT NULL,
                "name"	TEXT NOT NULL,
                "price"	REAL NOT NULL,
                CONSTRAINT "FK_materialTypeId" FOREIGN KEY("materialTypeId") REFERENCES materialType(id),
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
    )

    connection.commit()


def rows_to_dict(data, columnNames):
    returnData = []
    
    for row in data:
        rowData = {}
        for x, item in enumerate(row):
            rowData[columnNames[x]] = item
        returnData.append(rowData)
    
    return returnData

class MaterialType(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    # @property
    # def id(self):
    #     cursor.execute("SELECT id FROM materialType WHERE name = :name", {"name": self.name})
    #     data = cursor.fetchall()[0]
    #     if data:
    #         return data[0]
    #     else:
    #         return None
    
    @classmethod
    def from_name(cls, name):
        cursor.execute(
            "SELECT id, name FROM materialType WHERE name = :name", {"name": name}
        )

        data = cursor.fetchall()[0]
        if data:
            return cls(name = data[1])
        else:
            return None
    
    @classmethod
    def from_id(cls, id):
        cursor.execute(
            "SELECT id, name FROM materialType WHERE id = :id", {"id": id}
        )

        data = cursor.fetchall()[0]
        if data:
            return cls(id = data[0], name = data[1])
        else:
            return None
        
        
class Printer(object):
    def __init__(self, bedSizeHeight, bedSizeLength, bedSizeWidth, deprecationPerHour, deprecationTime, energyConsumption, materialType, name, price, totalServiceCost):
        self.bedSizeHeight = bedSizeHeight
        self.bedSizeLength = bedSizeLength
        self.bedSizeWidth = bedSizeWidth
        self.deprecationPerHour = deprecationPerHour
        self.deprecationTime = deprecationTime
        self.energyConsumption = energyConsumption
        self.materialType = materialType
        self.name = name
        self.price = price
        self.totalServiceCost = totalServiceCost
        
        if not isinstance(self.materialType, MaterialType): raise TypeError("materialType must be of type MaterialType()")
    
    @property
    def id(self):
        cursor.execute("SELECT id FROM printer WHERE name = :name", {"name": self.name})
        data = cursor.fetchall()[0]
        if data:
            return data[0]
        else:
            return None
        
    def insert(self):
        values = {
            "bedSizeHeight": self.bedSizeHeight,
            "bedSizeLength": self.bedSizeLength,
            "bedSizeWidth": self.bedSizeWidth,
            "deprecationPerHour": self.deprecationPerHour,
            "deprecationTime": self.deprecationTime,
            "energyConsumption": self.energyConsumption,
            "materialTypeId": self.materialType.id,
            "name": self.name,
            "price": self.price,
            "totalServiceCost": self.totalServiceCost
        }
        
        cursor.execute(
            """
                INSERT INTO printer ("bedSizeHeight", "bedSizeLength", "bedSizeWidth", "deprecationPerHour", "deprecationTime", "energyConsumption", "materialTypeId", "name", "price", "totalServiceCost")
                VALUES(:bedSizeHeight, :bedSizeWidth, :bedSizeLength, :deprecationPerHour, :deprecationTime, :energyConsumption, :materialTypeId, :name, :price, :totalServiceCost)
            """, values
        )

        connection.commit()
    
    @classmethod
    def from_name(cls, name):
        cursor.execute(
            "SELECT * FROM printer WHERE name = :name", {"name": name}
        )

        columnNames = [row[0] for row in cursor.description]
        
        data = cursor.fetchall()
        data = rows_to_dict(data, columnNames)[0]
        if data:
            return cls(bedSizeHeight = data["bedSizeHeight"],
                       bedSizeLength = data["bedSizeLength"],
                       bedSizeWidth = data["bedSizeWidth"],
                       deprecationPerHour = data["deprecationPerHour"],
                       deprecationTime = data["deprecationTime"],
                       energyConsumption = data["energyConsumption"],
                       materialType = MaterialType.from_id(data["materialTypeId"]),
                       name = data["name"],
                       price = data["price"],
                       totalServiceCost = data["totalServiceCost"])
        else:
            return None





if __name__ == '__main__':
    create_blank_database()


    cursor.execute(
        "SELECT * FROM materialType WHERE name = 'Masked Stereolithography (MSLA)'"
    )

    materialTypeId = cursor.fetchall()[0][0]

    values = {
        "materialTypeId": materialTypeId
    }

    cursor.execute(
        """
            INSERT INTO printer ("bedSizeHeight",
                                "bedSizeLength",
                                "bedSizeWidth",
                                "deprecationPerHour",
                                "deprecationTime",
                                "energyConsumption",
                                "materialTypeId",
                                "name",
                                "price",
                                "totalServiceCost"
                                )
            VALUES(149.00, 115.00, 65.00, 0.51, 5000.00, 1.00, :materialTypeId, "Elegoo Mars 2 Pro", 300.00, 2250.00)
        """, values
    )

    printerId = cursor.lastrowid

    connection.commit()

    values = {
        "printerId": printerId
    }

    cursor.execute(
        """
            INSERT INTO serviceCostCalcRow ("lifeInterval", "name", "price", "printerId")
            VALUES(1500.00, "FEP Film", 5.00, :printerId),
                (12000.00, "Screen", 30.00, :printerId),
                (12000.00, "Screen Misc", 20.00, :printerId)
        """, values
    )

    connection.commit()

    values = {
        "materialTypeId": materialTypeId
    }

    cursor.execute(
        """
            INSERT INTO material ("description", "materialTypeId", "name", "price")
            VALUES("Standard Gray", :materialTypeId, "Elegoo Standard Gray", 45.00)
        """, values
    )

    connection.commit()