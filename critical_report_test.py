#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime
import subprocess
import os

class CriticalReportTester:
    def __init__(self, base_url="https://proof-tracker-2.preview.emergentagent.com"):
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
            
            # Handle binary responses (like DOCX/PDF files)
            content_type = response.headers.get('content-type', '')
            if success and ('application/vnd.openxmlformats' in content_type or 'application/pdf' in content_type):
                return success, response.content
            
            # Handle JSON responses
            try:
                return success, response.json() if success else response.text
            except:
                # If JSON parsing fails, return text
                return success, response.text

        except Exception as e:
            return False, str(e)

    def test_libreoffice_installation_and_report_generation(self):
        """Test LibreOffice installation and report generation endpoints as per review request"""
        print("\n🔍 CRITICAL PRODUCTION ISSUE VERIFICATION")
        print("=" * 80)
        
        # Step 1: LibreOffice Installation Check
        print("\n1. LIBREOFFICE INSTALLATION CHECK")
        print("-" * 40)
        
        try:
            result = subprocess.run(['libreoffice', '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log_test("LibreOffice installation check", True, f"Version: {version}")
                print(f"   📋 LibreOffice Version: {version}")
            else:
                self.log_test("LibreOffice installation check", False, "LibreOffice not found or not working")
                return False
        except Exception as e:
            self.log_test("LibreOffice installation check", False, f"Error checking LibreOffice: {str(e)}")
            return False
        
        # Step 2: LibreOffice Headless Mode Check
        try:
            result = subprocess.run(['libreoffice', '--headless', '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log_test("LibreOffice headless mode check", True)
                print(f"   📋 Headless mode working")
            else:
                self.log_test("LibreOffice headless mode check", False, "Headless mode not working")
        except Exception as e:
            self.log_test("LibreOffice headless mode check", False, f"Error: {str(e)}")
        
        # Step 3: User Authentication
        print("\n2. USER AUTHENTICATION")
        print("-" * 40)
        
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"critical_test_{timestamp}@example.com"
        
        signup_data = {
            "name": f"Critical Test User {timestamp}",
            "email": test_email,
            "password": "CriticalTest123!",
            "organization_name": f"Critical Test Org {timestamp}",
            "industry": "Technology Testing"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("User authentication", True)
            print(f"   📋 Authenticated as: {self.user_data['name']}")
        else:
            self.log_test("User authentication", False, str(response))
            return False
        
        # Step 4: Create assessment and complete it for report testing
        print("\n3. ASSESSMENT CREATION AND COMPLETION")
        print("-" * 40)
        
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            self.log_test("Create assessment for report testing", False, str(response))
            return False
            
        test_assessment_id = response['id']
        self.log_test("Create assessment for report testing", True)
        print(f"   📋 Assessment ID: {test_assessment_id}")
        
        # Get questions and answer them all
        success, response = self.make_request('GET', f'assessments/{test_assessment_id}/questions')
        if not success:
            self.log_test("Get questions for report testing", False, str(response))
            return False
            
        # Answer all questions with varied responses
        question_count = 0
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for i, question in enumerate(questions):
                # Use varied answers to create realistic report data
                options = ["NON_IDEAL", "BASIC", "GOOD", "IDEAL"]
                option = options[i % len(options)]
                
                answer_data = {
                    "question_id": question['id'],
                    "option": option,
                    "note": f"Critical test answer - {option}"
                }
                
                success_answer, _ = self.make_request('POST', f'assessments/{test_assessment_id}/answer', answer_data)
                if success_answer:
                    question_count += 1
        
        self.log_test(f"Answered all {question_count} questions", True)
        print(f"   📋 Questions answered: {question_count}")
        
        # Submit assessment
        success, _ = self.make_request('POST', f'assessments/{test_assessment_id}/submit')
        if success:
            self.log_test("Submit assessment for report testing", True)
            print(f"   📋 Assessment submitted successfully")
        else:
            self.log_test("Submit assessment for report testing", False, "Failed to submit assessment")
            return False
        
        # Step 5: Test DOCX Report Generation
        print("\n4. DOCX REPORT GENERATION TESTING")
        print("-" * 40)
        
        success, docx_content = self.make_request('GET', f'assessments/{test_assessment_id}/report')
        if success and isinstance(docx_content, bytes):
            docx_size = len(docx_content)
            self.log_test("DOCX report generation endpoint", True, f"Generated {docx_size} bytes")
            print(f"   📋 DOCX file size: {docx_size:,} bytes")
            
            # Validate DOCX file structure (ZIP-based)
            if docx_content.startswith(b'PK'):
                self.log_test("DOCX file format validation", True, "Valid ZIP-based DOCX structure")
                print(f"   📋 DOCX format: Valid ZIP structure")
            else:
                self.log_test("DOCX file format validation", False, "Invalid DOCX format")
                print(f"   📋 DOCX format: Invalid - not ZIP-based")
        else:
            self.log_test("DOCX report generation endpoint", False, f"Failed: {docx_content}")
            print(f"   ❌ DOCX generation failed: {docx_content}")
            return False
        
        # Step 6: Test PDF Report Generation
        print("\n5. PDF REPORT GENERATION TESTING")
        print("-" * 40)
        
        success, pdf_content = self.make_request('GET', f'assessments/{test_assessment_id}/report/pdf')
        if success and isinstance(pdf_content, bytes):
            pdf_size = len(pdf_content)
            self.log_test("PDF report generation endpoint", True, f"Generated {pdf_size} bytes")
            print(f"   📋 PDF file size: {pdf_size:,} bytes")
            
            # Validate PDF file structure
            if pdf_content.startswith(b'%PDF'):
                self.log_test("PDF file format validation", True, "Valid PDF format with %PDF header")
                print(f"   📋 PDF format: Valid - starts with %PDF")
                
                # Check for PDF end marker
                if b'%%EOF' in pdf_content:
                    self.log_test("PDF file completeness check", True, "PDF has proper %%EOF marker")
                    print(f"   📋 PDF completeness: Valid - has %%EOF marker")
                else:
                    self.log_test("PDF file completeness check", False, "PDF missing %%EOF marker")
                    print(f"   📋 PDF completeness: Invalid - missing %%EOF marker")
            else:
                self.log_test("PDF file format validation", False, "Invalid PDF format")
                print(f"   📋 PDF format: Invalid - doesn't start with %PDF")
                return False
        else:
            self.log_test("PDF report generation endpoint", False, f"Failed: {pdf_content}")
            print(f"   ❌ PDF generation failed: {pdf_content}")
            return False
        
        # Step 7: Assessment Data Validation
        print("\n6. ASSESSMENT DATA VALIDATION")
        print("-" * 40)
        
        # Check assessment summary
        success, summary = self.make_request('GET', f'assessments/{test_assessment_id}/summary')
        if success:
            self.log_test("Assessment summary accessible", True)
            print(f"   📋 Overall score: {summary.get('overall_percentage', 'N/A')}%")
            print(f"   📋 Maturity level: {summary.get('overall_maturity', 'N/A')}")
            print(f"   📋 Domain scores: {len(summary.get('domain_scores', []))} domains")
        else:
            self.log_test("Assessment summary accessible", False, str(summary))
        
        # Step 8: System Dependencies Verification
        print("\n7. SYSTEM DEPENDENCIES VERIFICATION")
        print("-" * 40)
        
        # Check if report generator module exists
        try:
            sys.path.append('/app/backend')
            from report_generator import AMReportGenerator
            self.log_test("Report generator module import", True)
            print(f"   📋 AMReportGenerator class available")
        except ImportError as e:
            self.log_test("Report generator module import", False, f"Import error: {str(e)}")
            print(f"   ❌ Report generator import failed: {str(e)}")
        
        # Check template file existence
        template_paths = [
            '/app/backend/templates/docx/AM_AI_SAFE_Report_TEMPLATE_v8_10072025.docx',
            '/app/backend/templates/docx/AM_AI_SAFE_Report_TEMPLATE_preserving_styles.docx'
        ]
        
        for template_path in template_paths:
            if os.path.exists(template_path):
                file_size = os.path.getsize(template_path)
                self.log_test(f"Template file exists: {os.path.basename(template_path)}", True, f"Size: {file_size} bytes")
                print(f"   📋 Template: {os.path.basename(template_path)} ({file_size:,} bytes)")
            else:
                self.log_test(f"Template file exists: {os.path.basename(template_path)}", False, "File not found")
                print(f"   ❌ Template missing: {os.path.basename(template_path)}")
        
        print("\n" + "=" * 80)
        print("CRITICAL PRODUCTION ISSUE VERIFICATION COMPLETED")
        print("=" * 80)
        
        return True

    def run_critical_tests(self):
        """Run critical production tests"""
        print(f"🚨 CRITICAL PRODUCTION ISSUE VERIFICATION")
        print(f"📍 Base URL: {self.base_url}")
        print(f"📍 API URL: {self.api_url}")
        print("=" * 80)
        
        # Run the critical test
        self.test_libreoffice_installation_and_report_generation()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 CRITICAL TEST SUMMARY")
        print("=" * 80)
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"🔢 Total Tests: {self.tests_run}")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - Report generation is working correctly!")
        elif success_rate >= 75:
            print("✅ GOOD - Report generation is mostly functional")
        elif success_rate >= 50:
            print("⚠️  FAIR - Some report generation issues need attention")
        else:
            print("🚨 CRITICAL - Report generation has significant issues")
        
        print("=" * 80)

if __name__ == "__main__":
    tester = CriticalReportTester()
    tester.run_critical_tests()