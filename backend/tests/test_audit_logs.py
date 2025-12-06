from fastapi.testclient import TestClient
import sys
import os
import uuid

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import SessionLocal
from audit import AuditLog

client = TestClient(app)

def test_audit_logs():
    print("Starting Audit Logs Verification...")
    
    # Generate unique user to avoid collisions
    unique_id = str(uuid.uuid4())[:8]
    email = f"audit_test_{unique_id}@example.com"
    password = "testpassword123"
    
    # 1. Signup
    print(f"1. Signing up {email}...")
    response = client.post("/auth/signup", json={"email": email, "password": password})
    if response.status_code != 200:
        print(f"Signup failed: {response.text}")
        return
        
    user_id = response.json().get("user_id")
    if not user_id:
        print("Signup ok but no user_id returned")
        return
    
    # 2. Login
    print("2. Logging in...")
    response = client.post("/auth/login", json={"email": email, "password": password})
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
        
    token = response.json()["access_token"]
    
    # 3. Change Password
    print("3. Changing password...")
    new_password = "newpassword123"
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/auth/change-password", 
        json={"email": email, "old_password": password, "new_password": new_password},
        headers=headers
    )
    if response.status_code != 200:
        print(f"Change password failed: {response.text}")
        return

    new_token = response.json()["access_token"]
    new_headers = {"Authorization": f"Bearer {new_token}"}
    
    # 4. Verify Immediate Revocation of Old Token
    print("4. Verifying old token revocation...")
    old_headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/auth/logout", headers=old_headers) # Try to use old token
    if response.status_code == 401:
        print("   Success: Old token was revoked automatically!")
    else:
        print(f"   Warning: Old token still active (Status: {response.status_code}).")

    # 5. Logout with NEW token
    print("5. Logging out (with new token)...")
    response = client.post("/auth/logout", headers=new_headers)
    if response.status_code != 200:
        print(f"Logout failed: {response.text}")
        return
    
    # 6. Verify Logs
    print("5. Verifying DB records...")
    db = SessionLocal()
    try:
        logs = db.query(AuditLog).filter(AuditLog.user_id == user_id).order_by(AuditLog.timestamp).all()
        
        actions = [log.action for log in logs]
        print(f"   Found actions found for user {user_id}: {actions}")
        
        expected_actions = ["SIGNUP", "LOGIN", "CHANGE_PASSWORD", "LOGOUT"]
        missing = [act for act in expected_actions if act not in actions]
        
        if not missing:
            print("\nSUCCESS: All expected audit logs found!")
            print("Verified:")
            for log in logs:
                print(f" - {log.timestamp}: {log.action} | IP: {log.ip_address} | {log.details}")
        else:
            print(f"\nFAILURE: Missing logs for: {missing}")

    except Exception as e:
        print(f"Error verification DB: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_audit_logs()
