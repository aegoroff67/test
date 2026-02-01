#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class ReadinessBugTester:
    def __init__(self, base_url="https://risk-scan-portal.preview.emergentagent.com"):
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

    def test_authentication(self):
        """Test user authentication"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"readiness_test_{timestamp}@example.com"
        
        signup_data = {
            "name": f"Readiness Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Readiness Test Org {timestamp}",
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

    def test_readiness_assessment_bug_fixes(self):
        """Test the specific AI Readiness Assessment bug fixes"""
        print("\n🔍 TESTING AI READINESS ASSESSMENT BUG FIXES")
        print("=" * 60)
        
        # Create a Readiness assessment
        assessment_data = {"assessment_type": "Readiness"}
        success, response = self.make_request('POST', 'assessments', assessment_data)
        if not success:
            self.log_test("Create Readiness Assessment", False, str(response))
            return False
            
        readiness_assessment_id = response['id']
        assessment_type = response.get('assessment_type', 'Unknown')
        
        if assessment_type == 'Readiness':
            self.log_test("Create Readiness Assessment", True)
        else:
            self.log_test("Create Readiness Assessment", False, f"Expected 'Readiness', got '{assessment_type}'")
            return False
        
        # Get readiness questions to answer some
        success, questions_response = self.make_request('GET', f'assessments/{readiness_assessment_id}/questions')
        if not success:
            self.log_test("Get Readiness Assessment Questions", False, str(questions_response))
            return False
            
        self.log_test("Get Readiness Assessment Questions", True)
        
        # Collect all questions for answering
        all_readiness_questions = []
        for domain_data in questions_response:
            questions = domain_data.get('questions', [])
            all_readiness_questions.extend(questions)
        
        total_readiness_questions = len(all_readiness_questions)
        self.log_test(f"Total Readiness Questions Available: {total_readiness_questions}", total_readiness_questions == 48)
        
        # Answer at least 5-10 questions as requested
        questions_to_answer = min(10, len(all_readiness_questions))
        answered_count = 0
        
        for i in range(questions_to_answer):
            question = all_readiness_questions[i]
            answer_data = {
                "question_id": question['id'],
                "option": "ESTABLISHED",  # Use Readiness-specific option
                "note": f"Test answer {i+1} for readiness assessment"
            }
            
            success, _ = self.make_request('POST', f'assessments/{readiness_assessment_id}/answer', answer_data)
            if success:
                answered_count += 1
        
        self.log_test(f"Answered {answered_count} Readiness Questions", answered_count >= 5)
        
        # BUG 1: Test View All Button Crash Fix - GET /api/assessments/{assessment_id}/status
        print("\n🐛 BUG 1: Testing View All Button Crash Fix")
        print("-" * 40)
        
        success, status_response = self.make_request('GET', f'assessments/{readiness_assessment_id}/status')
        if not success:
            self.log_test("BUG 1: GET /api/assessments/{id}/status endpoint", False, str(status_response))
            return False
            
        self.log_test("BUG 1: GET /api/assessments/{id}/status endpoint", True)
        
        # Verify response has status_overview array (NOT domain_scores)
        if 'status_overview' in status_response:
            self.log_test("BUG 1: Response has status_overview array", True)
        else:
            self.log_test("BUG 1: Response has status_overview array", False, "Missing status_overview field")
            return False
        
        # Verify it does NOT have domain_scores (this was the bug)
        if 'domain_scores' not in status_response:
            self.log_test("BUG 1: Response does NOT have domain_scores (bug fixed)", True)
        else:
            self.log_test("BUG 1: Response does NOT have domain_scores (bug fixed)", False, "Still contains domain_scores field")
        
        status_overview = status_response['status_overview']
        
        # Verify each domain has domain_id, domain_name, and questions array
        domains_with_correct_structure = 0
        total_domains = len(status_overview)
        
        for domain in status_overview:
            has_domain_id = 'domain_id' in domain
            has_domain_name = 'domain_name' in domain  
            has_questions_array = 'questions' in domain and isinstance(domain['questions'], list)
            
            if has_domain_id and has_domain_name and has_questions_array:
                domains_with_correct_structure += 1
        
        if domains_with_correct_structure == total_domains:
            self.log_test("BUG 1: All domains have domain_id, domain_name, and questions array", True)
        else:
            self.log_test("BUG 1: All domains have domain_id, domain_name, and questions array", False, 
                        f"Only {domains_with_correct_structure}/{total_domains} domains have correct structure")
        
        # Verify each question has required fields
        total_questions_in_status = 0
        questions_with_correct_structure = 0
        
        for domain in status_overview:
            questions = domain.get('questions', [])
            total_questions_in_status += len(questions)
            
            for question in questions:
                has_question_id = 'question_id' in question
                has_question_code = 'question_code' in question
                has_question_text = 'question_text' in question
                has_answered = 'answered' in question and isinstance(question['answered'], bool)
                has_review_status = 'review_status' in question
                
                if has_question_id and has_question_code and has_question_text and has_answered and has_review_status:
                    questions_with_correct_structure += 1
        
        if questions_with_correct_structure == total_questions_in_status:
            self.log_test("BUG 1: All questions have question_id, question_code, question_text, answered, review_status", True)
        else:
            self.log_test("BUG 1: All questions have required fields", False,
                        f"Only {questions_with_correct_structure}/{total_questions_in_status} questions have all required fields")
        
        # Verify total questions count (should be 48 for Readiness)
        expected_readiness_questions = 48
        if total_questions_in_status == expected_readiness_questions:
            self.log_test(f"BUG 1: Total {expected_readiness_questions} questions across domains", True)
        else:
            self.log_test(f"BUG 1: Total {expected_readiness_questions} questions across domains", False,
                        f"Found {total_questions_in_status} questions, expected {expected_readiness_questions}")
        
        # Verify completion_percentage is calculated correctly
        completion_percentage = status_response.get('completion_percentage', 0)
        expected_percentage = (answered_count / expected_readiness_questions) * 100
        
        if abs(completion_percentage - expected_percentage) < 1:  # Allow small rounding differences
            self.log_test("BUG 1: completion_percentage calculated correctly", True)
        else:
            self.log_test("BUG 1: completion_percentage calculated correctly", False,
                        f"Expected ~{expected_percentage:.1f}%, got {completion_percentage}%")
        
        # BUG 2: Test Missing Tooltips Fix - GET /api/assessments/{assessment_id}/questions
        print("\n🐛 BUG 2: Testing Missing Tooltips Fix")
        print("-" * 40)
        
        success, questions_response = self.make_request('GET', f'assessments/{readiness_assessment_id}/questions')
        if not success:
            self.log_test("BUG 2: GET /api/assessments/{id}/questions endpoint", False, str(questions_response))
            return False
            
        self.log_test("BUG 2: GET /api/assessments/{id}/questions endpoint", True)
        
        # Check for additional_guide field in questions
        questions_with_tooltips = 0
        total_questions_checked = 0
        sample_questions_to_check = ['SA-01', 'GF-01', 'DR-01', 'TI-01', 'PC-01', 'PR-01', 'RE-01', 'CL-01']
        sample_questions_found = {}
        
        for domain_data in questions_response:
            questions = domain_data.get('questions', [])
            
            for question in questions:
                total_questions_checked += 1
                question_code = question.get('code', '')
                
                # Check if question has additional_guide field with substantial content
                additional_guide = question.get('additional_guide', '')
                if additional_guide and len(additional_guide.strip()) > 10:  # Substantial content
                    questions_with_tooltips += 1
                
                # Check specific sample questions
                if question_code in sample_questions_to_check:
                    sample_questions_found[question_code] = {
                        'has_additional_guide': bool(additional_guide and additional_guide.strip()),
                        'guide_length': len(additional_guide.strip()) if additional_guide else 0,
                        'guide_preview': additional_guide[:100] + '...' if additional_guide and len(additional_guide) > 100 else additional_guide
                    }
        
        # Log results for all questions
        if questions_with_tooltips == total_questions_checked:
            self.log_test("BUG 2: All questions have 'additional_guide' field with substantial content", True)
        else:
            self.log_test("BUG 2: All questions have 'additional_guide' field with substantial content", False,
                        f"Only {questions_with_tooltips}/{total_questions_checked} questions have substantial tooltips")
        
        # Check specific sample questions
        sample_questions_with_tooltips = 0
        for question_code in sample_questions_to_check:
            if question_code in sample_questions_found:
                question_data = sample_questions_found[question_code]
                if question_data['has_additional_guide'] and question_data['guide_length'] > 10:
                    self.log_test(f"BUG 2: {question_code} has meaningful tooltip content", True)
                    sample_questions_with_tooltips += 1
                    print(f"   📝 {question_code} tooltip preview: {question_data['guide_preview'][:50]}...")
                else:
                    self.log_test(f"BUG 2: {question_code} has meaningful tooltip content", False,
                                f"Guide length: {question_data['guide_length']} chars")
            else:
                self.log_test(f"BUG 2: {question_code} found in readiness questions", False, "Question not found")
        
        # Overall sample check
        if sample_questions_with_tooltips >= 5:  # At least 5 of the sample questions should have tooltips
            self.log_test("BUG 2: At least 5 sample questions have meaningful tooltips", True)
        else:
            self.log_test("BUG 2: At least 5 sample questions have meaningful tooltips", False,
                        f"Only {sample_questions_with_tooltips} sample questions have meaningful tooltips")
        
        # Summary of bug fixes
        print("\n📋 BUG FIX SUMMARY")
        print("-" * 40)
        
        bug1_fixed = (
            'status_overview' in status_response and 
            'domain_scores' not in status_response and
            domains_with_correct_structure == total_domains and
            questions_with_correct_structure == total_questions_in_status and
            total_questions_in_status == expected_readiness_questions
        )
        
        bug2_fixed = (
            questions_with_tooltips >= total_questions_checked * 0.8 and  # At least 80% have tooltips
            sample_questions_with_tooltips >= 5
        )
        
        if bug1_fixed:
            self.log_test("🎉 BUG 1 (View All Button Crash) - FIXED", True)
        else:
            self.log_test("❌ BUG 1 (View All Button Crash) - NOT FIXED", False, "Status endpoint structure issues remain")
        
        if bug2_fixed:
            self.log_test("🎉 BUG 2 (Missing Tooltips) - FIXED", True)
        else:
            self.log_test("❌ BUG 2 (Missing Tooltips) - NOT FIXED", False, "Tooltip content issues remain")
        
        return bug1_fixed and bug2_fixed

    def run_tests(self):
        """Run the readiness assessment bug fix tests"""
        print("🚀 Starting AI Readiness Assessment Bug Fix Tests")
        print("=" * 60)
        
        if not self.test_authentication():
            print("❌ Authentication failed - stopping tests")
            return False
        
        result = self.test_readiness_assessment_bug_fixes()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🏁 TEST SUMMARY")
        print("=" * 60)
        print(f"Total tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_run - self.tests_passed}")
        print(f"Success rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        if result:
            print("🎉 Both AI Readiness Assessment bugs have been FIXED!")
        else:
            print("⚠️  Some bugs remain unfixed - check details above")
            
        return result

if __name__ == "__main__":
    tester = ReadinessBugTester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)