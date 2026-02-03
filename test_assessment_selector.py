#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class AssessmentSelectorTester:
    def __init__(self, base_url="https://aiassess-portal.preview.emergentagent.com"):
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
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            
            try:
                return success, response.json() if success else response.text
            except:
                return success, response.text

        except Exception as e:
            return False, str(e)

    def test_user_authentication(self):
        """Test user registration and authentication"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"selector_test_{timestamp}@example.com"
        
        # Test signup
        signup_data = {
            "name": f"Selector Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Selector Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("User authentication", True)
            return True
        else:
            self.log_test("User authentication", False, str(response))
            return False

    def test_assessment_selector_flow(self):
        """Test the Assessment Selector page flow as specified in review request"""
        print("\n🎯 ASSESSMENT SELECTOR FLOW TEST")
        print("-" * 60)
        
        # Test 1: Verify user is authenticated
        if not self.token:
            self.log_test("User authentication for selector flow", False, "No authentication token available")
            return False
        
        self.log_test("User authentication for selector flow", True)
        
        # Test 2: Test assessment creation endpoint (simulates clicking "AI System Assessment" button)
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            self.log_test("Assessment creation via selector", False, str(response))
            return False
        
        if 'id' not in response:
            self.log_test("Assessment creation returns ID", False, "No assessment ID in response")
            return False
        
        new_assessment_id = response['id']
        self.log_test("Assessment creation via selector", True)
        self.log_test("Assessment creation returns ID", True)
        
        # Test 3: Verify assessment details are correct
        success, assessment_details = self.make_request('GET', f'assessments/{new_assessment_id}')
        if not success:
            self.log_test("Get new assessment details", False, str(assessment_details))
            return False
        
        # Verify assessment structure
        required_fields = ['id', 'name', 'status', 'started_at', 'progress', 'total_questions']
        missing_fields = [field for field in required_fields if field not in assessment_details]
        
        if not missing_fields:
            self.log_test("Assessment response structure complete", True)
        else:
            self.log_test("Assessment response structure complete", False, f"Missing fields: {missing_fields}")
        
        # Test 4: Verify assessment is in INCOMPLETE status (ready for questions)
        if assessment_details.get('status') == 'INCOMPLETE':
            self.log_test("New assessment status is INCOMPLETE", True)
        else:
            self.log_test("New assessment status is INCOMPLETE", False, f"Status is {assessment_details.get('status')}")
        
        # Test 5: Verify assessment has 88 total questions
        if assessment_details.get('total_questions') == 88:
            self.log_test("New assessment has 88 total questions", True)
        else:
            self.log_test("New assessment has 88 total questions", False, f"Has {assessment_details.get('total_questions')} questions")
        
        # Test 6: Verify assessment progress is 0 (no questions answered yet)
        if assessment_details.get('progress') == 0:
            self.log_test("New assessment progress is 0", True)
        else:
            self.log_test("New assessment progress is 0", False, f"Progress is {assessment_details.get('progress')}")
        
        # Test 7: Verify assessment questions are accessible (simulates redirect to /assessment/{id})
        success, questions_response = self.make_request('GET', f'assessments/{new_assessment_id}/questions')
        if not success:
            self.log_test("Assessment questions accessible after creation", False, str(questions_response))
            return False
        
        self.log_test("Assessment questions accessible after creation", True)
        
        # Test 8: Verify questions structure for assessment page
        if isinstance(questions_response, list) and len(questions_response) == 11:
            self.log_test("Assessment questions grouped by 11 domains", True)
        else:
            self.log_test("Assessment questions grouped by 11 domains", False, f"Got {len(questions_response) if isinstance(questions_response, list) else 'non-list'} domains")
        
        # Test 9: Count total questions in assessment
        total_questions_in_assessment = 0
        for domain_data in questions_response:
            questions = domain_data.get('questions', [])
            total_questions_in_assessment += len(questions)
        
        if total_questions_in_assessment == 88:
            self.log_test("Assessment contains all 88 questions", True)
        else:
            self.log_test("Assessment contains all 88 questions", False, f"Contains {total_questions_in_assessment} questions")
        
        # Test 10: Verify assessment can be found in user's assessment list
        success, assessments_list = self.make_request('GET', 'assessments')
        if not success:
            self.log_test("Get assessments list", False, str(assessments_list))
            return False
        
        # Find the newly created assessment in the list
        found_assessment = None
        for assessment in assessments_list:
            if assessment.get('id') == new_assessment_id:
                found_assessment = assessment
                break
        
        if found_assessment:
            self.log_test("New assessment appears in assessments list", True)
        else:
            self.log_test("New assessment appears in assessments list", False, "Assessment not found in list")
        
        print(f"\n📋 Assessment Selector Flow Summary:")
        print(f"   ✅ Created assessment ID: {new_assessment_id}")
        print(f"   ✅ Assessment name: {assessment_details.get('name', 'Unknown')}")
        print(f"   ✅ Status: {assessment_details.get('status', 'Unknown')}")
        print(f"   ✅ Total questions: {assessment_details.get('total_questions', 0)}")
        print(f"   ✅ Ready for user to start answering questions")
        
        return True

    def run_tests(self):
        """Run assessment selector flow tests"""
        print("🚀 Starting Assessment Selector Flow Tests")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"🔗 API URL: {self.api_url}")
        print("=" * 60)
        
        # Step 1: Authentication
        if not self.test_user_authentication():
            print("❌ Authentication failed - stopping tests")
            return False
        
        # Step 2: Assessment Selector Flow
        self.test_assessment_selector_flow()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🏁 TEST SUMMARY")
        print("=" * 60)
        print(f"Total tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_run - self.tests_passed}")
        print(f"Success rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed - check details above")
            return False

def main():
    tester = AssessmentSelectorTester()
    
    try:
        success = tester.run_tests()
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())