from fastapi.testclient import TestClient
import sys
import os

# Add backend directory to path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_auth_flow():
    print("Starting Auth Flow Verification (Refactored)...")
    
    # 1. Signup
    email = "meow@gmail.com"
    password = "meowmeow1234"
    print(f"1. Signing up with {email}...")
    response = client.post("/auth/signup", json={"email": email, "password": password})
    if response.status_code == 400:
        print("   User already exists, proceeding...")
    elif response.status_code != 200:
        print(f"   Signup failed: {response.text}")
        return

    # 2. Login
    print("2. Logging in...")
    response = client.post("/auth/login", json={"email": email, "password": password})
    if response.status_code != 200:
        print(f"   Login failed: {response.text}")
        return
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   Login successful.")

    # 3. Change Password (Unauthenticated Flow)
    new_password = "newpassword123"
    print("3. Changing password (Unauthenticated)...")
    response = client.post(
        "/auth/change-password",
        json={"email": email, "old_password": password, "new_password": new_password}
    )
    if response.status_code != 200:
        print(f"   Change password failed: {response.text}")
        return
    
    new_token = response.json().get("access_token")
    if not new_token:
        print("   Failure: No new token returned.")
        return
    print("   Password changed successfully. New token received.")
    new_headers = {"Authorization": f"Bearer {new_token}"}

    # 4. Logout (using OLD token) - Should still work as it's not expired, just old password
    print("4. Logging out (using old token)...")
    response = client.post("/auth/logout", headers=headers)
    if response.status_code != 200:
        print(f"   Logout failed: {response.text}")
        return
    print("   Logout successful.")

    # 5. Access Protected Route (using OLD token) - Should Fail (Revoked)
    print("5. Verifying old token invalidation...")
    response = client.post("/auth/logout", headers=headers) # Any protected route
    if response.status_code == 401:
        print("   Success: Old token is invalid (401).")
    else:
        print(f"   Failure: Expected 401, got {response.status_code}")
        return

    # 6. Login with Old Password - Should Fail
    print("6. Verifying old password invalidation...")
    response = client.post("/auth/login", json={"email": email, "password": password})
    if response.status_code == 401:
        print("   Success: Old password rejected (401).")
    else:
        print(f"   Failure: Expected 401, got {response.status_code}")
        return

    # 7. Login with New Password - Should Succeed
    print("7. Verifying new password login...")
    response = client.post("/auth/login", json={"email": email, "password": new_password})
    if response.status_code == 200:
        print("   Success: New password accepted.")
    else:
        print(f"   Failure: Login with new password failed: {response.text}")
        return

    print("\nALL TESTS PASSED!")

if __name__ == "__main__":
    test_auth_flow()
