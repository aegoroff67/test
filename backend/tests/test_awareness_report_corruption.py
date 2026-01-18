"""
Test script to isolate the Awareness report corruption issue.
This will systematically disable components to find the root cause.
"""
import asyncio
import sys
import os
from pathlib import Path
from zipfile import ZipFile, is_zipfile
import xml.etree.ElementTree as ET

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from report_generator import AMReportGenerator

def validate_docx_structure(docx_bytes: bytes, label: str = "") -> dict:
    """
    Validate DOCX structure by checking:
    1. Valid ZIP archive
    2. Required files exist
    3. XML files are well-formed
    """
    import io
    
    result = {
        'label': label,
        'is_valid_zip': False,
        'required_files_present': False,
        'xml_valid': False,
        'errors': []
    }
    
    try:
        # Check if it's a valid ZIP
        buffer = io.BytesIO(docx_bytes)
        if not is_zipfile(buffer):
            result['errors'].append("Not a valid ZIP file")
            return result
        
        result['is_valid_zip'] = True
        buffer.seek(0)
        
        required_files = [
            '[Content_Types].xml',
            'word/document.xml',
        ]
        
        with ZipFile(buffer, 'r') as zf:
            namelist = zf.namelist()
            
            # Check required files
            missing_files = [f for f in required_files if f not in namelist]
            if missing_files:
                result['errors'].append(f"Missing required files: {missing_files}")
            else:
                result['required_files_present'] = True
            
            # Validate XML files
            xml_errors = []
            for name in namelist:
                if name.endswith('.xml'):
                    try:
                        content = zf.read(name)
                        ET.fromstring(content)
                    except ET.ParseError as e:
                        xml_errors.append(f"{name}: {str(e)}")
            
            if xml_errors:
                result['errors'].extend(xml_errors)
            else:
                result['xml_valid'] = True
                
    except Exception as e:
        result['errors'].append(f"Unexpected error: {str(e)}")
    
    return result

def create_minimal_awareness_report_data() -> dict:
    """Create minimal test data for Awareness report generation."""
    return {
        'assessment': {
            'id': 'test-awareness-001',
            'date': '2025-01-20',
            'version': '1.0.0',
        },
        'overall': {
            'score': 65.0,
            'tier': 'Developing'
        },
        'org': {
            'name': 'Test Organization',
        },
        'awareness_info': {
            'org_name': 'Test Organization',
            'contact_name': 'John Doe',
            'contact_email': 'john@test.com',
            'industry': 'Technology',
            'org_size': '51-200',
            'business_unit': 'IT',
            'ai_familiarity': 'Somewhat familiar',
            'digital_maturity': 'Developing',
            'leadership_ai_interest': 'High',
            'tech_change_comfort': 'Comfortable',
            'digital_initiatives_level': 'Multiple initiatives',
            'data_skill_confidence': 'Moderate',
            'openness_to_learning': 'High',
            'governance_foundations': ['Data governance policy'],
        },
        'sector_name': 'Technology',
        'sector_average': 60.0,
        'questions_data': [
            {
                'domain': {'name': 'Awareness & Understanding', 'code': 'AU'},
                'questions': [
                    {
                        'code': 'AU-1',
                        'text': 'Test question 1',
                        'answer': {
                            'numeric_score': 3,
                            'selected_option': {'label': 'Developing', 'text': 'Some awareness'},
                            'comment': ''
                        }
                    }
                ]
            },
            {
                'domain': {'name': 'Benefits & Opportunities', 'code': 'BO'},
                'questions': [
                    {
                        'code': 'BO-1',
                        'text': 'Test question 2',
                        'answer': {
                            'numeric_score': 2,
                            'selected_option': {'label': 'Emerging', 'text': 'Limited awareness'},
                            'comment': ''
                        }
                    }
                ]
            },
        ],
        'heatmap_data': {
            'domains': [
                {
                    'name': 'Awareness & Understanding',
                    'questions': [{'code': 'AU-1', 'score': 3}]
                },
                {
                    'name': 'Benefits & Opportunities',
                    'questions': [{'code': 'BO-1', 'score': 2}]
                },
            ]
        },
        'actions': {
            'high': [
                {'domain': 'Awareness & Understanding', 'question_id': 'AU-1', 'text': 'Improve AI awareness'}
            ],
            'medium': [],
            'low': []
        },
        'sector_actions': {
            'high': [
                {'question_id': 'AU-1', 'domain': 'Awareness & Understanding', 'sector_action': 'Industry-specific action'}
            ],
            'medium': [],
            'low': []
        },
        'ai_narratives': {},
        'system_info': {},
    }

async def test_awareness_report_generation():
    """Test Awareness report generation step by step."""
    print("=" * 60)
    print("AWARENESS REPORT CORRUPTION TEST")
    print("=" * 60)
    
    # Check if template exists
    template_path = Path(__file__).parent.parent / "templates" / "docx" / "AM_AI_SAFE_Awareness_Report_TEMPLATE_v0.9.34_20260117.docx"
    if not template_path.exists():
        print(f"ERROR: Template not found at {template_path}")
        return
    
    print(f"Template found: {template_path}")
    
    # Test 1: Validate the template itself
    print("\n[Test 1] Validating template file...")
    with open(template_path, 'rb') as f:
        template_bytes = f.read()
    template_result = validate_docx_structure(template_bytes, "Template")
    print(f"  Template valid: {template_result['is_valid_zip'] and template_result['xml_valid']}")
    if template_result['errors']:
        print(f"  Template errors: {template_result['errors']}")
        return
    
    # Initialize generator
    generator = AMReportGenerator(assessment_type='Awareness')
    print(f"\n[INFO] Generator initialized with template: {generator.template_path}")
    
    # Create test data
    report_data = create_minimal_awareness_report_data()
    
    # Test 2: Generate heatmap image only
    print("\n[Test 2] Testing heatmap image generation...")
    try:
        heatmap_bytes = generator._generate_awareness_heatmap_image(report_data)
        print(f"  Heatmap generated: {len(heatmap_bytes)} bytes")
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return
    
    # Test 3: Generate full report
    print("\n[Test 3] Testing full DOCX report generation...")
    try:
        docx_bytes = generator._generate_docx_report(report_data, heatmap_bytes)
        print(f"  DOCX generated: {len(docx_bytes)} bytes")
        
        # Validate the output
        result = validate_docx_structure(docx_bytes, "Generated Report")
        print(f"  Valid ZIP: {result['is_valid_zip']}")
        print(f"  Required files: {result['required_files_present']}")
        print(f"  XML valid: {result['xml_valid']}")
        if result['errors']:
            print(f"  ERRORS: {result['errors']}")
        
        # Save for manual inspection
        output_path = Path(__file__).parent / "test_awareness_output.docx"
        with open(output_path, 'wb') as f:
            f.write(docx_bytes)
        print(f"\n  Output saved to: {output_path}")
        
    except Exception as e:
        import traceback
        print(f"  ERROR: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_awareness_report_generation())
