#!/usr/bin/env python3

import requests
import sys
import json
import traceback
import asyncio
import concurrent.futures
from datetime import datetime

class DeepCoroutineInvestigator:
    def __init__(self, base_url="https://reportgen-5.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
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

    def setup_test_environment(self):
        """Setup test environment with specific data patterns that might trigger coroutine errors"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"deep_test_{timestamp}@example.com"
        
        # Create user
        signup_data = {
            "name": f"Deep Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Deep Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.log_test("User setup", True)
        else:
            self.log_test("User setup", False, str(response))
            return False

        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if success and 'id' in response:
            self.assessment_id = response['id']
            self.log_test("Assessment setup", True)
            return True
        else:
            self.log_test("Assessment setup", False, str(response))
            return False

    def create_specific_answer_pattern(self):
        """Create specific answer patterns that might trigger async issues"""
        # Get questions
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            self.log_test("Get questions for pattern test", False, str(response))
            return False
        
        # Create a specific pattern: Mix of all answer types to create complex data structures
        answer_patterns = ["NON_IDEAL", "BASIC", "GOOD", "IDEAL"]
        question_count = 0
        
        for domain_idx, domain_data in enumerate(response):
            questions = domain_data.get('questions', [])
            for question_idx, question in enumerate(questions):
                # Use different patterns for different domains to create complex data
                pattern_idx = (domain_idx + question_idx) % len(answer_patterns)
                option = answer_patterns[pattern_idx]
                
                answer_data = {
                    "question_id": question['id'],
                    "option": option,
                    "note": f"Pattern test answer {question_count+1} - {option}"
                }
                
                success_answer, _ = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
                if success_answer:
                    question_count += 1
        
        self.log_test(f"Created complex answer pattern with {question_count} answers", True)
        
        # Submit assessment
        success, _ = self.make_request('POST', f'assessments/{self.assessment_id}/submit')
        if success:
            self.log_test("Assessment submitted with complex pattern", True)
            return True
        else:
            self.log_test("Assessment submission", False, "Failed to submit")
            return False

    def test_concurrent_report_requests(self):
        """Test concurrent report requests to trigger potential race conditions"""
        print("\n🔄 Testing Concurrent Report Requests...")
        
        def make_report_request(request_id):
            try:
                url = f"{self.api_url}/assessments/{self.assessment_id}/report"
                headers = {'Authorization': f'Bearer {self.token}'}
                
                response = requests.get(url, headers=headers, timeout=60)
                
                if response.status_code == 500:
                    error_text = response.text
                    if 'coroutine' in error_text.lower():
                        return f"COROUTINE_ERROR_{request_id}", error_text
                    else:
                        return f"SERVER_ERROR_{request_id}", error_text[:200]
                elif response.status_code == 200:
                    return f"SUCCESS_{request_id}", len(response.content)
                else:
                    return f"HTTP_ERROR_{request_id}", response.status_code
                    
            except Exception as e:
                return f"EXCEPTION_{request_id}", str(e)
        
        # Use ThreadPoolExecutor to make truly concurrent requests
        coroutine_errors = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_report_request, i) for i in range(10)]
            
            for future in concurrent.futures.as_completed(futures):
                result_type, result_data = future.result()
                
                if "COROUTINE_ERROR" in result_type:
                    self.log_test(f"Concurrent Request {result_type}", False, "COROUTINE ERROR DETECTED!")
                    print(f"🚨 COROUTINE ERROR IN CONCURRENT REQUEST:")
                    print(result_data)
                    print("-" * 80)
                    coroutine_errors.append(result_data)
                elif "SUCCESS" in result_type:
                    self.log_test(f"Concurrent Request {result_type}", True)
                else:
                    self.log_test(f"Concurrent Request {result_type}", False, str(result_data))
        
        return len(coroutine_errors) > 0

    def test_malformed_data_scenarios(self):
        """Test scenarios with potentially malformed data that might cause async issues"""
        print("\n🧪 Testing Malformed Data Scenarios...")
        
        # Test with empty assessment (should fail gracefully)
        empty_assessment_success, empty_response = self.make_request('POST', 'assessments', {})
        if empty_assessment_success:
            empty_assessment_id = empty_response['id']
            
            # Try to generate report for empty assessment
            try:
                url = f"{self.api_url}/assessments/{empty_assessment_id}/report"
                headers = {'Authorization': f'Bearer {self.token}'}
                
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 500:
                    error_text = response.text
                    if 'coroutine' in error_text.lower():
                        self.log_test("Empty Assessment Report - COROUTINE ERROR", False, "Found coroutine error!")
                        print(f"🚨 COROUTINE ERROR WITH EMPTY ASSESSMENT:")
                        print(error_text)
                        return True
                    else:
                        self.log_test("Empty Assessment Report - Expected Error", True)
                else:
                    self.log_test("Empty Assessment Report - Unexpected Success", False, f"Got {response.status_code}")
                    
            except Exception as e:
                self.log_test("Empty Assessment Report - Exception", False, str(e))
        
        return False

    def test_template_processing_edge_cases(self):
        """Test edge cases in template processing that might cause coroutine issues"""
        print("\n📄 Testing Template Processing Edge Cases...")
        
        # Test with very large notes (might cause memory/processing issues)
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if success and response:
            # Update one answer with a very large note
            first_question = response[0]['questions'][0]
            large_note = "X" * 10000  # 10KB note
            
            answer_data = {
                "question_id": first_question['id'],
                "option": "GOOD",
                "note": large_note
            }
            
            success_answer, _ = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
            if success_answer:
                self.log_test("Large note answer submitted", True)
                
                # Try to generate report
                try:
                    url = f"{self.api_url}/assessments/{self.assessment_id}/report"
                    headers = {'Authorization': f'Bearer {self.token}'}
                    
                    response = requests.get(url, headers=headers, timeout=60)
                    
                    if response.status_code == 500:
                        error_text = response.text
                        if 'coroutine' in error_text.lower():
                            self.log_test("Large Note Report - COROUTINE ERROR", False, "Found coroutine error!")
                            print(f"🚨 COROUTINE ERROR WITH LARGE NOTE:")
                            print(error_text)
                            return True
                        else:
                            self.log_test("Large Note Report - Other Error", False, error_text[:200])
                    else:
                        self.log_test("Large Note Report - Success", True)
                        
                except Exception as e:
                    self.log_test("Large Note Report - Exception", False, str(e))
        
        return False

    def run_deep_investigation(self):
        """Run comprehensive deep investigation for coroutine errors"""
        print("🔬 DEEP COROUTINE/ASYNC ERROR INVESTIGATION")
        print("=" * 70)
        print("Advanced testing for 'object of type 'coroutine' has no len()' error")
        print("Testing concurrent requests, edge cases, and malformed data")
        print("=" * 70)
        
        # Setup
        if not self.setup_test_environment():
            print("❌ Failed to setup test environment")
            return False
        
        if not self.create_specific_answer_pattern():
            print("❌ Failed to create test data pattern")
            return False
        
        # Run deep tests
        coroutine_error_found = False
        
        # Test concurrent requests
        if self.test_concurrent_report_requests():
            coroutine_error_found = True
        
        # Test malformed data scenarios
        if self.test_malformed_data_scenarios():
            coroutine_error_found = True
        
        # Test template processing edge cases
        if self.test_template_processing_edge_cases():
            coroutine_error_found = True
        
        # Results
        print("\n" + "=" * 70)
        print("🏁 DEEP COROUTINE ERROR INVESTIGATION COMPLETE")
        print("=" * 70)
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
            print("The coroutine error may have been fixed or requires specific conditions to reproduce.")
        
        return coroutine_error_found

if __name__ == "__main__":
    investigator = DeepCoroutineInvestigator()
    investigator.run_deep_investigation()