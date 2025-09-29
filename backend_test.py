#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class AMSafeAPITester:
    def __init__(self, base_url="https://amai-platform.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
        self.assessment_id = None
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
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=headers)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            return success, response.json() if success else response.text

        except Exception as e:
            return False, str(e)

    def test_signup(self):
        """Test user signup"""
        timestamp = datetime.now().strftime('%H%M%S')
        signup_data = {
            "name": f"Test User {timestamp}",
            "email": f"test{timestamp}@example.com",
            "password": "TestPass123!",
            "organization_name": f"Test Org {timestamp}",
            "industry": "Technology"
        }
        
        response = self.run_test(
            "User Signup",
            "POST",
            "auth/signup",
            200,
            data=signup_data
        )
        
        if response and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            return True
        return False

    def test_login(self):
        """Test user login with existing credentials"""
        if not self.user_data:
            return False
            
        login_data = {
            "email": self.user_data['email'],
            "password": "TestPass123!"
        }
        
        response = self.run_test(
            "User Login",
            "POST", 
            "auth/login",
            200,
            data=login_data
        )
        
        if response and 'access_token' in response:
            self.token = response['access_token']
            return True
        return False

    def test_get_me(self):
        """Test get current user"""
        response = self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )
        return response is not None

    def test_get_domains(self):
        """Test get domains - Enhanced version with 11 domains"""
        response = self.run_test(
            "Get Domains",
            "GET",
            "domains",
            200
        )
        
        if response and isinstance(response, list) and len(response) == 11:
            expected_domains = [
                "Fairness", "Transparency", "Explainability", "Accountability", 
                "Data Integrity", "Reliability", "Security", "Privacy", 
                "Safety", "Inclusivity", "Sustainability"
            ]
            actual_domains = [d['name'] for d in response]
            if all(domain in actual_domains for domain in expected_domains):
                self.log_test("Domain Content Validation (11 domains)", True)
                return True
            else:
                self.log_test("Domain Content Validation (11 domains)", False, f"Expected {expected_domains}, got {actual_domains}")
        else:
            self.log_test("Domain Count Validation", False, f"Expected 11 domains, got {len(response) if response else 0}")
        
        return response is not None

    def test_get_questions(self):
        """Test get questions - Enhanced version with 88 questions"""
        response = self.run_test(
            "Get Questions",
            "GET",
            "questions",
            200
        )
        
        if response and isinstance(response, list) and len(response) == 88:
            # Check if we have 8 questions per domain (11 domains × 8 questions = 88)
            domain_counts = {}
            question_codes = []
            for q in response:
                domain_id = q.get('domain_id')
                domain_counts[domain_id] = domain_counts.get(domain_id, 0) + 1
                question_codes.append(q.get('code', ''))
            
            if len(domain_counts) == 11 and all(count == 8 for count in domain_counts.values()):
                self.log_test("Questions Distribution Validation (8 per domain)", True)
                
                # Validate question codes format (e.g., FA-1, TR-1, etc.)
                expected_prefixes = ['FA-', 'TR-', 'EX-', 'AC-', 'DI-', 'RE-', 'SE-', 'PR-', 'SA-', 'IN-', 'SU-']
                code_validation = True
                for prefix in expected_prefixes:
                    prefix_codes = [code for code in question_codes if code.startswith(prefix)]
                    if len(prefix_codes) != 8:
                        code_validation = False
                        break
                
                if code_validation:
                    self.log_test("Question Codes Validation", True)
                else:
                    self.log_test("Question Codes Validation", False, "Not all domains have 8 properly coded questions")
                
                return True
            else:
                self.log_test("Questions Distribution Validation (8 per domain)", False, f"Expected 8 questions per domain for 11 domains, got {domain_counts}")
        else:
            self.log_test("Questions Count Validation", False, f"Expected 88 questions, got {len(response) if response else 0}")
        
        return response is not None

    def test_create_assessment(self):
        """Test create assessment"""
        response = self.run_test(
            "Create Assessment",
            "POST",
            "assessments",
            200
        )
        
        if response and 'id' in response:
            self.assessment_id = response['id']
            return True
        return False

    def test_get_assessments(self):
        """Test get assessments"""
        response = self.run_test(
            "Get Assessments",
            "GET",
            "assessments",
            200
        )
        
        if response and isinstance(response, list) and len(response) >= 1:
            # Check if our created assessment is in the list
            assessment_ids = [a['id'] for a in response]
            if hasattr(self, 'assessment_id') and self.assessment_id in assessment_ids:
                self.log_test("Assessment List Validation", True)
                return True
            else:
                self.log_test("Assessment List Validation", False, "Created assessment not found in list")
        
        return response is not None

    def test_get_assessment_details(self):
        """Test get assessment details"""
        if not hasattr(self, 'assessment_id'):
            self.log_test("Get Assessment Details", False, "No assessment ID available")
            return False
            
        response = self.run_test(
            "Get Assessment Details",
            "GET",
            f"assessments/{self.assessment_id}",
            200
        )
        
        if response and 'assessment' in response and 'questions' in response:
            questions = response['questions']
            if len(questions) == 88:
                self.log_test("Assessment Questions Count (88 questions)", True)
                
                # Validate progress format
                progress = response.get('progress', '')
                if progress == '0/88':
                    self.log_test("Assessment Progress Format", True)
                else:
                    self.log_test("Assessment Progress Format", False, f"Expected '0/88', got '{progress}'")
                
                return True
            else:
                self.log_test("Assessment Questions Count (88 questions)", False, f"Expected 88 questions, got {len(questions)}")
        
        return response is not None

    def test_save_answer(self):
        """Test save answer"""
        if not hasattr(self, 'assessment_id'):
            self.log_test("Save Answer", False, "No assessment ID available")
            return False
        
        # Get questions first
        assessment_response = self.run_test(
            "Get Assessment for Answer Test",
            "GET",
            f"assessments/{self.assessment_id}",
            200
        )
        
        if not assessment_response or 'questions' not in assessment_response:
            return False
        
        questions = assessment_response['questions']
        if not questions:
            self.log_test("Save Answer", False, "No questions available")
            return False
        
        # Save answer for first question
        first_question = questions[0]
        answer_data = {
            "question_id": first_question['id'],
            "option": "GOOD",
            "note": "Test answer note"
        }
        
        response = self.run_test(
            "Save Answer",
            "PATCH",
            f"assessments/{self.assessment_id}/answer",
            200,
            data=answer_data
        )
        
        return response is not None

    def test_submit_assessment_incomplete(self):
        """Test submit assessment when incomplete (should fail)"""
        if not hasattr(self, 'assessment_id'):
            self.log_test("Submit Incomplete Assessment", False, "No assessment ID available")
            return False
        
        response = self.run_test(
            "Submit Incomplete Assessment",
            "POST",
            f"assessments/{self.assessment_id}/submit",
            400  # Should fail with 400
        )
        
        # This should fail, so success means we got the expected 400 error
        return response is None  # None means we got the expected error

    def test_complete_assessment_flow(self):
        """Test completing an entire assessment"""
        if not hasattr(self, 'assessment_id'):
            self.log_test("Complete Assessment Flow", False, "No assessment ID available")
            return False
        
        # Get all questions
        assessment_response = self.run_test(
            "Get Assessment for Completion",
            "GET",
            f"assessments/{self.assessment_id}",
            200
        )
        
        if not assessment_response or 'questions' not in assessment_response:
            return False
        
        questions = assessment_response['questions']
        
        # Answer all questions
        options = ["IDEAL", "GOOD", "BASIC", "NON_IDEAL"]
        success_count = 0
        
        for i, question in enumerate(questions):
            option = options[i % len(options)]  # Cycle through options
            answer_data = {
                "question_id": question['id'],
                "option": option,
                "note": f"Test note for question {i+1}"
            }
            
            response = self.run_test(
                f"Answer Question {i+1} ({question['code']})",
                "PATCH",
                f"assessments/{self.assessment_id}/answer",
                200,
                data=answer_data
            )
            
            if response:
                success_count += 1
        
        if success_count == len(questions):
            self.log_test("Complete All Questions", True)
            return True
        else:
            self.log_test("Complete All Questions", False, f"Only answered {success_count}/{len(questions)} questions")
            return False

    def test_submit_complete_assessment(self):
        """Test submit complete assessment"""
        if not hasattr(self, 'assessment_id'):
            self.log_test("Submit Complete Assessment", False, "No assessment ID available")
            return False
        
        response = self.run_test(
            "Submit Complete Assessment",
            "POST",
            f"assessments/{self.assessment_id}/submit",
            200
        )
        
        return response is not None

    def test_get_assessment_summary(self):
        """Test get assessment summary"""
        if not hasattr(self, 'assessment_id'):
            self.log_test("Get Assessment Summary", False, "No assessment ID available")
            return False
        
        response = self.run_test(
            "Get Assessment Summary",
            "GET",
            f"assessments/{self.assessment_id}/summary",
            200
        )
        
        if response and 'overall_percentage' in response and 'domain_scores' in response:
            # Validate summary structure for 11 domains
            if len(response['domain_scores']) == 11:
                self.log_test("Summary Structure Validation (11 domains)", True)
                
                # Validate total questions count
                if response.get('total_questions') == 88:
                    self.log_test("Summary Total Questions Count", True)
                else:
                    self.log_test("Summary Total Questions Count", False, f"Expected 88 total questions, got {response.get('total_questions')}")
                
                return True
            else:
                self.log_test("Summary Structure Validation (11 domains)", False, f"Expected 11 domain scores, got {len(response['domain_scores'])}")
        
        return response is not None

    def test_generate_pdf_report(self):
        """Test PDF report generation"""
        if not hasattr(self, 'assessment_id'):
            self.log_test("Generate PDF Report", False, "No assessment ID available")
            return False
        
        response = self.run_test(
            "Generate PDF Report",
            "POST",
            f"reports/{self.assessment_id}/pdf",
            200
        )
        
        if response and 'url' in response:
            # Check if URL is the expected static URL
            expected_url = "https://example.com/static-sample-report.pdf"
            if response['url'] == expected_url:
                self.log_test("PDF Report URL Validation", True)
                return True
            else:
                self.log_test("PDF Report URL Validation", False, f"Expected {expected_url}, got {response['url']}")
        
        return response is not None

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting AM AI SAFE API Tests")
        print(f"   Base URL: {self.base_url}")
        print("=" * 60)
        
        # Authentication tests
        if not self.test_signup():
            print("❌ Signup failed, stopping tests")
            return False
        
        # Test login with the same credentials
        # Note: We'll skip separate login test since signup already gives us a token
        
        self.test_get_me()
        
        # Domain and question tests
        self.test_get_domains()
        self.test_get_questions()
        
        # Assessment workflow tests
        if not self.test_create_assessment():
            print("❌ Assessment creation failed, stopping assessment tests")
            return False
        
        self.test_get_assessments()
        self.test_get_assessment_details()
        self.test_save_answer()
        self.test_submit_assessment_incomplete()  # Should fail
        
        # Complete assessment flow
        if self.test_complete_assessment_flow():
            self.test_submit_complete_assessment()
            self.test_get_assessment_summary()
            self.test_generate_pdf_report()
        
        return True

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_run - self.tests_passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['details']}")
        
        return self.tests_passed == self.tests_run

def main():
    tester = AMSafeAPITester()
    
    try:
        success = tester.run_all_tests()
        tester.print_summary()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())