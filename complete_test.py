#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class CompleteTester:
    def __init__(self):
        self.base_url = "https://app.amaisafe.com"
        self.api_url = f"{self.base_url}/api"
        self.token = None
        self.user_data = None
        self.tests_run = 0
        self.tests_passed = 0

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")

    def make_request(self, method, endpoint, data=None, expected_status=200):
        """Make API request with error handling"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=60)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=60)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            
            # Handle binary responses (like DOCX/PDF files)
            content_type = response.headers.get('content-type', '')
            if success and ('application/vnd.openxmlformats' in content_type or 'application/pdf' in content_type):
                return success, response.content
            
            # Handle JSON responses
            try:
                return success, response.json() if success else response.text
            except:
                # If JSON parsing fails, return text
                return success, response.text

        except Exception as e:
            return False, str(e)

    def test_complete_flow(self):
        """Test complete assessment and report generation flow"""
        print("🚀 TESTING COMPLETE ASSESSMENT & REPORT FLOW")
        print("=" * 60)
        
        # Step 1: Authentication
        print("\n🔐 Step 1: Authentication")
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"complete_test_{timestamp}@amaisafe.com"
        
        signup_data = {
            "name": f"Complete Test {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Complete Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("Authentication successful", True)
        else:
            self.log_test("Authentication successful", False, str(response))
            return False
        
        # Step 2: Create assessment
        print("\n📋 Step 2: Create Assessment")
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            self.log_test("Create assessment", False, str(response))
            return False
        
        assessment_id = response['id']
        self.log_test("Create assessment", True, f"ID: {assessment_id}")
        
        # Step 3: Get all questions
        print("\n❓ Step 3: Get Questions")
        success, response = self.make_request('GET', f'assessments/{assessment_id}/questions')
        if not success:
            self.log_test("Get questions", False, str(response))
            return False
        
        # Count total questions
        total_questions = 0
        all_questions = []
        for domain_data in response:
            questions = domain_data.get('questions', [])
            total_questions += len(questions)
            all_questions.extend(questions)
        
        self.log_test("Get questions", True, f"Total: {total_questions} questions")
        
        # Step 4: Answer all questions
        print("\n✍️ Step 4: Answer All Questions")
        answer_options = ['IDEAL', 'GOOD', 'BASIC', 'NON_IDEAL']
        answered_count = 0
        
        for i, question in enumerate(all_questions):
            option = answer_options[i % len(answer_options)]
            answer_data = {
                "question_id": question['id'],
                "option": option,
                "note": f"Complete test answer {i+1}"
            }
            
            success, _ = self.make_request('POST', f'assessments/{assessment_id}/answer', answer_data)
            if success:
                answered_count += 1
            
            # Progress indicator
            if (i + 1) % 20 == 0:
                print(f"   Answered {i + 1}/{total_questions} questions...")
        
        self.log_test("Answer all questions", answered_count == total_questions, f"Answered: {answered_count}/{total_questions}")
        
        # Step 5: Submit assessment
        print("\n📤 Step 5: Submit Assessment")
        success, response = self.make_request('POST', f'assessments/{assessment_id}/submit')
        if success:
            self.log_test("Submit assessment", True)
        else:
            self.log_test("Submit assessment", False, str(response))
            return False
        
        # Step 6: Generate DOCX report
        print("\n📄 Step 6: Generate DOCX Report")
        success, response = self.make_request('GET', f'assessments/{assessment_id}/report')
        if success:
            file_size = len(response)
            self.log_test("DOCX report generation", True, f"Size: {file_size:,} bytes")
            
            # Validate DOCX format
            if isinstance(response, bytes) and response[:4] == b'PK\x03\x04':
                self.log_test("DOCX file format valid", True)
            else:
                self.log_test("DOCX file format valid", False, "Invalid DOCX format")
        else:
            self.log_test("DOCX report generation", False, str(response))
            if "500" in str(response):
                print("   🚨 500 Error - LibreOffice issue detected")
        
        # Step 7: Generate PDF report
        print("\n📄 Step 7: Generate PDF Report")
        success, response = self.make_request('GET', f'assessments/{assessment_id}/report/pdf')
        if success:
            file_size = len(response)
            self.log_test("PDF report generation", True, f"Size: {file_size:,} bytes")
            
            # Validate PDF format
            if isinstance(response, bytes) and response[:4] == b'%PDF':
                self.log_test("PDF file format valid", True)
                
                # Check for PDF end marker
                if b'%%EOF' in response[-100:]:
                    self.log_test("PDF file structure complete", True)
                else:
                    self.log_test("PDF file structure complete", False, "Missing %%EOF marker")
            else:
                self.log_test("PDF file format valid", False, "Invalid PDF format")
        else:
            self.log_test("PDF report generation", False, str(response))
            if "500" in str(response):
                print("   🚨 500 Error - LibreOffice issue detected")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 COMPLETE FLOW TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED!")
            print("✅ Authentication working")
            print("✅ Assessment creation working")
            print("✅ Question answering working")
            print("✅ Assessment submission working")
            print("✅ DOCX report generation working")
            print("✅ PDF report generation working")
            print("✅ LibreOffice PDF conversion working")
            return True
        else:
            print("⚠️  Some tests failed")
            failed_tests = self.tests_run - self.tests_passed
            if failed_tests > 0:
                print(f"❌ {failed_tests} test(s) failed - check details above")
            return False

def main():
    tester = CompleteTester()
    success = tester.test_complete_flow()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())