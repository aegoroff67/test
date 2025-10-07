#!/usr/bin/env python3

import requests
import sys
import json
import subprocess
from datetime import datetime

class ReportGenerationTester:
    def __init__(self, base_url="https://reportgen-5.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
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
            return success, response.json() if success else response.text

        except Exception as e:
            return False, str(e)

    def setup_user_and_assessment(self):
        """Setup user and complete assessment for report testing"""
        print("🔧 Setting up user and assessment...")
        
        # Create user
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"report_test_{timestamp}@example.com"
        
        signup_data = {
            "name": f"Report Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Report Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("User signup and authentication", True)
        else:
            self.log_test("User signup and authentication", False, str(response))
            return False

        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if success and 'id' in response:
            self.assessment_id = response['id']
            self.log_test("Assessment creation", True)
        else:
            self.log_test("Assessment creation", False, str(response))
            return False

        # Get questions and answer them all
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            self.log_test("Get questions", False, str(response))
            return False

        # Answer all questions with varied responses
        all_questions = []
        for domain_data in response:
            questions = domain_data.get('questions', [])
            all_questions.extend(questions)
        
        answer_options = ['IDEAL', 'GOOD', 'BASIC', 'NON_IDEAL']
        
        for i, question in enumerate(all_questions):
            option = answer_options[i % len(answer_options)]
            answer_data = {
                "question_id": question['id'],
                "option": option,
                "note": f"Test answer {i+1}"
            }
            
            success, _ = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
            if not success:
                self.log_test(f"Answer question {i+1}", False, "Failed to submit answer")
                return False
        
        self.log_test(f"Answered all {len(all_questions)} questions", True)

        # Submit assessment
        success, _ = self.make_request('POST', f'assessments/{self.assessment_id}/submit')
        if success:
            self.log_test("Submit assessment", True)
            return True
        else:
            self.log_test("Submit assessment", False, "Failed to submit")
            return False

    def test_docx_report_generation(self):
        """Test DOCX report generation after string/int fixes"""
        print("\n📄 Testing DOCX Report Generation...")
        
        url = f"{self.api_url}/assessments/{self.assessment_id}/report"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            response = requests.get(url, headers=headers, timeout=60)
            
            if response.status_code == 200:
                self.log_test("DOCX Report Generation Returns 200 OK", True)
                
                # Check MIME type
                content_type = response.headers.get('content-type', '')
                expected_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                if expected_type in content_type:
                    self.log_test("DOCX Report Has Correct MIME Type", True)
                else:
                    self.log_test("DOCX Report Has Correct MIME Type", False, f"Got: {content_type}")
                
                # Check file size (should be substantial)
                file_size = len(response.content)
                if file_size > 100000:  # > 100KB
                    self.log_test("DOCX Report Has Substantial File Size", True, f"Size: {file_size:,} bytes")
                else:
                    self.log_test("DOCX Report Has Substantial File Size", False, f"Size: {file_size:,} bytes")
                
                # Check ZIP structure (DOCX is ZIP-based)
                if response.content.startswith(b'PK'):
                    self.log_test("DOCX Report Has Valid ZIP Structure", True)
                else:
                    self.log_test("DOCX Report Has Valid ZIP Structure", False, "Not a valid ZIP file")
                
                # Check download headers
                content_disposition = response.headers.get('content-disposition', '')
                if 'attachment' in content_disposition:
                    self.log_test("DOCX Report Has Download Headers", True)
                else:
                    self.log_test("DOCX Report Has Download Headers", False, f"Got: {content_disposition}")
                    
                return True
                    
            else:
                self.log_test("DOCX Report Generation Returns 200 OK", False, f"Status: {response.status_code}")
                print(f"Response body: {response.text[:500]}")
                return False
                
        except Exception as e:
            self.log_test("DOCX Report Generation", False, f"Exception: {str(e)}")
            return False

    def test_pdf_report_generation(self):
        """Test PDF report generation after string/int fixes"""
        print("\n📄 Testing PDF Report Generation...")
        
        url = f"{self.api_url}/assessments/{self.assessment_id}/report/pdf"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            response = requests.get(url, headers=headers, timeout=60)
            
            if response.status_code == 200:
                self.log_test("PDF Report Generation Returns 200 OK", True)
                
                # Check MIME type
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type:
                    self.log_test("PDF Report Has Correct MIME Type", True)
                else:
                    self.log_test("PDF Report Has Correct MIME Type", False, f"Got: {content_type}")
                
                # Check file size
                file_size = len(response.content)
                if file_size > 100000:  # > 100KB
                    self.log_test("PDF Report Has Substantial File Size", True, f"Size: {file_size:,} bytes")
                else:
                    self.log_test("PDF Report Has Substantial File Size", False, f"Size: {file_size:,} bytes")
                
                # Check PDF structure
                if response.content.startswith(b'%PDF'):
                    self.log_test("PDF Report Has Valid PDF Header", True)
                else:
                    self.log_test("PDF Report Has Valid PDF Header", False, "Missing %PDF header")
                
                # Check PDF end marker
                if b'%%EOF' in response.content:
                    self.log_test("PDF Report Has Valid End Marker", True)
                else:
                    self.log_test("PDF Report Has Valid End Marker", False, "Missing %%EOF marker")
                    
                return True
                    
            else:
                self.log_test("PDF Report Generation Returns 200 OK", False, f"Status: {response.status_code}")
                print(f"Response body: {response.text[:500]}")
                return False
                
        except Exception as e:
            self.log_test("PDF Report Generation", False, f"Exception: {str(e)}")
            return False

    def check_backend_logs_for_errors(self):
        """Check backend logs for string/int comparison errors"""
        print("\n🔍 Checking Backend Logs for String/Int Comparison Errors...")
        
        try:
            result = subprocess.run(['tail', '-n', '50', '/var/log/supervisor/backend.err.log'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                log_content = result.stdout
                
                error_patterns = [
                    "'>=' not supported between instances of 'str' and 'int'",
                    "'<=' not supported between instances of 'str' and 'int'",
                    "'>' not supported between instances of 'str' and 'int'",
                    "'<' not supported between instances of 'str' and 'int'",
                    "TypeError: unsupported operand type(s)",
                    "can't compare str and int"
                ]
                
                errors_found = []
                for pattern in error_patterns:
                    if pattern in log_content:
                        errors_found.append(pattern)
                
                if not errors_found:
                    self.log_test("No String/Int Comparison Errors in Backend Logs", True)
                else:
                    self.log_test("No String/Int Comparison Errors in Backend Logs", False, f"Found: {errors_found}")
                    print("Recent backend log content:")
                    print(log_content[-1000:])  # Show last 1000 chars
                    
            else:
                self.log_test("Backend Log Check", False, "Could not read backend logs")
                
        except Exception as e:
            self.log_test("Backend Log Check", False, f"Exception: {str(e)}")

    def run_focused_tests(self):
        """Run focused report generation tests"""
        print("🚀 FOCUSED REPORT GENERATION TESTING AFTER STRING/INT FIXES")
        print("=" * 70)
        print("OBJECTIVE: Verify that string/integer comparison fixes have resolved file corruption")
        print("KEY FIXES TESTED:")
        print("1. _calculate_tier method handles string inputs")
        print("2. _generate_key_findings method converts score strings to floats")
        print("3. Template processing works without type errors")
        print("=" * 70)
        
        # Setup
        if not self.setup_user_and_assessment():
            print("❌ Setup failed - stopping tests")
            return
        
        # Test report generation
        docx_success = self.test_docx_report_generation()
        pdf_success = self.test_pdf_report_generation()
        
        # Check logs
        self.check_backend_logs_for_errors()
        
        # Results
        print("\n" + "=" * 70)
        print(f"🏁 TESTING COMPLETE")
        print(f"📊 Results: {self.tests_passed}/{self.tests_run} tests passed ({(self.tests_passed/self.tests_run*100):.1f}%)")
        
        if docx_success and pdf_success:
            print("✅ CRITICAL SUCCESS: Both DOCX and PDF generation working without corruption!")
        elif docx_success:
            print("⚠️  PARTIAL SUCCESS: DOCX generation working, PDF needs attention")
        else:
            print("❌ CRITICAL FAILURE: Report generation still has issues")

if __name__ == "__main__":
    tester = ReportGenerationTester()
    tester.run_focused_tests()