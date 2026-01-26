#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class StatusEndpointTester:
    def __init__(self, base_url="https://aireport-generator.preview.emergentagent.com"):
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
            if success:
                return True, response.json()
            else:
                return False, f"Status {response.status_code}: {response.text}"

        except Exception as e:
            return False, str(e)

    def setup_auth_and_assessment(self):
        """Setup authentication and create assessment for testing"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"status_test_{timestamp}@example.com"
        
        # Signup
        signup_data = {
            "name": f"Status Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Status Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.log_test("Authentication setup", True)
        else:
            self.log_test("Authentication setup", False, str(response))
            return False

        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if success and 'id' in response:
            self.assessment_id = response['id']
            self.log_test("Assessment creation", True)
            return True
        else:
            self.log_test("Assessment creation", False, str(response))
            return False

    def test_status_endpoint_exists(self):
        """Test that the status endpoint exists and returns 200"""
        if not self.assessment_id:
            self.log_test("Status endpoint exists", False, "No assessment ID")
            return False
            
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/status')
        if success:
            self.log_test("Status endpoint exists (returns 200)", True)
            return response
        else:
            self.log_test("Status endpoint exists (returns 200)", False, str(response))
            return None

    def test_status_endpoint_structure(self, response):
        """Test the status endpoint returns expected data structure"""
        if not response:
            self.log_test("Status endpoint structure", False, "No response data")
            return False

        # Check required fields
        required_fields = ['assessment_id', 'total_questions', 'answered_questions', 'completion_percentage', 'status_overview']
        missing_fields = []
        
        for field in required_fields:
            if field not in response:
                missing_fields.append(field)
        
        if not missing_fields:
            self.log_test("Status endpoint has all required fields", True)
        else:
            self.log_test("Status endpoint has all required fields", False, f"Missing: {missing_fields}")
            return False

        # Verify assessment_id matches
        if response.get('assessment_id') == self.assessment_id:
            self.log_test("Status endpoint returns correct assessment_id", True)
        else:
            self.log_test("Status endpoint returns correct assessment_id", False, 
                        f"Expected {self.assessment_id}, got {response.get('assessment_id')}")

        # Verify status_overview is an array
        status_overview = response.get('status_overview', [])
        if isinstance(status_overview, list):
            self.log_test("Status overview is an array", True)
        else:
            self.log_test("Status overview is an array", False, f"Got {type(status_overview)}")
            return False

        # Verify status_overview contains domains with questions
        if status_overview:
            first_domain = status_overview[0]
            domain_required_fields = ['domain_id', 'domain_name', 'questions']
            domain_missing = [f for f in domain_required_fields if f not in first_domain]
            
            if not domain_missing:
                self.log_test("Status overview domains have required fields", True)
            else:
                self.log_test("Status overview domains have required fields", False, f"Missing: {domain_missing}")
                return False

            # Check questions structure in domain
            questions = first_domain.get('questions', [])
            if questions and isinstance(questions, list):
                first_question = questions[0]
                question_required_fields = ['question_id', 'question_code', 'question_text', 'answered']
                question_missing = [f for f in question_required_fields if f not in first_question]
                
                if not question_missing:
                    self.log_test("Status overview questions have required fields", True)
                else:
                    self.log_test("Status overview questions have required fields", False, f"Missing: {question_missing}")
                    return False
            else:
                self.log_test("Status overview questions structure", False, "No questions or invalid structure")
                return False
        else:
            self.log_test("Status overview contains domains", False, "Status overview is empty")
            return False

        return True

    def test_status_endpoint_data_types(self, response):
        """Test that the status endpoint returns correct data types"""
        if not response:
            return False

        # Check data types
        type_checks = [
            ('assessment_id', str),
            ('total_questions', int),
            ('answered_questions', int),
            ('completion_percentage', (int, float)),
            ('status_overview', list)
        ]

        all_types_correct = True
        for field, expected_type in type_checks:
            value = response.get(field)
            if isinstance(value, expected_type):
                self.log_test(f"Status endpoint {field} has correct type", True)
            else:
                self.log_test(f"Status endpoint {field} has correct type", False, 
                            f"Expected {expected_type}, got {type(value)}")
                all_types_correct = False

        return all_types_correct

    def test_status_endpoint_with_answers(self):
        """Test status endpoint after submitting some answers"""
        if not self.assessment_id:
            return False

        # Get questions first
        success, questions_response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success or not questions_response:
            self.log_test("Get questions for answer test", False, "Could not get questions")
            return False

        # Submit an answer to first question
        if questions_response and len(questions_response) > 0:
            first_domain = questions_response[0]
            if first_domain.get('questions'):
                first_question = first_domain['questions'][0]
                question_id = first_question['id']
                
                answer_data = {
                    "question_id": question_id,
                    "option": "GOOD",
                    "note": "Test answer for status endpoint"
                }
                
                success, answer_response = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
                if success:
                    self.log_test("Submit test answer", True)
                else:
                    self.log_test("Submit test answer", False, str(answer_response))
                    return False

        # Test status endpoint after answer
        success, status_response = self.make_request('GET', f'assessments/{self.assessment_id}/status')
        if success:
            answered_questions = status_response.get('answered_questions', 0)
            if answered_questions > 0:
                self.log_test("Status endpoint shows answered questions count", True)
            else:
                self.log_test("Status endpoint shows answered questions count", False, 
                            f"Expected > 0, got {answered_questions}")

            completion_percentage = status_response.get('completion_percentage', 0)
            if completion_percentage > 0:
                self.log_test("Status endpoint shows completion percentage", True)
            else:
                self.log_test("Status endpoint shows completion percentage", False, 
                            f"Expected > 0, got {completion_percentage}")

            return True
        else:
            self.log_test("Status endpoint after answer", False, str(status_response))
            return False

    def run_status_tests(self):
        """Run all status endpoint tests"""
        print("🚀 Testing Status Endpoint for 'View All' Button Functionality")
        print("=" * 60)
        
        # Setup
        if not self.setup_auth_and_assessment():
            print("❌ Setup failed, stopping tests")
            return False

        # Test endpoint exists
        response = self.test_status_endpoint_exists()
        if not response:
            print("❌ Status endpoint not accessible, stopping tests")
            return False

        # Test structure
        if not self.test_status_endpoint_structure(response):
            print("❌ Status endpoint structure invalid")
            return False

        # Test data types
        self.test_status_endpoint_data_types(response)

        # Test with answers
        self.test_status_endpoint_with_answers()

        # Print results
        print("\n" + "=" * 60)
        print(f"📊 Status Endpoint Test Results: {self.tests_passed}/{self.tests_run} passed")
        print(f"✅ Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 Status endpoint is working correctly for 'View All' functionality!")
            return True
        else:
            print("⚠️  Some status endpoint tests failed. Check details above.")
            return False

def main():
    tester = StatusEndpointTester()
    
    try:
        success = tester.run_status_tests()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Status endpoint test execution failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())