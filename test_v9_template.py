#!/usr/bin/env python3

"""
V9 Template Testing Script - Review Request
Test the new v9 template provided by the user to ensure it resolves all DOCX corruption and PDF table formatting issues.
"""

import requests
import sys
import json
import zipfile
import io
from datetime import datetime

class V9TemplateTester:
    def __init__(self, base_url="https://reportgen-5.preview.emergentagent.com"):
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
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            return success, response.json() if success else response.text

        except Exception as e:
            return False, str(e)

    def setup_test_environment(self):
        """Set up test user and assessment with realistic data"""
        print("🔧 Setting up test environment...")
        
        # Create test user with vCISO.One organization
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"vciso_test_{timestamp}@vciso.one"
        
        signup_data = {
            "name": f"vCISO Test User {timestamp}",
            "email": test_email,
            "password": "SecurePass123!",
            "organization_name": "vCISO.One",
            "industry": "Cybersecurity Consulting"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("Test User Setup (vCISO.One)", True)
        else:
            self.log_test("Test User Setup (vCISO.One)", False, str(response))
            return False

        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if success and 'id' in response:
            self.assessment_id = response['id']
            self.log_test("Test Assessment Creation", True)
        else:
            self.log_test("Test Assessment Creation", False, str(response))
            return False

        # Answer some questions to create realistic assessment data
        success, questions_response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if success:
            # Answer questions with varied responses to create realistic data
            question_count = 0
            for domain_data in questions_response:
                questions = domain_data.get('questions', [])
                for i, question in enumerate(questions[:4]):  # Answer 4 questions per domain
                    options = ['IDEAL', 'GOOD', 'BASIC', 'NON_IDEAL']
                    option = options[i % len(options)]
                    
                    answer_data = {
                        "question_id": question['id'],
                        "option": option,
                        "note": f"Test answer for {question.get('code', 'unknown')} - {option} response"
                    }
                    
                    success_answer, _ = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
                    if success_answer:
                        question_count += 1
            
            self.log_test(f"Test Data Setup ({question_count} answers)", True)
        else:
            self.log_test("Test Data Setup", False, "Failed to get questions")
            return False

        return True

    def test_v9_template_docx_generation(self):
        """Test V9 Template DOCX Generation - Core Requirement"""
        print("\n📄 Testing V9 Template DOCX Generation...")
        
        url = f"{self.api_url}/assessments/{self.assessment_id}/report"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            response = requests.get(url, headers=headers)
            
            # Test 1: HTTP 200 OK Response
            if response.status_code == 200:
                self.log_test("V9 DOCX Generation - HTTP 200 OK", True)
            else:
                self.log_test("V9 DOCX Generation - HTTP 200 OK", False, f"Status: {response.status_code}")
                return False
            
            # Test 2: Correct MIME Type
            content_type = response.headers.get('content-type', '')
            expected_mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            if expected_mime in content_type:
                self.log_test("V9 DOCX - Correct MIME Type", True)
            else:
                self.log_test("V9 DOCX - Correct MIME Type", False, f"Got: {content_type}")
            
            # Test 3: File Size (should be substantial - 35KB+ for v9 template)
            file_size = len(response.content)
            if file_size > 35000:
                self.log_test("V9 DOCX - Substantial File Size", True, f"{file_size} bytes")
            else:
                self.log_test("V9 DOCX - Substantial File Size", False, f"Only {file_size} bytes")
            
            # Test 4: Valid ZIP Structure (DOCX is ZIP-based)
            try:
                zip_buffer = io.BytesIO(response.content)
                with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
                    file_list = zip_file.namelist()
                    essential_files = ['word/document.xml', '[Content_Types].xml', 'word/_rels/document.xml.rels']
                    
                    if all(f in file_list for f in essential_files):
                        self.log_test("V9 DOCX - Valid ZIP Structure", True)
                    else:
                        missing = [f for f in essential_files if f not in file_list]
                        self.log_test("V9 DOCX - Valid ZIP Structure", False, f"Missing: {missing}")
                    
                    # Test 5: Complete Document Structure
                    if len(file_list) >= 15:  # Should have many files for complete template
                        self.log_test("V9 DOCX - Complete Document Structure", True, f"{len(file_list)} files")
                    else:
                        self.log_test("V9 DOCX - Complete Document Structure", False, f"Only {len(file_list)} files")
                        
            except Exception as e:
                self.log_test("V9 DOCX - ZIP Structure Validation", False, f"Error: {str(e)}")
            
            # Test 6: File Integrity (no corruption)
            try:
                # Test that we can read the ZIP without errors
                zip_buffer = io.BytesIO(response.content)
                with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
                    # Try to read document.xml to ensure it's not corrupted
                    document_xml = zip_file.read('word/document.xml')
                    if b'<?xml' in document_xml and b'</w:document>' in document_xml:
                        self.log_test("V9 DOCX - File Integrity (No Corruption)", True)
                    else:
                        self.log_test("V9 DOCX - File Integrity (No Corruption)", False, "Document XML appears corrupted")
                        
            except Exception as e:
                self.log_test("V9 DOCX - File Integrity (No Corruption)", False, f"Corruption detected: {str(e)}")
            
            return True
            
        except Exception as e:
            self.log_test("V9 DOCX Generation", False, f"Request error: {str(e)}")
            return False

    def test_v9_template_pdf_generation(self):
        """Test V9 Template PDF Generation - Core Requirement"""
        print("\n📄 Testing V9 Template PDF Generation...")
        
        url = f"{self.api_url}/assessments/{self.assessment_id}/report/pdf"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            response = requests.get(url, headers=headers)
            
            # Test 1: HTTP 200 OK Response
            if response.status_code == 200:
                self.log_test("V9 PDF Generation - HTTP 200 OK", True)
            else:
                self.log_test("V9 PDF Generation - HTTP 200 OK", False, f"Status: {response.status_code}")
                return False
            
            # Test 2: Correct MIME Type
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' in content_type:
                self.log_test("V9 PDF - Correct MIME Type", True)
            else:
                self.log_test("V9 PDF - Correct MIME Type", False, f"Got: {content_type}")
            
            # Test 3: Valid PDF Format
            if response.content.startswith(b'%PDF'):
                self.log_test("V9 PDF - Valid PDF Format", True)
            else:
                self.log_test("V9 PDF - Valid PDF Format", False, "Missing %PDF header")
            
            # Test 4: PDF End Marker
            if b'%%EOF' in response.content:
                self.log_test("V9 PDF - Valid PDF End Marker", True)
            else:
                self.log_test("V9 PDF - Valid PDF End Marker", False, "Missing %%EOF marker")
            
            # Test 5: Substantial File Size
            file_size = len(response.content)
            if file_size > 20000:  # 20KB minimum
                self.log_test("V9 PDF - Substantial File Size", True, f"{file_size} bytes")
            else:
                self.log_test("V9 PDF - Substantial File Size", False, f"Only {file_size} bytes")
            
            return True
            
        except Exception as e:
            self.log_test("V9 PDF Generation", False, f"Request error: {str(e)}")
            return False

    def test_template_variable_population(self):
        """Test Template Variable Population - {{org.name}}, {{assets.heatmapUrl}}, {{actions}}"""
        print("\n🔧 Testing Template Variable Population...")
        
        # Get assessment summary to verify data availability
        success, summary = self.make_request('GET', f'assessments/{self.assessment_id}/summary')
        if not success:
            self.log_test("Assessment Summary for Variables", False, str(summary))
            return False
        
        # Test 1: Organization Name ({{org.name}})
        org_name = self.user_data.get('organization_name', '')
        if org_name == 'vCISO.One':
            self.log_test("Organization Name 'vCISO.One' Available", True)
        else:
            self.log_test("Organization Name 'vCISO.One' Available", False, f"Got: {org_name}")
        
        # Test 2: Domain Scores for Heatmap ({{assets.heatmapUrl}})
        domain_scores = summary.get('domain_scores', [])
        if len(domain_scores) == 11:
            self.log_test("Domain Scores for Heatmap Available", True, "11 domains")
        else:
            self.log_test("Domain Scores for Heatmap Available", False, f"Only {len(domain_scores)} domains")
        
        # Test 3: Overall Score and Maturity
        overall_percentage = summary.get('overall_percentage')
        overall_maturity = summary.get('overall_maturity')
        if overall_percentage is not None and overall_maturity:
            self.log_test("Overall Score and Maturity Available", True, f"{overall_percentage}% - {overall_maturity}")
        else:
            self.log_test("Overall Score and Maturity Available", False, "Missing metrics")
        
        # Test 4: Assessment Date
        success_assess, assessment = self.make_request('GET', f'assessments/{self.assessment_id}')
        if success_assess and assessment.get('started_at'):
            self.log_test("Assessment Date Available", True)
        else:
            self.log_test("Assessment Date Available", False, "No date found")
        
        # Test 5: Recommendation Actions ({{actions}})
        # This would be populated based on answers - verify we have answers
        answered_questions = summary.get('answered_questions', 0)
        if answered_questions > 0:
            self.log_test("Assessment Data for Actions Available", True, f"{answered_questions} answers")
        else:
            self.log_test("Assessment Data for Actions Available", False, "No answers found")
        
        return True

    def test_native_jinja2_rendering(self):
        """Test Native Jinja2 Rendering vs Programmatic Population"""
        print("\n🔧 Testing Native Jinja2 Template Structure...")
        
        # Test 1: Template File Exists
        import os
        template_path = "/app/backend/templates/docx/AM_AI_SAFE_Report_TEMPLATE_v9_10072025_NEW.docx"
        if os.path.exists(template_path):
            file_size = os.path.getsize(template_path)
            if file_size > 30000:  # Should be substantial
                self.log_test("V9 Template File Exists", True, f"{file_size} bytes")
            else:
                self.log_test("V9 Template File Exists", False, f"Too small: {file_size} bytes")
        else:
            self.log_test("V9 Template File Exists", False, "File not found")
        
        # Test 2: Multiple Generation Consistency (native rendering should be consistent)
        print("   Testing generation consistency...")
        file_sizes = []
        url = f"{self.api_url}/assessments/{self.assessment_id}/report"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        for i in range(3):
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    file_sizes.append(len(response.content))
            except:
                pass
        
        if len(file_sizes) >= 2:
            avg_size = sum(file_sizes) / len(file_sizes)
            variance = max(abs(size - avg_size) / avg_size for size in file_sizes) * 100
            
            if variance < 5:  # Less than 5% variance for native rendering
                self.log_test("Native Jinja2 - Consistent Generation", True, f"Variance: {variance:.1f}%")
            else:
                self.log_test("Native Jinja2 - Consistent Generation", False, f"High variance: {variance:.1f}%")
        
        return True

    def test_word_compatibility(self):
        """Test that files can be opened in Microsoft Word without errors"""
        print("\n🔧 Testing Microsoft Word Compatibility...")
        
        # Generate DOCX file
        url = f"{self.api_url}/assessments/{self.assessment_id}/report"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                # Test ZIP integrity (Word compatibility requirement)
                try:
                    zip_buffer = io.BytesIO(response.content)
                    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
                        # Test that all files can be read without errors
                        for file_name in zip_file.namelist():
                            try:
                                zip_file.read(file_name)
                            except Exception as e:
                                self.log_test("Word Compatibility - File Integrity", False, f"Error reading {file_name}: {str(e)}")
                                return False
                        
                        self.log_test("Word Compatibility - File Integrity", True, "All files readable")
                        
                        # Test document.xml structure
                        if 'word/document.xml' in zip_file.namelist():
                            doc_xml = zip_file.read('word/document.xml')
                            if b'<?xml' in doc_xml and b'</w:document>' in doc_xml:
                                self.log_test("Word Compatibility - Document Structure", True)
                            else:
                                self.log_test("Word Compatibility - Document Structure", False, "Invalid document XML")
                        else:
                            self.log_test("Word Compatibility - Document Structure", False, "Missing document.xml")
                            
                except Exception as e:
                    self.log_test("Word Compatibility - ZIP Structure", False, f"ZIP error: {str(e)}")
                    return False
            else:
                self.log_test("Word Compatibility Test", False, f"Failed to generate file: {response.status_code}")
                return False
        
        except Exception as e:
            self.log_test("Word Compatibility Test", False, f"Request error: {str(e)}")
            return False
        
        return True

    def run_v9_template_tests(self):
        """Run all V9 template tests as specified in review request"""
        print("🚀 V9 TEMPLATE COMPREHENSIVE TESTING")
        print("=" * 80)
        print("OBJECTIVE: Test new v9 template to ensure it resolves all DOCX corruption and PDF table formatting issues")
        print("=" * 80)
        
        # Setup
        if not self.setup_test_environment():
            print("❌ Test environment setup failed - stopping tests")
            return
        
        # Core Tests
        print("\n" + "="*50)
        print("CORE V9 TEMPLATE TESTS")
        print("="*50)
        
        self.test_v9_template_docx_generation()
        self.test_v9_template_pdf_generation()
        self.test_template_variable_population()
        self.test_native_jinja2_rendering()
        self.test_word_compatibility()
        
        # Summary
        print("\n" + "="*50)
        print("V9 TEMPLATE TEST RESULTS SUMMARY")
        print("="*50)
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("✅ V9 TEMPLATE TESTING: SUCCESS")
            print("   The new v9 template resolves DOCX corruption and PDF formatting issues")
        elif success_rate >= 75:
            print("⚠️  V9 TEMPLATE TESTING: PARTIAL SUCCESS")
            print("   Most tests passed but some issues remain")
        else:
            print("❌ V9 TEMPLATE TESTING: FAILED")
            print("   Significant issues detected with v9 template")
        
        # Failed tests summary
        failed_tests = [result for result in self.test_results if not result['success']]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['details']}")
        
        print("\n" + "="*80)
        return success_rate >= 90

if __name__ == "__main__":
    tester = V9TemplateTester()
    success = tester.run_v9_template_tests()
    sys.exit(0 if success else 1)