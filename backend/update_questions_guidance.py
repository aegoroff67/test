#!/usr/bin/env python3
"""
Script to update existing questions in the database with additional_guidance field
from complete_questions.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pathlib import Path
from complete_questions import COMPLETE_QUESTIONS_DATA

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def update_questions():
    """Update existing questions with additional_guidance field"""
    
    # Create a lookup dict by question code
    guidance_lookup = {
        q["code"]: q.get("additional_guidance") 
        for q in COMPLETE_QUESTIONS_DATA
    }
    
    # Get all questions from the database
    questions = await db.questions.find({}, {"_id": 0}).to_list(length=None)
    
    updated_count = 0
    for question in questions:
        code = question.get("code")
        if code in guidance_lookup:
            additional_guidance = guidance_lookup[code]
            
            # Update the question in the database
            result = await db.questions.update_one(
                {"code": code},
                {"$set": {"additional_guidance": additional_guidance}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                if additional_guidance:
                    print(f"✓ Updated {code} with additional_guidance")
                else:
                    print(f"- Set {code} additional_guidance to None")
    
    print(f"\n✅ Updated {updated_count} questions with additional_guidance field")
    
    # Verify PR-2 and PR-5
    print("\n🔍 Verifying PR-2 and PR-5:")
    pr2 = await db.questions.find_one({"code": "PR-2"}, {"_id": 0})
    pr5 = await db.questions.find_one({"code": "PR-5"}, {"_id": 0})
    
    if pr2:
        has_guidance = bool(pr2.get("additional_guidance"))
        print(f"PR-2: {'✓' if has_guidance else '✗'} additional_guidance present: {has_guidance}")
        if has_guidance:
            print(f"      Content preview: {pr2['additional_guidance'][:100]}...")
    
    if pr5:
        has_guidance = bool(pr5.get("additional_guidance"))
        print(f"PR-5: {'✓' if has_guidance else '✗'} additional_guidance present: {has_guidance}")
        if has_guidance:
            print(f"      Content preview: {pr5['additional_guidance'][:100]}...")

if __name__ == "__main__":
    print("Starting question update process...")
    asyncio.run(update_questions())
    print("\nDone!")
