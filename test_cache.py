import time
import os
import sys

# Add server directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'server'))

from cache_manager import CacheManager
import dbs_exec as dbe

def test_cache_performance():
    print("\n=== Testing Cache Performance ===")
    
    # First query - should be from database
    print("\nExecuting first query (should hit database)...")
    start_time = time.time()
    result1 = dbe.executeQuery("SELECT * FROM CUSTOMERS")
    db_time = time.time() - start_time
    print(f"Database query time: {db_time:.4f} seconds")

    # Second query - should be from cache
    print("\nExecuting second query (should hit cache)...")
    start_time = time.time()
    result2 = dbe.executeQuery("SELECT * FROM CUSTOMERS")
    cache_time = time.time() - start_time
    print(f"Cache query time: {cache_time:.4f} seconds")
    
    # Show performance improvement
    if db_time > cache_time:
        improvement = ((db_time - cache_time) / db_time) * 100
        print(f"\nPerformance improvement: {improvement:.2f}%")

def test_cache_invalidation():
    print("\n=== Testing Cache Invalidation ===")
    
    # Get initial data
    print("\nGetting initial data...")
    result1 = dbe.executeQuery("SELECT * FROM CUSTOMERS")
    
    # Insert new data
    print("\nInserting new data (should invalidate cache)...")
    dbe.executeQuery("""
        INSERT INTO CUSTOMERS 
        (first_name, last_name, ssn_num, phone_num, sms, balance)
        VALUES 
        ('Test', 'User', '123456789', '9876543210', 'Y', 1000.0)
    """)
    
    # Get data again
    print("\nGetting data after insert (should hit database)...")
    result2 = dbe.executeQuery("SELECT * FROM CUSTOMERS")
    
    # Compare results
    if len(result2[1]) > len(result1[1]):
        print("Cache invalidation successful - new data retrieved from database")

def test_auth_cache():
    print("\n=== Testing Authentication Cache ===")
    
    # First authentication
    print("\nFirst authentication attempt...")
    start_time = time.time()
    auth1 = dbe.authenticate(0, "admin")  # Using admin credentials
    auth_time1 = time.time() - start_time
    print(f"First authentication time: {auth_time1:.4f} seconds")
    
    # Second authentication (should be cached)
    print("\nSecond authentication attempt (should be cached)...")
    start_time = time.time()
    auth2 = dbe.authenticate(0, "admin")
    auth_time2 = time.time() - start_time
    print(f"Second authentication time: {auth_time2:.4f} seconds")
    
    if auth_time1 > auth_time2:
        improvement = ((auth_time1 - auth_time2) / auth_time1) * 100
        print(f"\nAuthentication cache improvement: {improvement:.2f}%")

def monitor_cache():
    print("\n=== Monitoring Redis Cache ===")
    cache = CacheManager()
    
    try:
        while True:
            # Get all cache keys
            keys = cache.redis_client.keys('*')
            print("\nCurrent cache contents:")
            print("-" * 50)
            
            for key in keys:
                ttl = cache.redis_client.ttl(key)
                print(f"Key: {key}")
                print(f"TTL: {ttl} seconds")
                print("-" * 50)
            
            time.sleep(2)  # Update every 2 seconds
    except KeyboardInterrupt:
        print("\nCache monitoring stopped")

def main():
    print("=== Redis Cache Testing Suite ===")
    print("\nMake sure Redis server and both banking servers are running!")
    
    while True:
        print("\nAvailable tests:")
        print("1. Test Cache Performance")
        print("2. Test Cache Invalidation")
        print("3. Test Authentication Cache")
        print("4. Monitor Cache")
        print("5. Exit")
        
        choice = input("\nSelect test to run (1-5): ")
        
        if choice == '1':
            test_cache_performance()
        elif choice == '2':
            test_cache_invalidation()
        elif choice == '3':
            test_auth_cache()
        elif choice == '4':
            monitor_cache()
        elif choice == '5':
            print("\nExiting test suite...")
            break
        else:
            print("\nInvalid choice!")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
