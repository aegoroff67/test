#!/usr/bin/env python3

import requests
import sys
import json
import zipfile
import io
from datetime import datetime

class CriticalFixesTester:
    def __init__(self, base_url="https://reportgen-5.preview.emergentagent.com"):
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
            return success, response.json() if success else response.text

        except Exception as e:
            return False, str(e)

    def setup_test_user(self):
        """Create test user and assessment"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"critical_test_{timestamp}@vciso.one"
        
        # Test signup
        signup_data = {
            "name": f"vCISO Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": "vCISO.One",
            "industry": "Cybersecurity Consulting"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("User setup for critical fixes test", True)
            return True
        else:
            self.log_test("User setup for critical fixes test", False, str(response))
            return False

    def test_critical_report_generation_fixes(self):
        """Test the two critical fixes: PDF generation variable scope and DOCX template corruption"""
        print("\n🔍 TESTING CRITICAL REPORT GENERATION FIXES")
        print("-" * 60)
        
        # Create a fresh assessment for report testing
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            self.log_test("Create assessment for report generation test", False, str(response))
            return False
            
        report_assessment_id = response['id']
        self.log_test("Create assessment for report generation test", True)
        
        # Get all questions and answer them to create a complete assessment
        success, response = self.make_request('GET', f'assessments/{report_assessment_id}/questions')
        if not success:
            self.log_test("Get questions for report test", False, str(response))
            return False
            
        # Answer all questions with realistic data pattern
        question_count = 0
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for i, question in enumerate(questions):
                # Create realistic answer pattern: mix of IDEAL, GOOD, BASIC, NON_IDEAL
                options = ['IDEAL', 'GOOD', 'BASIC', 'NON_IDEAL']
                option = options[i % len(options)]
                
                answer_data = {
                    "question_id": question['id'],
                    "option": option,
                    "note": f"Test answer for {question.get('code', 'unknown')} - {option} response"
                }
                
                success_answer, _ = self.make_request('POST', f'assessments/{report_assessment_id}/answer', answer_data)
                if success_answer:
                    question_count += 1
        
        self.log_test(f"Answered all {question_count} questions for report test", True)
        
        # Submit the assessment to make it complete
        success, _ = self.make_request('POST', f'assessments/{report_assessment_id}/submit')
        if success:
            self.log_test("Submit assessment for report generation", True)
        else:
            self.log_test("Submit assessment for report generation", False, "Failed to submit assessment")
            return False
        
        # Test 1: DOCX Generation with ENHANCED Template (37KB template fix)
        print("\n📄 Testing DOCX Generation with ENHANCED Template...")
        
        url = f"{self.api_url}/assessments/{report_assessment_id}/report"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            response = requests.get(url, headers=headers, timeout=60)
            
            if response.status_code == 200:
                self.log_test("DOCX Generation Returns 200 OK", True)
                
                # Check MIME type
                content_type = response.headers.get('content-type', '')
                if 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
                    self.log_test("DOCX Generation Returns Correct MIME Type", True)
                else:
                    self.log_test("DOCX Generation Returns Correct MIME Type", False, f"Got: {content_type}")
                
                # Check file size (should be substantial, not tiny)
                docx_size = len(response.content)
                if docx_size > 50000:  # Should be > 50KB for substantial content
                    self.log_test("DOCX File Size Substantial (>50KB)", True, f"Size: {docx_size} bytes")
                else:
                    self.log_test("DOCX File Size Substantial (>50KB)", False, f"Size: {docx_size} bytes")
                
                # Test DOCX file integrity (ZIP structure)
                try:
                    docx_io = io.BytesIO(response.content)
                    with zipfile.ZipFile(docx_io, 'r') as zip_file:
                        file_list = zip_file.namelist()
                        essential_files = ['word/document.xml', '[Content_Types].xml', 'word/_rels/document.xml.rels']
                        has_essential = all(f in file_list for f in essential_files)
                        
                        if has_essential:
                            self.log_test("DOCX File Has Valid ZIP Structure", True)
                        else:
                            self.log_test("DOCX File Has Valid ZIP Structure", False, "Missing essential files")
                        
                        # Check for corruption indicators
                        try:
                            document_xml = zip_file.read('word/document.xml').decode('utf-8')
                            if 'vCISO.One' in document_xml or self.user_data.get('organization_name', '') in document_xml:
                                self.log_test("DOCX Contains Real Organization Data", True)
                            else:
                                self.log_test("DOCX Contains Real Organization Data", False, "Organization name not found")
                        except Exception as e:
                            self.log_test("DOCX Document XML Readable", False, str(e))
                            
                except zipfile.BadZipFile:
                    self.log_test("DOCX File Has Valid ZIP Structure", False, "Not a valid ZIP file")
                except Exception as e:
                    self.log_test("DOCX File Integrity Check", False, str(e))
                    
            else:
                self.log_test("DOCX Generation Returns 200 OK", False, f"Status: {response.status_code}, Response: {response.text[:200]}")
                
        except Exception as e:
            self.log_test("DOCX Generation Request", False, str(e))
        
        # Test 2: PDF Generation with Variable Scope Fix
        print("\n📄 Testing PDF Generation with Variable Scope Fix...")
        
        url = f"{self.api_url}/assessments/{report_assessment_id}/report/pdf"
        
        try:
            response = requests.get(url, headers=headers, timeout=60)
            
            if response.status_code == 200:
                self.log_test("PDF Generation Returns 200 OK (Not 503)", True)
                
                # Check MIME type
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type:
                    self.log_test("PDF Generation Returns Correct MIME Type", True)
                else:
                    self.log_test("PDF Generation Returns Correct MIME Type", False, f"Got: {content_type}")
                
                # Check file size
                pdf_size = len(response.content)
                if pdf_size > 30000:  # Should be > 30KB for substantial content
                    self.log_test("PDF File Size Substantial (>30KB)", True, f"Size: {pdf_size} bytes")
                else:
                    self.log_test("PDF File Size Substantial (>30KB)", False, f"Size: {pdf_size} bytes")
                
                # Test PDF file integrity
                pdf_content = response.content
                if pdf_content.startswith(b'%PDF'):
                    self.log_test("PDF File Has Valid PDF Header", True)
                else:
                    self.log_test("PDF File Has Valid PDF Header", False, "Does not start with %PDF")
                
                if pdf_content.endswith(b'%%EOF') or b'%%EOF' in pdf_content[-50:]:
                    self.log_test("PDF File Has Valid EOF Marker", True)
                else:
                    self.log_test("PDF File Has Valid EOF Marker", False, "Missing %%EOF marker")
                
                # Check that it's not returning DOCX content as PDF (common error)
                if not pdf_content.startswith(b'PK'):  # ZIP signature (DOCX files start with PK)
                    self.log_test("PDF Not Returning DOCX Content", True)
                else:
                    self.log_test("PDF Not Returning DOCX Content", False, "PDF endpoint returning DOCX content")
                    
            elif response.status_code == 503:
                # This is the old error - should be fixed now
                self.log_test("PDF Generation Returns 200 OK (Not 503)", False, "Still returning 503 'Failed to generate PDF report'")
            else:
                self.log_test("PDF Generation Returns 200 OK (Not 503)", False, f"Status: {response.status_code}, Response: {response.text[:200]}")
                
        except Exception as e:
            self.log_test("PDF Generation Request", False, str(e))
        
        # Test 3: Content Verification - Check for Real Assessment Data
        print("\n📊 Testing Content Verification...")
        
        # Get assessment summary to verify data alignment
        success, summary_response = self.make_request('GET', f'assessments/{report_assessment_id}/summary')
        if success:
            overall_percentage = summary_response.get('overall_percentage', 0)
            overall_maturity = summary_response.get('overall_maturity', 'Unknown')
            domain_scores = summary_response.get('domain_scores', [])
            
            self.log_test("Assessment Summary Data Available", True, f"Score: {overall_percentage}%, Maturity: {overall_maturity}, Domains: {len(domain_scores)}")
            
            # Verify we have 11 domains with realistic scores
            if len(domain_scores) == 11:
                self.log_test("Assessment Has 11 Domain Scores", True)
            else:
                self.log_test("Assessment Has 11 Domain Scores", False, f"Found {len(domain_scores)} domains")
                
            # Check that scores are realistic (not all zeros or all same)
            scores = [d.get('percentage', 0) for d in domain_scores]
            unique_scores = len(set(scores))
            if unique_scores > 1:  # Should have variety in scores
                self.log_test("Domain Scores Show Realistic Variation", True, f"{unique_scores} unique scores")
            else:
                self.log_test("Domain Scores Show Realistic Variation", False, f"All scores same: {scores[0] if scores else 'N/A'}")
        else:
            self.log_test("Assessment Summary Data Available", False, str(summary_response))
        
        # Test 4: Template Size Verification (ENHANCED vs v8)
        print("\n📏 Testing Template Size Fix...")
        
        # Check that we're using the smaller ENHANCED template (37KB) not the large v8 template (173KB)
        # This is verified by checking the report generator's template path
        try:
            import sys
            sys.path.append('/app/backend')
            from report_generator import AMReportGenerator
            
            generator = AMReportGenerator()
            template_path = generator.template_path
            
            if 'ENHANCED' in template_path:
                self.log_test("Using ENHANCED Template (Not v8)", True, f"Template: {template_path}")
            else:
                self.log_test("Using ENHANCED Template (Not v8)", False, f"Template: {template_path}")
                
            # Check template file size
            import os
            if os.path.exists(template_path):
                template_size = os.path.getsize(template_path)
                if template_size < 100000:  # Should be ~37KB, much less than 173KB
                    self.log_test("Template Size Reasonable (<100KB)", True, f"Size: {template_size} bytes")
                else:
                    self.log_test("Template Size Reasonable (<100KB)", False, f"Size: {template_size} bytes - too large")
            else:
                self.log_test("Template File Exists", False, f"Template not found: {template_path}")
                
        except Exception as e:
            self.log_test("Template Verification", False, str(e))
        
        print(f"\n✅ Critical Report Generation Fixes Testing Complete")
        return True

    def run_test(self):
        """Run the critical fixes test"""
        print("🚀 Starting Critical Report Generation Fixes Test")
        print("=" * 60)
        
        if not self.setup_test_user():
            return False
            
        if not self.test_critical_report_generation_fixes():
            return False
        
        # Print final results
        print("\n" + "=" * 60)
        print("🏁 CRITICAL FIXES TESTING COMPLETE")
        print("=" * 60)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL CRITICAL FIXES VERIFIED!")
            print("✅ PDF Generation Variable Scope Fix: WORKING")
            print("✅ DOCX Template Corruption Fix: WORKING")
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} TESTS FAILED")
            print("❌ Some critical fixes may not be working properly")
        
        return self.tests_passed == self.tests_run

if __name__ == "__main__":
    tester = CriticalFixesTester()
    success = tester.run_test()
    sys.exit(0 if success else 1)