#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class ProductionTester:
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
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
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

    def test_authentication(self):
        """Test user authentication"""
        print("\n🔐 TESTING AUTHENTICATION")
        print("-" * 50)
        
        # Test backend accessibility
        try:
            response = requests.get(f"{self.base_url}/api/domains", timeout=10)
            if response.status_code == 200:
                self.log_test("Backend API accessible", True)
            else:
                self.log_test("Backend API accessible", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend API accessible", False, str(e))
            return False

        # Create test user
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"prod_test_{timestamp}@amaisafe.com"
        
        signup_data = {
            "name": f"Production Test {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("User signup and JWT token generation", True)
            return True
        else:
            self.log_test("User signup and JWT token generation", False, str(response))
            return False

    def test_specific_assessment_reports(self):
        """Test report generation for specific assessment ID"""
        print("\n📄 TESTING SPECIFIC ASSESSMENT REPORT GENERATION")
        print("-" * 50)
        
        # The specific assessment ID from the review request
        assessment_id = "89139e2e-5286-4e11-89e1-8ca5d830ca44"
        
        # Test DOCX generation
        print(f"Testing DOCX report for assessment: {assessment_id}")
        success, response = self.make_request('GET', f'assessments/{assessment_id}/report')
        
        if success:
            self.log_test("DOCX report generation", True, f"Size: {len(response)} bytes")
            
            # Validate DOCX format
            if isinstance(response, bytes) and response[:4] == b'PK\x03\x04':
                self.log_test("DOCX file format valid", True)
            else:
                self.log_test("DOCX file format valid", False, "Invalid DOCX format")
        else:
            self.log_test("DOCX report generation", False, str(response))
            if "500" in str(response):
                print("   🚨 500 Error detected - this matches the user's reported issue")
        
        # Test PDF generation
        print(f"Testing PDF report for assessment: {assessment_id}")
        success, response = self.make_request('GET', f'assessments/{assessment_id}/report/pdf')
        
        if success:
            self.log_test("PDF report generation", True, f"Size: {len(response)} bytes")
            
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
                print("   🚨 500 Error detected - this matches the user's reported issue")

    def test_new_assessment_reports(self):
        """Test report generation with a newly created assessment"""
        print("\n📋 TESTING NEW ASSESSMENT REPORT GENERATION")
        print("-" * 50)
        
        # Create new assessment
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            self.log_test("Create new assessment", False, str(response))
            return False
        
        assessment_id = response['id']
        self.log_test("Create new assessment", True)
        
        # Get questions and answer them
        success, response = self.make_request('GET', f'assessments/{assessment_id}/questions')
        if not success:
            self.log_test("Get assessment questions", False, str(response))
            return False
        
        # Answer first 10 questions to make it valid for report generation
        question_count = 0
        for domain_data in response:
            if question_count >= 10:
                break
            questions = domain_data.get('questions', [])
            for question in questions:
                if question_count >= 10:
                    break
                
                answer_data = {
                    "question_id": question['id'],
                    "option": "GOOD",
                    "note": "Test answer for report generation"
                }
                
                success, _ = self.make_request('POST', f'assessments/{assessment_id}/answer', answer_data)
                if success:
                    question_count += 1
        
        self.log_test(f"Answered {question_count} questions", True)
        
        # Test DOCX generation with new assessment
        success, response = self.make_request('GET', f'assessments/{assessment_id}/report')
        if success:
            self.log_test("New assessment DOCX generation", True, f"Size: {len(response)} bytes")
        else:
            self.log_test("New assessment DOCX generation", False, str(response))
        
        # Test PDF generation with new assessment
        success, response = self.make_request('GET', f'assessments/{assessment_id}/report/pdf')
        if success:
            self.log_test("New assessment PDF generation", True, f"Size: {len(response)} bytes")
        else:
            self.log_test("New assessment PDF generation", False, str(response))

    def run_production_tests(self):
        """Run all production tests"""
        print("🚀 STARTING PRODUCTION AUTHENTICATION & REPORT TESTS")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print(f"API URL: {self.api_url}")
        print("=" * 60)
        
        # Test authentication first
        if not self.test_authentication():
            print("❌ Authentication failed - cannot proceed with report tests")
            return False
        
        # Test specific assessment (the one causing issues)
        self.test_specific_assessment_reports()
        
        # Test with new assessment
        self.test_new_assessment_reports()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 PRODUCTION TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED!")
            return True
        else:
            print("⚠️  Some tests failed - check details above")
            return False

def main():
    tester = ProductionTester()
    success = tester.run_production_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())