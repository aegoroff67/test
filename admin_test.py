#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime
import secrets
import string

class AdminAPITester:
    def __init__(self, base_url="https://maturityai.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.super_admin_token = None
        self.admin_token = None
        self.member_token = None
        self.super_admin_user = None
        self.admin_user = None
        self.member_user = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.temp_user_id = None  # For deletion testing

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

    def make_request(self, method, endpoint, data=None, expected_status=200, token=None):
        """Make API request with error handling"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        # Use provided token or default to super admin token
        auth_token = token or self.super_admin_token
        if auth_token:
            headers['Authorization'] = f'Bearer {auth_token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            
            # Handle JSON responses
            try:
                return success, response.json() if success else response.text
            except:
                # If JSON parsing fails, return text
                return success, response.text

        except Exception as e:
            return False, str(e)

    def test_authentication_setup(self):
        """Test authentication with existing users"""
        print("\n🔐 AUTHENTICATION SETUP")
        print("-" * 60)
        
        # Test login with SUPER_ADMIN user (andrew@test.com)
        login_data = {
            "email": "andrew@test.com",
            "password": "password123"
        }
        
        success, response = self.make_request('POST', 'auth/login', login_data, token=None)
        if success and 'access_token' in response:
            self.super_admin_token = response['access_token']
            self.super_admin_user = response['user']
            self.log_test("SUPER_ADMIN login (andrew@test.com)", True)
            print(f"   📝 User role: {self.super_admin_user.get('role')}")
        else:
            self.log_test("SUPER_ADMIN login (andrew@test.com)", False, str(response))
            return False

        # Test login with ADMIN user (andrew@vciso.one)
        login_data = {
            "email": "andrew@vciso.one",
            "password": "password123"
        }
        
        success, response = self.make_request('POST', 'auth/login', login_data, token=None)
        if success and 'access_token' in response:
            self.admin_token = response['access_token']
            self.admin_user = response['user']
            self.log_test("ADMIN login (andrew@vciso.one)", True)
            print(f"   📝 User role: {self.admin_user.get('role')}")
        else:
            self.log_test("ADMIN login (andrew@vciso.one)", False, str(response))
            # This might fail if user doesn't exist, which is okay
            print(f"   ⚠️  ADMIN user might not exist: {response}")

        return True

    def test_admin_endpoints_authentication_required(self):
        """Test that admin endpoints require authentication"""
        print("\n🔒 AUTHENTICATION REQUIREMENTS")
        print("-" * 60)
        
        admin_endpoints = [
            ('GET', 'admin/users'),
            ('PUT', 'admin/users/test-id/role?new_role=MEMBER'),
            ('PUT', 'admin/users/test-id/toggle-active'),
            ('DELETE', 'admin/users/test-id'),
            ('POST', 'admin/users/test-id/reset-password')
        ]
        
        for method, endpoint in admin_endpoints:
            success, response = self.make_request(method, endpoint, expected_status=401, token=None)
            if success:
                self.log_test(f"{method} /{endpoint} requires authentication (401)", True)
            else:
                self.log_test(f"{method} /{endpoint} requires authentication (401)", False, 
                            f"Expected 401, got different status")

    def test_admin_endpoints_super_admin_required(self):
        """Test that admin endpoints require SUPER_ADMIN role"""
        print("\n👑 SUPER_ADMIN AUTHORIZATION")
        print("-" * 60)
        
        if not self.admin_token:
            print("   ⚠️  Skipping ADMIN role tests - no ADMIN user available")
            return True
        
        admin_endpoints = [
            ('GET', 'admin/users'),
            ('PUT', 'admin/users/test-id/role?new_role=MEMBER'),
            ('PUT', 'admin/users/test-id/toggle-active'),
            ('DELETE', 'admin/users/test-id'),
            ('POST', 'admin/users/test-id/reset-password')
        ]
        
        for method, endpoint in admin_endpoints:
            success, response = self.make_request(method, endpoint, expected_status=403, token=self.admin_token)
            if success:
                self.log_test(f"{method} /{endpoint} requires SUPER_ADMIN (403 for ADMIN)", True)
            else:
                self.log_test(f"{method} /{endpoint} requires SUPER_ADMIN (403 for ADMIN)", False, 
                            f"Expected 403, got different response: {response}")

    def test_get_all_users_endpoint(self):
        """Test GET /api/admin/users endpoint"""
        print("\n👥 GET ALL USERS ENDPOINT")
        print("-" * 60)
        
        success, response = self.make_request('GET', 'admin/users')
        if not success:
            self.log_test("GET /api/admin/users endpoint", False, str(response))
            return False
        
        self.log_test("GET /api/admin/users endpoint accessible", True)
        
        # Verify response is a list
        if not isinstance(response, list):
            self.log_test("Response is list of users", False, f"Expected list, got {type(response)}")
            return False
        
        self.log_test("Response is list of users", True)
        
        # Check if we have exactly 2 users as specified
        if len(response) == 2:
            self.log_test("Database contains exactly 2 users", True)
        else:
            self.log_test("Database contains exactly 2 users", False, f"Found {len(response)} users")
        
        # Verify user structure and find the expected users
        andrew_test_found = False
        andrew_vciso_found = False
        
        for user in response:
            required_fields = ['id', 'email', 'name', 'org_id', 'role', 'is_active', 'organization_name', 'industry']
            missing_fields = [field for field in required_fields if field not in user]
            
            if missing_fields:
                self.log_test(f"User {user.get('email', 'unknown')} has all required fields", False, 
                            f"Missing: {missing_fields}")
            else:
                self.log_test(f"User {user.get('email', 'unknown')} has all required fields", True)
            
            # Check for specific users
            if user.get('email') == 'andrew@test.com':
                andrew_test_found = True
                if user.get('role') == 'SUPER_ADMIN':
                    self.log_test("andrew@test.com has SUPER_ADMIN role", True)
                else:
                    self.log_test("andrew@test.com has SUPER_ADMIN role", False, f"Role is {user.get('role')}")
            
            elif user.get('email') == 'andrew@vciso.one':
                andrew_vciso_found = True
                if user.get('role') == 'ADMIN':
                    self.log_test("andrew@vciso.one has ADMIN role", True)
                else:
                    self.log_test("andrew@vciso.one has ADMIN role", False, f"Role is {user.get('role')}")
        
        if andrew_test_found:
            self.log_test("andrew@test.com user found", True)
        else:
            self.log_test("andrew@test.com user found", False, "SUPER_ADMIN user not found")
        
        if andrew_vciso_found:
            self.log_test("andrew@vciso.one user found", True)
        else:
            self.log_test("andrew@vciso.one user found", False, "ADMIN user not found")
        
        return True

    def test_update_user_role_endpoint(self):
        """Test PUT /api/admin/users/{user_id}/role endpoint"""
        print("\n🔄 UPDATE USER ROLE ENDPOINT")
        print("-" * 60)
        
        # First get all users to find a user to test with
        success, users = self.make_request('GET', 'admin/users')
        if not success or not users:
            self.log_test("Get users for role update test", False, "No users available")
            return False
        
        # Find a non-SUPER_ADMIN user to test with
        test_user = None
        for user in users:
            if user.get('role') != 'SUPER_ADMIN':
                test_user = user
                break
        
        if not test_user:
            self.log_test("Find non-SUPER_ADMIN user for role test", False, "No suitable user found")
            return False
        
        user_id = test_user['id']
        original_role = test_user['role']
        
        # Test valid role changes
        valid_roles = ['SUPER_ADMIN', 'ORG_ADMIN', 'ADMIN', 'MEMBER']
        new_role = 'MEMBER' if original_role != 'MEMBER' else 'ADMIN'
        
        # Test role update
        success, response = self.make_request('PUT', f'admin/users/{user_id}/role?new_role={new_role}')
        if success:
            self.log_test(f"Update user role to {new_role}", True)
            
            # Verify the role was actually updated
            success, updated_users = self.make_request('GET', 'admin/users')
            if success:
                updated_user = next((u for u in updated_users if u['id'] == user_id), None)
                if updated_user and updated_user.get('role') == new_role:
                    self.log_test("Role update verified in database", True)
                else:
                    self.log_test("Role update verified in database", False, 
                                f"Expected {new_role}, got {updated_user.get('role') if updated_user else 'user not found'}")
        else:
            self.log_test(f"Update user role to {new_role}", False, str(response))
        
        # Test invalid role value
        success, response = self.make_request('PUT', f'admin/users/{user_id}/role?new_role=INVALID_ROLE', expected_status=422)
        if success:
            self.log_test("Invalid role value returns 422", True)
        else:
            self.log_test("Invalid role value returns 422", False, "Should return 422 for invalid role")
        
        # Test non-existent user ID
        fake_user_id = "non-existent-user-id"
        success, response = self.make_request('PUT', f'admin/users/{fake_user_id}/role?new_role=MEMBER', expected_status=404)
        if success:
            self.log_test("Non-existent user ID returns 404", True)
        else:
            self.log_test("Non-existent user ID returns 404", False, "Should return 404 for non-existent user")
        
        # Restore original role
        success, response = self.make_request('PUT', f'admin/users/{user_id}/role?new_role={original_role}')
        if success:
            self.log_test(f"Restore original role ({original_role})", True)
        else:
            self.log_test(f"Restore original role ({original_role})", False, str(response))
        
        return True

    def test_toggle_user_active_endpoint(self):
        """Test PUT /api/admin/users/{user_id}/toggle-active endpoint"""
        print("\n🔄 TOGGLE USER ACTIVE STATUS ENDPOINT")
        print("-" * 60)
        
        # Get users to find a test user
        success, users = self.make_request('GET', 'admin/users')
        if not success or not users:
            self.log_test("Get users for active toggle test", False, "No users available")
            return False
        
        # Find a non-SUPER_ADMIN user to test with
        test_user = None
        for user in users:
            if user.get('role') != 'SUPER_ADMIN':
                test_user = user
                break
        
        if not test_user:
            self.log_test("Find user for active toggle test", False, "No suitable user found")
            return False
        
        user_id = test_user['id']
        original_status = test_user.get('is_active', True)
        
        # Test toggle active status
        success, response = self.make_request('PUT', f'admin/users/{user_id}/toggle-active')
        if success:
            self.log_test("Toggle user active status", True)
            
            # Verify response includes new status
            if 'is_active' in response:
                new_status = response['is_active']
                expected_status = not original_status
                if new_status == expected_status:
                    self.log_test("Response includes correct new is_active status", True)
                else:
                    self.log_test("Response includes correct new is_active status", False, 
                                f"Expected {expected_status}, got {new_status}")
                
                # Verify in database
                success, updated_users = self.make_request('GET', 'admin/users')
                if success:
                    updated_user = next((u for u in updated_users if u['id'] == user_id), None)
                    if updated_user and updated_user.get('is_active') == new_status:
                        self.log_test("Active status update verified in database", True)
                    else:
                        self.log_test("Active status update verified in database", False, 
                                    f"Database shows {updated_user.get('is_active') if updated_user else 'user not found'}")
            else:
                self.log_test("Response includes is_active field", False, "Missing is_active in response")
        else:
            self.log_test("Toggle user active status", False, str(response))
        
        # Toggle back to original status
        success, response = self.make_request('PUT', f'admin/users/{user_id}/toggle-active')
        if success:
            self.log_test("Toggle back to original status", True)
        else:
            self.log_test("Toggle back to original status", False, str(response))
        
        # Test with non-existent user ID
        fake_user_id = "non-existent-user-id"
        success, response = self.make_request('PUT', f'admin/users/{fake_user_id}/toggle-active', expected_status=404)
        if success:
            self.log_test("Toggle non-existent user returns 404", True)
        else:
            self.log_test("Toggle non-existent user returns 404", False, "Should return 404 for non-existent user")
        
        return True

    def test_reset_user_password_endpoint(self):
        """Test POST /api/admin/users/{user_id}/reset-password endpoint"""
        print("\n🔑 RESET USER PASSWORD ENDPOINT")
        print("-" * 60)
        
        # Get users to find a test user
        success, users = self.make_request('GET', 'admin/users')
        if not success or not users:
            self.log_test("Get users for password reset test", False, "No users available")
            return False
        
        # Find a non-SUPER_ADMIN user to test with
        test_user = None
        for user in users:
            if user.get('role') != 'SUPER_ADMIN':
                test_user = user
                break
        
        if not test_user:
            self.log_test("Find user for password reset test", False, "No suitable user found")
            return False
        
        user_id = test_user['id']
        user_email = test_user['email']
        
        # Test password reset
        success, response = self.make_request('POST', f'admin/users/{user_id}/reset-password')
        if success:
            self.log_test("Reset user password", True)
            
            # Verify response structure
            if 'temporary_password' in response:
                temp_password = response['temporary_password']
                
                # Verify password is 12 characters
                if len(temp_password) == 12:
                    self.log_test("Temporary password is 12 characters", True)
                else:
                    self.log_test("Temporary password is 12 characters", False, f"Length is {len(temp_password)}")
                
                # Verify password is alphanumeric
                if temp_password.isalnum():
                    self.log_test("Temporary password is alphanumeric", True)
                else:
                    self.log_test("Temporary password is alphanumeric", False, "Contains non-alphanumeric characters")
                
                # Test login with new password
                login_data = {
                    "email": user_email,
                    "password": temp_password
                }
                
                success, login_response = self.make_request('POST', 'auth/login', login_data, token=None)
                if success and 'access_token' in login_response:
                    self.log_test("Login with temporary password works", True)
                else:
                    self.log_test("Login with temporary password works", False, 
                                f"Login failed: {login_response}")
            else:
                self.log_test("Response includes temporary_password", False, "Missing temporary_password in response")
        else:
            self.log_test("Reset user password", False, str(response))
        
        # Test with non-existent user ID
        fake_user_id = "non-existent-user-id"
        success, response = self.make_request('POST', f'admin/users/{fake_user_id}/reset-password', expected_status=404)
        if success:
            self.log_test("Reset password for non-existent user returns 404", True)
        else:
            self.log_test("Reset password for non-existent user returns 404", False, "Should return 404 for non-existent user")
        
        return True

    def create_temporary_user_for_deletion(self):
        """Create a temporary user for deletion testing"""
        timestamp = datetime.now().strftime('%H%M%S')
        temp_email = f"temp_delete_user_{timestamp}@example.com"
        
        signup_data = {
            "name": f"Temp Delete User {timestamp}",
            "email": temp_email,
            "password": "TempPass123!",
            "organization_name": f"Temp Org {timestamp}",
            "industry": "Testing"
        }
        
        success, response = self.make_request('POST', 'auth/signup', signup_data, token=None)
        if success and 'user' in response:
            self.temp_user_id = response['user']['id']
            self.log_test("Create temporary user for deletion test", True)
            return True
        else:
            self.log_test("Create temporary user for deletion test", False, str(response))
            return False

    def test_delete_user_endpoint(self):
        """Test DELETE /api/admin/users/{user_id} endpoint"""
        print("\n🗑️ DELETE USER ENDPOINT")
        print("-" * 60)
        
        # Create a temporary user for deletion
        if not self.create_temporary_user_for_deletion():
            return False
        
        # Test deleting the temporary user
        success, response = self.make_request('DELETE', f'admin/users/{self.temp_user_id}')
        if success:
            self.log_test("Delete user account", True)
            
            # Verify user is actually removed from database
            success, users = self.make_request('GET', 'admin/users')
            if success:
                deleted_user = next((u for u in users if u['id'] == self.temp_user_id), None)
                if deleted_user is None:
                    self.log_test("User actually removed from database", True)
                else:
                    self.log_test("User actually removed from database", False, "User still exists in database")
            else:
                self.log_test("Verify user deletion in database", False, "Could not retrieve users")
        else:
            self.log_test("Delete user account", False, str(response))
        
        # Test that SUPER_ADMIN cannot delete their own account
        super_admin_id = self.super_admin_user['id']
        success, response = self.make_request('DELETE', f'admin/users/{super_admin_id}', expected_status=400)
        if success:
            self.log_test("SUPER_ADMIN cannot delete own account (400)", True)
        else:
            self.log_test("SUPER_ADMIN cannot delete own account (400)", False, "Should return 400 for self-deletion")
        
        # Test with non-existent user ID
        fake_user_id = "non-existent-user-id"
        success, response = self.make_request('DELETE', f'admin/users/{fake_user_id}', expected_status=404)
        if success:
            self.log_test("Delete non-existent user returns 404", True)
        else:
            self.log_test("Delete non-existent user returns 404", False, "Should return 404 for non-existent user")
        
        return True

    def test_data_integrity_after_operations(self):
        """Test data integrity after admin operations"""
        print("\n🔍 DATA INTEGRITY VERIFICATION")
        print("-" * 60)
        
        # Get all users and verify data integrity
        success, users = self.make_request('GET', 'admin/users')
        if not success:
            self.log_test("Get users for integrity check", False, str(users))
            return False
        
        # Verify organization relationships are maintained
        org_ids = set()
        for user in users:
            org_id = user.get('org_id')
            if org_id:
                org_ids.add(org_id)
            
            # Verify user has organization_name and industry
            if user.get('organization_name') and user.get('industry'):
                self.log_test(f"User {user.get('email')} has organization data", True)
            else:
                self.log_test(f"User {user.get('email')} has organization data", False, 
                            "Missing organization_name or industry")
        
        if org_ids:
            self.log_test("Organization relationships maintained", True)
        else:
            self.log_test("Organization relationships maintained", False, "No organization IDs found")
        
        # Verify no duplicate emails
        emails = [user.get('email') for user in users if user.get('email')]
        if len(emails) == len(set(emails)):
            self.log_test("No duplicate email addresses", True)
        else:
            self.log_test("No duplicate email addresses", False, "Duplicate emails found")
        
        return True

    def run_all_tests(self):
        """Run all admin functionality tests"""
        print("🚀 STARTING ADMIN SETTINGS FUNCTIONALITY TESTS")
        print("=" * 80)
        
        # Test sequence
        test_methods = [
            self.test_authentication_setup,
            self.test_admin_endpoints_authentication_required,
            self.test_admin_endpoints_super_admin_required,
            self.test_get_all_users_endpoint,
            self.test_update_user_role_endpoint,
            self.test_toggle_user_active_endpoint,
            self.test_reset_user_password_endpoint,
            self.test_delete_user_endpoint,
            self.test_data_integrity_after_operations
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log_test(f"Exception in {test_method.__name__}", False, str(e))
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 ADMIN FUNCTIONALITY TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 ALL ADMIN FUNCTIONALITY TESTS PASSED!")
        else:
            print(f"\n⚠️  {self.tests_run - self.tests_passed} TESTS FAILED")
            
            # Show failed tests
            failed_tests = [test for test in self.test_results if not test['success']]
            if failed_tests:
                print("\nFailed Tests:")
                for test in failed_tests:
                    print(f"  ❌ {test['test']}: {test['details']}")
        
        return self.tests_passed == self.tests_run

def main():
    """Main function to run admin tests"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        # Use the URL from frontend/.env
        base_url = "https://maturityai.preview.emergentagent.com"
    
    tester = AdminAPITester(base_url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()