import os
import json

# BAD WAY ❌ - never do this
def bad_database_connect():
    password = "admin123"  # hardcoded!
    host = "db.internal"
    return f"Connected to {host} with {password}"

# GOOD WAY ✅ - environment variable
def good_database_connect_env():
    password = os.environ.get('DB_PASSWORD')
    if not password:
        raise ValueError("DB_PASSWORD not set!")
    host = os.environ.get('DB_HOST', 'localhost')
    return f"Connected to {host} (password from env)"

# BEST WAY ✅ - secrets file (simulating Secrets Manager)
def best_database_connect():
    try:
        # In production: call AWS Secrets Manager
        # Here we simulate with a local secrets file
        with open('/tmp/secrets.json', 'r') as f:
            secrets = json.load(f)
        password = secrets['db_password']
        return f"Connected using rotated secret (expires: {secrets['expires']})"
    except FileNotFoundError:
        return "Secrets file not found - use Secrets Manager in production"

# Test all three approaches
print("=== Secrets Management Demo ===")
print(f"BAD:  {bad_database_connect()}")

os.environ['DB_PASSWORD'] = 'env_password_123'
os.environ['DB_HOST'] = 'prod-db.internal'
print(f"GOOD: {good_database_connect_env()}")

# Create a simulated secrets file
secrets = {
    "db_password": "r0t4t3d_p@ssw0rd_xyz",
    "expires": "2026-04-24T00:00:00Z",
    "version": "v3"
}
with open('/tmp/secrets.json', 'w') as f:
    json.dump(secrets, f)

print(f"BEST: {best_database_connect()}")
print("\n✅ Notice: no real password appears in source code!")
