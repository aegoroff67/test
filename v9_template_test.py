#!/usr/bin/env python3

import requests
import sys
import json
import io
import zipfile
from datetime import datetime

class V9TemplateAPITester:
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

    def setup_test_user_and_assessment(self):
        """Setup test user and complete assessment"""
        print("🔧 Setting up test user and assessment...")
        
        # Create test user
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"v9_test_user_{timestamp}@vciso.one"
        
        signup_data = {
            "name": "vCISO.One Test User",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": "vCISO.One",
            "industry": "Cybersecurity Consulting"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("Test user signup (vCISO.One)", True)
        else:
            self.log_test("Test user signup (vCISO.One)", False, str(response))
            return False

        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if success and 'id' in response:
            self.assessment_id = response['id']
            self.log_test("Assessment creation", True)
        else:
            self.log_test("Assessment creation", False, str(response))
            return False

        # Complete assessment with realistic answers
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            self.log_test("Get questions for completion", False, str(response))
            return False

        # Answer all questions with varied responses
        answer_options = ['IDEAL', 'GOOD', 'BASIC', 'NON_IDEAL']
        question_count = 0
        
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for i, question in enumerate(questions):
                option = answer_options[i % len(answer_options)]
                
                answer_data = {
                    "question_id": question['id'],
                    "option": option,
                    "note": f"V9 test answer for {question.get('code', 'question')}"
                }
                
                success_answer, _ = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
                if success_answer:
                    question_count += 1

        if question_count >= 88:
            self.log_test("Complete assessment (88 questions)", True)
            return True
        else:
            self.log_test("Complete assessment (88 questions)", False, f"Only answered {question_count}")
            return False

    def test_v9_template_docx_generation(self):
        """Test V9 template DOCX generation with text-only heatmap placeholder"""
        print("\n🔍 V9 TEMPLATE DOCX GENERATION TEST")
        print("-" * 60)
        
        # Test DOCX generation endpoint
        url = f"{self.api_url}/assessments/{self.assessment_id}/report"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            response = requests.get(url, headers=headers)
            
            # Check HTTP status
            if response.status_code == 200:
                self.log_test("V9 Template DOCX Generation - HTTP 200 OK", True)
            else:
                self.log_test("V9 Template DOCX Generation - HTTP 200 OK", False, f"Got {response.status_code}")
                return False
            
            # Check MIME type
            content_type = response.headers.get('content-type', '')
            expected_mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            if expected_mime in content_type:
                self.log_test("V9 Template DOCX - Correct MIME Type", True)
            else:
                self.log_test("V9 Template DOCX - Correct MIME Type", False, f"Got {content_type}")
            
            # Check file size (should be substantial, around 35KB as mentioned in review)
            file_size = len(response.content)
            if file_size > 30000:  # 30KB minimum
                self.log_test("V9 Template DOCX - Substantial File Size", True, f"{file_size/1024:.1f}KB")
            else:
                self.log_test("V9 Template DOCX - Substantial File Size", False, f"Only {file_size/1024:.1f}KB")
            
            # Check ZIP structure (DOCX is ZIP-based)
            try:
                docx_zip = zipfile.ZipFile(io.BytesIO(response.content))
                zip_files = docx_zip.namelist()
                
                # Essential DOCX files
                essential_files = ['word/document.xml', '[Content_Types].xml', 'word/_rels/document.xml.rels']
                has_essential = all(f in zip_files for f in essential_files)
                
                if has_essential:
                    self.log_test("V9 Template DOCX - Valid ZIP Structure", True)
                else:
                    missing = [f for f in essential_files if f not in zip_files]
                    self.log_test("V9 Template DOCX - Valid ZIP Structure", False, f"Missing: {missing}")
                
                # Check for heatmap text content (not image files since v9 uses text placeholder)
                document_xml = docx_zip.read('word/document.xml').decode('utf-8', errors='ignore')
                
                # Look for organization name "vCISO.One" as mentioned in review
                if 'vCISO.One' in document_xml or 'vciso' in document_xml.lower():
                    self.log_test("V9 Template - Organization Name Populated", True)
                else:
                    self.log_test("V9 Template - Organization Name Populated", False, "vCISO.One not found in document")
                
                # Check that heatmap placeholder is replaced with text (not {{assets.heatmapUrl}})
                if '{{assets.heatmapUrl}}' not in document_xml:
                    self.log_test("V9 Template - Heatmap Placeholder Replaced", True)
                else:
                    self.log_test("V9 Template - Heatmap Placeholder Replaced", False, "Placeholder still present")
                
                # Check for assessment data population
                if 'Assessment' in document_xml and 'Domain' in document_xml:
                    self.log_test("V9 Template - Assessment Data Populated", True)
                else:
                    self.log_test("V9 Template - Assessment Data Populated", False, "Assessment data not found")
                
                docx_zip.close()
                
            except Exception as e:
                self.log_test("V9 Template DOCX - ZIP Structure Analysis", False, str(e))
            
            return True
            
        except Exception as e:
            self.log_test("V9 Template DOCX Generation", False, str(e))
            return False

    def test_v9_template_pdf_generation(self):
        """Test V9 template PDF generation"""
        print("\n🔍 V9 TEMPLATE PDF GENERATION TEST")
        print("-" * 60)
        
        # Test PDF generation endpoint
        url = f"{self.api_url}/assessments/{self.assessment_id}/report/pdf"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            response = requests.get(url, headers=headers)
            
            # Check HTTP status (might be 503 if LibreOffice issues, but should not be 404)
            if response.status_code == 200:
                self.log_test("V9 Template PDF Generation - HTTP 200 OK", True)
                
                # Check MIME type
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type:
                    self.log_test("V9 Template PDF - Correct MIME Type", True)
                else:
                    self.log_test("V9 Template PDF - Correct MIME Type", False, f"Got {content_type}")
                
                # Check PDF format
                content = response.content
                if content.startswith(b'%PDF'):
                    self.log_test("V9 Template PDF - Valid PDF Format", True)
                    
                    # Check file size
                    file_size = len(content)
                    if file_size > 20000:  # 20KB minimum for PDF
                        self.log_test("V9 Template PDF - Substantial File Size", True, f"{file_size/1024:.1f}KB")
                    else:
                        self.log_test("V9 Template PDF - Substantial File Size", False, f"Only {file_size/1024:.1f}KB")
                else:
                    self.log_test("V9 Template PDF - Valid PDF Format", False, "Not a valid PDF")
                
            elif response.status_code == 503:
                self.log_test("V9 Template PDF Generation - Service Available", False, "PDF conversion temporarily unavailable (503)")
            else:
                self.log_test("V9 Template PDF Generation", False, f"Got {response.status_code}")
            
            return response.status_code in [200, 503]  # 503 is acceptable for PDF conversion issues
            
        except Exception as e:
            self.log_test("V9 Template PDF Generation", False, str(e))
            return False

    def test_v9_template_content_verification(self):
        """Test that V9 template properly populates assessment data"""
        print("\n🔍 V9 TEMPLATE CONTENT VERIFICATION TEST")
        print("-" * 60)
        
        # Get assessment summary to verify data is available
        success, summary = self.make_request('GET', f'assessments/{self.assessment_id}/summary')
        if not success:
            self.log_test("Get Assessment Summary for Content Test", False, str(summary))
            return False
        
        # Verify we have the expected data structure
        required_fields = ['overall_percentage', 'overall_maturity', 'domain_scores']
        missing_fields = [f for f in required_fields if f not in summary]
        
        if not missing_fields:
            self.log_test("Assessment Summary Data Available", True)
            
            # Check domain scores (should be 11 domains)
            domain_scores = summary.get('domain_scores', [])
            if len(domain_scores) == 11:
                self.log_test("V9 Template - 11 Domain Scores Available", True)
            else:
                self.log_test("V9 Template - 11 Domain Scores Available", False, f"Only {len(domain_scores)} domains")
            
            # Check overall score
            overall_percentage = summary.get('overall_percentage', 0)
            if overall_percentage > 0:
                self.log_test("V9 Template - Overall Score Available", True, f"{overall_percentage}%")
            else:
                self.log_test("V9 Template - Overall Score Available", False, "No overall score")
            
            # Check maturity tier
            overall_maturity = summary.get('overall_maturity', '')
            if overall_maturity:
                self.log_test("V9 Template - Maturity Tier Available", True, overall_maturity)
            else:
                self.log_test("V9 Template - Maturity Tier Available", False, "No maturity tier")
            
            return True
        else:
            self.log_test("Assessment Summary Data Available", False, f"Missing: {missing_fields}")
            return False

    def test_v9_template_file_integrity(self):
        """Test V9 template file integrity and Word compatibility"""
        print("\n🔍 V9 TEMPLATE FILE INTEGRITY TEST")
        print("-" * 60)
        
        # Generate DOCX report multiple times to test consistency
        url = f"{self.api_url}/assessments/{self.assessment_id}/report"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            file_sizes = []
            for i in range(3):
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    file_sizes.append(len(response.content))
                else:
                    self.log_test("V9 Template File Integrity", False, f"HTTP {response.status_code}")
                    return False
            
            if len(file_sizes) == 3:
                # Check file size consistency (should be very similar)
                avg_size = sum(file_sizes) / len(file_sizes)
                variance = max(abs(size - avg_size) for size in file_sizes)
                variance_percent = (variance / avg_size) * 100
                
                if variance_percent < 10:  # Less than 10% variance
                    self.log_test("V9 Template - Consistent File Generation", True, f"Variance: {variance_percent:.1f}%")
                else:
                    self.log_test("V9 Template - Consistent File Generation", False, f"High variance: {variance_percent:.1f}%")
            
            # Test ZIP integrity on the last generated file
            try:
                docx_zip = zipfile.ZipFile(io.BytesIO(response.content))
                
                # Test ZIP integrity
                bad_files = docx_zip.testzip()
                if bad_files is None:
                    self.log_test("V9 Template - ZIP Integrity Check", True)
                else:
                    self.log_test("V9 Template - ZIP Integrity Check", False, f"Corrupted files: {bad_files}")
                
                # Check XML well-formedness
                try:
                    document_xml = docx_zip.read('word/document.xml')
                    # Basic XML check - should start with <?xml
                    if document_xml.startswith(b'<?xml'):
                        self.log_test("V9 Template - Document XML Well-formed", True)
                    else:
                        self.log_test("V9 Template - Document XML Well-formed", False, "Invalid XML header")
                except Exception as e:
                    self.log_test("V9 Template - Document XML Well-formed", False, str(e))
                
                docx_zip.close()
                
            except Exception as e:
                self.log_test("V9 Template - ZIP Analysis", False, str(e))
            
            return True
            
        except Exception as e:
            self.log_test("V9 Template File Integrity", False, str(e))
            return False

    def run_v9_template_tests(self):
        """Run all V9 template specific tests"""
        print("🎯 V9 TEMPLATE TESTING FOR AM AI SAFE REPORT GENERATION")
        print("=" * 80)
        print("OBJECTIVE: Test v9 template with text-only heatmap placeholder")
        print("FOCUS: Ensure no corruption and proper content population")
        print("=" * 80)
        
        # Setup
        if not self.setup_test_user_and_assessment():
            print("❌ Setup failed - stopping tests")
            return
        
        # Run V9 template specific tests
        self.test_v9_template_docx_generation()
        self.test_v9_template_pdf_generation()
        self.test_v9_template_content_verification()
        self.test_v9_template_file_integrity()
        
        # Print final summary
        print("\n" + "=" * 80)
        print("🏁 V9 TEMPLATE TESTING COMPLETE")
        print("=" * 80)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL V9 TEMPLATE TESTS PASSED!")
            print("✅ V9 template DOCX generation working correctly")
            print("✅ Text-only heatmap placeholder functioning")
            print("✅ Content population verified")
            print("✅ File integrity confirmed")
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} TESTS FAILED")
            print("❌ Some issues remain with V9 template functionality")

if __name__ == "__main__":
    tester = V9TemplateAPITester()
    tester.run_v9_template_tests()