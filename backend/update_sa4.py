import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def update_sa4():
    # Get environment variables
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'am_ai_safe_db')
    
    print(f"Connecting to: {db_name}")
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Update SA-4 question
    result = await db.questions.update_one(
        {"code": "SA-4"},
        {"$set": {
            "text": "How do you handle situations where the system's actions conflict with human safety requirements or safety policies?",
            "foundational_answer": "No specific measures exist to handle conflicts between system actions and human safety requirements.",
            "developing_answer": "Rely mainly on manual intervention and ad-hoc decisions to address safety conflicts when they arise.",
            "established_answer": "Include basic safety protocols and some human override options, but they are not consistently documented, tested, or reviewed.",
            "leading_answer": "Implement documented safety protocols, including clearly defined fail-safe mechanisms, human override capabilities, and escalation paths. These are tested against realistic scenarios and regularly reviewed."
        }}
    )
    
    print(f"✅ Updated SA-4: {result.modified_count} document(s) modified")
    
    # Verify the update
    sa4 = await db.questions.find_one({"code": "SA-4"})
    if sa4:
        print(f"✅ Verified - Question text: {sa4['text']}")
        print(f"✅ Verified - Leading answer: {sa4['leading_answer'][:100]}...")
    else:
        print("❌ SA-4 not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_sa4())
