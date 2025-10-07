#!/usr/bin/env python3

"""
NaN Investigation Test
Investigates the NaN corruption issue found in DOCX files.
"""

import requests
import sys
import json
import zipfile
import io
from datetime import datetime

class NaNInvestigator:
    def __init__(self, base_url="https://reportgen-5.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
        self.assessment_id = None

    def make_request(self, method, endpoint, data=None, expected_status=200, stream=False):
        """Make API request with error handling"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, stream=stream)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, stream=stream)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            
            if stream:
                return success, response
            else:
                return success, response.json() if success and response.content else response.text

        except Exception as e:
            return False, str(e)

    def setup_and_complete_assessment(self):
        """Set up user and complete assessment"""
        print("🔧 Setting up test environment...")
        
        # Create user
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"nan_test_{timestamp}@vciso.one"
        
        signup_data = {
            "name": f"NaN Test User {timestamp}",
            "email": test_email,
            "password": "NaNTest123!",
            "organization_name": "vCISO.One",
            "industry": "Cybersecurity Consulting"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            print(f"✅ Created user: {self.user_data.get('organization_name')}")
        else:
            print(f"❌ Failed to create user: {response}")
            return False

        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if success and 'id' in response:
            self.assessment_id = response['id']
            print(f"✅ Created assessment: {self.assessment_id}")
        else:
            print(f"❌ Failed to create assessment: {response}")
            return False

        # Complete assessment with simple answers
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            print(f"❌ Failed to get questions: {response}")
            return False

        # Answer all questions with a simple pattern
        question_count = 0
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for question in questions:
                # Simple pattern: IDEAL, GOOD, BASIC, NON_IDEAL
                options = ["IDEAL", "GOOD", "BASIC", "NON_IDEAL"]
                option = options[question_count % 4]
                
                answer_data = {
                    "question_id": question['id'],
                    "option": option,
                    "note": f"Test answer {question_count + 1}"
                }

                success, _ = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
                if success:
                    question_count += 1

        print(f"✅ Answered {question_count} questions")

        # Submit assessment
        success, _ = self.make_request('POST', f'assessments/{self.assessment_id}/submit')
        if success:
            print("✅ Assessment submitted")
            return True
        else:
            print(f"❌ Failed to submit assessment: {_}")
            return False

    def investigate_nan_issue(self):
        """Investigate the NaN issue in generated DOCX"""
        print("\n🔍 INVESTIGATING NaN ISSUE")
        print("-" * 60)
        
        # Generate DOCX report
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/report', stream=True)
        
        if not success:
            print(f"❌ Failed to generate report: {response}")
            return False
        
        docx_bytes = response.content
        print(f"✅ Generated DOCX: {len(docx_bytes):,} bytes")
        
        # Analyze DOCX content
        try:
            with zipfile.ZipFile(io.BytesIO(docx_bytes), 'r') as zip_file:
                # Read document.xml
                doc_xml = zip_file.read('word/document.xml').decode('utf-8', errors='ignore')
                
                # Find all NaN occurrences
                nan_positions = []
                start = 0
                while True:
                    pos = doc_xml.find('NaN', start)
                    if pos == -1:
                        break
                    
                    # Get context around NaN (200 chars before and after)
                    context_start = max(0, pos - 200)
                    context_end = min(len(doc_xml), pos + 200)
                    context = doc_xml[context_start:context_end]
                    
                    nan_positions.append({
                        'position': pos,
                        'context': context,
                        'before': doc_xml[context_start:pos],
                        'after': doc_xml[pos+3:context_end]
                    })
                    start = pos + 1
                
                print(f"🚨 Found {len(nan_positions)} NaN occurrences in document.xml")
                
                # Analyze each NaN occurrence
                for i, nan_info in enumerate(nan_positions[:10]):  # Show first 10
                    print(f"\n--- NaN Occurrence #{i+1} (Position {nan_info['position']}) ---")
                    
                    # Look for patterns around NaN
                    before = nan_info['before'][-100:]  # Last 100 chars before NaN
                    after = nan_info['after'][:100]     # First 100 chars after NaN
                    
                    print(f"Before: ...{before}")
                    print(f"After:  {after}...")
                    
                    # Check if it's in a specific XML element
                    if '<w:t>' in before and '</w:t>' in after:
                        print("   🎯 NaN is inside a text element")
                    
                    # Look for numeric patterns
                    import re
                    numbers_before = re.findall(r'\d+\.?\d*', before)
                    numbers_after = re.findall(r'\d+\.?\d*', after)
                    
                    if numbers_before:
                        print(f"   Numbers before: {numbers_before}")
                    if numbers_after:
                        print(f"   Numbers after: {numbers_after}")
                
                # Check for other corruption indicators
                corruption_indicators = [
                    ('undefined', 'JavaScript undefined values'),
                    ('null', 'Null values'),
                    ('Infinity', 'Infinity values'),
                    ('-Infinity', 'Negative infinity values'),
                    ('{{', 'Unprocessed template variables'),
                    ('}}', 'Unprocessed template variables'),
                ]
                
                print(f"\n🔍 CHECKING FOR OTHER CORRUPTION INDICATORS:")
                for indicator, description in corruption_indicators:
                    count = doc_xml.count(indicator)
                    if count > 0:
                        print(f"   🚨 Found {count} occurrences of '{indicator}' ({description})")
                        
                        # Show first few occurrences
                        start = 0
                        for j in range(min(3, count)):
                            pos = doc_xml.find(indicator, start)
                            if pos != -1:
                                context_start = max(0, pos - 50)
                                context_end = min(len(doc_xml), pos + 50)
                                context = doc_xml[context_start:context_end]
                                print(f"      {j+1}. ...{context}...")
                                start = pos + 1
                    else:
                        print(f"   ✅ No '{indicator}' found")
                
                # Save the document.xml for further analysis
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                xml_filename = f"/tmp/document_with_nan_{timestamp}.xml"
                with open(xml_filename, 'w', encoding='utf-8') as f:
                    f.write(doc_xml)
                print(f"\n💾 Saved document.xml to: {xml_filename}")
                
                return len(nan_positions) > 0
                
        except Exception as e:
            print(f"❌ Error analyzing DOCX: {str(e)}")
            return False

    def get_assessment_data_for_analysis(self):
        """Get assessment data to understand where NaN might be coming from"""
        print("\n🔍 ANALYZING ASSESSMENT DATA")
        print("-" * 60)
        
        # Get assessment summary
        success, summary = self.make_request('GET', f'assessments/{self.assessment_id}/summary')
        if success:
            print("📊 Assessment Summary:")
            print(f"   Overall percentage: {summary.get('overall_percentage')}")
            print(f"   Overall maturity: {summary.get('overall_maturity')}")
            print(f"   Total questions: {summary.get('total_questions')}")
            print(f"   Answered questions: {summary.get('answered_questions')}")
            
            domain_scores = summary.get('domain_scores', [])
            print(f"   Domain scores: {len(domain_scores)} domains")
            
            # Check for NaN in domain scores
            for domain in domain_scores:
                domain_name = domain.get('domain_name', 'Unknown')
                percentage = domain.get('percentage', 0)
                score = domain.get('score', 0)
                max_score = domain.get('max_score', 0)
                
                print(f"      {domain_name}: {percentage}% ({score}/{max_score})")
                
                # Check for NaN values
                if str(percentage) == 'nan' or str(score) == 'nan' or str(max_score) == 'nan':
                    print(f"         🚨 NaN detected in {domain_name} domain!")
                
                # Check for division by zero scenarios
                if max_score == 0 and score > 0:
                    print(f"         ⚠️  Potential division by zero in {domain_name}")
        else:
            print(f"❌ Failed to get summary: {summary}")
        
        # Get assessment questions and answers
        success, questions = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if success:
            print(f"\n📋 Assessment Questions: {len(questions)} domains")
            
            for domain_data in questions:
                domain_name = domain_data.get('domain', {}).get('name', 'Unknown')
                domain_questions = domain_data.get('questions', [])
                
                answered_count = sum(1 for q in domain_questions if q.get('answer'))
                total_count = len(domain_questions)
                
                print(f"   {domain_name}: {answered_count}/{total_count} answered")
                
                # Check for problematic answers
                for question in domain_questions:
                    answer = question.get('answer')
                    if answer:
                        numeric_score = answer.get('numeric_score')
                        if str(numeric_score) == 'nan':
                            print(f"      🚨 NaN score in question {question.get('code', 'N/A')}")
        else:
            print(f"❌ Failed to get questions: {questions}")

    def run_investigation(self):
        """Run the complete NaN investigation"""
        print("=" * 80)
        print("NaN CORRUPTION INVESTIGATION")
        print("=" * 80)
        print(f"Target: {self.base_url}")
        print(f"Started: {datetime.now().isoformat()}")
        
        # Setup and complete assessment
        if not self.setup_and_complete_assessment():
            print("❌ Failed to set up test environment")
            return False
        
        # Get assessment data for analysis
        self.get_assessment_data_for_analysis()
        
        # Investigate NaN issue
        nan_found = self.investigate_nan_issue()
        
        # Final report
        print("\n" + "=" * 80)
        print("INVESTIGATION RESULTS")
        print("=" * 80)
        
        if nan_found:
            print("🚨 CRITICAL FINDING: NaN values detected in generated DOCX")
            print("   This confirms the corruption issue reported by the user")
            print("   The NaN values are likely caused by:")
            print("   1. Division by zero in percentage calculations")
            print("   2. Invalid numeric operations in report generation")
            print("   3. Missing or null data in assessment calculations")
            print("\n📋 RECOMMENDED ACTIONS:")
            print("   1. Fix division by zero errors in percentage calculations")
            print("   2. Add null/undefined checks in numeric operations")
            print("   3. Implement proper error handling for edge cases")
            print("   4. Add validation for assessment data before report generation")
        else:
            print("✅ No NaN values detected in this test")
            print("   The corruption may be intermittent or data-dependent")
            print("   Continue monitoring with different test scenarios")
        
        print(f"\n⏰ Investigation completed: {datetime.now().isoformat()}")
        return True


def main():
    """Main execution function"""
    investigator = NaNInvestigator()
    
    try:
        success = investigator.run_investigation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Investigation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Investigation failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()