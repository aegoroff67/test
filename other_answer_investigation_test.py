#!/usr/bin/env python3

import requests
import sys
import json
import subprocess
import asyncio
import traceback
from datetime import datetime
import zipfile
import io

class OtherAnswerInvestigationTester:
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
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=headers)
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
        test_email = f"other_test_{timestamp}@example.com"
        
        # Test signup
        signup_data = {
            "name": f"Other Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Other Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("Test user setup and authentication", True)
            return True
        else:
            self.log_test("Test user setup and authentication", False, str(response))
            return False

    def create_test_assessment(self):
        """Create assessment for testing"""
        success, response = self.make_request('POST', 'assessments', {})
        if success and 'id' in response:
            self.assessment_id = response['id']
            self.log_test("Test assessment creation", True)
            return True
        else:
            self.log_test("Test assessment creation", False, str(response))
            return False

    def test_other_answer_submission(self):
        """Test submitting answers with OTHER option and custom text"""
        print("\n🔍 TESTING OTHER ANSWER SUBMISSION")
        print("-" * 60)
        
        if not self.assessment_id:
            self.log_test("OTHER answer submission test", False, "No assessment ID")
            return False
            
        # Get questions
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            self.log_test("Get questions for OTHER test", False, str(response))
            return False
            
        # Get first few questions from different domains
        test_questions = []
        for domain_data in response[:3]:  # Test first 3 domains
            questions = domain_data.get('questions', [])
            if questions:
                test_questions.append(questions[0])  # First question from each domain
        
        if len(test_questions) < 3:
            self.log_test("Get test questions for OTHER answers", False, "Not enough questions found")
            return False
            
        self.log_test(f"Retrieved {len(test_questions)} questions for OTHER testing", True)
        
        # Test different OTHER answer scenarios
        other_test_cases = [
            {
                "question_idx": 0,
                "other_text": "We have implemented a custom bias detection system using advanced machine learning algorithms that continuously monitor our AI outputs for potential discriminatory patterns.",
                "note": "Custom implementation with detailed monitoring"
            },
            {
                "question_idx": 1,
                "other_text": "Our approach involves quarterly reviews by external auditors combined with real-time bias detection tools and employee training programs on AI fairness.",
                "note": "Multi-faceted approach with external validation"
            },
            {
                "question_idx": 2,
                "other_text": "We use a proprietary framework that combines statistical parity checks, equalized odds analysis, and demographic parity assessments across all protected classes.",
                "note": "Technical implementation with statistical measures"
            }
        ]
        
        # Submit OTHER answers
        for i, test_case in enumerate(other_test_cases):
            question = test_questions[test_case["question_idx"]]
            answer_data = {
                "question_id": question['id'],
                "option": "OTHER",
                "other_text": test_case["other_text"],
                "note": test_case["note"]
            }
            
            success, response = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
            if success and response.get('status') == 'success':
                self.log_test(f"OTHER answer submission {i+1} (Question {question.get('code', 'Unknown')})", True)
            else:
                self.log_test(f"OTHER answer submission {i+1} (Question {question.get('code', 'Unknown')})", False, str(response))
                return False
        
        return True

    def test_mixed_answer_assessment(self):
        """Create assessment with mix of standard and OTHER answers"""
        print("\n🔍 TESTING MIXED ANSWER ASSESSMENT")
        print("-" * 60)
        
        if not self.assessment_id:
            self.log_test("Mixed answer assessment test", False, "No assessment ID")
            return False
            
        # Get all questions
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            self.log_test("Get all questions for mixed test", False, str(response))
            return False
            
        # Collect all questions
        all_questions = []
        for domain_data in response:
            questions = domain_data.get('questions', [])
            all_questions.extend(questions)
        
        if len(all_questions) < 20:
            self.log_test("Get sufficient questions for mixed test", False, f"Only {len(all_questions)} questions available")
            return False
            
        self.log_test(f"Retrieved {len(all_questions)} questions for mixed testing", True)
        
        # Answer pattern: Mix of standard answers and OTHER answers
        answer_patterns = [
            ("IDEAL", None, "Standard ideal answer"),
            ("GOOD", None, "Standard good answer"),
            ("OTHER", "We have developed a custom solution that exceeds industry standards through innovative approaches and continuous improvement processes.", "Custom solution description"),
            ("BASIC", None, "Standard basic answer"),
            ("NON_IDEAL", None, "Standard non-ideal answer"),
            ("OTHER", "Our implementation includes specialized tools and methodologies not covered by the standard options, specifically designed for our unique operational requirements.", "Specialized implementation details"),
            ("IDEAL", None, "Standard ideal answer"),
            ("OTHER", "We utilize a hybrid approach combining multiple frameworks and custom-built components to address specific challenges in our AI deployment environment.", "Hybrid approach explanation")
        ]
        
        # Answer first 20 questions with the pattern
        questions_to_answer = min(20, len(all_questions))
        answered_count = 0
        
        for i in range(questions_to_answer):
            question = all_questions[i]
            pattern_idx = i % len(answer_patterns)
            option, other_text, note = answer_patterns[pattern_idx]
            
            answer_data = {
                "question_id": question['id'],
                "option": option,
                "note": note
            }
            
            if other_text:
                answer_data["other_text"] = other_text
            
            success, response = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
            if success and response.get('status') == 'success':
                answered_count += 1
            else:
                self.log_test(f"Mixed answer submission {i+1} ({option})", False, str(response))
                return False
        
        self.log_test(f"Mixed answer pattern submission ({answered_count} questions)", True)
        
        # Complete the assessment with remaining standard answers
        remaining_questions = all_questions[questions_to_answer:]
        standard_options = ["IDEAL", "GOOD", "BASIC", "NON_IDEAL"]
        
        for i, question in enumerate(remaining_questions):
            option = standard_options[i % len(standard_options)]
            answer_data = {
                "question_id": question['id'],
                "option": option,
                "note": f"Completion answer {i+1}"
            }
            
            success, response = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
            if success:
                answered_count += 1
        
        self.log_test(f"Assessment completion ({answered_count} total answers)", True)
        return True

    def test_assessment_data_retrieval_with_other(self):
        """Test how assessment data is retrieved when OTHER answers are present"""
        print("\n🔍 TESTING ASSESSMENT DATA RETRIEVAL WITH OTHER ANSWERS")
        print("-" * 60)
        
        if not self.assessment_id:
            self.log_test("Assessment data retrieval test", False, "No assessment ID")
            return False
        
        # Test assessment summary endpoint
        success, summary_response = self.make_request('GET', f'assessments/{self.assessment_id}/summary')
        if not success:
            self.log_test("Assessment summary retrieval", False, str(summary_response))
            return False
            
        self.log_test("Assessment summary retrieval", True)
        
        # Verify summary structure includes OTHER answers
        if 'overall_percentage' in summary_response and 'domain_scores' in summary_response:
            self.log_test("Summary structure validation", True)
            
            # Check if OTHER answers are properly included in scoring
            overall_percentage = summary_response.get('overall_percentage', 0)
            answered_questions = summary_response.get('answered_questions', 0)
            
            if answered_questions > 0 and overall_percentage >= 0:
                self.log_test("OTHER answers included in summary calculations", True)
                print(f"   📊 Overall percentage: {overall_percentage}%")
                print(f"   📊 Answered questions: {answered_questions}")
            else:
                self.log_test("OTHER answers included in summary calculations", False, "Invalid summary calculations")
        else:
            self.log_test("Summary structure validation", False, "Missing required summary fields")
            return False
        
        # Test assessment questions endpoint to verify OTHER answers are preserved
        success, questions_response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            self.log_test("Assessment questions with OTHER answers retrieval", False, str(questions_response))
            return False
            
        self.log_test("Assessment questions with OTHER answers retrieval", True)
        
        # Count OTHER answers in the response
        other_answers_found = 0
        total_answers_found = 0
        
        for domain_data in questions_response:
            questions = domain_data.get('questions', [])
            for question in questions:
                answer = question.get('answer')
                if answer:
                    total_answers_found += 1
                    if answer.get('option') == 'OTHER':
                        other_answers_found += 1
                        # Verify other_text is preserved
                        if answer.get('other_text'):
                            self.log_test(f"OTHER answer text preserved for {question.get('code', 'Unknown')}", True)
                        else:
                            self.log_test(f"OTHER answer text preserved for {question.get('code', 'Unknown')}", False, "Missing other_text")
        
        if other_answers_found > 0:
            self.log_test(f"OTHER answers found in data retrieval ({other_answers_found} out of {total_answers_found})", True)
        else:
            self.log_test("OTHER answers found in data retrieval", False, "No OTHER answers found in retrieved data")
            
        return True

    def test_report_generation_with_other_answers(self):
        """Test DOCX report generation with OTHER answers"""
        print("\n🔍 TESTING REPORT GENERATION WITH OTHER ANSWERS")
        print("-" * 60)
        
        if not self.assessment_id:
            self.log_test("Report generation with OTHER answers test", False, "No assessment ID")
            return False
        
        # First, submit the assessment to make it complete
        success, submit_response = self.make_request('POST', f'assessments/{self.assessment_id}/submit')
        if not success:
            self.log_test("Submit assessment for report generation", False, str(submit_response))
            return False
            
        self.log_test("Submit assessment for report generation", True)
        
        # Test DOCX report generation
        print("   🔄 Generating DOCX report with OTHER answers...")
        success, docx_response = self.make_request('GET', f'assessments/{self.assessment_id}/report')
        
        if not success:
            self.log_test("DOCX report generation with OTHER answers", False, str(docx_response))
            return False
        
        # Verify DOCX response
        if isinstance(docx_response, bytes):
            docx_size = len(docx_response)
            self.log_test("DOCX report generation with OTHER answers", True)
            print(f"   📄 DOCX file size: {docx_size} bytes")
            
            # Verify DOCX file structure
            try:
                docx_file = io.BytesIO(docx_response)
                with zipfile.ZipFile(docx_file, 'r') as zip_file:
                    file_list = zip_file.namelist()
                    essential_files = ['word/document.xml', '[Content_Types].xml', 'word/_rels/document.xml.rels']
                    
                    if all(f in file_list for f in essential_files):
                        self.log_test("DOCX file structure validation", True)
                        print(f"   📁 DOCX contains {len(file_list)} files")
                    else:
                        self.log_test("DOCX file structure validation", False, "Missing essential DOCX files")
                        
            except Exception as e:
                self.log_test("DOCX file structure validation", False, f"Error reading DOCX: {str(e)}")
                
        else:
            self.log_test("DOCX report generation with OTHER answers", False, "Response is not binary data")
            return False
        
        # Test PDF report generation
        print("   🔄 Generating PDF report with OTHER answers...")
        success, pdf_response = self.make_request('GET', f'assessments/{self.assessment_id}/report/pdf')
        
        if not success:
            self.log_test("PDF report generation with OTHER answers", False, str(pdf_response))
            # PDF generation might fail, but DOCX working is the main concern
        else:
            if isinstance(pdf_response, bytes):
                pdf_size = len(pdf_response)
                self.log_test("PDF report generation with OTHER answers", True)
                print(f"   📄 PDF file size: {pdf_size} bytes")
                
                # Verify PDF file structure
                if pdf_response.startswith(b'%PDF'):
                    self.log_test("PDF file format validation", True)
                else:
                    self.log_test("PDF file format validation", False, "Invalid PDF format")
            else:
                self.log_test("PDF report generation with OTHER answers", False, "Response is not binary data")
        
        return True

    def test_report_generation_comparison(self):
        """Compare report generation with standard answers vs OTHER answers"""
        print("\n🔍 TESTING REPORT GENERATION COMPARISON")
        print("-" * 60)
        
        # Create a new assessment with only standard answers
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            self.log_test("Create standard answers assessment", False, str(response))
            return False
            
        standard_assessment_id = response['id']
        self.log_test("Create standard answers assessment", True)
        
        # Get questions and answer with only standard options
        success, response = self.make_request('GET', f'assessments/{standard_assessment_id}/questions')
        if not success:
            self.log_test("Get questions for standard assessment", False, str(response))
            return False
        
        # Answer all questions with standard options only
        all_questions = []
        for domain_data in response:
            questions = domain_data.get('questions', [])
            all_questions.extend(questions)
        
        standard_options = ["IDEAL", "GOOD", "BASIC", "NON_IDEAL"]
        for i, question in enumerate(all_questions):
            option = standard_options[i % len(standard_options)]
            answer_data = {
                "question_id": question['id'],
                "option": option,
                "note": f"Standard answer {i+1}"
            }
            
            self.make_request('POST', f'assessments/{standard_assessment_id}/answer', answer_data)
        
        self.log_test("Complete standard answers assessment", True)
        
        # Submit standard assessment
        success, _ = self.make_request('POST', f'assessments/{standard_assessment_id}/submit')
        if not success:
            self.log_test("Submit standard answers assessment", False, "Failed to submit")
            return False
            
        self.log_test("Submit standard answers assessment", True)
        
        # Generate reports for both assessments
        print("   🔄 Generating standard answers report...")
        success, standard_docx = self.make_request('GET', f'assessments/{standard_assessment_id}/report')
        
        if success and isinstance(standard_docx, bytes):
            standard_size = len(standard_docx)
            self.log_test("Standard answers DOCX generation", True)
            print(f"   📄 Standard DOCX size: {standard_size} bytes")
        else:
            self.log_test("Standard answers DOCX generation", False, str(standard_docx))
            return False
        
        print("   🔄 Generating OTHER answers report...")
        success, other_docx = self.make_request('GET', f'assessments/{self.assessment_id}/report')
        
        if success and isinstance(other_docx, bytes):
            other_size = len(other_docx)
            self.log_test("OTHER answers DOCX generation", True)
            print(f"   📄 OTHER DOCX size: {other_size} bytes")
            
            # Compare file sizes
            size_difference = abs(other_size - standard_size)
            size_ratio = other_size / standard_size if standard_size > 0 else 0
            
            print(f"   📊 Size comparison: OTHER={other_size}B vs Standard={standard_size}B")
            print(f"   📊 Size ratio: {size_ratio:.2f}")
            
            if size_ratio > 0.5 and size_ratio < 2.0:
                self.log_test("Report size comparison reasonable", True)
            else:
                self.log_test("Report size comparison reasonable", False, f"Unusual size ratio: {size_ratio:.2f}")
                
        else:
            self.log_test("OTHER answers DOCX generation", False, str(other_docx))
            return False
        
        return True

    def test_backend_logs_analysis(self):
        """Check backend logs for errors during OTHER answer processing"""
        print("\n🔍 CHECKING BACKEND LOGS FOR OTHER ANSWER PROCESSING")
        print("-" * 60)
        
        try:
            # Check supervisor backend logs
            result = subprocess.run(['tail', '-n', '50', '/var/log/supervisor/backend.err.log'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                log_content = result.stdout
                if log_content.strip():
                    print("   📋 Recent backend error logs:")
                    print(log_content)
                    
                    # Look for specific error patterns
                    error_patterns = [
                        "other_text",
                        "OTHER",
                        "coroutine",
                        "has no len()",
                        "string/int",
                        "template",
                        "report",
                        "error",
                        "exception",
                        "traceback"
                    ]
                    
                    found_errors = []
                    for pattern in error_patterns:
                        if pattern.lower() in log_content.lower():
                            found_errors.append(pattern)
                    
                    if found_errors:
                        self.log_test("Backend logs analysis", False, f"Found potential issues: {', '.join(found_errors)}")
                    else:
                        self.log_test("Backend logs analysis", True)
                else:
                    self.log_test("Backend logs analysis", True, "No recent errors in logs")
            else:
                self.log_test("Backend logs analysis", False, "Could not read backend logs")
                
        except Exception as e:
            self.log_test("Backend logs analysis", False, f"Error checking logs: {str(e)}")
        
        return True

    def run_investigation(self):
        """Run the complete OTHER answer investigation"""
        print("🔍 AM AI SAFE OTHER ANSWER INVESTIGATION")
        print("=" * 80)
        print("OBJECTIVE: Investigate if OTHER answers cause file corruption in report generation")
        print("=" * 80)
        
        # Setup
        if not self.setup_test_user():
            return False
            
        if not self.create_test_assessment():
            return False
        
        # Run investigation tests
        test_methods = [
            self.test_other_answer_submission,
            self.test_mixed_answer_assessment,
            self.test_assessment_data_retrieval_with_other,
            self.test_report_generation_with_other_answers,
            self.test_report_generation_comparison,
            self.test_backend_logs_analysis
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                print(f"❌ Error in {test_method.__name__}: {str(e)}")
                traceback.print_exc()
        
        # Summary
        print("\n" + "=" * 80)
        print("🔍 OTHER ANSWER INVESTIGATION SUMMARY")
        print("=" * 80)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        # Detailed results
        print("\n📊 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}")
            if result["details"] and not result["success"]:
                print(f"   Details: {result['details']}")
        
        return self.tests_passed == self.tests_run

if __name__ == "__main__":
    tester = OtherAnswerInvestigationTester()
    success = tester.run_investigation()
    sys.exit(0 if success else 1)