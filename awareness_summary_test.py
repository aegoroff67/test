#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class AwarenessAssessmentSummaryTester:
    def __init__(self, base_url="https://maturityradar.preview.emergentagent.com"):
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

    def test_user_authentication(self):
        """Test user authentication - try superadmin first, then create new user"""
        # Try superadmin credentials first
        login_data = {
            "email": "superadmin@emergentmethods.ai",
            "password": "password123"
        }
        
        success, response = self.make_request('POST', 'auth/login', login_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("User authentication (superadmin)", True)
            return True
        
        # If superadmin fails, create a new test user
        import random
        test_email = f"awareness_test_{random.randint(100000, 999999)}@example.com"
        
        signup_data = {
            "name": f"Awareness Test User {random.randint(100000, 999999)}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Awareness Test Org {random.randint(100000, 999999)}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("User authentication (new test user)", True)
            return True
        else:
            self.log_test("User authentication", False, str(response))
            return False

    def test_awareness_assessment_creation(self):
        """Test creating an Awareness assessment"""
        assessment_data = {
            "assessment_type": "Awareness"
        }
        
        success, response = self.make_request('POST', 'assessments', assessment_data)
        if success and 'id' in response:
            self.awareness_assessment_id = response['id']
            assessment_type = response.get('assessment_type')
            if assessment_type == 'Awareness':
                self.log_test("Awareness assessment creation", True)
                return True
            else:
                self.log_test("Awareness assessment creation", False, f"Expected type 'Awareness', got '{assessment_type}'")
        else:
            self.log_test("Awareness assessment creation", False, str(response))
            return False

    def test_awareness_assessment_questions_structure(self):
        """Test Awareness assessment questions structure"""
        if not self.awareness_assessment_id:
            self.log_test("Awareness questions structure test", False, "No awareness assessment ID")
            return False
            
        success, response = self.make_request('GET', f'assessments/{self.awareness_assessment_id}/questions')
        if not success:
            self.log_test("Awareness assessment questions endpoint", False, str(response))
            return False
            
        # Verify 5 domains for Awareness
        if len(response) == 5:
            self.log_test("Awareness assessment returns 5 domains", True)
        else:
            self.log_test("Awareness assessment returns 5 domains", False, f"Found {len(response)} domains")
            
        # Verify domain names
        expected_domains = [
            "Awareness & Understanding",
            "Leadership & Vision", 
            "Data & Digital Readiness",
            "People & Skills",
            "Governance & Trust Foundations"
        ]
        
        actual_domains = [d.get('domain', {}).get('name') for d in response]
        if set(actual_domains) == set(expected_domains):
            self.log_test("Awareness domains have correct names", True)
        else:
            missing = set(expected_domains) - set(actual_domains)
            self.log_test("Awareness domains have correct names", False, f"Missing: {missing}")
            
        # Count total questions (should be 25)
        total_questions = sum(len(d.get('questions', [])) for d in response)
        if total_questions == 25:
            self.log_test("Awareness assessment has 25 questions", True)
        else:
            self.log_test("Awareness assessment has 25 questions", False, f"Found {total_questions} questions")
            
        # Verify each domain has 5 questions
        all_domains_have_5_questions = True
        for domain_data in response:
            domain_name = domain_data.get('domain', {}).get('name', 'Unknown')
            question_count = len(domain_data.get('questions', []))
            if question_count != 5:
                self.log_test(f"Domain '{domain_name}' has 5 questions", False, f"Found {question_count} questions")
                all_domains_have_5_questions = False
            else:
                self.log_test(f"Domain '{domain_name}' has 5 questions", True)
                
        return len(response) == 5 and total_questions == 25 and all_domains_have_5_questions

    def test_awareness_answer_submission(self):
        """Test submitting answers for Awareness assessment with 1-4 scale"""
        if not self.awareness_assessment_id:
            self.log_test("Awareness answer submission test", False, "No awareness assessment ID")
            return False
            
        # Get questions
        success, response = self.make_request('GET', f'assessments/{self.awareness_assessment_id}/questions')
        if not success or not response:
            self.log_test("Get awareness questions for answer test", False, "No questions available")
            return False
            
        # Test each Awareness answer option with expected scores
        awareness_options = [
            ('EARLY_AWARENESS', 1),
            ('EXPLORING_OPPORTUNITIES', 2),
            ('BUILDING_READINESS', 3),
            ('READY_TO_PROGRESS', 4)
        ]
        
        # Get first question from first domain
        first_domain = response[0] if response else None
        if not first_domain or not first_domain.get('questions'):
            self.log_test("Get awareness questions for answer test", False, "No questions in first domain")
            return False
            
        first_question = first_domain['questions'][0]
        question_id = first_question['id']
        
        for option, expected_score in awareness_options:
            answer_data = {
                "question_id": question_id,
                "option": option,
                "note": f"Test note for {option}"
            }
            
            success, response = self.make_request('POST', f'assessments/{self.awareness_assessment_id}/answer', answer_data)
            if success and response.get('status') == 'success':
                self.log_test(f"Awareness answer option {option} submission", True)
            else:
                self.log_test(f"Awareness answer option {option} submission", False, str(response))
                
        return True

    def test_complete_awareness_assessment(self):
        """Complete an Awareness assessment with varied answers across domains"""
        if not self.awareness_assessment_id:
            self.log_test("Complete awareness assessment test", False, "No awareness assessment ID")
            return False
            
        # Get all questions
        success, response = self.make_request('GET', f'assessments/{self.awareness_assessment_id}/questions')
        if not success or not response:
            self.log_test("Get awareness questions for completion", False, str(response))
            return False
            
        # Create varied answer pattern as specified in review request
        # Domain 1: 2 questions, Domain 2: 3 questions, etc.
        domain_answer_counts = [2, 3, 4, 5, 5]  # Total: 19 questions answered
        awareness_options = ['EARLY_AWARENESS', 'EXPLORING_OPPORTUNITIES', 'BUILDING_READINESS', 'READY_TO_PROGRESS']
        
        answered_count = 0
        for domain_idx, domain_data in enumerate(response):
            questions = domain_data.get('questions', [])
            answers_for_domain = domain_answer_counts[domain_idx] if domain_idx < len(domain_answer_counts) else len(questions)
            
            for q_idx in range(min(answers_for_domain, len(questions))):
                question = questions[q_idx]
                # Vary the answers: use different scores (1,2,3,4)
                option = awareness_options[q_idx % len(awareness_options)]
                
                answer_data = {
                    "question_id": question['id'],
                    "option": option,
                    "note": f"Test answer for domain {domain_idx+1}, question {q_idx+1}"
                }
                
                success, _ = self.make_request('POST', f'assessments/{self.awareness_assessment_id}/answer', answer_data)
                if success:
                    answered_count += 1
        
        self.log_test(f"Answered {answered_count} awareness questions with varied scores", True)
        return answered_count > 0

    def test_awareness_assessment_summary(self):
        """Test Awareness assessment summary endpoint with specific requirements"""
        if not self.awareness_assessment_id:
            self.log_test("Awareness assessment summary test", False, "No awareness assessment ID")
            return False
            
        success, response = self.make_request('GET', f'assessments/{self.awareness_assessment_id}/summary')
        if not success:
            self.log_test("Awareness assessment summary endpoint", False, str(response))
            return False
            
        self.log_test("Awareness assessment summary endpoint accessible", True)
        
        # Verify response structure
        required_fields = ['overall_percentage', 'overall_maturity', 'domain_scores', 'total_questions', 'answered_questions']
        if all(field in response for field in required_fields):
            self.log_test("Awareness summary response structure", True)
        else:
            missing = [f for f in required_fields if f not in response]
            self.log_test("Awareness summary response structure", False, f"Missing: {missing}")
            
        # Verify total_questions = 25
        if response.get('total_questions') == 25:
            self.log_test("Awareness summary total_questions = 25", True)
        else:
            self.log_test("Awareness summary total_questions = 25", False, f"Got {response.get('total_questions')}")
            
        # Verify domain_scores has exactly 5 domains
        domain_scores = response.get('domain_scores', [])
        if len(domain_scores) == 5:
            self.log_test("Awareness summary has 5 domain scores", True)
        else:
            self.log_test("Awareness summary has 5 domain scores", False, f"Got {len(domain_scores)} domains")
            
        # Verify domain names
        expected_domain_names = [
            "Awareness & Understanding",
            "Leadership & Vision",
            "Data & Digital Readiness", 
            "People & Skills",
            "Governance & Trust Foundations"
        ]
        
        actual_domain_names = [d.get('domain_name') for d in domain_scores]
        if set(actual_domain_names) == set(expected_domain_names):
            self.log_test("Awareness summary domain names correct", True)
        else:
            missing = set(expected_domain_names) - set(actual_domain_names)
            self.log_test("Awareness summary domain names correct", False, f"Missing: {missing}")
            
        # Verify each domain has correct structure and max_score calculation
        for domain in domain_scores:
            domain_name = domain.get('domain_name', 'Unknown')
            score = domain.get('score', 0)
            max_score = domain.get('max_score', 0)
            percentage = domain.get('percentage', 0)
            
            # Each domain should have max_score = questions × 4 (5 questions × 4 = 20)
            if max_score == 20:
                self.log_test(f"Domain '{domain_name}' max_score = 20 (5×4)", True)
            else:
                self.log_test(f"Domain '{domain_name}' max_score = 20 (5×4)", False, f"Got {max_score}")
                
            # Verify percentage calculation
            expected_percentage = (score / max_score * 100) if max_score > 0 else 0
            if abs(percentage - expected_percentage) < 0.1:
                self.log_test(f"Domain '{domain_name}' percentage calculation correct", True)
            else:
                self.log_test(f"Domain '{domain_name}' percentage calculation correct", False, 
                            f"Expected {expected_percentage:.1f}%, got {percentage:.1f}%")
        
        # Verify overall_percentage calculation (total_score / (25 × 4) × 100)
        total_score = sum(d.get('score', 0) for d in domain_scores)
        expected_overall = (total_score / (25 * 4) * 100) if total_score > 0 else 0
        actual_overall = response.get('overall_percentage', 0)
        
        if abs(actual_overall - expected_overall) < 0.1:
            self.log_test("Awareness overall_percentage calculation correct", True)
        else:
            self.log_test("Awareness overall_percentage calculation correct", False,
                        f"Expected {expected_overall:.1f}%, got {actual_overall:.1f}%")
        
        return True

    def test_awareness_maturity_tiers(self):
        """Test Awareness-specific maturity tier assignment"""
        if not self.awareness_assessment_id:
            self.log_test("Awareness maturity tiers test", False, "No awareness assessment ID")
            return False
            
        success, response = self.make_request('GET', f'assessments/{self.awareness_assessment_id}/summary')
        if not success:
            self.log_test("Get awareness summary for maturity test", False, str(response))
            return False
            
        overall_percentage = response.get('overall_percentage', 0)
        overall_maturity = response.get('overall_maturity', '')
        
        # Test Awareness-specific thresholds
        if overall_percentage >= 71:
            expected_maturity = "Established"
        elif overall_percentage >= 41:
            expected_maturity = "Developing"
        else:
            expected_maturity = "Foundational"
            
        if overall_maturity == expected_maturity:
            self.log_test(f"Awareness maturity tier correct ({overall_percentage:.1f}% → {expected_maturity})", True)
        else:
            self.log_test(f"Awareness maturity tier correct ({overall_percentage:.1f}% → {expected_maturity})", False,
                        f"Expected '{expected_maturity}', got '{overall_maturity}'")
            
        # Verify it's using Awareness tiers (not System tiers)
        valid_awareness_tiers = ["Foundational", "Developing", "Established"]
        if overall_maturity in valid_awareness_tiers:
            self.log_test("Uses Awareness maturity tiers (not System tiers)", True)
        else:
            self.log_test("Uses Awareness maturity tiers (not System tiers)", False,
                        f"Got '{overall_maturity}', expected one of {valid_awareness_tiers}")
            
        return overall_maturity == expected_maturity

    def test_system_vs_awareness_comparison(self):
        """Test that System and Awareness assessments work independently"""
        # Create a System assessment
        success, response = self.make_request('POST', 'assessments', {"assessment_type": "System"})
        if not success:
            self.log_test("Create System assessment for comparison", False, str(response))
            return False
            
        system_assessment_id = response['id']
        self.log_test("Create System assessment for comparison", True)
        
        # Get System assessment summary (should work even if incomplete)
        success, system_response = self.make_request('GET', f'assessments/{system_assessment_id}/summary')
        if success:
            self.log_test("System assessment summary still works", True)
            
            # Verify System assessment characteristics
            system_domains = system_response.get('domain_scores', [])
            system_total_questions = system_response.get('total_questions', 0)
            
            if len(system_domains) == 11:
                self.log_test("System assessment has 11 domains", True)
            else:
                self.log_test("System assessment has 11 domains", False, f"Got {len(system_domains)} domains")
                
            if system_total_questions == 88:
                self.log_test("System assessment has 88 questions", True)
            else:
                self.log_test("System assessment has 88 questions", False, f"Got {system_total_questions} questions")
                
        else:
            self.log_test("System assessment summary still works", False, str(system_response))
            
        # Compare with Awareness assessment
        if self.awareness_assessment_id:
            success, awareness_response = self.make_request('GET', f'assessments/{self.awareness_assessment_id}/summary')
            if success:
                awareness_domains = awareness_response.get('domain_scores', [])
                awareness_total_questions = awareness_response.get('total_questions', 0)
                
                # Verify they're different
                if len(awareness_domains) == 5 and len(system_domains) == 11:
                    self.log_test("System (11) and Awareness (5) domains are different", True)
                else:
                    self.log_test("System (11) and Awareness (5) domains are different", False,
                                f"System: {len(system_domains)}, Awareness: {len(awareness_domains)}")
                    
                if awareness_total_questions == 25 and system_total_questions == 88:
                    self.log_test("System (88) and Awareness (25) questions are different", True)
                else:
                    self.log_test("System (88) and Awareness (25) questions are different", False,
                                f"System: {system_total_questions}, Awareness: {awareness_total_questions}")
                    
        return True

    def test_awareness_edge_cases(self):
        """Test edge cases for Awareness assessment"""
        # Test 1: All minimum scores (all 1s)
        success, response = self.make_request('POST', 'assessments', {"assessment_type": "Awareness"})
        if success:
            min_assessment_id = response['id']
            
            success, questions_response = self.make_request('GET', f'assessments/{min_assessment_id}/questions')
            if success:
                # Answer all questions with minimum score (EARLY_AWARENESS = 1)
                for domain_data in questions_response:
                    for question in domain_data.get('questions', []):
                        answer_data = {
                            "question_id": question['id'],
                            "option": "EARLY_AWARENESS",
                            "note": "Minimum score test"
                        }
                        self.make_request('POST', f'assessments/{min_assessment_id}/answer', answer_data)
                        
                # Test summary
                success, summary_response = self.make_request('GET', f'assessments/{min_assessment_id}/summary')
                if success:
                    overall_percentage = summary_response.get('overall_percentage', 0)
                    overall_maturity = summary_response.get('overall_maturity', '')
                    
                    # With all 1s: total_score = 25, max_score = 100, percentage = 25%
                    expected_percentage = 25.0
                    if abs(overall_percentage - expected_percentage) < 0.1:
                        self.log_test("All minimum scores calculation (25%)", True)
                    else:
                        self.log_test("All minimum scores calculation (25%)", False,
                                    f"Expected {expected_percentage}%, got {overall_percentage}%")
                        
                    if overall_maturity == "Foundational":
                        self.log_test("All minimum scores maturity (Foundational)", True)
                    else:
                        self.log_test("All minimum scores maturity (Foundational)", False,
                                    f"Expected 'Foundational', got '{overall_maturity}'")
        
        # Test 2: All maximum scores (all 4s)
        success, response = self.make_request('POST', 'assessments', {"assessment_type": "Awareness"})
        if success:
            max_assessment_id = response['id']
            
            success, questions_response = self.make_request('GET', f'assessments/{max_assessment_id}/questions')
            if success:
                # Answer all questions with maximum score (READY_TO_PROGRESS = 4)
                for domain_data in questions_response:
                    for question in domain_data.get('questions', []):
                        answer_data = {
                            "question_id": question['id'],
                            "option": "READY_TO_PROGRESS",
                            "note": "Maximum score test"
                        }
                        self.make_request('POST', f'assessments/{max_assessment_id}/answer', answer_data)
                        
                # Test summary
                success, summary_response = self.make_request('GET', f'assessments/{max_assessment_id}/summary')
                if success:
                    overall_percentage = summary_response.get('overall_percentage', 0)
                    overall_maturity = summary_response.get('overall_maturity', '')
                    
                    # With all 4s: total_score = 100, max_score = 100, percentage = 100%
                    expected_percentage = 100.0
                    if abs(overall_percentage - expected_percentage) < 0.1:
                        self.log_test("All maximum scores calculation (100%)", True)
                    else:
                        self.log_test("All maximum scores calculation (100%)", False,
                                    f"Expected {expected_percentage}%, got {overall_percentage}%")
                        
                    if overall_maturity == "Established":
                        self.log_test("All maximum scores maturity (Established)", True)
                    else:
                        self.log_test("All maximum scores maturity (Established)", False,
                                    f"Expected 'Established', got '{overall_maturity}'")
        
        return True

    def test_domain_score_calculations_detailed(self):
        """Test detailed domain score calculations as specified in review request"""
        # Create assessment with specific answer pattern
        success, response = self.make_request('POST', 'assessments', {"assessment_type": "Awareness"})
        if not success:
            self.log_test("Create assessment for detailed score test", False, str(response))
            return False
            
        calc_assessment_id = response['id']
        
        # Get questions
        success, questions_response = self.make_request('GET', f'assessments/{calc_assessment_id}/questions')
        if not success:
            self.log_test("Get questions for detailed score test", False, str(questions_response))
            return False
            
        # Answer first domain with pattern [1, 2, 3, 4, 4] as specified in review request
        first_domain = questions_response[0]
        questions = first_domain.get('questions', [])
        answer_options = ['EARLY_AWARENESS', 'EXPLORING_OPPORTUNITIES', 'BUILDING_READINESS', 'READY_TO_PROGRESS', 'READY_TO_PROGRESS']
        
        for i, question in enumerate(questions[:5]):
            answer_data = {
                "question_id": question['id'],
                "option": answer_options[i],
                "note": f"Detailed calc test answer {i+1}"
            }
            self.make_request('POST', f'assessments/{calc_assessment_id}/answer', answer_data)
            
        # Get summary and verify calculations
        success, summary_response = self.make_request('GET', f'assessments/{calc_assessment_id}/summary')
        if success:
            domain_scores = summary_response.get('domain_scores', [])
            if domain_scores:
                first_domain_score = domain_scores[0]
                score = first_domain_score.get('score', 0)
                max_score = first_domain_score.get('max_score', 0)
                percentage = first_domain_score.get('percentage', 0)
                
                # Expected: score = 1+2+3+4+4 = 14, max_score = 5×4 = 20, percentage = 70.0
                expected_score = 14
                expected_max_score = 20
                expected_percentage = 70.0
                
                if score == expected_score:
                    self.log_test("Domain score calculation (1+2+3+4+4=14)", True)
                else:
                    self.log_test("Domain score calculation (1+2+3+4+4=14)", False, f"Expected {expected_score}, got {score}")
                    
                if max_score == expected_max_score:
                    self.log_test("Domain max_score calculation (5×4=20)", True)
                else:
                    self.log_test("Domain max_score calculation (5×4=20)", False, f"Expected {expected_max_score}, got {max_score}")
                    
                if abs(percentage - expected_percentage) < 0.1:
                    self.log_test("Domain percentage calculation (14/20=70%)", True)
                else:
                    self.log_test("Domain percentage calculation (14/20=70%)", False, f"Expected {expected_percentage}%, got {percentage}%")
                    
        return True

    def run_all_tests(self):
        """Run comprehensive Awareness Assessment Results Summary tests as per review request"""
        print("\n🔥 AI AWARENESS & FOUNDATIONS ASSESSMENT RESULTS SUMMARY TESTING")
        print("=" * 80)
        print("Testing the AI Awareness & Foundations Assessment Results Summary feature")
        print("Focus: Backend endpoint testing with 5 domains, 25 questions, 1-4 scoring scale")
        print("-" * 80)
        
        # Authentication
        if not self.test_user_authentication():
            print("❌ Authentication failed - stopping tests")
            return False
        
        # Test 1: Create Awareness Assessment
        if self.test_awareness_assessment_creation():
            # Test 2: Verify Questions Structure (5 domains, 25 questions)
            self.test_awareness_assessment_questions_structure()
            
            # Test 3: Test Answer Submission (1-4 scale)
            self.test_awareness_answer_submission()
            
            # Test 4: Complete Assessment with Varied Answers
            self.test_complete_awareness_assessment()
            
            # Test 5: Test Summary Endpoint Structure
            self.test_awareness_assessment_summary()
            
            # Test 6: Test Maturity Tier Assignment
            self.test_awareness_maturity_tiers()
            
            # Test 7: Test Detailed Domain Score Calculations
            self.test_domain_score_calculations_detailed()
        
        # Test 8: Compare System vs Awareness Assessments
        self.test_system_vs_awareness_comparison()
        
        # Test 9: Test Edge Cases
        self.test_awareness_edge_cases()
        
        print(f"\n📊 Awareness Assessment Results Summary Tests Complete")
        print(f"Tests Run: {self.tests_run} | Passed: {self.tests_passed} | Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        return self.tests_passed == self.tests_run

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

if __name__ == "__main__":
    tester = AwarenessAssessmentSummaryTester()
    
    # Run the specific Awareness Assessment Results Summary tests
    success = tester.run_all_tests()
    
    # Print final summary
    tester.print_summary()
    
    if success:
        print("\n🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        sys.exit(1)