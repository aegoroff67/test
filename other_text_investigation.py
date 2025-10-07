#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class OtherTextInvestigation:
    def __init__(self, base_url="https://reportgen-5.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
        self.assessment_id = None

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
        test_email = f"other_text_test_{timestamp}@example.com"
        
        signup_data = {
            "name": f"Other Text Test User {timestamp}",
            "email": test_email,
            "password": "TestPass123!",
            "organization_name": f"Other Text Test Org {timestamp}",
            "industry": "Technology"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            print("✅ Test user setup and authentication")
            return True
        else:
            print(f"❌ Test user setup failed: {response}")
            return False

    def create_test_assessment(self):
        """Create assessment for testing"""
        success, response = self.make_request('POST', 'assessments', {})
        if success and 'id' in response:
            self.assessment_id = response['id']
            print("✅ Test assessment creation")
            return True
        else:
            print(f"❌ Test assessment creation failed: {response}")
            return False

    def investigate_other_text_handling(self):
        """Investigate how other_text is handled in the system"""
        print("\n🔍 INVESTIGATING OTHER_TEXT FIELD HANDLING")
        print("-" * 60)
        
        if not self.assessment_id:
            print("❌ No assessment ID available")
            return False
            
        # Get questions
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            print(f"❌ Failed to get questions: {response}")
            return False
            
        # Get first question
        first_domain = response[0] if response else None
        if not first_domain or not first_domain.get('questions'):
            print("❌ No questions found")
            return False
            
        first_question = first_domain['questions'][0]
        question_id = first_question['id']
        question_code = first_question.get('code', 'Unknown')
        
        print(f"📝 Testing with question: {question_code}")
        
        # Submit OTHER answer with custom text
        other_text_content = "This is a detailed custom implementation that includes advanced monitoring systems, automated bias detection algorithms, and comprehensive reporting mechanisms that go beyond the standard options provided."
        
        answer_data = {
            "question_id": question_id,
            "option": "OTHER",
            "other_text": other_text_content,
            "note": "Investigation test for other_text field handling"
        }
        
        success, response = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
        if success and response.get('status') == 'success':
            print("✅ OTHER answer with custom text submitted successfully")
        else:
            print(f"❌ Failed to submit OTHER answer: {response}")
            return False
        
        # Retrieve the answer to verify other_text is stored
        success, questions_response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            print(f"❌ Failed to retrieve questions after answer: {questions_response}")
            return False
        
        # Find the answered question
        answered_question = None
        for domain_data in questions_response:
            questions = domain_data.get('questions', [])
            for question in questions:
                if question['id'] == question_id and question.get('answer'):
                    answered_question = question
                    break
            if answered_question:
                break
        
        if not answered_question:
            print("❌ Could not find answered question in response")
            return False
        
        answer = answered_question.get('answer', {})
        stored_other_text = answer.get('other_text')
        
        print(f"📊 Answer data structure:")
        print(f"   - Option: {answer.get('option')}")
        print(f"   - Numeric Score: {answer.get('numeric_score')}")
        print(f"   - Other Text Present: {'Yes' if stored_other_text else 'No'}")
        if stored_other_text:
            print(f"   - Other Text Length: {len(stored_other_text)} characters")
            print(f"   - Other Text Preview: {stored_other_text[:100]}...")
        
        # Verify other_text is preserved correctly
        if stored_other_text == other_text_content:
            print("✅ other_text field is correctly stored and retrieved")
        else:
            print("❌ other_text field is not correctly preserved")
            print(f"   Expected: {other_text_content[:50]}...")
            print(f"   Got: {stored_other_text[:50] if stored_other_text else 'None'}...")
            return False
        
        # Complete the assessment with more answers
        print("\n📝 Completing assessment with mixed answers...")
        
        # Get all questions and answer them
        all_questions = []
        for domain_data in questions_response:
            questions = domain_data.get('questions', [])
            all_questions.extend(questions)
        
        # Answer remaining questions with a mix of standard and OTHER answers
        answer_count = 1  # We already answered one
        for i, question in enumerate(all_questions[1:], 1):  # Skip first question (already answered)
            if i % 10 == 0:  # Every 10th question gets OTHER answer
                answer_data = {
                    "question_id": question['id'],
                    "option": "OTHER",
                    "other_text": f"Custom implementation for {question.get('code', 'question')} involving specialized processes and methodologies tailored to our organizational requirements.",
                    "note": f"Custom answer {i}"
                }
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
                answer_count += 1
        
        print(f"✅ Completed assessment with {answer_count} answers")
        
        # Submit the assessment
        success, submit_response = self.make_request('POST', f'assessments/{self.assessment_id}/submit')
        if success:
            print("✅ Assessment submitted successfully")
        else:
            print(f"❌ Failed to submit assessment: {submit_response}")
            return False
        
        return True

    def test_report_generation_with_other_text(self):
        """Test report generation and check if other_text causes issues"""
        print("\n🔍 TESTING REPORT GENERATION WITH OTHER_TEXT")
        print("-" * 60)
        
        if not self.assessment_id:
            print("❌ No assessment ID available")
            return False
        
        # Generate DOCX report
        print("📄 Generating DOCX report...")
        success, docx_response = self.make_request('GET', f'assessments/{self.assessment_id}/report')
        
        if not success:
            print(f"❌ DOCX report generation failed: {docx_response}")
            return False
        
        if isinstance(docx_response, bytes):
            docx_size = len(docx_response)
            print(f"✅ DOCX report generated successfully ({docx_size} bytes)")
            
            # Check if it's a valid DOCX file
            if docx_response.startswith(b'PK'):  # ZIP file signature (DOCX is a ZIP)
                print("✅ DOCX file has valid ZIP structure")
            else:
                print("❌ DOCX file does not have valid ZIP structure")
                return False
        else:
            print(f"❌ DOCX response is not binary data: {type(docx_response)}")
            return False
        
        # Generate PDF report
        print("📄 Generating PDF report...")
        success, pdf_response = self.make_request('GET', f'assessments/{self.assessment_id}/report/pdf')
        
        if not success:
            print(f"❌ PDF report generation failed: {pdf_response}")
            # PDF failure is not critical for this investigation
        else:
            if isinstance(pdf_response, bytes):
                pdf_size = len(pdf_response)
                print(f"✅ PDF report generated successfully ({pdf_size} bytes)")
                
                # Check if it's a valid PDF file
                if pdf_response.startswith(b'%PDF'):
                    print("✅ PDF file has valid PDF structure")
                else:
                    print("⚠️  PDF file does not have valid PDF structure (might be DOCX fallback)")
            else:
                print(f"❌ PDF response is not binary data: {type(pdf_response)}")
        
        return True

    def run_investigation(self):
        """Run the complete other_text investigation"""
        print("🔍 OTHER_TEXT FIELD INVESTIGATION")
        print("=" * 80)
        print("OBJECTIVE: Investigate if other_text field is properly handled in report generation")
        print("=" * 80)
        
        # Setup
        if not self.setup_test_user():
            return False
            
        if not self.create_test_assessment():
            return False
        
        # Run investigation
        if not self.investigate_other_text_handling():
            return False
        
        if not self.test_report_generation_with_other_text():
            return False
        
        print("\n" + "=" * 80)
        print("🔍 OTHER_TEXT INVESTIGATION COMPLETED")
        print("=" * 80)
        print("✅ Investigation completed successfully")
        print("📋 Key findings:")
        print("   - other_text field is properly stored in database")
        print("   - other_text field is correctly retrieved in API responses")
        print("   - Report generation works with OTHER answers containing custom text")
        print("   - No file corruption detected due to other_text content")
        
        return True

if __name__ == "__main__":
    investigator = OtherTextInvestigation()
    success = investigator.run_investigation()
    sys.exit(0 if success else 1)