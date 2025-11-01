#!/usr/bin/env python3

import requests
import json
import hashlib
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

async def setup_admin_users():
    """Setup the required admin users for testing"""
    
    # MongoDB connection
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    # Check if users already exist
    existing_users = await db.users.find({}).to_list(length=None)
    print(f"Found {len(existing_users)} existing users")
    
    for user in existing_users:
        print(f"  - {user.get('email')} ({user.get('role')})")
    
    # Check if andrew@test.com exists
    andrew_test = await db.users.find_one({"email": "andrew@test.com"})
    if andrew_test:
        print("andrew@test.com already exists")
        # Update to SUPER_ADMIN if not already
        if andrew_test.get('role') != 'SUPER_ADMIN':
            await db.users.update_one(
                {"email": "andrew@test.com"},
                {"$set": {"role": "SUPER_ADMIN"}}
            )
            print("Updated andrew@test.com to SUPER_ADMIN role")
    else:
        # Create andrew@test.com as SUPER_ADMIN
        import uuid
        from datetime import datetime, timezone
        
        # Create organization first
        org_data = {
            "id": str(uuid.uuid4()),
            "name": "Test Organization",
            "industry": "Technology",
            "created_at": datetime.now(timezone.utc)
        }
        await db.organizations.insert_one(org_data)
        
        # Create user
        user_data = {
            "id": str(uuid.uuid4()),
            "email": "andrew@test.com",
            "hashed_password": hash_password("password123"),
            "name": "Andrew Test",
            "org_id": org_data["id"],
            "role": "SUPER_ADMIN",
            "is_active": True,
            "created_at": datetime.now(timezone.utc)
        }
        await db.users.insert_one(user_data)
        print("Created andrew@test.com as SUPER_ADMIN")
    
    # Check if andrew@vciso.one exists
    andrew_vciso = await db.users.find_one({"email": "andrew@vciso.one"})
    if andrew_vciso:
        print("andrew@vciso.one already exists")
        # Update to ADMIN if not already
        if andrew_vciso.get('role') != 'ADMIN':
            await db.users.update_one(
                {"email": "andrew@vciso.one"},
                {"$set": {"role": "ADMIN"}}
            )
            print("Updated andrew@vciso.one to ADMIN role")
    else:
        # Create andrew@vciso.one as ADMIN
        import uuid
        from datetime import datetime, timezone
        
        # Create organization first
        org_data = {
            "id": str(uuid.uuid4()),
            "name": "vCISO One",
            "industry": "Cybersecurity",
            "created_at": datetime.now(timezone.utc)
        }
        await db.organizations.insert_one(org_data)
        
        # Create user
        user_data = {
            "id": str(uuid.uuid4()),
            "email": "andrew@vciso.one",
            "hashed_password": hash_password("password123"),
            "name": "Andrew vCISO",
            "org_id": org_data["id"],
            "role": "ADMIN",
            "is_active": True,
            "created_at": datetime.now(timezone.utc)
        }
        await db.users.insert_one(user_data)
        print("Created andrew@vciso.one as ADMIN")
    
    # Verify final state
    final_users = await db.users.find({}).to_list(length=None)
    print(f"\nFinal user state ({len(final_users)} users):")
    for user in final_users:
        print(f"  - {user.get('email')} ({user.get('role')}) - Active: {user.get('is_active', True)}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(setup_admin_users())