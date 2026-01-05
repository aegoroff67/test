#!/usr/bin/env python3
"""
Enhanced AM AI SAFE Backend API Testing
Testing the 4 major enhancements:
1. Domain-by-domain question progression
2. Complete explanations from spreadsheet as help_text/context
3. Pre-defined answer options from spreadsheet
4. Simplified assessment status overview with domain grouping
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, List, Any

class EnhancedAPITester:
    def __init__(self, base_url="https://insight-metrics-10.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
        self.tests_run = 0
        self.tests_passed = 0
        self.assessment_id = None
        
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def run_test(self, name: str, test_func, *args, **kwargs):
        """Run a single test and track results"""
        self.tests_run += 1
        self.log(f"🔍 Testing: {name}")
        
        try:
            result = test_func(*args, **kwargs)
            if result:
                self.tests_passed += 1
                self.log(f"✅ PASSED: {name}")
                return True
            else:
                self.log(f"❌ FAILED: {name}")
                return False
        except Exception as e:
            self.log(f"❌ ERROR in {name}: {str(e)}")
            return False
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, expected_status: int = 200) -> tuple:
        """Make HTTP request and return (success, response_data)"""
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
                raise ValueError(f"Unsupported method: {method}")
                
            success = response.status_code == expected_status
            
            if success:
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                self.log(f"Request failed: {method} {endpoint} - Status: {response.status_code}")
                try:
                    error_data = response.json()
                    self.log(f"Error details: {error_data}")
                except:
                    self.log(f"Error text: {response.text}")
                return False, {}
                
        except Exception as e:
            self.log(f"Request exception: {str(e)}")
            return False, {}
    
    def test_authentication(self) -> bool:
        """Test user authentication"""
        # Create unique test user
        timestamp = datetime.now().strftime("%H%M%S")
        test_email = f"test_enhanced_{timestamp}@example.com"
        
        signup_data = {
            "name": f"Test Enhanced User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Test Enhanced Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            return True
        return False
    
    def test_domains_structure(self) -> bool:
        """Test that all 11 domains are properly structured"""
        success, domains = self.make_request('GET', 'domains')
        if not success:
            return False
            
        # Verify we have exactly 11 domains
        if len(domains) != 11:
            self.log(f"Expected 11 domains, got {len(domains)}")
            return False
            
        # Verify domain names match the enhanced set
        expected_domains = [
            "Fairness", "Transparency", "Explainability", "Accountability",
            "Data Integrity", "Reliability", "Security", "Privacy", 
            "Safety", "Inclusivity", "Sustainability"
        ]
        
        domain_names = [d['name'] for d in domains]
        for expected in expected_domains:
            if expected not in domain_names:
                self.log(f"Missing expected domain: {expected}")
                return False
                
        self.log(f"✓ All 11 domains present: {', '.join(domain_names)}")
        return True
    
    def test_questions_structure(self) -> bool:
        """Test that all 88 questions are properly structured with enhancements"""
        success, questions = self.make_request('GET', 'questions')
        if not success:
            return False
            
        # Verify we have exactly 88 questions
        if len(questions) != 88:
            self.log(f"Expected 88 questions, got {len(questions)}")
            return False
            
        # Group questions by domain and verify structure
        domain_questions = {}
        for question in questions:
            domain_id = question['domain_id']
            if domain_id not in domain_questions:
                domain_questions[domain_id] = []
            domain_questions[domain_id].append(question)
        
        # Verify each domain has exactly 8 questions
        for domain_id, q_list in domain_questions.items():
            if len(q_list) != 8:
                self.log(f"Domain {domain_id} has {len(q_list)} questions, expected 8")
                return False
        
        # Test Enhancement 2: Complete explanations as help_text
        questions_with_help = [q for q in questions if q.get('help_text')]
        if len(questions_with_help) < 80:  # Most questions should have help text
            self.log(f"Only {len(questions_with_help)} questions have help_text, expected most of 88")
            return False
            
        # Test Enhancement 3: Pre-defined answers from spreadsheet
        questions_with_predefined = [q for q in questions if q.get('predefined_answers')]
        if len(questions_with_predefined) < 1:  # At least some questions should have predefined answers
            self.log(f"No questions have predefined_answers")
            return False
            
        # Verify question codes follow domain pattern (FA-1, FA-2, etc.)
        all_codes = [q['code'] for q in questions]
        fa_codes = [code for code in all_codes if code.startswith('FA-')]
        tr_codes = [code for code in all_codes if code.startswith('TR-')]
        
        if len(fa_codes) != 8:
            self.log(f"Expected 8 FA codes, got {len(fa_codes)}: {fa_codes}")
            return False
            
        if len(tr_codes) != 8:
            self.log(f"Expected 8 TR codes, got {len(tr_codes)}: {tr_codes}")
            return False
            
        self.log(f"✓ All 88 questions properly structured with enhancements")
        self.log(f"✓ {len(questions_with_help)} questions have help_text context")
        self.log(f"✓ {len(questions_with_predefined)} questions have predefined_answers")
        return True
    
    def test_assessment_creation(self) -> bool:
        """Test assessment creation with enhanced question set"""
        success, response = self.make_request('POST', 'assessments')
        if success and 'id' in response:
            self.assessment_id = response['id']
            self.log(f"✓ Assessment created with ID: {self.assessment_id}")
            return True
        return False
    
    def test_assessment_structure(self) -> bool:
        """Test assessment structure with domain-by-domain progression"""
        if not self.assessment_id:
            return False
            
        success, data = self.make_request('GET', f'assessments/{self.assessment_id}')
        if not success:
            return False
            
        questions = data.get('questions', [])
        domains = data.get('domains', [])
        
        # Verify we get all 88 questions
        if len(questions) != 88:
            self.log(f"Expected 88 questions in assessment, got {len(questions)}")
            return False
            
        # Verify domain-by-domain ordering
        # Questions should be grouped by domain (all FA questions, then all TR questions, etc.)
        current_domain = None
        domain_changes = 0
        
        for question in questions:
            if current_domain != question['domain_id']:
                current_domain = question['domain_id']
                domain_changes += 1
        
        # Should have exactly 11 domain changes (one for each domain)
        if domain_changes != 11:
            self.log(f"Expected 11 domain changes, got {domain_changes}")
            return False
            
        # Test Enhancement 2 & 3: Verify questions have help_text and predefined_answers
        first_question = questions[0]
        if not first_question.get('help_text'):
            self.log(f"First question missing help_text: {first_question['code']}")
            return False
            
        if not first_question.get('predefined_answers'):
            self.log(f"First question missing predefined_answers: {first_question['code']}")
            return False
            
        self.log(f"✓ Assessment structure correct with domain-by-domain progression")
        self.log(f"✓ Questions include help_text and predefined_answers")
        return True
    
    def test_status_endpoint(self) -> bool:
        """Test Enhancement 4: Simplified assessment status overview"""
        if not self.assessment_id:
            return False
            
        success, data = self.make_request('GET', f'assessments/{self.assessment_id}/status')
        if not success:
            return False
            
        # Verify status structure
        required_fields = ['status_overview', 'total_questions', 'answered_questions', 'completion_percentage']
        for field in required_fields:
            if field not in data:
                self.log(f"Missing required field in status: {field}")
                return False
        
        # Verify total questions is 88
        if data['total_questions'] != 88:
            self.log(f"Expected 88 total questions, got {data['total_questions']}")
            return False
            
        # Verify status overview structure
        status_overview = data['status_overview']
        if len(status_overview) != 11:
            self.log(f"Expected 11 domains in status overview, got {len(status_overview)}")
            return False
            
        # Verify each domain has 8 questions
        for domain in status_overview:
            if len(domain['questions']) != 8:
                self.log(f"Domain {domain['domain_name']} has {len(domain['questions'])} questions, expected 8")
                return False
                
            # Verify question structure
            for question in domain['questions']:
                required_q_fields = ['question_id', 'question_code', 'answered']
                for field in required_q_fields:
                    if field not in question:
                        self.log(f"Missing field in question status: {field}")
                        return False
        
        self.log(f"✓ Status endpoint returns proper domain-grouped data")
        self.log(f"✓ All 11 domains with 8 questions each in status overview")
        return True
    
    def test_domain_progression_logic(self) -> bool:
        """Test domain-by-domain progression by answering questions"""
        if not self.assessment_id:
            return False
            
        # Get assessment questions
        success, data = self.make_request('GET', f'assessments/{self.assessment_id}')
        if not success:
            return False
            
        questions = data.get('questions', [])
        
        # Answer first question (should be FA-1)
        first_question = questions[0]
        if not first_question['code'].startswith('FA-'):
            self.log(f"Expected first question to be FA-*, got {first_question['code']}")
            return False
            
        # Use first predefined answer if available
        predefined_answers = first_question.get('predefined_answers', [])
        if not predefined_answers:
            self.log(f"First question has no predefined answers")
            return False
            
        answer_data = {
            "question_id": first_question['id'],
            "option": predefined_answers[0],  # Use first predefined answer
            "note": "Test answer for domain progression"
        }
        
        success, response = self.make_request('PATCH', f'assessments/{self.assessment_id}/answer', answer_data)
        if not success:
            return False
            
        # Verify answer was saved
        if not response.get('saved'):
            self.log(f"Answer was not saved properly")
            return False
            
        self.log(f"✓ Domain progression logic working - answered {first_question['code']}")
        self.log(f"✓ Used predefined answer: {predefined_answers[0][:50]}...")
        return True
    
    def test_complete_workflow(self) -> bool:
        """Test complete enhanced workflow"""
        # Test assessment list
        success, assessments = self.make_request('GET', 'assessments')
        if not success:
            return False
            
        # Find our assessment
        our_assessment = None
        for assessment in assessments:
            if assessment['id'] == self.assessment_id:
                our_assessment = assessment
                break
                
        if not our_assessment:
            self.log(f"Could not find our assessment in list")
            return False
            
        # Verify total questions is 88
        if our_assessment['total_questions'] != 88:
            self.log(f"Assessment shows {our_assessment['total_questions']} total questions, expected 88")
            return False
            
        # Verify progress tracking
        if our_assessment['progress'] != 1:  # We answered 1 question
            self.log(f"Expected progress 1, got {our_assessment['progress']}")
            return False
            
        self.log(f"✓ Complete workflow working with enhanced 88-question system")
        return True
    
    def run_all_tests(self):
        """Run all enhanced feature tests"""
        self.log("🚀 Starting Enhanced AM AI SAFE Backend Testing")
        self.log("=" * 60)
        
        # Test sequence
        tests = [
            ("Authentication", self.test_authentication),
            ("11 Domains Structure", self.test_domains_structure),
            ("88 Questions with Enhancements", self.test_questions_structure),
            ("Assessment Creation", self.test_assessment_creation),
            ("Domain-by-Domain Assessment Structure", self.test_assessment_structure),
            ("Status Endpoint with Domain Grouping", self.test_status_endpoint),
            ("Domain Progression Logic", self.test_domain_progression_logic),
            ("Complete Enhanced Workflow", self.test_complete_workflow),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
            
        # Summary
        self.log("=" * 60)
        self.log(f"📊 TEST SUMMARY")
        self.log(f"Tests Run: {self.tests_run}")
        self.log(f"Tests Passed: {self.tests_passed}")
        self.log(f"Tests Failed: {self.tests_run - self.tests_passed}")
        self.log(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            self.log("🎉 ALL ENHANCED FEATURES WORKING CORRECTLY!")
            return 0
        else:
            self.log("⚠️  Some enhanced features need attention")
            return 1

def main():
    tester = EnhancedAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())