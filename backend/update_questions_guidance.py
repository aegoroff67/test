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
    """Update existing questions with text, explanation, additional_guidance, and evidence_types fields"""
    
    # Create a lookup dict by question code
    questions_lookup = {
        q["code"]: q
        for q in COMPLETE_QUESTIONS_DATA
    }
    
    # Get all questions from the database
    questions = await db.questions.find({}, {"_id": 0}).to_list(length=None)
    
    updated_count = 0
    for question in questions:
        code = question.get("code")
        if code in questions_lookup:
            source_question = questions_lookup[code]
            
            # Prepare update fields
            update_fields = {
                "text": source_question.get("text"),
                "explanation": source_question.get("explanation"),
                "additional_guidance": source_question.get("additional_guidance"),
                "evidence_types": source_question.get("evidence_types"),
                "foundational_answer": source_question.get("foundational_answer"),
                "developing_answer": source_question.get("developing_answer"),
                "established_answer": source_question.get("established_answer"),
                "leading_answer": source_question.get("leading_answer")
            }
            
            # Update the question in the database
            result = await db.questions.update_one(
                {"code": code},
                {"$set": update_fields}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                if source_question.get("evidence_types"):
                    print(f"✓ Updated {code} (text, explanation, additional_guidance, evidence_types)")
                else:
                    print(f"✓ Updated {code} (text, explanation, additional_guidance)")
    
    print(f"\n✅ Updated {updated_count} questions with complete data")
    
    # Verify PR-2 and PR-5
    print("\n🔍 Verifying PR-2 and PR-5:")
    pr2 = await db.questions.find_one({"code": "PR-2"}, {"_id": 0})
    pr5 = await db.questions.find_one({"code": "PR-5"}, {"_id": 0})
    
    if pr2:
        has_guidance = bool(pr2.get("additional_guidance"))
        has_evidence = bool(pr2.get("evidence_types"))
        print(f"PR-2: {'✓' if has_guidance else '✗'} additional_guidance present: {has_guidance}")
        print(f"      {'✓' if has_evidence else '✗'} evidence_types present: {has_evidence}")
        if has_guidance:
            print(f"      Guidance preview: {pr2['additional_guidance'][:80]}...")
        if has_evidence:
            print(f"      Evidence preview: {pr2['evidence_types'][:80]}...")
    
    if pr5:
        has_guidance = bool(pr5.get("additional_guidance"))
        has_evidence = bool(pr5.get("evidence_types"))
        print(f"\nPR-5: {'✓' if has_guidance else '✗'} additional_guidance present: {has_guidance}")
        print(f"      {'✓' if has_evidence else '✗'} evidence_types present: {has_evidence}")
        if has_guidance:
            print(f"      Guidance preview: {pr5['additional_guidance'][:80]}...")
        if has_evidence:
            print(f"      Evidence preview: {pr5['evidence_types'][:80]}...")

if __name__ == "__main__":
    print("Starting question update process...")
    asyncio.run(update_questions())
    print("\nDone!")
