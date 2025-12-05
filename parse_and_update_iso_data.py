#!/usr/bin/env python3
"""
Parse the complete Excel extraction and update all ISO 42001 alignment data
"""

import json
import re

# The extracted data from the Excel file contains all questions in a structured format
# Each entry has: Question Code, Alignment Rationale, Citation, and Control Intent

# I'll parse the extracted text systematically
raw_extracted_text = open('/app/extracted_excel_data.txt', 'r').read() if os.path.exists('/app/extracted_excel_data.txt') else ""

def parse_extracted_data(text):
    """
    Parse the extraction output to get all question mappings
    Returns dict: {question_code: {alignmentRationale, citation, controlIntent}}
    """
    updates = {}
    
    # Pattern to match question entries
    # Looking for: **Question Code/ID:** CODE followed by the three fields
    
    lines = text.split('\n')
    current_question = None
    current_field = None
    current_text = []
    
    for line in lines:
        # Check for question code
        if '**Question Code/ID:**' in line or '*   **Question Code/ID:**' in line:
            # Save previous question if exists
            if current_question and current_field:
                updates[current_question][current_field] = ' '.join(current_text).strip()
                current_text = []
            
            # Extract question code
            match = re.search(r'([A-Z]{2}-\d+)', line)
            if match:
                current_question = match.group(1)
                updates[current_question] = {}
                current_field = None
        
        # Check for field headers
        elif '**Alignment Details / Rationale:**' in line:
            if current_question and current_field:
                updates[current_question][current_field] = ' '.join(current_text).strip()
                current_text = []
            current_field = 'alignmentRationale'
        
        elif '**ISO/IEC 42001 Reference(s):**' in line:
            if current_question and current_field:
                updates[current_question][current_field] = ' '.join(current_text).strip()
                current_text = []
            current_field = 'citation'
        
        elif '**Control Intent (Plain Language Summary):**' in line or '**Control Intent (Plain Language Summary:**' in line:
            if current_question and current_field:
                updates[current_question][current_field] = ' '.join(current_text).strip()
                current_text = []
            current_field = 'controlIntent'
        
        # Collect content
        elif current_question and current_field and line.strip():
            # Remove markdown list markers
            clean_line = re.sub(r'^\*\s+', '', line.strip())
            if clean_line:
                current_text.append(clean_line)
    
    # Save last question
    if current_question and current_field and current_text:
        updates[current_question][current_field] = ' '.join(current_text).strip()
    
    return updates

# For now, since we have the extracted content in the function results earlier,
# I'll manually structure the key ones we need to update

print("Starting comprehensive ISO 42001 data update...")
print("=" * 60)

# Load existing JSON data
with open('/app/frontend/src/data/iso42001AlignmentData.json', 'r') as f:
    data = json.load(f)

print(f"Loaded {len(data)} existing questions")

# I'll note that FA-1 and FA-2 are already updated based on earlier scripts
# Let me verify what's already been updated

already_has_control_intent = sum(1 for q in data.values() if 'controlIntent' in q)
print(f"Questions with controlIntent field: {already_has_control_intent}")

# List questions that still need updating
needs_update = [code for code, q_data in data.items() if 'controlIntent' not in q_data]
print(f"Questions needing update: {len(needs_update)}")
if len(needs_update) <= 10:
    print(f"Codes: {needs_update}")

COMPLETE_UPDATE
