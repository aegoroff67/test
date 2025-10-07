#!/usr/bin/env python3

import requests
import sys
import json
import traceback
from datetime import datetime

class CoroutineErrorInvestigator:
    def __init__(self, base_url="https://reportgen-5.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
        self.assessment_id = None
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
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            return success, response.json() if success else response.text

        except Exception as e:
            return False, str(e)

    def setup_test_user_and_assessment(self):
        """Create test user and assessment for testing"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"coroutine_test_{timestamp}@example.com"
        
        # Test signup
        signup_data = {
            "name": f"Coroutine Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Coroutine Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("User signup for coroutine test", True)
        else:
            self.log_test("User signup for coroutine test", False, str(response))
            return False

        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if success and 'id' in response:
            self.assessment_id = response['id']
            self.log_test("Assessment creation for coroutine test", True)
            return True
        else:
            self.log_test("Assessment creation for coroutine test", False, str(response))
            return False

    def complete_assessment(self):
        """Complete the assessment to enable report generation"""
        # Get questions
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            self.log_test("Get questions for coroutine test", False, str(response))
            return False
        
        # Answer all questions
        question_count = 0
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for question in questions:
                answer_data = {
                    "question_id": question['id'],
                    "option": "GOOD",
                    "note": "Test answer for coroutine investigation"
                }
                
                success_answer, _ = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
                if success_answer:
                    question_count += 1
        
        self.log_test(f"Answered {question_count} questions", True)
        
        # Submit assessment
        success, _ = self.make_request('POST', f'assessments/{self.assessment_id}/submit')
        if success:
            self.log_test("Assessment submitted", True)
            return True
        else:
            self.log_test("Assessment submission", False, "Failed to submit")
            return False

    def test_docx_generation_for_coroutine_error(self):
        """Test DOCX generation specifically looking for coroutine errors"""
        print("\n🔍 Testing DOCX Generation for Coroutine Errors...")
        
        try:
            url = f"{self.api_url}/assessments/{self.assessment_id}/report"
            headers = {'Authorization': f'Bearer {self.token}'}
            
            response = requests.get(url, headers=headers, timeout=60)
            
            if response.status_code == 200:
                self.log_test("DOCX Generation - HTTP 200 OK", True)
                
                # Check content type
                content_type = response.headers.get('content-type', '')
                if 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
                    self.log_test("DOCX Generation - Correct MIME Type", True)
                else:
                    self.log_test("DOCX Generation - Correct MIME Type", False, f"Got: {content_type}")
                
                # Check file size
                content_length = len(response.content)
                self.log_test(f"DOCX Generation - File Size: {content_length} bytes", content_length > 1000)
                
            elif response.status_code == 500:
                # Check for coroutine error
                error_text = response.text
                if 'coroutine' in error_text.lower():
                    self.log_test("DOCX Generation - COROUTINE ERROR DETECTED", False, f"Found coroutine error!")
                    print(f"🚨 CRITICAL COROUTINE ERROR FOUND:")
                    print(f"📝 Full error details:")
                    print(error_text)
                    print("-" * 80)
                    return True  # We found the error we were looking for
                else:
                    self.log_test("DOCX Generation - Server Error (Non-Coroutine)", False, f"500 error: {error_text[:200]}...")
            else:
                self.log_test("DOCX Generation - HTTP Status", False, f"Got {response.status_code}")
                
        except Exception as e:
            self.log_test("DOCX Generation - Request Exception", False, f"Exception: {str(e)}")
            print(f"Exception details: {traceback.format_exc()}")
        
        return False

    def test_pdf_generation_for_coroutine_error(self):
        """Test PDF generation specifically looking for coroutine errors"""
        print("\n🔍 Testing PDF Generation for Coroutine Errors...")
        
        try:
            url = f"{self.api_url}/assessments/{self.assessment_id}/report/pdf"
            headers = {'Authorization': f'Bearer {self.token}'}
            
            response = requests.get(url, headers=headers, timeout=60)
            
            if response.status_code == 200:
                self.log_test("PDF Generation - HTTP 200 OK", True)
                
                # Check content type
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type:
                    self.log_test("PDF Generation - Correct MIME Type", True)
                else:
                    self.log_test("PDF Generation - Incorrect MIME Type", False, f"Got: {content_type}")
                
                # Check file size
                content_length = len(response.content)
                self.log_test(f"PDF Generation - File Size: {content_length} bytes", content_length > 1000)
                
            elif response.status_code == 500:
                # Check for coroutine error
                error_text = response.text
                if 'coroutine' in error_text.lower():
                    self.log_test("PDF Generation - COROUTINE ERROR DETECTED", False, f"Found coroutine error!")
                    print(f"🚨 CRITICAL COROUTINE ERROR FOUND:")
                    print(f"📝 Full error details:")
                    print(error_text)
                    print("-" * 80)
                    return True  # We found the error we were looking for
                else:
                    self.log_test("PDF Generation - Server Error (Non-Coroutine)", False, f"500 error: {error_text[:200]}...")
            else:
                self.log_test("PDF Generation - HTTP Status", False, f"Got {response.status_code}")
                
        except Exception as e:
            self.log_test("PDF Generation - Request Exception", False, f"Exception: {str(e)}")
            print(f"Exception details: {traceback.format_exc()}")
        
        return False

    def test_rapid_requests_for_race_conditions(self):
        """Test rapid requests to trigger potential race conditions"""
        print("\n⚡ Testing Rapid Requests for Race Conditions...")
        
        coroutine_error_found = False
        
        for i in range(5):
            try:
                url = f"{self.api_url}/assessments/{self.assessment_id}/report"
                headers = {'Authorization': f'Bearer {self.token}'}
                
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    self.log_test(f"Rapid Request {i+1} - Success", True)
                elif response.status_code == 500:
                    error_text = response.text
                    if 'coroutine' in error_text.lower():
                        self.log_test(f"Rapid Request {i+1} - COROUTINE ERROR", False, "Found coroutine error!")
                        print(f"🚨 COROUTINE ERROR IN RAPID REQUEST {i+1}:")
                        print(error_text)
                        print("-" * 80)
                        coroutine_error_found = True
                    else:
                        self.log_test(f"Rapid Request {i+1} - Server Error", False, f"500 error")
                else:
                    self.log_test(f"Rapid Request {i+1} - HTTP Error", False, f"Status {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Rapid Request {i+1} - Exception", False, f"Exception: {str(e)}")
        
        return coroutine_error_found

    def run_investigation(self):
        """Run the complete coroutine error investigation"""
        print("🚨 COROUTINE/ASYNC ERROR INVESTIGATION")
        print("=" * 60)
        print("Investigating the 'object of type 'coroutine' has no len()' error")
        print("in the AM AI SAFE report generation system")
        print("=" * 60)
        
        # Setup
        if not self.setup_test_user_and_assessment():
            print("❌ Failed to setup test environment")
            return False
        
        if not self.complete_assessment():
            print("❌ Failed to complete assessment")
            return False
        
        # Test for coroutine errors
        coroutine_error_found = False
        
        # Test DOCX generation
        if self.test_docx_generation_for_coroutine_error():
            coroutine_error_found = True
        
        # Test PDF generation
        if self.test_pdf_generation_for_coroutine_error():
            coroutine_error_found = True
        
        # Test rapid requests
        if self.test_rapid_requests_for_race_conditions():
            coroutine_error_found = True
        
        # Results
        print("\n" + "=" * 60)
        print("🏁 COROUTINE ERROR INVESTIGATION COMPLETE")
        print("=" * 60)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if coroutine_error_found:
            print("🚨 COROUTINE ERROR DETECTED!")
            print("The 'object of type 'coroutine' has no len()' error was found.")
            print("This indicates an async function is being called without await.")
        else:
            print("✅ NO COROUTINE ERRORS DETECTED")
            print("The report generation system appears to be working correctly.")
            print("The coroutine error may have been fixed or is not reproducible.")
        
        return coroutine_error_found

if __name__ == "__main__":
    investigator = CoroutineErrorInvestigator()
    investigator.run_investigation()