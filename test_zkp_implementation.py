import os
import sys
import time
from colorama import Fore, Style, init
import server.dbs_exec as dbe
from zkp.password_zkp import PasswordZKP

# Initialize colorama for colored output
init()

class ZKPTester:
    def __init__(self):
        self.zkp = PasswordZKP()
        print(f"{Fore.CYAN}ZKP Implementation Testing Suite{Style.RESET_ALL}\n")

    def test_admin_login(self):
        """Test admin authentication with ZKP"""
        print(f"{Fore.YELLOW}1. Testing Admin Authentication{Style.RESET_ALL}")
        print("-" * 60)

        test_cases = [
            {"account": 0, "password": "admin", "expected": True, "desc": "Valid Admin Login"},
            {"account": 0, "password": "wrong", "expected": False, "desc": "Wrong Admin Password"},
            {"account": 1, "password": "admin", "expected": False, "desc": "Wrong Account Number"},
        ]

        for case in test_cases:
            print(f"\nTest Case: {case['desc']}")
            print(f"Account: {case['account']}, Password: {case['password']}")
            result = dbe.isUserAdmin(case['account'], case['password'])
            success = result == case['expected']
            color = Fore.GREEN if success else Fore.RED
            print(f"Result: {color}{'PASSED' if success else 'FAILED'}{Style.RESET_ALL}")

        input("\nPress Enter to continue...\n")

    def test_proof_uniqueness(self):
        """Test that each proof is unique"""
        print(f"{Fore.YELLOW}2. Testing Proof Uniqueness{Style.RESET_ALL}")
        print("-" * 60)

        password = "admin"
        proofs = []
        
        print("Generating multiple proofs for same password...")
        for i in range(3):
            proof = self.zkp.generate_proof(password)
            proofs.append(proof['commitment'])
            print(f"\nProof {i+1}: {proof['commitment']}")

        # Check all proofs are different
        unique = len(set(proofs)) == len(proofs)
        color = Fore.GREEN if unique else Fore.RED
        print(f"\nAll proofs unique: {color}{'PASSED' if unique else 'FAILED'}{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...\n")

    def test_verification_performance(self):
        """Test ZKP verification performance"""
        print(f"{Fore.YELLOW}3. Testing Authentication Performance{Style.RESET_ALL}")
        print("-" * 60)

        iterations = 10
        password = "admin"
        times = []

        print(f"Performing {iterations} authentications...")
        for i in range(iterations):
            start_time = time.time()
            dbe.isUserAdmin(0, password)
            end_time = time.time()
            times.append(end_time - start_time)
            print(f"Authentication {i+1}: {times[-1]:.4f} seconds")

        avg_time = sum(times) / len(times)
        print(f"\nAverage authentication time: {Fore.CYAN}{avg_time:.4f} seconds{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...\n")

    def test_multiple_sessions(self):
        """Test multiple login sessions"""
        print(f"{Fore.YELLOW}4. Testing Multiple Login Sessions{Style.RESET_ALL}")
        print("-" * 60)

        print("Simulating multiple login sessions...")
        
        for session in range(3):
            print(f"\nSession {session + 1}:")
            print("-" * 20)
            result = dbe.isUserAdmin(0, "admin")
            color = Fore.GREEN if result else Fore.RED
            print(f"Authentication: {color}{'SUCCESS' if result else 'FAILED'}{Style.RESET_ALL}")
            time.sleep(1)  # Simulate time between sessions

        input("\nPress Enter to continue...\n")

    def test_error_handling(self):
        """Test error handling in ZKP verification"""
        print(f"{Fore.YELLOW}5. Testing Error Handling{Style.RESET_ALL}")
        print("-" * 60)

        test_cases = [
            {"account": None, "password": "admin", "desc": "Invalid Account (None)"},
            {"account": 0, "password": "", "desc": "Empty Password"},
            {"account": "invalid", "password": "admin", "desc": "Invalid Account Type"},
        ]

        for case in test_cases:
            print(f"\nTest Case: {case['desc']}")
            try:
                result = dbe.isUserAdmin(case['account'], case['password'])
                print(f"Result: {Fore.GREEN}Handled Gracefully{Style.RESET_ALL}")
            except Exception as e:
                print(f"Result: {Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

        input("\nPress Enter to continue...\n")

def main():
    tester = ZKPTester()
    
    while True:
        print(f"{Fore.CYAN}ZKP Testing Menu{Style.RESET_ALL}")
        print("\n1. Test Admin Authentication")
        print("2. Test Proof Uniqueness")
        print("3. Test Authentication Performance")
        print("4. Test Multiple Sessions")
        print("5. Test Error Handling")
        print("6. Run All Tests")
        print("7. Exit")
        
        choice = input("\nSelect test to run (1-7): ")
        print()
        
        if choice == '1':
            tester.test_admin_login()
        elif choice == '2':
            tester.test_proof_uniqueness()
        elif choice == '3':
            tester.test_verification_performance()
        elif choice == '4':
            tester.test_multiple_sessions()
        elif choice == '5':
            tester.test_error_handling()
        elif choice == '6':
            tester.test_admin_login()
            tester.test_proof_uniqueness()
            tester.test_verification_performance()
            tester.test_multiple_sessions()
            tester.test_error_handling()
        elif choice == '7':
            print("Testing completed.")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
