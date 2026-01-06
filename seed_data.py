"""
Seed script to populate database with sample data for testing
Run: python seed_data.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models
from app.auth import get_password_hash

def seed_database():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing data (optional - comment out to keep data)
        # db.query(models.ChatLog).delete()
        # db.query(models.Payment).delete()
        # db.query(models.Invoice).delete()
        # db.query(models.ScheduledMaintenance).delete()
        # db.query(models.AMCContract).delete()
        # db.query(models.Warranty).delete()
        # db.query(models.Order).delete()
        # db.query(models.Equipment).delete()
        # db.query(models.Ticket).delete()
        # db.query(models.UserClient).delete()
        # db.query(models.User).delete()
        # db.query(models.Client).delete()
        # db.commit()
        
        # 1. Create sample clients
        print("Creating clients...")
        client1 = models.Client(
            name="City Hospital",
            client_code="CLIENT_001",
            address="123 Medical Plaza, New York, NY"
        )
        client2 = models.Client(
            name="Rural Clinic",
            client_code="CLIENT_002",
            address="456 Healthcare Ave, Texas, TX"
        )
        db.add_all([client1, client2])
        db.commit()
        
        # 2. Create sample users
        print("Creating users...")
        user1 = models.User(
            email="admin@cityhospital.com",
            password_hash=get_password_hash("Venku@1982")
        )
        user2 = models.User(
            email="doctor@cityhospital.com",
            password_hash=get_password_hash("Venku@1982")
        )
        user3 = models.User(
            email="staff@ruralclinic.com",
            password_hash=get_password_hash("Venku@1982")
        )
        db.add_all([user1, user2, user3])
        db.commit()
        
        # 3. Link users to clients
        print("Linking users to clients...")
        uc1 = models.UserClient(user_id=user1.id, client_id=client1.id, is_primary=1)
        uc2 = models.UserClient(user_id=user2.id, client_id=client1.id, is_primary=1)
        uc3 = models.UserClient(user_id=user3.id, client_id=client2.id, is_primary=1)
        db.add_all([uc1, uc2, uc3])
        db.commit()
        
        # 4. Create sample equipment
        print("Creating equipment...")
        eq1 = models.Equipment(
            client_id=client1.id,
            model_name="Ultrasound Machine Pro 3000",
            serial_number="USM-001-2023",
            category="ultrasound",
            purchase_date=datetime.now() - timedelta(days=365),
            status="active"
        )
        eq2 = models.Equipment(
            client_id=client1.id,
            model_name="X-Ray Digital Plus",
            serial_number="XRA-002-2023",
            category="xray",
            purchase_date=datetime.now() - timedelta(days=180),
            status="active"
        )
        eq3 = models.Equipment(
            client_id=client2.id,
            model_name="Patient Monitor 500",
            serial_number="MON-003-2024",
            category="monitoring",
            purchase_date=datetime.now() - timedelta(days=30),
            status="active"
        )
        db.add_all([eq1, eq2, eq3])
        db.commit()
        
        # 5. Create sample orders
        print("Creating orders...")
        order1 = models.Order(
            client_id=client1.id,
            equipment_id=eq1.id,
            status="delivered",
            order_date=datetime.now() - timedelta(days=100),
            expected_delivery_date=datetime.now() - timedelta(days=85),
            tracking_number="TRK-2024-001"
        )
        order2 = models.Order(
            client_id=client1.id,
            equipment_id=eq2.id,
            status="shipped",
            order_date=datetime.now() - timedelta(days=50),
            expected_delivery_date=datetime.now() + timedelta(days=5),
            tracking_number="TRK-2024-002"
        )
        order3 = models.Order(
            client_id=client2.id,
            equipment_id=eq3.id,
            status="confirmed",
            order_date=datetime.now() - timedelta(days=10),
            expected_delivery_date=datetime.now() + timedelta(days=20),
            tracking_number="TRK-2024-003"
        )
        db.add_all([order1, order2, order3])
        db.commit()
        
        # 6. Create sample warranties
        print("Creating warranties...")
        war1 = models.Warranty(
            equipment_id=eq1.id,
            start_date=datetime.now() - timedelta(days=365),
            end_date=datetime.now() + timedelta(days=365),
            coverage_details="Full coverage including parts and labor",
            status="active"
        )
        war2 = models.Warranty(
            equipment_id=eq2.id,
            start_date=datetime.now() - timedelta(days=180),
            end_date=datetime.now() + timedelta(days=550),
            coverage_details="Parts and labor for 2 years",
            status="active"
        )
        db.add_all([war1, war2])
        db.commit()
        
        # 7. Create sample AMC contracts
        print("Creating AMC contracts...")
        amc1 = models.AMCContract(
            equipment_id=eq1.id,
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now() + timedelta(days=335),
            sla_details="4-hour response time, 99.5% uptime",
            status="active",
            cost=5000.00
        )
        amc2 = models.AMCContract(
            equipment_id=eq2.id,
            start_date=datetime.now() - timedelta(days=60),
            end_date=datetime.now() + timedelta(days=305),
            sla_details="8-hour response time, 99% uptime",
            status="active",
            cost=3000.00
        )
        db.add_all([amc1, amc2])
        db.commit()
        
        # 8. Create sample invoices
        print("Creating invoices...")
        inv1 = models.Invoice(
            client_id=client1.id,
            amount=50000.00,
            currency="USD",
            status="paid",
            invoice_date=datetime.now() - timedelta(days=60),
            due_date=datetime.now() - timedelta(days=30)
        )
        inv2 = models.Invoice(
            client_id=client1.id,
            amount=25000.00,
            currency="USD",
            status="pending",
            invoice_date=datetime.now() - timedelta(days=10),
            due_date=datetime.now() + timedelta(days=20)
        )
        inv3 = models.Invoice(
            client_id=client2.id,
            amount=15000.00,
            currency="USD",
            status="pending",
            invoice_date=datetime.now() - timedelta(days=5),
            due_date=datetime.now() + timedelta(days=25)
        )
        db.add_all([inv1, inv2, inv3])
        db.commit()
        
        # 9. Create sample payments
        print("Creating payments...")
        payment1 = models.Payment(
            invoice_id=inv1.id,
            amount=50000.00,
            payment_date=datetime.now() - timedelta(days=30),
            method="bank_transfer"
        )
        db.add(payment1)
        db.commit()
        
        # 10. Create sample tickets
        print("Creating tickets...")
        ticket1 = models.Ticket(
            client_id=client1.id,
            user_id=user1.id,
            subject="Ultrasound machine calibration needed",
            description="The ultrasound machine needs recalibration for accurate readings",
            status="in_progress",
            priority="high"
        )
        ticket2 = models.Ticket(
            client_id=client1.id,
            user_id=user2.id,
            subject="X-Ray machine not connecting to network",
            description="Cannot connect X-Ray machine to hospital network for data transfer",
            status="open",
            priority="critical"
        )
        ticket3 = models.Ticket(
            client_id=client2.id,
            user_id=user3.id,
            subject="Maintenance schedule inquiry",
            description="When is the next scheduled maintenance for patient monitors?",
            status="open",
            priority="medium"
        )
        db.add_all([ticket1, ticket2, ticket3])
        db.commit()
        
        # 11. Create sample scheduled maintenance
        print("Creating scheduled maintenance...")
        maint1 = models.ScheduledMaintenance(
            equipment_id=eq1.id,
            scheduled_date=datetime.now() + timedelta(days=30),
            status="scheduled",
            notes="Quarterly preventive maintenance"
        )
        maint2 = models.ScheduledMaintenance(
            equipment_id=eq2.id,
            scheduled_date=datetime.now() + timedelta(days=15),
            status="scheduled",
            notes="Replace filters and check calibration"
        )
        db.add_all([maint1, maint2])
        db.commit()
        
        print("\n✅ Database seeded successfully!")
        print("\n📋 Sample Data Created:")
        print(f"  - Clients: 2")
        print(f"  - Users: 3")
        print(f"  - Equipment: 3")
        print(f"  - Orders: 3")
        print(f"  - Warranties: 2")
        print(f"  - AMC Contracts: 2")
        print(f"  - Invoices: 3")
        print(f"  - Payments: 1")
        print(f"  - Tickets: 3")
        print(f"  - Scheduled Maintenance: 2")
        
        print("\n🧪 Test Credentials:")
        print("  Email: admin@cityhospital.com")
        print("  Password: password123")
        print("  Client Code: CLIENT_001")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
