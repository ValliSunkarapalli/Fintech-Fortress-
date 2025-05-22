import os
import sys
import time
import hashlib
from colorama import Fore, Style, init

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from zkp.password_zkp import PasswordZKP
import server.dbs_exec as dbe

# Initialize colorama for colored output
init()

class SecurityDemo:
    def __init__(self):
        self.zkp = PasswordZKP()
        print(f"{Fore.CYAN}Initializing Security Feature Demonstration{Style.RESET_ALL}\n")

    def demonstrate_traditional_vs_zkp(self):
        """Demonstrate difference between traditional and ZKP authentication"""
        print(f"{Fore.YELLOW}1. Traditional vs Zero Knowledge Proof Authentication{Style.RESET_ALL}")
        print("-" * 60)
        
        # Sample password
        password = "MySecurePass123"
        print(f"Original Password: {password}")
        
        # Traditional Method
        print("\nTraditional Password Storage:")
        hash_value = hashlib.sha256(password.encode()).hexdigest()
        print(f"Stored Password Hash: {hash_value}")
        print("Issue: If database is compromised, hash can be subjected to offline attacks")
        
        # ZKP Method
        print("\nZero Knowledge Proof Method:")
        _, public_key = self.zkp.generate_keypair(password)
        proof = self.zkp.generate_proof(password)
        
        print(f"Public Key (stored): {public_key}")
        print(f"Proof (generated each time): {proof['commitment']}")
        print("Advantage: Even if database is compromised, password remains secure")
        input("\nPress Enter to continue...\n")

    def demonstrate_attack_scenarios(self):
        """Demonstrate various attack scenarios"""
        print(f"{Fore.YELLOW}2. Attack Scenario Demonstrations{Style.RESET_ALL}")
        print("-" * 60)
        
        password = "MySecurePass123"
        
        # Replay Attack
        print("\nReplay Attack Scenario:")
        print("Generating two proofs for the same password...")
        proof1 = self.zkp.generate_proof(password)
        time.sleep(1)  # Small delay
        proof2 = self.zkp.generate_proof(password)
        
        print(f"First Proof Commitment: {proof1['commitment']}")
        print(f"Second Proof Commitment: {proof2['commitment']}")
        print("Note: Each proof is different even for the same password")
        
        # Database Compromise
        print("\nDatabase Compromise Scenario:")
        _, public_key = self.zkp.generate_keypair(password)
        print(f"If attacker gets public key ({public_key})")
        print("They still cannot reverse-engineer the password")
        input("\nPress Enter to continue...\n")

    def demonstrate_authentication_process(self):
        """Demonstrate actual authentication process"""
        print(f"{Fore.YELLOW}3. Live Authentication Process{Style.RESET_ALL}")
        print("-" * 60)
        
        # Set up test account
        test_account = 999
        test_password = "TestPass123"
        
        print("Setting up test account...")
        success = dbe.setup_auth_for_new_account(test_account, test_password)
        
        if success:
            print("\nTesting Valid Password:")
            print(f"Account: {test_account}")
            print(f"Password: {test_password}")
            result = dbe.authenticate(test_account, test_password)
            print(f"Authentication Result: {Fore.GREEN if result else Fore.RED}{result}{Style.RESET_ALL}")
            
            print("\nTesting Invalid Password:")
            wrong_password = "WrongPass123"
            print(f"Account: {test_account}")
            print(f"Wrong Password: {wrong_password}")
            result = dbe.authenticate(test_account, wrong_password)
            print(f"Authentication Result: {Fore.GREEN if not result else Fore.RED}{result}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to set up test account{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...\n")

    def demonstrate_performance(self):
        """Demonstrate performance metrics"""
        print(f"{Fore.YELLOW}4. Performance Metrics{Style.RESET_ALL}")
        print("-" * 60)
        
        password = "TestPassword123"
        iterations = 100
        
        print(f"\nPerforming {iterations} authentications...")
        
        # ZKP Performance
        start_time = time.time()
        for _ in range(iterations):
            proof = self.zkp.generate_proof(password)
            _, public_key = self.zkp.generate_keypair(password)
            self.zkp.verify_proof(proof, public_key)
        zkp_time = time.time() - start_time
        
        # Traditional Performance
        start_time = time.time()
        for _ in range(iterations):
            hashlib.sha256(password.encode()).hexdigest()
        traditional_time = time.time() - start_time
        
        print(f"\nZKP Authentication Time (100 iterations): {zkp_time:.3f} seconds")
        print(f"Traditional Hash Time (100 iterations): {traditional_time:.3f} seconds")
        print("\nNote: ZKP is slightly slower but provides much stronger security guarantees")
        input("\nPress Enter to continue...\n")

    def security_comparison(self):
        """Show security comparison table"""
        print(f"{Fore.YELLOW}5. Security Feature Comparison{Style.RESET_ALL}")
        print("-" * 60)
        
        features = [
            ("Password Never Transmitted", "❌ No", "✅ Yes"),
            ("Resistant to Replay Attacks", "❌ No", "✅ Yes"),
            ("Safe if Database Compromised", "❌ No", "✅ Yes"),
            ("Unique Proof Each Login", "❌ No", "✅ Yes"),
            ("Protection Against Offline Attacks", "❌ No", "✅ Yes"),
        ]
        
        print("\nFeature               | Traditional | ZKP")
        print("-" * 50)
        for feature, trad, zkp in features:
            print(f"{feature:<20} | {trad:<11} | {zkp}")
        
        input("\nPress Enter to end demonstration...\n")

def main():
    demo = SecurityDemo()
    
    while True:
        print(f"{Fore.CYAN}Zero Knowledge Proof Security Demonstration{Style.RESET_ALL}")
        print("\nAvailable Demonstrations:")
        print("1. Traditional vs ZKP Authentication")
        print("2. Attack Scenario Demonstrations")
        print("3. Live Authentication Process")
        print("4. Performance Metrics")
        print("5. Security Feature Comparison")
        print("6. Exit")
        
        choice = input("\nSelect demonstration (1-6): ")
        print()
        
        if choice == '1':
            demo.demonstrate_traditional_vs_zkp()
        elif choice == '2':
            demo.demonstrate_attack_scenarios()
        elif choice == '3':
            demo.demonstrate_authentication_process()
        elif choice == '4':
            demo.demonstrate_performance()
        elif choice == '5':
            demo.security_comparison()
        elif choice == '6':
            print("Demonstration ended.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
