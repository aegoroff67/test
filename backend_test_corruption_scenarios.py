#!/usr/bin/env python3

"""
DOCX Corruption Scenarios Test
Tests specific scenarios that might cause DOCX corruption in real API calls.
"""

import requests
import sys
import json
import asyncio
import traceback
from datetime import datetime
import zipfile
import io
import os
import tempfile
from pathlib import Path

# Add backend to path for direct imports
sys.path.append('/app/backend')

class CorruptionScenariosTest:
    def __init__(self, base_url="https://reportgen-5.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
        self.tests_run = 0
        self.tests_passed = 0
        self.corruption_scenarios = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")

    def log_corruption_finding(self, scenario, finding):
        """Log corruption finding"""
        self.corruption_scenarios.append({
            "scenario": scenario,
            "finding": finding,
            "timestamp": datetime.now().isoformat()
        })
        print(f"🚨 CORRUPTION [{scenario}]: {finding}")

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

    def setup_test_user(self):
        """Set up test user"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"corruption_test_{timestamp}@vciso.one"
        
        signup_data = {
            "name": f"Corruption Test User {timestamp}",
            "email": test_email,
            "password": "CorruptionTest123!",
            "organization_name": "vCISO.One",
            "industry": "Cybersecurity Consulting"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            return True
        return False

    def test_scenario_template_injection(self):
        """Test Scenario 1: Template injection in OTHER answers"""
        print("\n🔍 SCENARIO 1: Template Injection in OTHER Answers")
        print("-" * 60)
        
        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            return False
        assessment_id = response['id']
        
        # Get questions
        success, response = self.make_request('GET', f'assessments/{assessment_id}/questions')
        if not success:
            return False
        
        # Answer with template injection attempts
        template_injection_answers = [
            "{{org.name}} - This might break template processing",
            "{% for item in items %}This is a loop{% endfor %}",
            "{{assets.heatmapUrl}} - Direct template variable reference",
            "{{actions.high}} - Action reference that might cause issues",
            "{{ malicious_code }} - Undefined variable reference"
        ]
        
        question_count = 0
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for i, question in enumerate(questions[:5]):  # Test first 5 questions
                injection_text = template_injection_answers[i % len(template_injection_answers)]
                
                answer_data = {
                    "question_id": question['id'],
                    "option": "OTHER",
                    "other_text": injection_text,
                    "note": f"Template injection test {i+1}"
                }
                
                success, _ = self.make_request('POST', f'assessments/{assessment_id}/answer', answer_data)
                if success:
                    question_count += 1
                else:
                    self.log_corruption_finding("TEMPLATE_INJECTION", f"Failed to submit answer with: {injection_text}")
        
        # Complete remaining questions with normal answers
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for question in questions[5:]:  # Skip first 5 already answered
                answer_data = {
                    "question_id": question['id'],
                    "option": "GOOD",
                    "note": "Normal answer"
                }
                success, _ = self.make_request('POST', f'assessments/{assessment_id}/answer', answer_data)
                if success:
                    question_count += 1
        
        # Submit assessment
        success, _ = self.make_request('POST', f'assessments/{assessment_id}/submit')
        if not success:
            self.log_corruption_finding("TEMPLATE_INJECTION", "Failed to submit assessment")
            return False
        
        # Generate report and check for corruption
        success, response = self.make_request('GET', f'assessments/{assessment_id}/report', stream=True)
        if success:
            docx_bytes = response.content
            corruption_detected = self.analyze_docx_for_corruption(docx_bytes, "TEMPLATE_INJECTION")
            
            if corruption_detected:
                self.log_corruption_finding("TEMPLATE_INJECTION", "DOCX corruption detected with template injection")
            else:
                print("✅ Template injection handled correctly - no corruption")
                
            return True
        else:
            self.log_corruption_finding("TEMPLATE_INJECTION", f"Report generation failed: {response}")
            return False

    def test_scenario_unicode_characters(self):
        """Test Scenario 2: Unicode characters in OTHER answers"""
        print("\n🔍 SCENARIO 2: Unicode Characters in OTHER Answers")
        print("-" * 60)
        
        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            return False
        assessment_id = response['id']
        
        # Get questions
        success, response = self.make_request('GET', f'assessments/{assessment_id}/questions')
        if not success:
            return False
        
        # Answer with various unicode characters
        unicode_answers = [
            "中文测试 - Chinese characters that might cause encoding issues",
            "العربية - Arabic text with right-to-left direction",
            "русский язык - Cyrillic characters",
            "🚀🔥💯 - Emoji characters that might break XML",
            "àáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ - Extended Latin characters",
            "∑∏∆∇∂∫∞≠≤≥±×÷ - Mathematical symbols",
            "♠♣♥♦♪♫☀☁☂☃ - Special symbols"
        ]
        
        question_count = 0
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for i, question in enumerate(questions[:7]):  # Test first 7 questions
                unicode_text = unicode_answers[i % len(unicode_answers)]
                
                answer_data = {
                    "question_id": question['id'],
                    "option": "OTHER",
                    "other_text": unicode_text,
                    "note": f"Unicode test {i+1}"
                }
                
                success, _ = self.make_request('POST', f'assessments/{assessment_id}/answer', answer_data)
                if success:
                    question_count += 1
                else:
                    self.log_corruption_finding("UNICODE", f"Failed to submit answer with: {unicode_text[:50]}")
        
        # Complete remaining questions
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for question in questions[7:]:
                answer_data = {
                    "question_id": question['id'],
                    "option": "BASIC",
                    "note": "Normal answer"
                }
                success, _ = self.make_request('POST', f'assessments/{assessment_id}/answer', answer_data)
                if success:
                    question_count += 1
        
        # Submit and generate report
        success, _ = self.make_request('POST', f'assessments/{assessment_id}/submit')
        if not success:
            return False
        
        success, response = self.make_request('GET', f'assessments/{assessment_id}/report', stream=True)
        if success:
            docx_bytes = response.content
            corruption_detected = self.analyze_docx_for_corruption(docx_bytes, "UNICODE")
            
            if corruption_detected:
                self.log_corruption_finding("UNICODE", "DOCX corruption detected with unicode characters")
            else:
                print("✅ Unicode characters handled correctly - no corruption")
                
            return True
        else:
            self.log_corruption_finding("UNICODE", f"Report generation failed: {response}")
            return False

    def test_scenario_xml_html_injection(self):
        """Test Scenario 3: XML/HTML injection in OTHER answers"""
        print("\n🔍 SCENARIO 3: XML/HTML Injection in OTHER Answers")
        print("-" * 60)
        
        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            return False
        assessment_id = response['id']
        
        # Get questions
        success, response = self.make_request('GET', f'assessments/{assessment_id}/questions')
        if not success:
            return False
        
        # Answer with XML/HTML injection attempts
        xml_html_answers = [
            "<script>alert('XSS')</script> - JavaScript injection attempt",
            "<xml><malicious>content</malicious></xml> - XML injection",
            "<?xml version='1.0'?><root>XML declaration</root>",
            "<![CDATA[CDATA section that might break parsing]]>",
            "&lt;&gt;&amp;&quot;&apos; - HTML entities",
            "<!-- HTML comment --> <div>HTML content</div>",
            "<w:p><w:r><w:t>Direct Word XML injection</w:t></w:r></w:p>"
        ]
        
        question_count = 0
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for i, question in enumerate(questions[:7]):  # Test first 7 questions
                xml_text = xml_html_answers[i % len(xml_html_answers)]
                
                answer_data = {
                    "question_id": question['id'],
                    "option": "OTHER",
                    "other_text": xml_text,
                    "note": f"XML/HTML injection test {i+1}"
                }
                
                success, _ = self.make_request('POST', f'assessments/{assessment_id}/answer', answer_data)
                if success:
                    question_count += 1
                else:
                    self.log_corruption_finding("XML_HTML", f"Failed to submit answer with: {xml_text[:50]}")
        
        # Complete remaining questions
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for question in questions[7:]:
                answer_data = {
                    "question_id": question['id'],
                    "option": "NON_IDEAL",
                    "note": "Normal answer"
                }
                success, _ = self.make_request('POST', f'assessments/{assessment_id}/answer', answer_data)
                if success:
                    question_count += 1
        
        # Submit and generate report
        success, _ = self.make_request('POST', f'assessments/{assessment_id}/submit')
        if not success:
            return False
        
        success, response = self.make_request('GET', f'assessments/{assessment_id}/report', stream=True)
        if success:
            docx_bytes = response.content
            corruption_detected = self.analyze_docx_for_corruption(docx_bytes, "XML_HTML")
            
            if corruption_detected:
                self.log_corruption_finding("XML_HTML", "DOCX corruption detected with XML/HTML injection")
            else:
                print("✅ XML/HTML injection handled correctly - no corruption")
                
            return True
        else:
            self.log_corruption_finding("XML_HTML", f"Report generation failed: {response}")
            return False

    def test_scenario_large_content(self):
        """Test Scenario 4: Very large content in OTHER answers"""
        print("\n🔍 SCENARIO 4: Large Content in OTHER Answers")
        print("-" * 60)
        
        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if not success:
            return False
        assessment_id = response['id']
        
        # Get questions
        success, response = self.make_request('GET', f'assessments/{assessment_id}/questions')
        if not success:
            return False
        
        # Create very large content
        large_content = "This is a very long answer that contains a lot of text. " * 200  # ~11KB
        very_large_content = "Extremely long content with repeated text. " * 500  # ~21KB
        
        large_answers = [
            large_content,
            very_large_content,
            "A" * 5000,  # 5KB of A's
            "Mixed content: " + "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 100,
            "Numbers: " + " ".join([str(i) for i in range(1000)])  # Lots of numbers
        ]
        
        question_count = 0
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for i, question in enumerate(questions[:5]):  # Test first 5 questions
                large_text = large_answers[i % len(large_answers)]
                
                answer_data = {
                    "question_id": question['id'],
                    "option": "OTHER",
                    "other_text": large_text,
                    "note": f"Large content test {i+1} - {len(large_text)} characters"
                }
                
                success, _ = self.make_request('POST', f'assessments/{assessment_id}/answer', answer_data)
                if success:
                    question_count += 1
                    print(f"   ✅ Submitted {len(large_text):,} character answer")
                else:
                    self.log_corruption_finding("LARGE_CONTENT", f"Failed to submit large answer ({len(large_text)} chars)")
        
        # Complete remaining questions
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for question in questions[5:]:
                answer_data = {
                    "question_id": question['id'],
                    "option": "IDEAL",
                    "note": "Normal answer"
                }
                success, _ = self.make_request('POST', f'assessments/{assessment_id}/answer', answer_data)
                if success:
                    question_count += 1
        
        # Submit and generate report
        success, _ = self.make_request('POST', f'assessments/{assessment_id}/submit')
        if not success:
            return False
        
        success, response = self.make_request('GET', f'assessments/{assessment_id}/report', stream=True)
        if success:
            docx_bytes = response.content
            print(f"   Generated DOCX size: {len(docx_bytes):,} bytes")
            
            corruption_detected = self.analyze_docx_for_corruption(docx_bytes, "LARGE_CONTENT")
            
            if corruption_detected:
                self.log_corruption_finding("LARGE_CONTENT", "DOCX corruption detected with large content")
            else:
                print("✅ Large content handled correctly - no corruption")
                
            return True
        else:
            self.log_corruption_finding("LARGE_CONTENT", f"Report generation failed: {response}")
            return False

    def analyze_docx_for_corruption(self, docx_bytes, scenario):
        """Analyze DOCX bytes for corruption indicators"""
        if not docx_bytes:
            self.log_corruption_finding(scenario, "Empty DOCX file received")
            return True
        
        try:
            # Check if it's a valid ZIP file
            with zipfile.ZipFile(io.BytesIO(docx_bytes), 'r') as zip_file:
                file_list = zip_file.namelist()
                
                # Check for essential files
                essential_files = ['word/document.xml', '[Content_Types].xml']
                missing_files = [f for f in essential_files if f not in file_list]
                
                if missing_files:
                    self.log_corruption_finding(scenario, f"Missing essential files: {missing_files}")
                    return True
                
                # Check document.xml for corruption
                try:
                    document_xml = zip_file.read('word/document.xml')
                    document_text = document_xml.decode('utf-8', errors='ignore')
                    
                    # Check for unprocessed template variables
                    if '{{' in document_text or '}}' in document_text:
                        self.log_corruption_finding(scenario, "Unprocessed template variables found")
                        return True
                    
                    # Check for malformed XML
                    if not document_text.startswith('<?xml'):
                        self.log_corruption_finding(scenario, "Document.xml doesn't start with XML declaration")
                        return True
                    
                    # Check for specific corruption patterns
                    corruption_patterns = [
                        'undefined',
                        'null',
                        'NaN',
                        'error',
                        'exception',
                        'traceback'
                    ]
                    
                    for pattern in corruption_patterns:
                        if pattern.lower() in document_text.lower():
                            self.log_corruption_finding(scenario, f"Found corruption pattern: {pattern}")
                            return True
                    
                    print(f"   📄 Document.xml size: {len(document_xml):,} bytes")
                    print(f"   📁 ZIP contains {len(file_list)} files")
                    
                    return False  # No corruption detected
                    
                except Exception as e:
                    self.log_corruption_finding(scenario, f"Error reading document.xml: {str(e)}")
                    return True
                    
        except zipfile.BadZipFile:
            self.log_corruption_finding(scenario, "File is not a valid ZIP/DOCX file")
            return True
        except Exception as e:
            self.log_corruption_finding(scenario, f"Error analyzing DOCX: {str(e)}")
            return True

    def run_all_corruption_scenarios(self):
        """Run all corruption scenario tests"""
        print("=" * 80)
        print("DOCX CORRUPTION SCENARIOS TEST")
        print("=" * 80)
        print(f"Target: {self.base_url}")
        print(f"Started: {datetime.now().isoformat()}")
        
        # Setup
        if not self.setup_test_user():
            print("❌ Failed to set up test user")
            return False
        
        print(f"✅ Test user created: {self.user_data.get('organization_name')}")
        
        # Run scenarios
        scenarios = [
            ("Template Injection", self.test_scenario_template_injection),
            ("Unicode Characters", self.test_scenario_unicode_characters),
            ("XML/HTML Injection", self.test_scenario_xml_html_injection),
            ("Large Content", self.test_scenario_large_content)
        ]
        
        for scenario_name, scenario_func in scenarios:
            try:
                print(f"\n{'='*20} {scenario_name} {'='*20}")
                success = scenario_func()
                if success:
                    print(f"✅ {scenario_name} completed successfully")
                else:
                    print(f"❌ {scenario_name} failed")
            except Exception as e:
                print(f"❌ {scenario_name} crashed: {str(e)}")
                traceback.print_exc()
        
        # Generate final report
        self.generate_corruption_report()
        
        return True

    def generate_corruption_report(self):
        """Generate final corruption analysis report"""
        print("\n" + "=" * 80)
        print("CORRUPTION ANALYSIS REPORT")
        print("=" * 80)
        
        print(f"\n📊 TEST SUMMARY:")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        print(f"\n🚨 CORRUPTION FINDINGS:")
        if self.corruption_scenarios:
            for finding in self.corruption_scenarios:
                print(f"  • [{finding['scenario']}] {finding['finding']}")
        else:
            print("  ✅ No corruption detected in any scenario")
        
        print(f"\n🎯 ANALYSIS:")
        
        # Analyze corruption patterns
        scenarios_with_corruption = set([f['scenario'] for f in self.corruption_scenarios])
        
        if scenarios_with_corruption:
            print(f"Scenarios with corruption: {', '.join(scenarios_with_corruption)}")
            
            # Identify most problematic scenario
            scenario_counts = {}
            for finding in self.corruption_scenarios:
                scenario = finding['scenario']
                scenario_counts[scenario] = scenario_counts.get(scenario, 0) + 1
            
            most_problematic = max(scenario_counts.items(), key=lambda x: x[1])
            print(f"Most problematic scenario: {most_problematic[0]} ({most_problematic[1]} issues)")
        else:
            print("✅ All scenarios handled correctly - no corruption detected")
            print("The DOCX generation system appears to be robust against common corruption causes")
        
        print(f"\n📋 RECOMMENDATIONS:")
        if self.corruption_scenarios:
            print("1. Focus on fixing the scenarios that showed corruption")
            print("2. Implement additional input validation for OTHER answers")
            print("3. Add template variable escaping to prevent injection")
            print("4. Improve unicode handling in document generation")
            print("5. Add content size limits for OTHER answers")
        else:
            print("1. Current system appears robust - continue monitoring")
            print("2. Consider adding automated corruption detection")
            print("3. Implement regular testing with edge cases")
        
        print(f"\n⏰ Analysis completed: {datetime.now().isoformat()}")


def main():
    """Main execution function"""
    tester = CorruptionScenariosTest()
    
    try:
        success = tester.run_all_corruption_scenarios()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()