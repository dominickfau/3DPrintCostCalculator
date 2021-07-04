import sqlite3

connection = sqlite3.connect("test.db")

cursor = connection.cursor()

def insert_test_data():
    create_blank_database()
    cursor.execute(
            """
                INSERT INTO material (description, materialTypeId, name, price, quantity)
                VALUES("Standard Gray", 30, "Elegoo Standard Gray", 45.00, 1000.00),
                    ("Black PLA", 10, "Hatchbox PLA Black", 30.00, 1000.00)
            """
    )
    
    cursor.execute(
            """
                INSERT INTO printer (bedSizeHeight, bedSizeLength, bedSizeWidth, deprecationPerHour, deprecationTime, energyConsumption, materialTypeId, name, price, totalServiceCost)
                VALUES(160.00, 100.00, 80.00, 0.51, 5000.00, 1.01, 30, "Elegoo Mars 2 Pro", 300.00, 2250.00),
                    (180.00, 220.00, 220.00, 0.32, 5000.00, 0.75, 10, "Ender 3 Pro", 400.00, 1000.50)
            """
    )
    
    connection.commit()
    
def insert_default_data():
    try:
        cursor.execute(
            """
                INSERT INTO setting ("name", "value")
                VALUES("Energy Cost", 0.15),
                    ("Labor Rate", 30.00),
                    ("Failure Rate", 10.00)
            """
        )
    except sqlite3.IntegrityError:
        pass
    
    try:
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
    except sqlite3.IntegrityError:
        pass
    
    
def create_blank_database():
    try:
        cursor.execute(
                """
                    CREATE TABLE "setting" (
                    "id"	INTEGER NOT NULL,
                    "name"	TEXT NOT NULL UNIQUE,
                    "value"	REAL NOT NULL,
                    PRIMARY KEY("id" AUTOINCREMENT)
                    );
                """
        )
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute(
                """
                    CREATE TABLE "materialType" (
                    "id"	INTEGER NOT NULL,
                    "name"	TEXT NOT NULL,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
                """
        )
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute(
                """
                    CREATE TABLE "printer" (
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
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute(
                """
                    CREATE TABLE "serviceCostCalcRow" (
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
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute(
                """
                    CREATE TABLE "material" (
                    "id"	INTEGER NOT NULL,
                    "description"	TEXT NOT NULL,
                    "materialTypeId" INTEGER NOT NULL,
                    "name"	TEXT NOT NULL UNIQUE,
                    "price"	REAL NOT NULL,
                    "quantity"	REAL NOT NULL,
                    CONSTRAINT "FK_materialTypeId" FOREIGN KEY("materialTypeId") REFERENCES materialType(id),
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
                """
        )
    except sqlite3.OperationalError:
        pass

    connection.commit()


def rows_to_dict(data, columnNames):
    returnData = []
    
    for row in data:
        rowData = {}
        for x, item in enumerate(row):
            rowData[columnNames[x]] = item
        returnData.append(rowData)
    
    return returnData

class Setting(object):
    def __init__(self, id, name, value):
        self.id = id
        self.name = name
        self.value = value
    
    def update(self):
        values = {
            "id": self.id,
            "name": self.name,
            "value": self.value
        }
        
        cursor.execute(
            """
                UPDATE setting SET name = :name, value = :value
                WHERE id = :id
            """, values
        )

        connection.commit()
        
    @classmethod
    def from_name(cls, name):
        cursor.execute(
            "SELECT id, name, value FROM setting WHERE name = :name", {"name": name}
        )

        data = cursor.fetchall()[0]
        if data:
            return cls(id = data[0], name = data[1], value = data[2])
        else:
            return None
    
    @classmethod
    def find_all(cls):
        cursor.execute("SELECT name FROM setting")

        columnNames = [row[0] for row in cursor.description]
        
        data = cursor.fetchall()
        data = rows_to_dict(data, columnNames)
        
        objects = []
        if data:
            for row in data:
                objects.append(cls.from_name(row["name"]))
        return objects
    
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
            return cls(id = data[0], name = data[1])
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
    
    @classmethod
    def find_all(cls):
        cursor.execute("SELECT name FROM materialType")

        columnNames = [row[0] for row in cursor.description]
        
        data = cursor.fetchall()
        data = rows_to_dict(data, columnNames)
        
        objects = []
        if data:
            for row in data:
                objects.append(cls.from_name(row["name"]))
        return objects
        
        
class Printer(object):
    REQUIRED_KEYS = [
            "bedSizeHeight",
            "bedSizeLength",
            "bedSizeWidth",
            "deprecationPerHour",
            "deprecationTime",
            "energyConsumption",
            "materialTypeName",
            "name",
            "price",
            "totalServiceCost"
        ]
    
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
        try:
            data = cursor.fetchall()[0]
        except IndexError:
            data = None
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
                INSERT INTO printer ("bedSizeHeight", "bedSizeLength", "bedSizeWidth", "deprecationPerHour",
                                        "deprecationTime", "energyConsumption", "materialTypeId", "name", "price", "totalServiceCost")

                VALUES(:bedSizeHeight, :bedSizeWidth, :bedSizeLength, :deprecationPerHour, :deprecationTime,
                        :energyConsumption, :materialTypeId, :name, :price, :totalServiceCost)
            """, values
        )

        connection.commit()
    
    def update(self, id):
        values = {
            "id": id,
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
                UPDATE printer SET bedSizeHeight = :bedSizeHeight, bedSizeLength = :bedSizeLength, bedSizeWidth = :bedSizeWidth,
                                deprecationPerHour = :deprecationPerHour, deprecationTime = :deprecationTime,
                                energyConsumption = :energyConsumption, materialTypeId = :materialTypeId,
                                name = :name, price = :price, totalServiceCost = :totalServiceCost
                WHERE id = :id
            """, values
        )

        connection.commit()
    
    def delete(self, id):
        values = {"id": id}
        cursor.execute("DELETE FROM printer WHERE id = :id", values)

        connection.commit()
        
    @classmethod
    def from_dictionary(cls, dictionary):
        for key in cls.REQUIRED_KEYS:
            if key not in dictionary.keys(): raise ValueError(f"Printer missing required key {key}")
            
        return cls(bedSizeHeight = dictionary["bedSizeHeight"],
                    bedSizeLength = dictionary["bedSizeLength"],
                    bedSizeWidth = dictionary["bedSizeWidth"],
                    deprecationPerHour = dictionary["deprecationPerHour"],
                    deprecationTime = dictionary["deprecationTime"],
                    energyConsumption = dictionary["energyConsumption"],
                    materialType = MaterialType.from_name(dictionary["materialTypeName"]),
                    name = dictionary["name"],
                    price = dictionary["price"],
                    totalServiceCost = dictionary["totalServiceCost"])
    
    @classmethod
    def from_name(cls, name):
        cursor.execute(
            "SELECT * FROM printer WHERE name = :name", {"name": name}
        )

        columnNames = [row[0] for row in cursor.description]
        
        data = cursor.fetchall()
        if data:
            data = rows_to_dict(data, columnNames)[0]
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
    
    @classmethod
    def find_all(cls):
        cursor.execute("SELECT name FROM printer")

        columnNames = [row[0] for row in cursor.description]
        
        data = cursor.fetchall()
        data = rows_to_dict(data, columnNames)
        
        objects = []
        if data:
            for row in data:
                objects.append(cls.from_name(row["name"]))
        
        return objects
        
class Material(object):
    REQUIRED_KEYS = [
        "name",
        "price",
        "quantity",
        "materialTypeName",
        "description"
    ]
    def __init__(self, description, materialType, name, price, quantity):
        self.description = description
        self.materialType = materialType
        self.name = name
        self.price = price
        self.quantity = quantity
        
        if not isinstance(self.materialType, MaterialType): raise TypeError("materialType must be of type MaterialType()")
    
    @property
    def id(self):
        cursor.execute("SELECT id FROM material WHERE name = :name", {"name": self.name})
        try:
            data = cursor.fetchall()[0]
        except IndexError:
            data = None
        if data:
            return data[0]
        else:
            return None
        
    def insert(self):
        values = {
            "description": self.description,
            "materialTypeId": self.materialType.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
           }
        
        cursor.execute(
            """
                INSERT INTO material (description, materialTypeId, name, price, quantity)
                VALUES(:description, :materialTypeId, :name, :price, :quantity)
            """, values
        )

        connection.commit()
        
    def update(self, id):
        values = {
            "id": id,
            "description": self.description,
            "materialTypeId": self.materialType.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
           }
        
        cursor.execute(
            """
                UPDATE material SET description = :description, materialTypeId = :materialTypeId, name = :name, price = :price, quantity = :quantity
                WHERE id = :id
            """, values
        )

        connection.commit()
    
    def delete(self, id):
        values = {"id": id}
        cursor.execute("DELETE FROM material WHERE id = :id", values)

        connection.commit()
    
    @classmethod
    def from_name(cls, name):
        cursor.execute(
            "SELECT * FROM material WHERE name = :name", {"name": name}
        )

        columnNames = [row[0] for row in cursor.description]
        
        data = cursor.fetchall()
        data = rows_to_dict(data, columnNames)[0]
        if data:
            return cls(description = data["description"],
                       materialType = MaterialType.from_id(data["materialTypeId"]),
                       name = data["name"],
                       price = data["price"],
                       quantity = data["quantity"])
        else:
            return None
    
    @classmethod
    def find_all(cls):
        cursor.execute("SELECT name FROM material")

        columnNames = [row[0] for row in cursor.description]
        
        data = cursor.fetchall()
        data = rows_to_dict(data, columnNames)
        
        objects = []
        if data:
            for row in data:
                objects.append(cls.from_name(row["name"]))
        return objects
    
    @classmethod
    def from_dictionary(cls, dictionary):
        for key in cls.REQUIRED_KEYS:
            if key not in dictionary.keys(): raise ValueError(f"Material missing required key {key}")
            
        return cls(description = dictionary["description"],
                    materialType = MaterialType.from_name(dictionary["materialTypeName"]),
                    name = dictionary["name"],
                    price = dictionary["price"],
                    quantity = dictionary["quantity"])