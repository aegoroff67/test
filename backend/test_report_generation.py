#!/usr/bin/env python3
"""
Test script for report generation endpoints.
"""

from report_generator import AMReportGenerator
import asyncio

async def test_report_generation():
    """Test the report generation with mock data."""
    
    # Create mock assessment data
    mock_assessment_data = {
        "assessment": {
            "id": "test-id",
            "created_at": "2025-01-01",
            "status": "COMPLETED"
        },
        "questions_data": [
            {
                "domain": {"name": "Fairness", "id": "fairness"},
                "questions": [
                    {
                        "id": "q1",
                        "code": "FA-1",
                        "text": "Test question 1",
                        "answer": {"numeric_score": 2}
                    },
                    {
                        "id": "q2", 
                        "code": "FA-2",
                        "text": "Test question 2",
                        "answer": {"numeric_score": 1}
                    }
                ]
            }
        ],
        "summary": {
            "overall_percentage": 75.0
        }
    }
    
    mock_user_data = {
        "organization_name": "Test Organization"
    }
    
    try:
        # Initialize report generator
        generator = AMReportGenerator()
        
        # Test report generation
        docx_bytes, pdf_bytes = await generator.generate_report(
            "test-assessment-id",
            mock_assessment_data,
            mock_user_data
        )
        
        print(f"✅ Report generation successful!")
        print(f"   DOCX size: {len(docx_bytes)} bytes")
        print(f"   PDF size: {len(pdf_bytes)} bytes")
        
        # Save test files
        with open("/tmp/test_report.docx", "wb") as f:
            f.write(docx_bytes)
        
        with open("/tmp/test_report.pdf", "wb") as f:
            f.write(pdf_bytes)
            
        print("✅ Test files saved to /tmp/test_report.docx and /tmp/test_report.pdf")
        
    except Exception as e:
        print(f"❌ Report generation failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_report_generation())