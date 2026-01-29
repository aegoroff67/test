"""
FAIRA Assessment API Tests
Tests the FAIRA form endpoints including A4.7 and A4.8 gated sections
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://maturity-assessment-3.preview.emergentagent.com')

class TestFairaAPI:
    """FAIRA Assessment API tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Login and get auth token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "andrew@test.com",
            "password": "password123"
        })
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        self.token = data["access_token"]
        self.user = data["user"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        print(f"Logged in as: {self.user['email']}")
    
    def test_get_assessments(self):
        """Test getting list of assessments"""
        response = requests.get(f"{BASE_URL}/api/assessments", headers=self.headers)
        assert response.status_code == 200, f"Failed to get assessments: {response.text}"
        data = response.json()
        print(f"Found {len(data)} assessments")
        
        # Find FAIRA assessments
        faira_assessments = [a for a in data if a.get("assessment_type") == "FAIRA"]
        print(f"Found {len(faira_assessments)} FAIRA assessments")
        assert len(faira_assessments) > 0, "No FAIRA assessments found"
        
        # Store first FAIRA assessment ID for other tests
        self.faira_id = faira_assessments[0]["id"]
        return self.faira_id
    
    def test_get_faira_assessment_details(self):
        """Test getting FAIRA assessment details"""
        # First get assessment ID
        faira_id = self.test_get_assessments()
        
        response = requests.get(f"{BASE_URL}/api/assessments/{faira_id}", headers=self.headers)
        assert response.status_code == 200, f"Failed to get assessment: {response.text}"
        data = response.json()
        
        print(f"Assessment name: {data.get('name')}")
        print(f"Assessment type: {data.get('assessment_type')}")
        print(f"Status: {data.get('status')}")
        
        # Check FAIRA form data exists
        faira_form = data.get("faira_form", {})
        print(f"FAIRA form has {len(faira_form)} fields")
        
        # Verify A4.7 and A4.8 fields exist
        a4_7_fields = [k for k in faira_form.keys() if k.startswith("A4_7")]
        a4_8_fields = [k for k in faira_form.keys() if k.startswith("A4_8")]
        print(f"A4.7 fields: {a4_7_fields}")
        print(f"A4.8 fields: {a4_8_fields}")
        
        return data
    
    def test_save_faira_form_with_a4_8(self):
        """Test saving FAIRA form with A4.8 gated section data"""
        # First get assessment ID
        faira_id = self.test_get_assessments()
        
        # Get current form data
        response = requests.get(f"{BASE_URL}/api/assessments/{faira_id}", headers=self.headers)
        current_data = response.json().get("faira_form", {})
        
        # Update with A4.8 test data
        test_form_data = {
            **current_data,
            "A4_8": "Yes",
            "A4_8_action_types": ["Eligibility / access decisions", "Service entitlements / benefits decisions"],
            "A4_8_trigger_pathway": "Used as decision support (human makes final decision)",
            "A4_8_affected_parties": ["Individuals / citizens", "Employees / workers"],
            "A4_8_decision_records": ["Audit logs of outputs and decisions", "Human approval record captured"],
            "A4_8_review_appeal": "Yes — documented and operational",
            "A4_8_legal_basis": ["Legislation / regulation explicitly authorising action"],
            "A4_8_notes": "Test notes for A4.8g"
        }
        
        # Save form
        response = requests.put(
            f"{BASE_URL}/api/assessments/{faira_id}/faira-form",
            json=test_form_data,
            headers=self.headers
        )
        assert response.status_code == 200, f"Failed to save form: {response.text}"
        print("Successfully saved FAIRA form with A4.8 data")
        
        # Verify data was saved
        response = requests.get(f"{BASE_URL}/api/assessments/{faira_id}", headers=self.headers)
        saved_data = response.json().get("faira_form", {})
        
        assert saved_data.get("A4_8") == "Yes", "A4.8 gate question not saved"
        assert "Eligibility / access decisions" in saved_data.get("A4_8_action_types", []), "A4.8a not saved"
        assert saved_data.get("A4_8_trigger_pathway") == "Used as decision support (human makes final decision)", "A4.8b not saved"
        assert "Individuals / citizens" in saved_data.get("A4_8_affected_parties", []), "A4.8c not saved"
        assert "Audit logs of outputs and decisions" in saved_data.get("A4_8_decision_records", []), "A4.8d not saved"
        assert saved_data.get("A4_8_review_appeal") == "Yes — documented and operational", "A4.8e not saved"
        assert "Legislation / regulation explicitly authorising action" in saved_data.get("A4_8_legal_basis", []), "A4.8f not saved"
        assert saved_data.get("A4_8_notes") == "Test notes for A4.8g", "A4.8g notes not saved"
        
        print("All A4.8 sub-fields verified successfully")
    
    def test_save_faira_form_with_a4_7(self):
        """Test saving FAIRA form with A4.7 gated section data"""
        # First get assessment ID
        faira_id = self.test_get_assessments()
        
        # Get current form data
        response = requests.get(f"{BASE_URL}/api/assessments/{faira_id}", headers=self.headers)
        current_data = response.json().get("faira_form", {})
        
        # Update with A4.7 test data
        test_form_data = {
            **current_data,
            "A4_7": "Yes",
            "A4_7_pii_types": ["Name / identity attributes", "Contact details (email, phone, address)"],
            "A4_7_access_scope": "Internal users only",
            "A4_7_access_controls": ["Role-based access control (RBAC)", "Audit logging / access logs"],
            "A4_7_notes": "Test notes for A4.7d"
        }
        
        # Save form
        response = requests.put(
            f"{BASE_URL}/api/assessments/{faira_id}/faira-form",
            json=test_form_data,
            headers=self.headers
        )
        assert response.status_code == 200, f"Failed to save form: {response.text}"
        print("Successfully saved FAIRA form with A4.7 data")
        
        # Verify data was saved
        response = requests.get(f"{BASE_URL}/api/assessments/{faira_id}", headers=self.headers)
        saved_data = response.json().get("faira_form", {})
        
        assert saved_data.get("A4_7") == "Yes", "A4.7 gate question not saved"
        assert "Name / identity attributes" in saved_data.get("A4_7_pii_types", []), "A4.7a not saved"
        assert saved_data.get("A4_7_access_scope") == "Internal users only", "A4.7b not saved"
        assert "Role-based access control (RBAC)" in saved_data.get("A4_7_access_controls", []), "A4.7c not saved"
        assert saved_data.get("A4_7_notes") == "Test notes for A4.7d", "A4.7d notes not saved"
        
        print("All A4.7 sub-fields verified successfully")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
