#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class DashboardProgressTester:
    def __init__(self, base_url="https://ai-governance-16.preview.emergentagent.com"):
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
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            
            try:
                return success, response.json() if success else response.text
            except:
                return success, response.text

        except Exception as e:
            return False, str(e)

    def authenticate(self):
        """Authenticate by creating a test user"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"dashboard_test_{timestamp}@example.com"
        
        # First try to signup
        signup_data = {
            "name": f"Dashboard Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Dashboard Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("Authentication (signup)", True)
            return True
        else:
            self.log_test("Authentication (signup)", False, str(response))
            return False

    def test_dashboard_progress_display_fix(self):
        """Test the Dashboard progress display fix for Awareness vs System assessments"""
        print("\n🔍 TESTING DASHBOARD PROGRESS DISPLAY FIX")
        print("-" * 60)
        
        # Test 1: Create Awareness Assessment and verify total_questions = 25
        print("📋 Test 1: Awareness Assessment Progress Display")
        awareness_data = {"assessment_type": "Awareness"}
        success, response = self.make_request('POST', 'assessments', awareness_data)
        if not success:
            self.log_test("Create Awareness Assessment", False, str(response))
            return False
            
        awareness_assessment_id = response['id']
        self.log_test("Create Awareness Assessment", True)
        
        # Verify Awareness assessment has correct total_questions
        if response.get('assessment_type') == 'Awareness':
            self.log_test("Awareness assessment type correct", True)
        else:
            self.log_test("Awareness assessment type correct", False, f"Got {response.get('assessment_type')}")
            
        if response.get('total_questions') == 25:
            self.log_test("Awareness assessment total_questions = 25", True)
        else:
            self.log_test("Awareness assessment total_questions = 25", False, f"Got {response.get('total_questions')}")
            
        if response.get('progress') == 0:
            self.log_test("Awareness assessment initial progress = 0", True)
        else:
            self.log_test("Awareness assessment initial progress = 0", False, f"Got {response.get('progress')}")
        
        # Test 2: Create System Assessment and verify total_questions = 88
        print("\n📋 Test 2: System Assessment Progress Display")
        system_data = {"assessment_type": "System"}
        success, response = self.make_request('POST', 'assessments', system_data)
        if not success:
            self.log_test("Create System Assessment", False, str(response))
            return False
            
        system_assessment_id = response['id']
        self.log_test("Create System Assessment", True)
        
        # Verify System assessment has correct total_questions
        if response.get('assessment_type') == 'System':
            self.log_test("System assessment type correct", True)
        else:
            self.log_test("System assessment type correct", False, f"Got {response.get('assessment_type')}")
            
        if response.get('total_questions') == 88:
            self.log_test("System assessment total_questions = 88", True)
        else:
            self.log_test("System assessment total_questions = 88", False, f"Got {response.get('total_questions')}")
            
        if response.get('progress') == 0:
            self.log_test("System assessment initial progress = 0", True)
        else:
            self.log_test("System assessment initial progress = 0", False, f"Got {response.get('progress')}")
        
        # Test 3: Answer some questions in Awareness assessment and verify progress
        print("\n📋 Test 3: Awareness Assessment Partial Progress")
        
        # Get Awareness questions (should be 25)
        success, awareness_questions_response = self.make_request('GET', f'assessments/{awareness_assessment_id}/questions')
        if not success:
            self.log_test("Get Awareness questions", False, str(awareness_questions_response))
            return False
            
        # Count total Awareness questions
        awareness_questions = []
        for domain_data in awareness_questions_response:
            questions = domain_data.get('questions', [])
            awareness_questions.extend(questions)
            
        if len(awareness_questions) == 25:
            self.log_test("Awareness assessment has 25 questions", True)
        else:
            self.log_test("Awareness assessment has 25 questions", False, f"Got {len(awareness_questions)} questions")
        
        # Answer 10 Awareness questions
        questions_to_answer = 10
        for i in range(min(questions_to_answer, len(awareness_questions))):
            question = awareness_questions[i]
            answer_data = {
                "question_id": question['id'],
                "option": "EXPLORING_OPPORTUNITIES",  # Awareness-specific option
                "note": f"Awareness test answer {i+1}"
            }
            
            success, _ = self.make_request('POST', f'assessments/{awareness_assessment_id}/answer', answer_data)
            if not success:
                self.log_test(f"Answer Awareness question {i+1}", False, "Failed to submit answer")
                return False
        
        self.log_test(f"Answered {questions_to_answer} Awareness questions", True)
        
        # Check GET /api/assessments to verify progress display
        success, assessments_list = self.make_request('GET', 'assessments')
        if not success:
            self.log_test("Get assessments list", False, str(assessments_list))
            return False
            
        # Find our Awareness assessment in the list
        awareness_in_list = None
        system_in_list = None
        for assessment in assessments_list:
            if assessment['id'] == awareness_assessment_id:
                awareness_in_list = assessment
            elif assessment['id'] == system_assessment_id:
                system_in_list = assessment
        
        if awareness_in_list:
            if awareness_in_list.get('progress') == questions_to_answer:
                self.log_test(f"Awareness assessment progress = {questions_to_answer}", True)
            else:
                self.log_test(f"Awareness assessment progress = {questions_to_answer}", False, f"Got {awareness_in_list.get('progress')}")
                
            if awareness_in_list.get('total_questions') == 25:
                self.log_test("Awareness assessment total_questions = 25 in list", True)
            else:
                self.log_test("Awareness assessment total_questions = 25 in list", False, f"Got {awareness_in_list.get('total_questions')}")
                
            # Calculate progress ratio
            progress_ratio = (awareness_in_list.get('progress', 0) / awareness_in_list.get('total_questions', 1)) * 100
            expected_ratio = (questions_to_answer / 25) * 100
            if abs(progress_ratio - expected_ratio) < 0.1:
                self.log_test(f"Awareness progress ratio = {expected_ratio:.1f}%", True)
            else:
                self.log_test(f"Awareness progress ratio = {expected_ratio:.1f}%", False, f"Got {progress_ratio:.1f}%")
        else:
            self.log_test("Find Awareness assessment in list", False, "Awareness assessment not found in list")
        
        if system_in_list:
            if system_in_list.get('total_questions') == 88:
                self.log_test("System assessment total_questions = 88 in list", True)
            else:
                self.log_test("System assessment total_questions = 88 in list", False, f"Got {system_in_list.get('total_questions')}")
        else:
            self.log_test("Find System assessment in list", False, "System assessment not found in list")
        
        # Test 4: Verify both assessments show correct total_questions in same response
        print("\n📋 Test 4: Multiple Assessment Types in Same Response")
        
        success, final_assessments_list = self.make_request('GET', 'assessments')
        if not success:
            self.log_test("Get final assessments list", False, str(final_assessments_list))
            return False
            
        # Find both assessments and verify their total_questions
        final_awareness = None
        final_system = None
        for assessment in final_assessments_list:
            if assessment['id'] == awareness_assessment_id:
                final_awareness = assessment
            elif assessment['id'] == system_assessment_id:
                final_system = assessment
        
        if final_awareness and final_system:
            self.log_test("Both assessments found in final list", True)
            
            # Verify Awareness: total_questions = 25
            if final_awareness.get('total_questions') == 25:
                self.log_test("Final check: Awareness total_questions = 25", True)
            else:
                self.log_test("Final check: Awareness total_questions = 25", False, f"Got {final_awareness.get('total_questions')}")
            
            # Verify System: total_questions = 88
            if final_system.get('total_questions') == 88:
                self.log_test("Final check: System total_questions = 88", True)
            else:
                self.log_test("Final check: System total_questions = 88", False, f"Got {final_system.get('total_questions')}")
            
            # Verify progress values are correct
            if final_awareness.get('progress') == questions_to_answer:
                self.log_test(f"Final check: Awareness progress = {questions_to_answer}", True)
            else:
                self.log_test(f"Final check: Awareness progress = {questions_to_answer}", False, f"Got {final_awareness.get('progress')}")
        else:
            self.log_test("Both assessments found in final list", False, "One or both assessments missing")
        
        print("\n✅ Dashboard Progress Display Fix Testing Complete")
        return True

    def run_test(self):
        """Run the dashboard progress display test"""
        print("🚀 Starting Dashboard Progress Display Fix Test")
        print("=" * 60)
        
        if not self.authenticate():
            print("❌ Authentication failed - stopping test")
            return False
        
        success = self.test_dashboard_progress_display_fix()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 TEST SUMMARY")
        print(f"Total tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed - check details above")
            
        return success

if __name__ == "__main__":
    tester = DashboardProgressTester()
    success = tester.run_test()
    sys.exit(0 if success else 1)