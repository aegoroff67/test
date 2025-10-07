#!/usr/bin/env python3

"""
Direct API vs Database Comparison Test
This test directly compares API-generated DOCX with database-generated DOCX using the same data.
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

class DirectComparisonTester:
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

    def setup_test_environment(self):
        """Set up test user and complete assessment"""
        print("🔧 Setting up test environment...")
        
        # Create user
        timestamp = datetime.now().strftime('%H%M%S')
        test_email = f"direct_test_{timestamp}@vciso.one"
        
        signup_data = {
            "name": f"Direct Test User {timestamp}",
            "email": test_email,
            "password": "DirectTest123!",
            "organization_name": "vCISO.One",
            "industry": "Cybersecurity Consulting"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data)
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response['user']
            self.log_test("Create test user", True)
        else:
            self.log_test("Create test user", False, str(response))
            return False

        # Create assessment
        success, response = self.make_request('POST', 'assessments', {})
        if success and 'id' in response:
            self.assessment_id = response['id']
            self.log_test("Create assessment", True)
        else:
            self.log_test("Create assessment", False, str(response))
            return False

        # Complete assessment with specific patterns
        success = self.complete_assessment_with_test_patterns()
        if success:
            self.log_test("Complete assessment", True)
        else:
            self.log_test("Complete assessment", False)
            return False

        return True

    def complete_assessment_with_test_patterns(self):
        """Complete assessment with specific test patterns"""
        # Get all questions
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/questions')
        if not success:
            return False

        # Answer all questions with a mix of patterns
        question_count = 0
        for domain_data in response:
            questions = domain_data.get('questions', [])
            for question in questions:
                # Use different answer patterns
                if question_count % 4 == 0:
                    option = "IDEAL"
                    note = "Comprehensive implementation with best practices"
                elif question_count % 4 == 1:
                    option = "GOOD"
                    note = "Solid implementation with room for improvement"
                elif question_count % 4 == 2:
                    option = "BASIC"
                    note = "Basic implementation with gaps"
                else:
                    option = "NON_IDEAL"
                    note = "Limited implementation"
                
                answer_data = {
                    "question_id": question['id'],
                    "option": option,
                    "note": note
                }

                success, _ = self.make_request('POST', f'assessments/{self.assessment_id}/answer', answer_data)
                if success:
                    question_count += 1

        # Submit assessment
        success, _ = self.make_request('POST', f'assessments/{self.assessment_id}/submit')
        return success and question_count > 0

    async def test_direct_database_generation(self):
        """Test direct database-based report generation"""
        print("🔍 Testing direct database report generation...")
        
        try:
            # Import required modules
            from motor.motor_asyncio import AsyncIOMotorClient
            from report_generator import AMReportGenerator
            import os
            from dotenv import load_dotenv
            
            # Load environment
            load_dotenv('/app/backend/.env')
            
            # Connect to database
            mongo_url = os.environ['MONGO_URL']
            client = AsyncIOMotorClient(mongo_url)
            db = client[os.environ['DB_NAME']]
            
            # Create user object for report generation
            class MockUser:
                def __init__(self, user_data):
                    self.id = user_data['id']
                    self.org_id = user_data['org_id']
                    self.organization_name = user_data['organization_name']
            
            current_user = MockUser(self.user_data)
            
            # Generate report directly
            report_generator = AMReportGenerator()
            docx_bytes, filename = await report_generator.generate_report_for_assessment(
                self.assessment_id, db, current_user
            )
            
            print(f"✅ Direct generation successful: {len(docx_bytes)} bytes")
            
            # Close database connection
            client.close()
            
            return docx_bytes, True
            
        except Exception as e:
            print(f"❌ Direct generation failed: {str(e)}")
            traceback.print_exc()
            return None, False

    def test_api_generation(self):
        """Test API-based report generation"""
        print("🔍 Testing API report generation...")
        
        success, response = self.make_request('GET', f'assessments/{self.assessment_id}/report', stream=True)
        
        if success:
            docx_bytes = response.content
            print(f"✅ API generation successful: {len(docx_bytes)} bytes")
            return docx_bytes, True
        else:
            print(f"❌ API generation failed: {response}")
            return None, False

    def compare_docx_files_detailed(self, api_bytes, direct_bytes):
        """Detailed comparison of DOCX files"""
        print("\n🔍 DETAILED DOCX COMPARISON")
        print("-" * 60)
        
        if not api_bytes or not direct_bytes:
            print("❌ Cannot compare - one or both files are empty")
            return
        
        # Size comparison
        api_size = len(api_bytes)
        direct_size = len(direct_bytes)
        print(f"API size: {api_size:,} bytes")
        print(f"Direct size: {direct_size:,} bytes")
        print(f"Size difference: {abs(api_size - direct_size):,} bytes")
        
        # ZIP structure comparison
        try:
            with zipfile.ZipFile(io.BytesIO(api_bytes), 'r') as api_zip:
                api_files = set(api_zip.namelist())
                
            with zipfile.ZipFile(io.BytesIO(direct_bytes), 'r') as direct_zip:
                direct_files = set(direct_zip.namelist())
            
            print(f"\nAPI ZIP files: {len(api_files)}")
            print(f"Direct ZIP files: {len(direct_files)}")
            
            # Check for file differences
            only_in_api = api_files - direct_files
            only_in_direct = direct_files - api_files
            common_files = api_files & direct_files
            
            if only_in_api:
                print(f"Files only in API: {only_in_api}")
            if only_in_direct:
                print(f"Files only in Direct: {only_in_direct}")
            
            print(f"Common files: {len(common_files)}")
            
            # Compare document.xml content
            if 'word/document.xml' in common_files:
                self.compare_document_xml(api_bytes, direct_bytes)
            
            # Compare media files
            api_media = [f for f in api_files if f.startswith('word/media/')]
            direct_media = [f for f in direct_files if f.startswith('word/media/')]
            
            print(f"\nAPI media files: {api_media}")
            print(f"Direct media files: {direct_media}")
            
        except Exception as e:
            print(f"❌ Error comparing ZIP structures: {str(e)}")

    def compare_document_xml(self, api_bytes, direct_bytes):
        """Compare document.xml content between API and direct generation"""
        print("\n📄 DOCUMENT.XML COMPARISON")
        print("-" * 40)
        
        try:
            with zipfile.ZipFile(io.BytesIO(api_bytes), 'r') as api_zip:
                api_doc = api_zip.read('word/document.xml')
                
            with zipfile.ZipFile(io.BytesIO(direct_bytes), 'r') as direct_zip:
                direct_doc = direct_zip.read('word/document.xml')
            
            # Convert to text for comparison
            api_text = api_doc.decode('utf-8', errors='ignore')
            direct_text = direct_doc.decode('utf-8', errors='ignore')
            
            print(f"API document.xml size: {len(api_doc):,} bytes")
            print(f"Direct document.xml size: {len(direct_doc):,} bytes")
            
            # Check for template variables (corruption indicator)
            api_template_vars = api_text.count('{{') + api_text.count('}}')
            direct_template_vars = direct_text.count('{{') + direct_text.count('}}')
            
            print(f"API template variables: {api_template_vars}")
            print(f"Direct template variables: {direct_template_vars}")
            
            if api_template_vars > 0:
                print("⚠️  API document contains unprocessed template variables!")
                # Find and show template variables
                import re
                vars_found = re.findall(r'\{\{[^}]+\}\}', api_text)
                for var in vars_found[:5]:  # Show first 5
                    print(f"   Template var: {var}")
            
            if direct_template_vars > 0:
                print("⚠️  Direct document contains unprocessed template variables!")
            
            # Check for organization name
            org_name = self.user_data.get('organization_name', '')
            api_has_org = org_name in api_text
            direct_has_org = org_name in direct_text
            
            print(f"API contains org name '{org_name}': {api_has_org}")
            print(f"Direct contains org name '{org_name}': {direct_has_org}")
            
            # Check for assessment data
            data_indicators = ['Domain', 'Score', 'Recommendation', 'Assessment']
            for indicator in data_indicators:
                api_count = api_text.count(indicator)
                direct_count = direct_text.count(indicator)
                print(f"'{indicator}' - API: {api_count}, Direct: {direct_count}")
            
            # Check if documents are identical
            if api_doc == direct_doc:
                print("✅ Documents are identical")
            else:
                print("❌ Documents differ")
                
                # Find first difference
                for i, (a, d) in enumerate(zip(api_doc, direct_doc)):
                    if a != d:
                        print(f"First difference at byte {i}: API={a} Direct={d}")
                        break
            
        except Exception as e:
            print(f"❌ Error comparing document.xml: {str(e)}")

    def save_files_for_analysis(self, api_bytes, direct_bytes):
        """Save files for external analysis"""
        print("\n💾 SAVING FILES FOR ANALYSIS")
        print("-" * 40)
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Save API file
            api_filename = f"/tmp/api_report_{timestamp}.docx"
            with open(api_filename, 'wb') as f:
                f.write(api_bytes)
            print(f"API file saved: {api_filename}")
            
            # Save Direct file
            direct_filename = f"/tmp/direct_report_{timestamp}.docx"
            with open(direct_filename, 'wb') as f:
                f.write(direct_bytes)
            print(f"Direct file saved: {direct_filename}")
            
            # Try to validate with LibreOffice
            print("\n🔍 VALIDATING WITH LIBREOFFICE")
            import subprocess
            
            for filename, label in [(api_filename, "API"), (direct_filename, "Direct")]:
                try:
                    # Try to convert to PDF to test validity
                    result = subprocess.run([
                        'libreoffice', '--headless', '--invisible', '--convert-to', 'pdf',
                        '--outdir', '/tmp', filename
                    ], capture_output=True, timeout=30)
                    
                    if result.returncode == 0:
                        print(f"✅ {label} file is valid (LibreOffice conversion successful)")
                    else:
                        print(f"❌ {label} file validation failed: {result.stderr.decode()}")
                        
                except Exception as e:
                    print(f"❌ {label} file validation error: {str(e)}")
            
        except Exception as e:
            print(f"❌ Error saving files: {str(e)}")

    async def run_comparison_test(self):
        """Run the complete comparison test"""
        print("=" * 80)
        print("DIRECT API vs DATABASE COMPARISON TEST")
        print("=" * 80)
        
        # Setup
        if not self.setup_test_environment():
            print("❌ Failed to set up test environment")
            return False
        
        # Test API generation
        api_bytes, api_success = self.test_api_generation()
        
        # Test direct generation
        direct_bytes, direct_success = await self.test_direct_database_generation()
        
        # Compare results
        if api_success and direct_success:
            self.compare_docx_files_detailed(api_bytes, direct_bytes)
            self.save_files_for_analysis(api_bytes, direct_bytes)
            
            # Final assessment
            print("\n" + "=" * 80)
            print("FINAL ASSESSMENT")
            print("=" * 80)
            
            if api_bytes == direct_bytes:
                print("✅ API and Direct generation produce IDENTICAL results")
                print("   No corruption detected - issue may be elsewhere")
            else:
                print("❌ API and Direct generation produce DIFFERENT results")
                print("   This confirms there is a difference in the generation process")
                
                # Analyze the type of difference
                api_size = len(api_bytes) if api_bytes else 0
                direct_size = len(direct_bytes) if direct_bytes else 0
                
                if api_size == 0:
                    print("   API generation returned empty file")
                elif direct_size == 0:
                    print("   Direct generation returned empty file")
                elif abs(api_size - direct_size) > 1000:
                    print("   Significant size difference suggests content corruption")
                else:
                    print("   Minor differences may be due to timestamps or metadata")
            
        elif api_success and not direct_success:
            print("❌ API succeeded but Direct failed - Direct method has issues")
        elif not api_success and direct_success:
            print("❌ Direct succeeded but API failed - API has corruption issues")
        else:
            print("❌ Both methods failed - System-wide issues")
        
        print(f"\nTests completed: {self.tests_passed}/{self.tests_run} passed")
        return True


def main():
    """Main execution function"""
    tester = DirectComparisonTester()
    
    try:
        # Run async test
        success = asyncio.run(tester.run_comparison_test())
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