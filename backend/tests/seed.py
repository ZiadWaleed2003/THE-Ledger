from ..src.core.database import get_db_base , get_db_session_factory_and_engine
from ..src.models.asset import Asset

from datetime import datetime

def init_db():
    # 1. Create the Tables
    print("Creating database tables...")
    db , engine = get_db_session_factory_and_engine()
    base = get_db_base()
    base.metadata.create_all(bind=engine)

    
    # Check if data exists
    if db.query(Asset).first():
        print("Database already contains data. Skipping seed.")
        return

    print("Seeding data...")
    assets = [
        Asset(
            name="MacBook Pro M3",
            category="Electronics",
            value=2500.0,
            status="In Use",
            purchase_date=datetime(2025, 1, 15)
        ),
        Asset(
            name="Herman Miller Chair",
            category="Furniture",
            value=1200.0,
            status="In Use",
            purchase_date=datetime(2024, 11, 20)
        ),
        Asset(
            name="Dell UltraSharp Monitor",
            category="Electronics",
            value=600.0,
            status="Maintenance",
            purchase_date=datetime(2024, 8, 5)
        ),
        Asset(
            name="NVIDIA H100 GPU",
            category="Hardware",
            value=30000.0,
            status="Reserved",
            purchase_date=datetime(2025, 2, 1)
        )
    ]

    # 3. Save to DB
    for asset in assets:
        db.add(asset)
    
    db.commit()
    print("Success! Database populated.")
    db.close()

if __name__ == "__main__":
    init_db()