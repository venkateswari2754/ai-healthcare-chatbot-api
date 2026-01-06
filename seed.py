from app.database import SessionLocal, engine, Base
from app.models import Client, Equipment

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # 1. Check if client exists
    existing_client = db.query(Client).filter(Client.client_code == "HOSP001").first()
    if not existing_client:
        print("Seeding Client...")
        client = Client(
            name="General Hospital",
            client_code="HOSP001",
            address="123 Health St, Medicity"
        )
        db.add(client)
        db.commit()
        print("Client 'HOSP001' created.")
    else:
        print("Client 'HOSP001' already exists.")

    db.close()

if __name__ == "__main__":
    seed_data()