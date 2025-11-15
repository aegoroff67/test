import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def update_ac3():
    # Get environment variables
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'am_ai_safe_db')
    
    print(f"Connecting to: {db_name}")
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Update AC-3 question
    result = await db.questions.update_one(
        {"code": "AC-3"},
        {"$set": {
            "text": "Are roles and responsibilities for AI risk, ethics, and compliance formally defined and assigned (e.g., system owner, risk owner, model steward)?",
            "foundational_answer": "No clear roles or responsibilities for AI risk, ethics, or compliance have been defined.",
            "developing_answer": "Responsibility is assumed by a team or function, but individual accountabilities are unclear.",
            "established_answer": "Roles and responsibilities are understood informally and partially documented, but not consistently maintained or reviewed.",
            "leading_answer": "Roles and responsibilities for AI risk, ethics, and compliance are clearly defined, formally documented, and assigned to named owners (e.g., system owner, risk owner, model steward), with regular review."
        }}
    )
    
    print(f"✅ Updated AC-3: {result.modified_count} document(s) modified")
    
    # Verify the update
    ac3 = await db.questions.find_one({"code": "AC-3"})
    if ac3:
        print(f"✅ Verified - Question text: {ac3['text']}")
        print(f"✅ Verified - Leading answer: {ac3['leading_answer'][:100]}...")
    else:
        print("❌ AC-3 not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_ac3())
