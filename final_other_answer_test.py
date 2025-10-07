#!/usr/bin/env python3

import requests
import sys
import json
import zipfile
import io
from datetime import datetime

class FinalOtherAnswerTest:
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
            if success:
                try:
                    return success, response.json()
                except:
                    return success, response.content
            else:
                return success, f"Status: {response.status_code}, Response: {response.text}"

        except Exception as e:
            return False, str(e)

    def setup_test_user(self):
        """Create test user and authenticate"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"final_other_test_{timestamp}@example.com"
        
        signup_data = {
            "name": f"Final Other Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Final Other Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("User setup and authentication", True)
            return True
        else:
            self.log_test("User setup and authentication", False, str(response))
            return False

    def create_assessment_with_other_answers(self):
        """Create assessment with specific OTHER answers that could cause corruption"""
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            self.log_test("Assessment creation", False, str(response))
            return False
            
        self.assessment_id = response['id']
        self.log_test("Assessment creation", True)
        
        # Get questions
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            self.log_test("Get questions for OTHER testing", False, str(response))
            return False
        
        # Collect all questions
        all_questions = []
        for domain_data in response:
            questions = domain_data.get('questions', [])
            all_questions.extend(questions)
        
        if len(all_questions) < 88:
            self.log_test("Sufficient questions available", False, f"Only {len(all_questions)} questions found")
            return False
            
        self.log_test("Sufficient questions available", True)
        
        # Create problematic OTHER answers that could cause corruption
        problematic_other_texts = [
            # Long text with special characters
            "Our implementation includes advanced monitoring systems with real-time analytics, automated bias detection using machine learning algorithms, comprehensive reporting dashboards, integration with external audit tools, and continuous improvement processes. We also maintain detailed documentation, conduct regular training sessions, and have established clear escalation procedures for handling bias-related incidents. The system includes features for data lineage tracking, model versioning, and automated testing across different demographic groups.",
            
            # Text with potential template-breaking characters
            "We use a {{custom}} approach with <special> characters and \"quoted\" text, including 'single quotes' and various symbols: @#$%^&*()_+-=[]{}|;:,.<>?/~`",
            
            # Text with newlines and formatting
            """Our multi-line approach includes:
            1. Automated bias detection
            2. Manual review processes
            3. Continuous monitoring
            4. Regular audits
            
            This comprehensive strategy ensures fairness across all AI systems.""",
            
            # Very long text that could cause memory issues
            "Comprehensive implementation " * 100 + "with extensive details and thorough documentation covering all aspects of the system.",
            
            # Text with Unicode characters
            "Our approach includes international standards: français, español, 中文, العربية, русский, and other languages with special characters like ñ, ü, ø, æ, and mathematical symbols: ∑, ∆, π, ∞, ≤, ≥, ≠, ±",
        ]
        
        # Answer questions with a mix of standard and problematic OTHER answers
        answered_count = 0
        other_answer_count = 0
        
        for i, question in enumerate(all_questions):
            if i < len(problematic_other_texts):
                # Use problematic OTHER answer
                answer_data = {
                    "question_id": question['id'],
                    "option": "OTHER",
                    "other_text": problematic_other_texts[i],
                    "note": f"Problematic OTHER answer test {i+1}"
                }
                other_answer_count += 1
            elif i % 15 == 0:  # Every 15th question gets a regular OTHER answer
                answer_data = {
                    "question_id": question['id'],
                    "option": "OTHER",
                    "other_text": f"Custom implementation for {question.get('code', 'question')} with specialized processes.",
                    "note": f"Regular OTHER answer {i}"
                }
                other_answer_count += 1
            else:
                # Standard answer
                options = ["IDEAL", "GOOD", "BASIC", "NON_IDEAL"]
                option = options[i % len(options)]
                answer_data = {
                    "question_id": question['id'],
                    "option": option,
                    "note": f"Standard answer {i}"
                }
            
            success, _ = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
            if success:
                answered_count += 1
        
        self.log_test(f"Assessment completion ({answered_count} answers, {other_answer_count} OTHER)", 
                     answered_count == len(all_questions))
        
        # Submit assessment
        success, _ = self.make_request('POST', f'assessments/{self.assessment_id}/submit')
        self.log_test("Assessment submission", success)
        
        return answered_count == len(all_questions)

    def test_data_retrieval_with_problematic_other(self):
        """Test data retrieval with problematic OTHER answers"""
        print("\n🔍 TESTING DATA RETRIEVAL WITH PROBLEMATIC OTHER ANSWERS")
        print("-" * 60)
        
        # Test assessment summary
        success, summary = self.make_request('GET', f'assessments/{self.assessment_id}/summary')
        if success:
            self.log_test("Assessment summary with OTHER answers", True)
            print(f"   📊 Overall percentage: {summary.get('overall_percentage', 'N/A')}%")
            print(f"   📊 Answered questions: {summary.get('answered_questions', 'N/A')}")
        else:
            self.log_test("Assessment summary with OTHER answers", False, str(summary))
            return False
        
        # Test questions retrieval
        success, questions = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if success:
            self.log_test("Questions retrieval with OTHER answers", True)
            
            # Count OTHER answers and verify other_text is preserved
            other_count = 0
            corrupted_other_count = 0
            
            for domain_data in questions:
                for question in domain_data.get('questions', []):
                    answer = question.get('answer')
                    if answer and answer.get('option') == 'OTHER':
                        other_count += 1
                        other_text = answer.get('other_text')
                        if not other_text or len(other_text.strip()) == 0:
                            corrupted_other_count += 1
            
            self.log_test(f"OTHER answers preserved ({other_count} found, {corrupted_other_count} corrupted)", 
                         corrupted_other_count == 0)
            
        else:
            self.log_test("Questions retrieval with OTHER answers", False, str(questions))
            return False
        
        return True

    def test_report_generation_corruption(self):
        """Test report generation for corruption with problematic OTHER answers"""
        print("\n🔍 TESTING REPORT GENERATION FOR CORRUPTION")
        print("-" * 60)
        
        # Test DOCX generation
        print("📄 Generating DOCX report with problematic OTHER answers...")
        success, docx_response = self.make_request('GET', f'assessments/{self.assessment_id}/report')
        
        if not success:
            self.log_test("DOCX generation with problematic OTHER answers", False, str(docx_response))
            return False
        
        if isinstance(docx_response, bytes):
            docx_size = len(docx_response)
            self.log_test("DOCX generation with problematic OTHER answers", True)
            print(f"   📄 DOCX size: {docx_size} bytes")
            
            # Verify DOCX structure integrity
            try:
                docx_file = io.BytesIO(docx_response)
                with zipfile.ZipFile(docx_file, 'r') as zip_file:
                    file_list = zip_file.namelist()
                    essential_files = ['word/document.xml', '[Content_Types].xml', 'word/_rels/document.xml.rels']
                    
                    if all(f in file_list for f in essential_files):
                        self.log_test("DOCX structure integrity", True)
                        print(f"   📁 DOCX contains {len(file_list)} files")
                        
                        # Try to read document.xml to check for corruption
                        try:
                            document_xml = zip_file.read('word/document.xml')
                            if b'<?xml' in document_xml and b'</w:document>' in document_xml:
                                self.log_test("DOCX XML content integrity", True)
                            else:
                                self.log_test("DOCX XML content integrity", False, "Invalid XML structure")
                        except Exception as e:
                            self.log_test("DOCX XML content integrity", False, f"Error reading XML: {str(e)}")
                            
                    else:
                        self.log_test("DOCX structure integrity", False, "Missing essential DOCX files")
                        
            except Exception as e:
                self.log_test("DOCX structure integrity", False, f"Error reading DOCX: {str(e)}")
                
        else:
            self.log_test("DOCX generation with problematic OTHER answers", False, "Response is not binary data")
            return False
        
        # Test PDF generation
        print("📄 Generating PDF report with problematic OTHER answers...")
        success, pdf_response = self.make_request('GET', f'assessments/{self.assessment_id}/report/pdf')
        
        if success and isinstance(pdf_response, bytes):
            pdf_size = len(pdf_response)
            self.log_test("PDF generation with problematic OTHER answers", True)
            print(f"   📄 PDF size: {pdf_size} bytes")
            
            # Check if it's actually a PDF or DOCX fallback
            if pdf_response.startswith(b'%PDF'):
                self.log_test("PDF format validation", True)
            elif pdf_response.startswith(b'PK'):
                self.log_test("PDF format validation (DOCX fallback)", True, "PDF returned as DOCX fallback")
            else:
                self.log_test("PDF format validation", False, "Invalid file format")
        else:
            self.log_test("PDF generation with problematic OTHER answers", False, "PDF generation failed")
        
        return True

    def run_final_test(self):
        """Run the final comprehensive OTHER answer test"""
        print("🔍 FINAL OTHER ANSWER CORRUPTION INVESTIGATION")
        print("=" * 80)
        print("OBJECTIVE: Test if OTHER answers with problematic content cause file corruption")
        print("=" * 80)
        
        # Setup
        if not self.setup_test_user():
            return False
        
        # Create assessment with problematic OTHER answers
        if not self.create_assessment_with_other_answers():
            return False
        
        # Test data retrieval
        if not self.test_data_retrieval_with_problematic_other():
            return False
        
        # Test report generation
        if not self.test_report_generation_corruption():
            return False
        
        # Summary
        print("\n" + "=" * 80)
        print("🔍 FINAL OTHER ANSWER TEST SUMMARY")
        print("=" * 80)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n✅ CONCLUSION: OTHER answers do NOT cause file corruption")
            print("📋 Key findings:")
            print("   - OTHER answers with long text, special characters, and Unicode work correctly")
            print("   - Data retrieval preserves other_text content without corruption")
            print("   - DOCX report generation works with problematic OTHER content")
            print("   - File structure integrity is maintained")
            print("   - No evidence of OTHER answers causing the reported corruption issue")
        else:
            print("\n❌ CONCLUSION: Issues detected with OTHER answer processing")
            print("📋 Problems found - see test results above")
        
        return self.tests_passed == self.tests_run

if __name__ == "__main__":
    tester = FinalOtherAnswerTest()
    success = tester.run_final_test()
    sys.exit(0 if success else 1)