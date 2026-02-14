"""
Evidence Phase 1 API Tests
Tests for:
1. Evidence creation with new fields (evidence_summary, limitations)
2. Evidence update with new fields
3. Archive endpoint POST /api/evidence/{id}/archive
4. Restore endpoint POST /api/evidence/{id}/restore
5. Get evidence by question endpoint
"""

import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test credentials
TEST_EMAIL = "andrew@test.com"
TEST_PASSWORD = "password123"


@pytest.fixture(scope="module")
def auth_token():
    """Get authentication token for test user"""
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    })
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token") or data.get("token")
    pytest.skip(f"Authentication failed: {response.status_code} - {response.text}")


@pytest.fixture(scope="module")
def auth_headers(auth_token):
    """Authenticated headers for API calls"""
    return {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="module")
def test_assessment_id(auth_headers):
    """Get or create a test assessment ID"""
    # Try to get existing FAIRA assessments
    response = requests.get(f"{BASE_URL}/api/assessments?type=faira", headers=auth_headers)
    if response.status_code == 200:
        assessments = response.json()
        if assessments and len(assessments) > 0:
            return assessments[0].get("assessment_id")
    # Return a placeholder if no assessment found
    return "test-assessment-" + str(uuid.uuid4())


class TestEvidenceCreationWithNewFields:
    """Test evidence creation with Phase 1 new fields"""
    
    def test_create_evidence_with_summary_and_limitations(self, auth_headers, test_assessment_id):
        """Test creating evidence with evidence_summary and limitations fields"""
        evidence_data = {
            "evidence_title": "TEST_Phase1_Evidence_Summary",
            "file_name": "test_policy.pdf",
            "file_type": "pdf",
            "file_url": f"uploads/test_{uuid.uuid4()}.pdf",
            "evidence_type": "Policy",
            "lifecycle_phase": "Design",
            "trust_level": "Draft",
            "applies_to_scope": "Organisation-wide",
            "assessment_id": test_assessment_id,
            "linked_question_ids": ["B3-1"],
            "is_reusable": False,
            "evidence_summary": "This policy demonstrates our commitment to AI fairness testing with defined procedures.",
            "limitations": "Policy is in draft stage and has not been externally reviewed."
        }
        
        response = requests.post(f"{BASE_URL}/api/evidence", json=evidence_data, headers=auth_headers)
        
        assert response.status_code in [200, 201], f"Create evidence failed: {response.status_code} - {response.text}"
        data = response.json()
        
        # Verify evidence_id was returned
        assert "evidence_id" in data, "evidence_id not returned in response"
        
        # Store for cleanup
        TestEvidenceCreationWithNewFields.created_evidence_id = data["evidence_id"]
        print(f"Created evidence with ID: {data['evidence_id']}")
    
    def test_get_evidence_has_new_fields(self, auth_headers):
        """Verify the created evidence has the new fields"""
        evidence_id = getattr(TestEvidenceCreationWithNewFields, 'created_evidence_id', None)
        if not evidence_id:
            pytest.skip("No evidence created in previous test")
        
        response = requests.get(f"{BASE_URL}/api/evidence/{evidence_id}", headers=auth_headers)
        
        assert response.status_code == 200, f"Get evidence failed: {response.status_code}"
        data = response.json()
        
        # Verify new fields are present
        assert "evidence_summary" in data, "evidence_summary field missing"
        assert "limitations" in data, "limitations field missing"
        assert data["evidence_summary"] == "This policy demonstrates our commitment to AI fairness testing with defined procedures."
        assert data["limitations"] == "Policy is in draft stage and has not been externally reviewed."
        print("Evidence summary and limitations fields verified")
    
    def test_create_evidence_without_new_fields(self, auth_headers, test_assessment_id):
        """Test creating evidence without new fields (should work - they're optional)"""
        evidence_data = {
            "evidence_title": "TEST_Phase1_Evidence_NoNewFields",
            "file_name": "test_document.docx",
            "file_type": "docx",
            "file_url": f"uploads/test_{uuid.uuid4()}.docx",
            "evidence_type": "Procedure",
            "linked_question_ids": ["B4-1"],
            "assessment_id": test_assessment_id,
        }
        
        response = requests.post(f"{BASE_URL}/api/evidence", json=evidence_data, headers=auth_headers)
        
        assert response.status_code in [200, 201], f"Create evidence failed: {response.status_code} - {response.text}"
        data = response.json()
        
        # Store for cleanup
        TestEvidenceCreationWithNewFields.created_evidence_id_2 = data.get("evidence_id")
        print(f"Created evidence without new fields: {data.get('evidence_id')}")


class TestEvidenceUpdate:
    """Test evidence update with new fields"""
    
    def test_update_evidence_summary_and_limitations(self, auth_headers):
        """Test updating evidence_summary and limitations fields"""
        evidence_id = getattr(TestEvidenceCreationWithNewFields, 'created_evidence_id', None)
        if not evidence_id:
            pytest.skip("No evidence to update")
        
        update_data = {
            "evidence_summary": "Updated summary: This policy now includes comprehensive bias testing procedures.",
            "limitations": "Updated limitations: Awaiting external audit."
        }
        
        response = requests.put(f"{BASE_URL}/api/evidence/{evidence_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200, f"Update evidence failed: {response.status_code} - {response.text}"
        
        # Verify update was applied
        get_response = requests.get(f"{BASE_URL}/api/evidence/{evidence_id}", headers=auth_headers)
        assert get_response.status_code == 200
        data = get_response.json()
        
        assert data["evidence_summary"] == update_data["evidence_summary"]
        assert data["limitations"] == update_data["limitations"]
        print("Evidence summary and limitations update verified")


class TestArchiveRestoreEndpoints:
    """Test archive and restore endpoints"""
    
    created_evidence_id = None
    
    def test_create_evidence_for_archive_test(self, auth_headers, test_assessment_id):
        """Create evidence to test archive/restore"""
        evidence_data = {
            "evidence_title": "TEST_Archive_Restore_Evidence",
            "file_name": "archive_test.pdf",
            "file_type": "pdf",
            "file_url": f"uploads/archive_test_{uuid.uuid4()}.pdf",
            "evidence_type": "Risk Assessment",
            "linked_question_ids": ["B5-1"],
            "assessment_id": test_assessment_id,
            "evidence_summary": "Test evidence for archive/restore functionality",
            "limitations": None
        }
        
        response = requests.post(f"{BASE_URL}/api/evidence", json=evidence_data, headers=auth_headers)
        assert response.status_code in [200, 201], f"Create evidence failed: {response.status_code}"
        
        data = response.json()
        TestArchiveRestoreEndpoints.created_evidence_id = data["evidence_id"]
        print(f"Created evidence for archive test: {data['evidence_id']}")
    
    def test_archive_endpoint(self, auth_headers):
        """Test POST /api/evidence/{id}/archive"""
        evidence_id = TestArchiveRestoreEndpoints.created_evidence_id
        if not evidence_id:
            pytest.skip("No evidence to archive")
        
        response = requests.post(f"{BASE_URL}/api/evidence/{evidence_id}/archive", headers=auth_headers)
        
        assert response.status_code == 200, f"Archive failed: {response.status_code} - {response.text}"
        data = response.json()
        
        assert "message" in data
        assert data.get("status") == "Archived" or "archived" in data.get("message", "").lower()
        print(f"Archive response: {data}")
    
    def test_archive_already_archived(self, auth_headers):
        """Test archiving already archived evidence returns 400"""
        evidence_id = TestArchiveRestoreEndpoints.created_evidence_id
        if not evidence_id:
            pytest.skip("No evidence to test")
        
        response = requests.post(f"{BASE_URL}/api/evidence/{evidence_id}/archive", headers=auth_headers)
        
        # Should fail because already archived
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print("Correctly rejected archiving already archived evidence")
    
    def test_restore_endpoint(self, auth_headers):
        """Test POST /api/evidence/{id}/restore"""
        evidence_id = TestArchiveRestoreEndpoints.created_evidence_id
        if not evidence_id:
            pytest.skip("No evidence to restore")
        
        response = requests.post(f"{BASE_URL}/api/evidence/{evidence_id}/restore", headers=auth_headers)
        
        assert response.status_code == 200, f"Restore failed: {response.status_code} - {response.text}"
        data = response.json()
        
        assert "message" in data
        assert data.get("status") == "Active" or "restored" in data.get("message", "").lower()
        print(f"Restore response: {data}")
    
    def test_restore_not_archived(self, auth_headers):
        """Test restoring non-archived evidence returns 400"""
        evidence_id = TestArchiveRestoreEndpoints.created_evidence_id
        if not evidence_id:
            pytest.skip("No evidence to test")
        
        response = requests.post(f"{BASE_URL}/api/evidence/{evidence_id}/restore", headers=auth_headers)
        
        # Should fail because not archived
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print("Correctly rejected restoring non-archived evidence")
    
    def test_archive_nonexistent_evidence(self, auth_headers):
        """Test archiving non-existent evidence returns 404"""
        fake_id = str(uuid.uuid4())
        response = requests.post(f"{BASE_URL}/api/evidence/{fake_id}/archive", headers=auth_headers)
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        print("Correctly returned 404 for non-existent evidence archive")
    
    def test_restore_nonexistent_evidence(self, auth_headers):
        """Test restoring non-existent evidence returns 404"""
        fake_id = str(uuid.uuid4())
        response = requests.post(f"{BASE_URL}/api/evidence/{fake_id}/restore", headers=auth_headers)
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        print("Correctly returned 404 for non-existent evidence restore")


class TestGetEvidenceByQuestion:
    """Test get evidence by question endpoint"""
    
    def test_get_evidence_by_question_code(self, auth_headers, test_assessment_id):
        """Test GET /api/evidence/by-question/{question_id}"""
        # Create evidence linked to B3-1
        evidence_data = {
            "evidence_title": "TEST_Evidence_B3_1",
            "file_name": "b3_test.pdf",
            "file_type": "pdf",
            "file_url": f"uploads/b3_test_{uuid.uuid4()}.pdf",
            "evidence_type": "Audit Report",
            "linked_question_ids": ["B3-1"],
            "assessment_id": test_assessment_id,
        }
        
        create_response = requests.post(f"{BASE_URL}/api/evidence", json=evidence_data, headers=auth_headers)
        assert create_response.status_code in [200, 201]
        created_id = create_response.json().get("evidence_id")
        
        # Get evidence by question code
        response = requests.get(
            f"{BASE_URL}/api/evidence/by-question/B3-1?assessment_id={test_assessment_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200, f"Get by question failed: {response.status_code}"
        evidence_list = response.json()
        
        assert isinstance(evidence_list, list), "Response should be a list"
        
        # Find our created evidence
        found = any(e.get("evidence_id") == created_id for e in evidence_list)
        assert found, f"Created evidence {created_id} not found in response"
        print(f"Found {len(evidence_list)} evidence items for question B3-1")
        
        # Store for cleanup
        TestGetEvidenceByQuestion.created_evidence_id = created_id


class TestCleanup:
    """Cleanup test data"""
    
    def test_cleanup_test_evidence(self, auth_headers):
        """Archive all TEST_ prefixed evidence"""
        # Get all evidence
        response = requests.get(f"{BASE_URL}/api/evidence", headers=auth_headers)
        if response.status_code != 200:
            print(f"Could not get evidence for cleanup: {response.status_code}")
            return
        
        evidence_list = response.json()
        cleaned = 0
        
        for evidence in evidence_list:
            title = evidence.get("evidence_title", "")
            if title.startswith("TEST_"):
                evidence_id = evidence.get("evidence_id")
                if evidence_id:
                    # Archive test evidence
                    archive_response = requests.post(
                        f"{BASE_URL}/api/evidence/{evidence_id}/archive",
                        headers=auth_headers
                    )
                    if archive_response.status_code in [200, 400]:  # 400 if already archived
                        cleaned += 1
        
        print(f"Cleaned up {cleaned} test evidence items")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
