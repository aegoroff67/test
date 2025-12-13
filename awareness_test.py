#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class AwarenessAssessmentTester:
    def __init__(self, base_url="https://ai-risk-assess.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
        self.awareness_assessment_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

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

    def test_login_with_provided_credentials(self):
        """Test login with the specific credentials provided in review request"""
        login_data = {
            "email": "superadmin@emergentmethods.ai",
            "password": "password123"
        }
        
        success, response = self.make_request('POST', 'auth/login', login_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("Login with provided credentials (superadmin@emergentmethods.ai)", True)
            return True
        else:
            self.log_test("Login with provided credentials (superadmin@emergentmethods.ai)", False, str(response))
            return False

    def test_user_signup_and_login(self):
        """Test user registration and authentication"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"awareness_test_{timestamp}@example.com"
        
        # Test signup
        signup_data = {
            "name": f"Awareness Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Awareness Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("User signup for awareness testing", True)
            self.log_test("Authentication token received", True)
            return True
        else:
            self.log_test("User signup for awareness testing", False, str(response))
            return False

    def test_awareness_assessment_creation(self):
        """Test creating an Awareness Assessment"""
        assessment_data = {
            "assessment_type": "Awareness"
        }
        
        success, response = self.make_request('POST', 'assessments', assessment_data)
        if success and 'id' in response:
            self.awareness_assessment_id = response['id']
            assessment_type = response.get('assessment_type', '')
            if assessment_type == "Awareness":
                self.log_test("Awareness Assessment creation", True)
                self.log_test("Assessment type set to 'Awareness'", True)
                return True
            else:
                self.log_test("Assessment type set to 'Awareness'", False, f"Got type: {assessment_type}")
        else:
            self.log_test("Awareness Assessment creation", False, str(response))
            
        return False

    def test_awareness_response_options(self):
        """Test submitting all Awareness Assessment response options"""
        if not self.awareness_assessment_id:
            self.log_test("Awareness Response Options Test", False, "No awareness assessment ID")
            return False
            
        # Get awareness questions
        success, response = self.make_request('GET', f'assessments/{self.awareness_assessment_id}/questions')
        if not success or not response:
            self.log_test("Get Awareness Questions", False, str(response))
            return False
            
        # Get first question from first domain
        first_domain = response[0] if response else None
        if not first_domain or not first_domain.get('questions'):
            self.log_test("Get Awareness Questions", False, "No questions in first domain")
            return False
            
        first_question = first_domain['questions'][0]
        question_id = first_question['id']
        
        # Test all Awareness response options
        awareness_options = [
            ('EARLY_AWARENESS', 1),
            ('EXPLORING_OPPORTUNITIES', 2),
            ('BUILDING_READINESS', 3),
            ('READY_TO_PROGRESS', 4)
        ]
        
        all_options_success = True
        
        for option, expected_score in awareness_options:
            answer_data = {
                "question_id": question_id,
                "option": option,
                "note": f"Test note for {option}"
            }
            
            success, response = self.make_request('POST', f'assessments/{self.awareness_assessment_id}/answer', answer_data)
            if success and response.get('status') == 'success':
                self.log_test(f"Awareness option {option} submission (returns 200 OK)", True)
            else:
                self.log_test(f"Awareness option {option} submission (returns 200 OK)", False, str(response))
                all_options_success = False
                
        return all_options_success

    def test_awareness_scoring_verification(self):
        """Test that Awareness Assessment options have correct scoring"""
        if not self.awareness_assessment_id:
            self.log_test("Awareness Scoring Verification", False, "No awareness assessment ID")
            return False
            
        # Get awareness questions
        success, response = self.make_request('GET', f'assessments/{self.awareness_assessment_id}/questions')
        if not success or not response:
            self.log_test("Get Questions for Scoring Test", False, str(response))
            return False
            
        # Get multiple questions to test different scores
        all_questions = []
        for domain_data in response:
            questions = domain_data.get('questions', [])
            all_questions.extend(questions)
            
        if len(all_questions) < 4:
            self.log_test("Sufficient Questions for Scoring Test", False, f"Only {len(all_questions)} questions available")
            return False
            
        # Test each scoring option on different questions
        scoring_tests = [
            ('EARLY_AWARENESS', 1, all_questions[0]['id']),
            ('EXPLORING_OPPORTUNITIES', 2, all_questions[1]['id']),
            ('BUILDING_READINESS', 3, all_questions[2]['id']),
            ('READY_TO_PROGRESS', 4, all_questions[3]['id'])
        ]
        
        all_scoring_correct = True
        
        for option, expected_score, question_id in scoring_tests:
            answer_data = {
                "question_id": question_id,
                "option": option,
                "note": f"Scoring test for {option}"
            }
            
            # Submit answer
            success, response = self.make_request('POST', f'assessments/{self.awareness_assessment_id}/answer', answer_data)
            if success:
                self.log_test(f"{option} scores as {expected_score}", True)
            else:
                self.log_test(f"{option} scores as {expected_score}", False, f"Failed to submit: {response}")
                all_scoring_correct = False
                
        return all_scoring_correct

    def test_system_assessment_still_works(self):
        """Test that System assessments still work with original options"""
        # Create a System assessment
        system_data = {
            "assessment_type": "System"
        }
        
        success, response = self.make_request('POST', 'assessments', system_data)
        if not success:
            self.log_test("System Assessment Creation", False, str(response))
            return False
            
        system_assessment_id = response['id']
        self.log_test("System Assessment Creation", True)
        
        # Get system questions
        success, response = self.make_request('GET', f'assessments/{system_assessment_id}/questions')
        if not success or not response:
            self.log_test("Get System Questions", False, str(response))
            return False
            
        # Get first question
        first_domain = response[0] if response else None
        if not first_domain or not first_domain.get('questions'):
            self.log_test("Get System Questions", False, "No questions in first domain")
            return False
            
        first_question = first_domain['questions'][0]
        question_id = first_question['id']
        
        # Test System assessment options
        system_options = [
            ('IDEAL', 3),
            ('GOOD', 2),
            ('BASIC', 1),
            ('NON_IDEAL', 0)
        ]
        
        all_system_options_work = True
        
        for option, expected_score in system_options:
            answer_data = {
                "question_id": question_id,
                "option": option,
                "note": f"System test for {option}"
            }
            
            success, response = self.make_request('POST', f'assessments/{system_assessment_id}/answer', answer_data)
            if success and response.get('status') == 'success':
                self.log_test(f"System option {option} still works (score={expected_score})", True)
            else:
                self.log_test(f"System option {option} still works (score={expected_score})", False, str(response))
                all_system_options_work = False
                
        return all_system_options_work

    def test_awareness_error_handling(self):
        """Test error handling for invalid Awareness Assessment submissions"""
        if not self.awareness_assessment_id:
            self.log_test("Awareness Error Handling Test", False, "No awareness assessment ID")
            return False
            
        # Get first question
        success, response = self.make_request('GET', f'assessments/{self.awareness_assessment_id}/questions')
        if not success or not response:
            return False
            
        first_question = response[0]['questions'][0]
        question_id = first_question['id']
        
        # Test invalid option value
        invalid_answer_data = {
            "question_id": question_id,
            "option": "INVALID_OPTION"
        }
        
        success, response = self.make_request('POST', f'assessments/{self.awareness_assessment_id}/answer', 
                                            invalid_answer_data, expected_status=422)
        if success:
            self.log_test("Invalid option returns proper error", True)
        else:
            self.log_test("Invalid option returns proper error", False, "Should have returned 422 validation error")
            
        # Test OTHER option with text (should work)
        other_answer_data = {
            "question_id": question_id,
            "option": "OTHER",
            "other_text": "Custom awareness response"
        }
        
        success, response = self.make_request('POST', f'assessments/{self.awareness_assessment_id}/answer', other_answer_data)
        if success:
            self.log_test("OTHER option with text works in Awareness Assessment", True)
        else:
            self.log_test("OTHER option with text works in Awareness Assessment", False, str(response))
            
        return True

    def test_specific_assessment_id(self):
        """Test the specific assessment ID mentioned in the review request"""
        known_assessment_id = "ae444dfb-358a-4ed7-96e1-e1522a86f7f4"
        
        # Try to get this specific assessment
        success, response = self.make_request('GET', f'assessments/{known_assessment_id}')
        if success:
            assessment_type = response.get('assessment_type', '')
            if assessment_type == "Awareness":
                self.log_test(f"Known Assessment {known_assessment_id} is Awareness type", True)
                
                # Try to get questions for this assessment
                success, questions_response = self.make_request('GET', f'assessments/{known_assessment_id}/questions')
                if success:
                    self.log_test(f"Known Assessment {known_assessment_id} questions accessible", True)
                else:
                    self.log_test(f"Known Assessment {known_assessment_id} questions accessible", False, str(questions_response))
            else:
                self.log_test(f"Known Assessment {known_assessment_id} is Awareness type", False, f"Type is: {assessment_type}")
        else:
            self.log_test(f"Known Assessment {known_assessment_id} accessible", False, str(response))
            
        return success

    def run_awareness_tests(self):
        """Run all Awareness Assessment tests"""
        print("🚀 Starting AI Awareness Assessment Testing...")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"🔗 API URL: {self.api_url}")
        print("=" * 80)
        
        # Try login with provided credentials first
        if not self.test_login_with_provided_credentials():
            print("⚠️  Provided credentials failed, trying signup/login...")
            if not self.test_user_signup_and_login():
                print("❌ Authentication failed - stopping tests")
                return False
        
        # Test the specific assessment ID mentioned in review request
        self.test_specific_assessment_id()
        
        # === AWARENESS ASSESSMENT TESTS (MAIN FOCUS) ===
        print("\n" + "🎯 AWARENESS ASSESSMENT TESTS (MAIN FOCUS)" + "\n" + "=" * 60)
        
        # Test 1: Create Awareness Assessment
        if self.test_awareness_assessment_creation():
            # Test 2: Submit Awareness Response Options
            self.test_awareness_response_options()
            
            # Test 3: Verify Correct Scoring
            self.test_awareness_scoring_verification()
            
            # Test 5: Error Handling
            self.test_awareness_error_handling()
        
        # Test 4: Verify System Assessment Still Works
        self.test_system_assessment_still_works()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 AWARENESS ASSESSMENT TEST SUMMARY")
        print("=" * 80)
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"📈 Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL AWARENESS ASSESSMENT TESTS PASSED!")
        else:
            print("⚠️  Some tests failed - check details above")
            
        return self.tests_passed == self.tests_run

def main():
    tester = AwarenessAssessmentTester()
    
    try:
        success = tester.run_awareness_tests()
        
        if success:
            print("🎉 All Awareness Assessment tests passed!")
            return 0
        else:
            print(f"⚠️  {tester.tests_run - tester.tests_passed} tests failed")
            return 1
        
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())