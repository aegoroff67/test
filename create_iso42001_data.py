#!/usr/bin/env python3
"""
Script to parse ISO 42001 alignment CSV and generate JSON data for the frontend.
"""
import csv
import json

def parse_csv_to_json(csv_file_path, json_output_path):
    """Parse the ISO 42001 alignment CSV and create JSON data structure."""
    
    alignment_data = {}
    
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            question_id = row['Question ID'].strip()
            domain = row['Domain'].strip()
            alignment_type = row['Alignment Type'].strip()
            confidence = row['Confidence Level'].strip()
            reasoning = row['Alignment Details / Rationale'].strip()
            references = row['ISO 42001 Reference(s)'].strip()
            
            alignment_data[question_id] = {
                "domain": domain,
                "alignmentType": alignment_type,
                "confidence": confidence,
                "reasoning": reasoning,
                "references": references
            }
    
    # Write to JSON file
    with open(json_output_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(alignment_data, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully created {json_output_path}")
    print(f"📊 Processed {len(alignment_data)} question alignments")
    
    # Print summary by domain
    domains = {}
    for question_id, data in alignment_data.items():
        domain = data['domain']
        domains[domain] = domains.get(domain, 0) + 1
    
    print("\n📋 Alignment data by domain:")
    for domain, count in sorted(domains.items()):
        print(f"  • {domain}: {count} questions")

if __name__ == "__main__":
    csv_file = "/tmp/iso42001_alignment.csv"
    json_output = "/app/frontend/src/data/iso42001AlignmentData.json"
    
    parse_csv_to_json(csv_file, json_output)
