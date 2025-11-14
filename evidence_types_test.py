#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class EvidenceTypesAPITester:
    def __init__(self, base_url="https://ai-assessment-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
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
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            
            # Handle JSON responses
            try:
                return success, response.json() if success else response.text
            except:
                return success, response.text

        except Exception as e:
            return False, str(e)

    def test_organisation_questions_data_integrity(self):
        """Test that all 80 Organisation-wide questions have evidence_types field"""
        print("\n📊 Testing Organisation Questions Data Integrity")
        
        # Import the organisation questions data
        try:
            import sys
            sys.path.append('/app/backend')
            from organisation_questions import ORGANISATION_QUESTIONS_DATA
            
            total_questions = len(ORGANISATION_QUESTIONS_DATA)
            
            # Verify 80 questions total
            if total_questions == 80:
                self.log_test("Organisation questions count (80 questions)", True)
            else:
                self.log_test("Organisation questions count (80 questions)", False, f"Found {total_questions} questions")
            
            # Check evidence_types field presence and content
            questions_with_evidence_types = 0
            questions_with_non_empty_evidence_types = 0
            sample_questions_checked = {}
            
            # Sample question codes to verify
            sample_codes = ["GO-01", "AE-02", "AE-05", "RM-01", "DS-01", "FI-01", "GO-08", "PL-01", "CA-01", "RE-01"]
            
            for question_data in ORGANISATION_QUESTIONS_DATA:
                question_code = question_data.get("code", "").strip('"""')
                
                # Check if evidence_types field exists
                if "evidence_types" in question_data:
                    questions_with_evidence_types += 1
                    
                    # Check if evidence_types content is non-empty
                    evidence_types = question_data["evidence_types"]
                    if evidence_types and evidence_types.strip():
                        questions_with_non_empty_evidence_types += 1
                        
                        # Collect sample questions for uniqueness check
                        if question_code in sample_codes:
                            sample_questions_checked[question_code] = evidence_types[:100] + "..." if len(evidence_types) > 100 else evidence_types
            
            # Log results
            if questions_with_evidence_types == total_questions:
                self.log_test("All 80 questions have evidence_types field", True)
            else:
                self.log_test("All 80 questions have evidence_types field", False, 
                            f"Only {questions_with_evidence_types}/{total_questions} questions have evidence_types field")
            
            if questions_with_non_empty_evidence_types == total_questions:
                self.log_test("All 80 questions have non-empty evidence_types content", True)
            else:
                self.log_test("All 80 questions have non-empty evidence_types content", False,
                            f"Only {questions_with_non_empty_evidence_types}/{total_questions} questions have non-empty evidence_types")
            
            # Verify sample questions have unique evidence_types content
            if len(sample_questions_checked) >= 5:  # At least 5 sample questions found
                self.log_test("Sample question codes found for uniqueness check", True)
                
                # Check for uniqueness by comparing content
                unique_contents = set(sample_questions_checked.values())
                if len(unique_contents) == len(sample_questions_checked):
                    self.log_test("Sample questions have unique evidence_types content", True)
                else:
                    self.log_test("Sample questions have unique evidence_types content", False,
                                f"Found {len(unique_contents)} unique contents for {len(sample_questions_checked)} sample questions")
                
                # Log sample evidence_types for verification
                print("   📝 Sample evidence_types content:")
                for code, content in list(sample_questions_checked.items())[:3]:
                    print(f"      {code}: {content}")
            else:
                self.log_test("Sample question codes found for uniqueness check", False,
                            f"Only found {len(sample_questions_checked)} sample questions out of {len(sample_codes)} expected")
            
            return questions_with_evidence_types == total_questions and questions_with_non_empty_evidence_types == total_questions
            
        except ImportError as e:
            self.log_test("Import organisation_questions.py", False, f"Import error: {str(e)}")
            return False
        except Exception as e:
            self.log_test("Organisation questions data integrity test", False, f"Error: {str(e)}")
            return False

    def test_orgwide_assessment_evidence_types_api(self):
        """Test API response includes evidence_types field for Orgwide assessments"""
        print("\n🌐 Testing Orgwide Assessment API Evidence Types")
        
        # Step 1: Login with test credentials
        login_data = {
            "email": "andrew@test.com",
            "password": "password123"
        }
        
        success, response = self.make_request('POST', 'auth/login', login_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("Login with test credentials (andrew@test.com)", True)
        else:
            self.log_test("Login with test credentials (andrew@test.com)", False, str(response))
            return False
        
        # Step 2: Create Orgwide assessment
        assessment_data = {
            "assessment_type": "Orgwide"
        }
        
        success, response = self.make_request('POST', 'assessments', assessment_data)
        if success and 'id' in response:
            orgwide_assessment_id = response['id']
            self.log_test("Create Orgwide assessment", True)
        else:
            self.log_test("Create Orgwide assessment", False, str(response))
            return False
        
        # Step 3: Get assessment questions and verify evidence_types field
        success, response = self.make_request('GET', f'assessments/{orgwide_assessment_id}/questions')
        if not success:
            self.log_test("GET Orgwide assessment questions", False, str(response))
            return False
        
        self.log_test("GET Orgwide assessment questions endpoint", True)
        
        # Verify response structure and evidence_types field
        if not isinstance(response, list):
            self.log_test("Orgwide questions response structure", False, "Response is not a list of domains")
            return False
        
        # Count questions and check evidence_types
        total_questions = 0
        questions_with_evidence_types = 0
        questions_with_evidence_content = 0
        sample_evidence_types = {}
        
        # Sample question codes to verify specific content
        sample_codes = ["AE-02", "AE-05", "CA-01"]
        
        for domain_data in response:
            domain_name = domain_data.get('domain', {}).get('name', 'Unknown')
            questions = domain_data.get('questions', [])
            total_questions += len(questions)
            
            for question in questions:
                question_code = question.get('code', '')
                
                # Check for evidence_types field
                if 'evidence_types' in question:
                    questions_with_evidence_types += 1
                    
                    evidence_types = question['evidence_types']
                    if evidence_types and evidence_types.strip():
                        questions_with_evidence_content += 1
                        
                        # Collect sample questions for content verification
                        if question_code in sample_codes:
                            sample_evidence_types[question_code] = evidence_types
        
        # Verify 80 questions total
        if total_questions == 80:
            self.log_test("Orgwide assessment returns 80 questions", True)
        else:
            self.log_test("Orgwide assessment returns 80 questions", False, f"Found {total_questions} questions")
        
        # Verify evidence_types field presence
        if questions_with_evidence_types == total_questions:
            self.log_test("All Orgwide questions include evidence_types field", True)
        else:
            self.log_test("All Orgwide questions include evidence_types field", False,
                        f"Only {questions_with_evidence_types}/{total_questions} questions have evidence_types field")
        
        # Verify evidence_types content
        if questions_with_evidence_content == total_questions:
            self.log_test("All Orgwide questions have evidence_types content", True)
        else:
            self.log_test("All Orgwide questions have evidence_types content", False,
                        f"Only {questions_with_evidence_content}/{total_questions} questions have evidence_types content")
        
        # Verify evidence_types structure and content
        if sample_evidence_types:
            self.log_test("Sample evidence_types content retrieved", True)
            
            # Check for expected content structure
            valid_structure_count = 0
            for code, content in sample_evidence_types.items():
                if "Key Evidence Types:" in content and "In short:" in content:
                    valid_structure_count += 1
            
            if valid_structure_count == len(sample_evidence_types):
                self.log_test("Evidence_types content has expected structure", True)
            else:
                self.log_test("Evidence_types content has expected structure", False,
                            f"Only {valid_structure_count}/{len(sample_evidence_types)} samples have expected structure")
            
            # Log sample content for verification
            print("   📝 Sample evidence_types content:")
            for code, content in list(sample_evidence_types.items())[:2]:
                print(f"      {code}: {content[:150]}...")
        else:
            self.log_test("Sample evidence_types content retrieved", False, "No sample questions found")
        
        return (questions_with_evidence_types == total_questions and 
                questions_with_evidence_content == total_questions)

    def test_cross_assessment_evidence_types(self):
        """Test evidence_types behavior across different assessment types"""
        print("\n🔄 Testing Cross-Assessment Type Evidence Types")
        
        # Test System Assessment (should not have evidence_types or use static helpContent)
        success, response = self.make_request('POST', 'assessments', {"assessment_type": "System"})
        if success and 'id' in response:
            system_assessment_id = response['id']
            self.log_test("Create System assessment", True)
            
            # Get System assessment questions
            success, system_response = self.make_request('GET', f'assessments/{system_assessment_id}/questions')
            if success:
                self.log_test("GET System assessment questions", True)
                
                # Check that System questions don't have evidence_types or use different structure
                system_has_evidence_types = False
                for domain_data in system_response:
                    questions = domain_data.get('questions', [])
                    for question in questions:
                        if question.get('evidence_types'):
                            system_has_evidence_types = True
                            break
                    if system_has_evidence_types:
                        break
                
                if not system_has_evidence_types:
                    self.log_test("System assessments do not have evidence_types field", True)
                else:
                    self.log_test("System assessments do not have evidence_types field", False, "System questions have evidence_types")
            else:
                self.log_test("GET System assessment questions", False, str(system_response))
        else:
            self.log_test("Create System assessment", False, str(response))
        
        # Test Readiness Assessment (should have evidence_types working)
        success, response = self.make_request('POST', 'assessments', {"assessment_type": "Readiness"})
        if success and 'id' in response:
            readiness_assessment_id = response['id']
            self.log_test("Create Readiness assessment", True)
            
            # Get Readiness assessment questions
            success, readiness_response = self.make_request('GET', f'assessments/{readiness_assessment_id}/questions')
            if success:
                self.log_test("GET Readiness assessment questions", True)
                
                # Check if Readiness questions have additional_guide (equivalent to evidence_types)
                readiness_has_guide = False
                for domain_data in readiness_response:
                    questions = domain_data.get('questions', [])
                    for question in questions:
                        if question.get('additional_guide'):
                            readiness_has_guide = True
                            break
                    if readiness_has_guide:
                        break
                
                if readiness_has_guide:
                    self.log_test("Readiness assessments have additional_guide field", True)
                else:
                    self.log_test("Readiness assessments have additional_guide field", False, "No additional_guide found")
            else:
                self.log_test("GET Readiness assessment questions", False, str(readiness_response))
        else:
            self.log_test("Create Readiness assessment", False, str(response))
        
        # Verify Orgwide assessments have distinct evidence_types content
        success, response = self.make_request('POST', 'assessments', {"assessment_type": "Orgwide"})
        if success and 'id' in response:
            orgwide_assessment_id = response['id']
            
            success, orgwide_response = self.make_request('GET', f'assessments/{orgwide_assessment_id}/questions')
            if success:
                # Verify Orgwide has evidence_types (distinct from other assessment types)
                orgwide_evidence_types_count = 0
                for domain_data in orgwide_response:
                    questions = domain_data.get('questions', [])
                    for question in questions:
                        if question.get('evidence_types'):
                            orgwide_evidence_types_count += 1
                
                if orgwide_evidence_types_count > 0:
                    self.log_test("Orgwide assessments have distinct evidence_types content", True)
                else:
                    self.log_test("Orgwide assessments have distinct evidence_types content", False, "No evidence_types found")
            else:
                self.log_test("Verify Orgwide evidence_types distinctness", False, str(orgwide_response))
        else:
            self.log_test("Create Orgwide assessment for distinctness test", False, str(response))
        
        return True

    def run_evidence_types_tests(self):
        """Run Evidence Types functionality tests"""
        print("🔍 TESTING EVIDENCE TYPES FUNCTIONALITY FOR ORGANISATION-WIDE AI MATURITY ASSESSMENT")
        print("=" * 80)
        
        # Test 1: Backend Data Integrity - Check organisation_questions.py data
        print("\n1️⃣ BACKEND DATA INTEGRITY TESTS")
        self.test_organisation_questions_data_integrity()
        
        # Test 2: Create Orgwide assessment and test API response
        print("\n2️⃣ API RESPONSE TESTS")
        self.test_orgwide_assessment_evidence_types_api()
        
        # Test 3: Cross-Assessment Type Tests
        print("\n3️⃣ CROSS-ASSESSMENT TYPE TESTS")
        self.test_cross_assessment_evidence_types()
        
        # Print summary
        print("\n" + "=" * 80)
        print(f"📊 EVIDENCE TYPES TEST SUMMARY")
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL EVIDENCE TYPES TESTS PASSED!")
        else:
            print("⚠️  Some tests failed - check details above")
            
        return self.tests_passed == self.tests_run

if __name__ == "__main__":
    tester = EvidenceTypesAPITester()
    tester.run_evidence_types_tests()