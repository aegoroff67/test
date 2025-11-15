import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def update_in3():
    # Get environment variables
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'am_ai_safe_db')
    
    print(f"Connecting to: {db_name}")
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Update IN-3 question
    result = await db.questions.update_one(
        {"code": "IN-3"},
        {"$set": {
            "text": "Have you audited the system for potential exclusionary outcomes or unintended impacts on different demographic, cultural, or accessibility groups?",
            "foundational_answer": "No audits have been conducted for exclusionary outcomes or unintended group impacts.",
            "developing_answer": "Address exclusionary outcomes reactively when raised by users, regulators, or staff, without structured audits.",
            "established_answer": "Perform occasional audits for exclusionary impacts affecting some key user groups, with partial follow-up.",
            "leading_answer": "Conduct regular, comprehensive audits for exclusionary outcomes across multiple demographic, cultural, and accessibility groups, and take documented corrective actions."
        }}
    )
    
    print(f"✅ Updated IN-3: {result.modified_count} document(s) modified")
    
    # Verify the update
    in3 = await db.questions.find_one({"code": "IN-3"})
    if in3:
        print(f"✅ Verified - Question text: {in3['text']}")
        print(f"✅ Verified - Leading answer: {in3['leading_answer'][:100]}...")
    else:
        print("❌ IN-3 not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_in3())
