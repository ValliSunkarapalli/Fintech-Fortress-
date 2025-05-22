import os
import sys
from zkp.password_zkp import PasswordZKP

def test_password_zkp():
    print("Testing Password ZKP Implementation")
    print("-" * 40)
    
    zkp = PasswordZKP()
    
    # Test 1: Valid password
    print("\nTest 1: Valid Password")
    password = "testpassword123"
    _, public_key = zkp.generate_keypair(password)
    proof = zkp.generate_proof(password)
    result = zkp.verify_proof(proof, public_key)
    print(f"Valid Password Test: {'PASSED' if result else 'FAILED'}")
    
    # Test 2: Invalid password
    print("\nTest 2: Invalid Password")
    wrong_password = "wrongpassword"
    proof = zkp.generate_proof(wrong_password)
    result = not zkp.verify_proof(proof, public_key)
    print(f"Invalid Password Test: {'PASSED' if result else 'FAILED'}")
    
    # Test 3: Admin password
    print("\nTest 3: Admin Password")
    admin_password = "admin"
    _, admin_public_key = zkp.generate_keypair(admin_password)
    proof = zkp.generate_proof(admin_password)
    result = zkp.verify_proof(proof, admin_public_key)
    print(f"Admin Password Test: {'PASSED' if result else 'FAILED'}")

if __name__ == "__main__":
    test_password_zkp()
