#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class AMSafeAPITester:
    def __init__(self, base_url="https://assessment-data.preview.emergentagent.com"):
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
            self.log_test("Authentication token received", True)
        else:
            self.log_test("User signup", False, str(response))
            return False

        # Test login with same credentials
        login_data = {
            "email": test_email,
            "password": "TestPass123!"
        }
        
        success, response = self.make_request('POST', 'auth/login', login_data)
        if success and 'access_token' in response:
            self.log_test("User login", True)
        else:
            self.log_test("User login", False, str(response))
            
        return True

    def test_domains_and_questions_structure(self):
        """Test that domains and questions are properly structured"""
        # Test domains endpoint
        success, domains = self.make_request('GET', 'domains')
        if not success:
            self.log_test("Domains endpoint", False, str(domains))
            return False
            
        # Verify 11 domains
        if len(domains) == 11:
            self.log_test("11 domains present", True)
        else:
            self.log_test("11 domains present", False, f"Found {len(domains)} domains")
            
        # Verify domain names
        expected_domains = [
            "Fairness", "Transparency", "Explainability", "Accountability",
            "Data Integrity", "Reliability", "Security", "Privacy", 
            "Safety", "Inclusivity", "Sustainability"
        ]
        
        domain_names = [d['name'] for d in domains]
        if set(domain_names) == set(expected_domains):
            self.log_test("All expected domain names present", True)
        else:
            missing = set(expected_domains) - set(domain_names)
            self.log_test("All expected domain names present", False, f"Missing: {missing}")

        # Test questions endpoint
        success, questions = self.make_request('GET', 'questions')
        if not success:
            self.log_test("Questions endpoint", False, str(questions))
            return False
            
        # Verify 88 questions (11 domains × 8 questions each)
        if len(questions) == 88:
            self.log_test("88 questions present", True)
        else:
            self.log_test("88 questions present", False, f"Found {len(questions)} questions")
            
        # Verify question structure includes answer content fields
        sample_question = questions[0] if questions else None
        if sample_question:
            required_fields = ['ideal_answer', 'good_answer', 'basic_answer', 'non_ideal_answer']
            has_answer_fields = all(field in sample_question for field in required_fields)
            if has_answer_fields:
                self.log_test("Questions have answer content fields", True)
            else:
                missing_fields = [f for f in required_fields if f not in sample_question]
                self.log_test("Questions have answer content fields", False, f"Missing: {missing_fields}")
                
        return True

    def test_assessment_creation(self):
        """Test assessment creation"""
        success, response = self.make_request('POST', 'assessments', {})
        if success and 'id' in response:
            self.assessment_id = response['id']
            self.log_test("Assessment creation", True)
            return True
        else:
            self.log_test("Assessment creation", False, str(response))
            return False

    def test_assessment_details(self):
        """Test assessment details endpoint"""
        if not self.assessment_id:
            self.log_test("Assessment details", False, "No assessment ID")
            return False
            
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}')
        if not success:
            self.log_test("Assessment details", False, str(response))
            return False
            
        # Verify structure
        required_keys = ['assessment', 'questions', 'domains', 'progress']
        if all(key in response for key in required_keys):
            self.log_test("Assessment details structure", True)
        else:
            missing = [k for k in required_keys if k not in response]
            self.log_test("Assessment details structure", False, f"Missing: {missing}")
            
        # Verify questions have answer content
        questions = response.get('questions', [])
        if questions:
            sample_q = questions[0]
            answer_fields = ['ideal_answer', 'good_answer', 'basic_answer', 'non_ideal_answer']
            has_content = any(sample_q.get(field) for field in answer_fields)
            if has_content:
                self.log_test("Questions contain answer content", True)
            else:
                self.log_test("Questions contain answer content", False, "No answer content found")
                
        return True

    def test_answer_system(self):
        """Test the corrected answer system with 4 standard options + Other"""
        if not self.assessment_id:
            self.log_test("Answer system test", False, "No assessment ID")
            return False
            
        # Get first question
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}')
        if not success or not response.get('questions'):
            self.log_test("Get questions for answer test", False, "No questions available")
            return False
            
        first_question = response['questions'][0]
        question_id = first_question['id']
        
        # Test each standard answer option
        standard_options = [
            ('IDEAL', 3),
            ('GOOD', 2), 
            ('BASIC', 1),
            ('NON_IDEAL', 0)
        ]
        
        for option, expected_score in standard_options:
            answer_data = {
                "question_id": question_id,
                "option": option,
                "note": f"Test note for {option}"
            }
            
            success, response = self.make_request('PATCH', f'assessments/{self.assessment_id}/answer', answer_data)
            if success:
                if response.get('score') == expected_score:
                    self.log_test(f"Answer option {option} (score {expected_score})", True)
                else:
                    self.log_test(f"Answer option {option} (score {expected_score})", False, 
                                f"Expected score {expected_score}, got {response.get('score')}")
            else:
                self.log_test(f"Answer option {option}", False, str(response))
                
        # Test OTHER option with text
        other_answer_data = {
            "question_id": question_id,
            "option": "OTHER",
            "other_text": "This is a custom response that should be flagged for review",
            "note": "Test note for OTHER option"
        }
        
        success, response = self.make_request('PATCH', f'assessments/{self.assessment_id}/answer', other_answer_data)
        if success:
            if response.get('needs_review') == True:
                self.log_test("OTHER option flags for review", True)
            else:
                self.log_test("OTHER option flags for review", False, "needs_review not set to True")
                
            if response.get('score') == 0:
                self.log_test("OTHER option score (0)", True)
            else:
                self.log_test("OTHER option score (0)", False, f"Expected 0, got {response.get('score')}")
        else:
            self.log_test("OTHER option submission", False, str(response))
            
        # Test OTHER option validation (should fail without text)
        invalid_other_data = {
            "question_id": question_id,
            "option": "OTHER"
            # No other_text provided
        }
        
        success, response = self.make_request('PATCH', f'assessments/{self.assessment_id}/answer', 
                                            invalid_other_data, expected_status=400)
        if success:
            self.log_test("OTHER option validation (requires text)", True)
        else:
            self.log_test("OTHER option validation (requires text)", False, "Should have failed without other_text")
            
        return True

    def test_status_view(self):
        """Test the status view endpoint for View All functionality"""
        if not self.assessment_id:
            self.log_test("Status view test", False, "No assessment ID")
            return False
            
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/status')
        if not success:
            self.log_test("Status endpoint", False, str(response))
            return False
            
        # Verify structure for View All screen
        required_keys = ['status_overview', 'total_questions', 'answered_questions', 'completion_percentage']
        if all(key in response for key in required_keys):
            self.log_test("Status endpoint structure", True)
        else:
            missing = [k for k in required_keys if k not in response]
            self.log_test("Status endpoint structure", False, f"Missing: {missing}")
            
        # Verify 11 domains in status overview
        status_overview = response.get('status_overview', [])
        if len(status_overview) == 11:
            self.log_test("Status shows 11 domains", True)
        else:
            self.log_test("Status shows 11 domains", False, f"Found {len(status_overview)} domains")
            
        # Verify each domain has 8 questions
        all_domains_have_8_questions = True
        for domain in status_overview:
            if len(domain.get('questions', [])) != 8:
                all_domains_have_8_questions = False
                break
                
        if all_domains_have_8_questions:
            self.log_test("Each domain has 8 questions in status", True)
        else:
            self.log_test("Each domain has 8 questions in status", False, "Some domains don't have 8 questions")
            
        # Verify total questions is 88
        if response.get('total_questions') == 88:
            self.log_test("Status shows 88 total questions", True)
        else:
            self.log_test("Status shows 88 total questions", False, f"Shows {response.get('total_questions')}")
            
        return True

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
        """Run comprehensive test suite"""
        print("🚀 Starting AM AI SAFE Corrected Answer System Tests")
        print("=" * 60)
        
        # Authentication tests
        if not self.test_user_signup_and_login():
            print("❌ Authentication failed, stopping tests")
            return False
            
        # Structure tests
        self.test_domains_and_questions_structure()
        
        # Assessment tests
        if not self.test_assessment_creation():
            print("❌ Assessment creation failed, stopping tests")
            return False
            
        self.test_assessment_details()
        
        # Core functionality tests
        self.test_answer_system()
        self.test_status_view()
        
        # Print results
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        print(f"✅ Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed! Corrected answer system working correctly.")
            return True
        else:
            print("⚠️  Some tests failed. Check details above.")
            return False

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