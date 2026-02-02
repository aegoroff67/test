#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class DashboardBadgeSubmitValidationTester:
    def __init__(self, base_url="https://safeguard-report-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
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
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            
            # Handle JSON responses
            try:
                return success, response.json() if success else response.text
            except:
                # If JSON parsing fails, return text
                return success, response.text

        except Exception as e:
            return False, str(e)

    def test_user_signup_and_login(self):
        """Test user registration and authentication"""
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
            self.log_test("User signup", True)
            return True
        else:
            self.log_test("User signup", False, str(response))
            return False

    def test_dashboard_badge_and_submit_validation_fixes(self):
        """Test Dashboard badge and Submit validation fixes for Awareness assessments"""
        print("\n🔍 TESTING DASHBOARD BADGE AND SUBMIT VALIDATION FIXES")
        print("-" * 80)
        
        # Test 1: Create Awareness Assessment
        awareness_data = {"assessment_type": "Awareness"}
        success, response = self.make_request('POST', 'assessments', awareness_data)
        if not success:
            self.log_test("Create Awareness Assessment", False, str(response))
            return False
            
        awareness_assessment_id = response['id']
        assessment_type = response.get('assessment_type', 'Unknown')
        
        if assessment_type == 'Awareness':
            self.log_test("Create Awareness Assessment", True)
        else:
            self.log_test("Create Awareness Assessment", False, f"Expected 'Awareness', got '{assessment_type}'")
            return False
        
        # Test 2: Submit partial Awareness assessment (10/25 questions)
        success, questions_response = self.make_request('GET', f'assessments/{awareness_assessment_id}/questions')
        if not success:
            self.log_test("Get Awareness Assessment Questions", False, str(questions_response))
            return False
            
        # Collect all questions from all domains
        all_questions = []
        for domain_data in questions_response:
            questions = domain_data.get('questions', [])
            all_questions.extend(questions)
        
        total_questions = len(all_questions)
        if total_questions == 25:
            self.log_test("Awareness Assessment has 25 questions", True)
        else:
            self.log_test("Awareness Assessment has 25 questions", False, f"Found {total_questions} questions")
        
        # Answer 10 out of 25 questions
        questions_to_answer = 10
        for i in range(questions_to_answer):
            question = all_questions[i]
            answer_data = {
                "question_id": question['id'],
                "option": "BUILDING_READINESS",  # Awareness-specific option
                "note": f"Partial answer {i+1}"
            }
            
            success, _ = self.make_request('POST', f'assessments/{awareness_assessment_id}/answer', answer_data)
            if not success:
                self.log_test(f"Answer Awareness question {i+1}", False, "Failed to submit answer")
                return False
        
        self.log_test(f"Answered {questions_to_answer}/25 Awareness questions", True)
        
        # Test 3: Try to submit incomplete Awareness assessment (should fail with correct count)
        success, submit_response = self.make_request('POST', f'assessments/{awareness_assessment_id}/submit', expected_status=400)
        if success:
            # Check if error message mentions correct remaining count (15 questions)
            error_message = str(submit_response)
            remaining_questions = 25 - questions_to_answer  # Should be 15
            
            if f"{remaining_questions} questions remain" in error_message:
                self.log_test("Submit validation shows correct remaining count for Awareness", True)
                print(f"   📝 Correct error message: {error_message}")
            else:
                self.log_test("Submit validation shows correct remaining count for Awareness", False, 
                            f"Expected '{remaining_questions} questions remain', got: {error_message}")
        else:
            self.log_test("Submit incomplete Awareness assessment returns 400", False, "Should have returned 400 error")
        
        # Test 4: Complete all remaining questions
        remaining_questions_list = all_questions[questions_to_answer:]
        for i, question in enumerate(remaining_questions_list):
            answer_data = {
                "question_id": question['id'],
                "option": "READY_TO_PROGRESS",  # Awareness-specific option
                "note": f"Completing question {i+1}"
            }
            
            success, _ = self.make_request('POST', f'assessments/{awareness_assessment_id}/answer', answer_data)
            if not success:
                self.log_test(f"Complete remaining Awareness question {i+1}", False, "Failed to submit answer")
                return False
        
        self.log_test("Completed all 25 Awareness questions", True)
        
        # Test 5: Submit completed Awareness assessment (should succeed)
        success, submit_response = self.make_request('POST', f'assessments/{awareness_assessment_id}/submit')
        if success:
            self.log_test("Submit completed Awareness assessment succeeds", True)
            print(f"   📝 Success response: {submit_response}")
        else:
            self.log_test("Submit completed Awareness assessment succeeds", False, f"Submit failed: {submit_response}")
            return False
        
        # Test 6: Verify assessment status is COMPLETED
        success, assessment_response = self.make_request('GET', f'assessments/{awareness_assessment_id}')
        if success:
            status = assessment_response.get('status')
            if status == 'COMPLETED':
                self.log_test("Awareness assessment status updated to COMPLETED", True)
            else:
                self.log_test("Awareness assessment status updated to COMPLETED", False, f"Status is {status}")
        else:
            self.log_test("Check Awareness assessment status after submission", False, str(assessment_response))
        
        # Test 7: Test System Assessment still works correctly
        system_data = {"assessment_type": "System"}
        success, response = self.make_request('POST', 'assessments', system_data)
        if not success:
            self.log_test("Create System Assessment for comparison", False, str(response))
            return False
            
        system_assessment_id = response['id']
        
        # Get System assessment questions (should be 88)
        success, system_questions_response = self.make_request('GET', f'assessments/{system_assessment_id}/questions')
        if success:
            system_all_questions = []
            for domain_data in system_questions_response:
                questions = domain_data.get('questions', [])
                system_all_questions.extend(questions)
            
            if len(system_all_questions) == 88:
                self.log_test("System Assessment still has 88 questions", True)
            else:
                self.log_test("System Assessment still has 88 questions", False, f"Found {len(system_all_questions)} questions")
        
        # Answer 40 out of 88 System questions
        system_questions_to_answer = 40
        for i in range(system_questions_to_answer):
            question = system_all_questions[i]
            answer_data = {
                "question_id": question['id'],
                "option": "GOOD",  # System-specific option
                "note": f"System answer {i+1}"
            }
            
            success, _ = self.make_request('POST', f'assessments/{system_assessment_id}/answer', answer_data)
            if not success:
                self.log_test(f"Answer System question {i+1}", False, "Failed to submit answer")
                return False
        
        # Try to submit incomplete System assessment
        success, submit_response = self.make_request('POST', f'assessments/{system_assessment_id}/submit', expected_status=400)
        if success:
            error_message = str(submit_response)
            remaining_system_questions = 88 - system_questions_to_answer  # Should be 48
            
            if f"{remaining_system_questions} questions remain" in error_message:
                self.log_test("Submit validation shows correct remaining count for System", True)
                print(f"   📝 System error message: {error_message}")
            else:
                self.log_test("Submit validation shows correct remaining count for System", False, 
                            f"Expected '{remaining_system_questions} questions remain', got: {error_message}")
        
        # Test 8: Test Overall Percentage Calculation for Awareness
        # Get summary for completed Awareness assessment
        success, awareness_summary = self.make_request('GET', f'assessments/{awareness_assessment_id}/summary')
        if success:
            overall_percentage = awareness_summary.get('overall_percentage', 0)
            
            # Calculate expected percentage: 
            # 10 questions with BUILDING_READINESS (score 3) + 15 questions with READY_TO_PROGRESS (score 4)
            # Total score = (10 * 3) + (15 * 4) = 30 + 60 = 90
            # Max score = 25 * 4 = 100
            # Expected percentage = 90/100 * 100 = 90.0%
            expected_percentage = 90.0
            
            if abs(overall_percentage - expected_percentage) < 0.1:  # Allow small floating point differences
                self.log_test("Awareness overall percentage calculation correct", True)
                print(f"   📝 Calculated percentage: {overall_percentage}% (expected: {expected_percentage}%)")
            else:
                self.log_test("Awareness overall percentage calculation correct", False, 
                            f"Expected {expected_percentage}%, got {overall_percentage}%")
        else:
            self.log_test("Get Awareness assessment summary", False, str(awareness_summary))
        
        # Test 9: Edge Cases
        # Test with 24/25 answered (should fail with "1 question remains")
        edge_case_data = {"assessment_type": "Awareness"}
        success, response = self.make_request('POST', 'assessments', edge_case_data)
        if success:
            edge_assessment_id = response['id']
            
            # Answer 24 out of 25 questions
            for i in range(24):
                question = all_questions[i]
                answer_data = {
                    "question_id": question['id'],
                    "option": "EXPLORING_OPPORTUNITIES",
                    "note": f"Edge case answer {i+1}"
                }
                self.make_request('POST', f'assessments/{edge_assessment_id}/answer', answer_data)
            
            # Try to submit (should fail with "1 question remains")
            success, submit_response = self.make_request('POST', f'assessments/{edge_assessment_id}/submit', expected_status=400)
            if success:
                error_message = str(submit_response)
                if "1 question remains" in error_message or "1 questions remain" in error_message:
                    self.log_test("Edge case: 24/25 answered shows '1 question remains'", True)
                else:
                    self.log_test("Edge case: 24/25 answered shows '1 question remains'", False, 
                                f"Got: {error_message}")
        
        return True

    def run_tests(self):
        """Run the specific tests for Dashboard badge and Submit validation fixes"""
        print("🚀 Starting Dashboard Badge and Submit Validation Testing")
        print("=" * 80)
        
        # Authentication tests
        if not self.test_user_signup_and_login():
            print("❌ Authentication failed - stopping tests")
            return
        
        # Run the main test
        self.test_dashboard_badge_and_submit_validation_fixes()
        
        # Print summary
        print("\n" + "=" * 80)
        print(f"📊 TEST SUMMARY")
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("⚠️  Some tests failed - check details above")

if __name__ == "__main__":
    tester = DashboardBadgeSubmitValidationTester()
    tester.run_tests()