import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def update_su1():
    # Get environment variables
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'am_ai_safe_db')
    
    print(f"Connecting to: {db_name}")
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Update SU-1 question
    result = await db.questions.update_one(
        {"code": "SU-1"},
        {"$set": {
            "text": "How do you assess the environmental impact of training and running your AI system (e.g., energy usage, compute intensity, carbon footprint)?",
            "foundational_answer": "No assessments are conducted to measure the environmental impact of the AI system.",
            "developing_answer": "Informally estimate environmental impact without consistent measurement or documentation.",
            "established_answer": "Conduct periodic assessments of energy usage and emissions, mainly during major training runs, with some influence on technical decisions.",
            "leading_answer": "Regularly measure and report the environmental impact of both training and inference workloads, including energy use, compute intensity, and estimated carbon emissions, and use this data to guide design and infrastructure decisions."
        }}
    )
    
    print(f"✅ Updated SU-1: {result.modified_count} document(s) modified")
    
    # Verify the update
    su1 = await db.questions.find_one({"code": "SU-1"})
    if su1:
        print(f"✅ Verified - Question text: {su1['text']}")
        print(f"✅ Verified - Leading answer: {su1['leading_answer'][:100]}...")
    else:
        print("❌ SU-1 not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_su1())
