import logging

from sqlmodel import Session, SQLModel, create_engine

logger = logging.getLogger(f"{__name__}")

DATABASE_URL = f"sqlite:///database.db"


engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


class DBContext:
    """Context manager for talking to the database."""
    
    def __init__(self, dissable_foreign_key_checks: bool=False):
        logger.debug("[DATABASE] Session created.")
        self.db = Session(engine)
        self.db.expire_on_commit = False
        self.dissable_foreign_key_checks = dissable_foreign_key_checks
        if self.dissable_foreign_key_checks:
            logger.warning("[DATABASE] Dissabling foreign key checks.")
            self.db.execute("SET foreign_key_checks = 0;")

    def __enter__(self) -> Session:
        logger.debug("[DATABASE] Starting DB context.")
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        # logger.debug("Exiting DB context.")
        if self.dissable_foreign_key_checks:
            logger.warning("[DATABASE] Enabling foreign key checks.")
            self.db.execute("SET foreign_key_checks = 1;")
        self.db.close()
        logger.debug("[DATABASE] Session closed.")


def get_session() -> Session:
    """ Returns the current db connection """
    with DBContext() as session:
        yield session