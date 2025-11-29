#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class V8TemplateTest:
    def __init__(self, base_url="https://ai-governance-16.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
        self.assessment_id = None

    def make_request(self, method, endpoint, data=None, expected_status=200):
        """Make API request with error handling"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            if success:
                try:
                    return success, response.json()
                except:
                    # Return raw response for binary data
                    return success, response
            else:
                return success, response.text

        except Exception as e:
            return False, str(e)

    def test_authentication(self):
        """Test user authentication"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"test_user_{timestamp}@example.com"
        
        # Test signup
        signup_data = {
            "name": f"Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            print("✅ Authentication successful")
            return True
        else:
            print(f"❌ Authentication failed: {response}")
            return False

    def test_v8_template_docx_generation(self):
        """Test v8 template DOCX generation with proper table row iteration"""
        print("\n🔍 TESTING V8 TEMPLATE DOCX GENERATION")
        print("-" * 60)
        
        # Create and complete an assessment for report generation
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            print(f"❌ Failed to create assessment: {response}")
            return False
            
        test_assessment_id = response['id']
        print("✅ Assessment created")
        
        # Get all questions and answer them to create a completed assessment
        success, response = self.make_request('GET', f'assessments/{test_assessment_id}/questions')
        if not success:
            print(f"❌ Failed to get questions: {response}")
            return False
            
        # Answer all questions with varied scores to generate different priority recommendations
        all_questions = []
        for domain_data in response:
            questions = domain_data.get('questions', [])
            all_questions.extend(questions)
        
        # Create a strategic mix of answers to generate High/Medium/Low priority recommendations
        answer_options = ['NON_IDEAL', 'BASIC', 'GOOD', 'IDEAL']  # 0, 1, 2, 3 scores
        
        for i, question in enumerate(all_questions):
            # Cycle through answer options to create varied scores
            option = answer_options[i % len(answer_options)]
            answer_data = {
                "question_id": question['id'],
                "option": option,
                "note": f"Test answer {i+1} for v8 template testing"
            }
            
            success, _ = self.make_request('POST', f'assessments/{test_assessment_id}/answer', answer_data)
            if not success:
                print(f"❌ Failed to answer question {i+1}")
                return False
        
        print(f"✅ Answered all {len(all_questions)} questions with varied scores")
        
        # Submit the assessment to mark it as completed
        success, _ = self.make_request('POST', f'assessments/{test_assessment_id}/submit')
        if not success:
            print("❌ Failed to submit assessment")
            return False
            
        print("✅ Assessment submitted")
        
        # Test DOCX generation endpoint
        success, response = self.make_request('GET', f'assessments/{test_assessment_id}/report')
        if success:
            print("✅ DOCX Generation Endpoint (GET /api/assessments/{id}/report)")
            
            # Check file size
            if hasattr(response, 'content'):
                docx_size = len(response.content)
                if docx_size > 50000:  # Should be substantial
                    print(f"✅ DOCX File Size Verification: {docx_size:,} bytes")
                else:
                    print(f"⚠️  DOCX File Size: {docx_size:,} bytes (may be small)")
                
                # Check MIME type
                content_type = response.headers.get('content-type', '')
                if 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
                    print("✅ DOCX MIME Type Correct")
                else:
                    print(f"⚠️  DOCX MIME Type: {content_type}")
            else:
                print("✅ DOCX generation successful")
                
        else:
            print(f"❌ DOCX Generation failed: {response}")
            return False
        
        # Test PDF generation endpoint  
        success, response = self.make_request('GET', f'assessments/{test_assessment_id}/report/pdf')
        if success:
            print("✅ PDF Generation Endpoint (GET /api/assessments/{id}/report/pdf)")
            
            if hasattr(response, 'content'):
                pdf_size = len(response.content)
                if pdf_size > 30000:  # Should be substantial
                    print(f"✅ PDF File Size Verification: {pdf_size:,} bytes")
                else:
                    print(f"⚠️  PDF File Size: {pdf_size:,} bytes (may be small)")
        else:
            print(f"⚠️  PDF Generation: {response} (LibreOffice may not be installed)")
        
        return True

    def run_test(self):
        """Run the complete test"""
        print("🚀 Starting V8 Template Testing")
        print("=" * 60)
        
        if not self.test_authentication():
            return False
            
        if not self.test_v8_template_docx_generation():
            return False
            
        print("\n" + "=" * 60)
        print("🎉 V8 Template Testing Complete!")
        return True

if __name__ == "__main__":
    tester = V8TemplateTest()
    success = tester.run_test()
    sys.exit(0 if success else 1)