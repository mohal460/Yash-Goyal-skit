# # import requests

# # BASE_URL = "http://127.0.0.1:5000"
# # session = requests.Session()  # This remembers our login cookie

# # print("--- 1. STAFF REGISTRATION & LOGIN ---")
# # session.post(f"{BASE_URL}/api/auth/register", json={"username": "cashier_1", "password": "password123"})
# # res = session.post(f"{BASE_URL}/api/auth/login", json={"username": "cashier_1", "password": "password123"})
# # print("Login:", res.json())

# # print("\n--- 2. CREATE A MEMBER ---")
# # res = session.post(f"{BASE_URL}/api/members/", json={"phone": "555-1234", "name": "Alex"})
# # print("Member Created:", res.json())

# # print("\n--- 3. EARN POINTS (Base Tier: 1x) ---")
# # # Spend $100. Should get 100 points.
# # res = session.post(f"{BASE_URL}/api/purchases/", json={"phone": "555-1234", "amount": 100})
# # print("Earned 100pts:", res.json())

# # print("\n--- 4. REDEEM POINTS (Math Check) ---")
# # # Redeem coffee for 40 points. Balance should drop to 60.
# # res = session.post(f"{BASE_URL}/api/redemptions/", json={"phone": "555-1234", "points": 40, "item": "Latte"})
# # print("Redeemed Latte:", res.json())

# # print("\n--- 5. LEVEL UP TO SILVER ---")
# # # Spend $400 more to hit 500 lifetime points (Silver threshold)
# # res = session.post(f"{BASE_URL}/api/purchases/", json={"phone": "555-1234", "amount": 400})
# # print("Hit Silver Tier:", res.json())

# # print("\n--- 6. SILVER MULTIPLIER CHECK (1.5x) ---")
# # # Spend $10. Should get 15 points instead of 10.
# # res = session.post(f"{BASE_URL}/api/purchases/", json={"phone": "555-1234", "amount": 10})
# # print("Silver Multiplier Earn:", res.json())

# # other this is test valid and validation 
# import requests

# BASE_URL = "http://127.0.0.1:5000"
# session = requests.Session()

# # Login first
# session.post(
#     f"{BASE_URL}/api/auth/login",
#     json={"username": "cashier_1", "password": "password123"}
# )

# print("\n--- TEST 1: MEMBER NOT FOUND ---")
# res = session.post(
#     f"{BASE_URL}/api/purchases/",
#     json={"phone": "9999999", "amount": 100}
# )
# print(res.status_code, res.json())

# print("\n--- TEST 2: REDEEM MORE THAN BALANCE ---")
# res = session.post(
#     f"{BASE_URL}/api/redemptions/",
#     json={
#         "phone": "555-1234",
#         "points": 99999,
#         "item": "Expensive Reward"
#     }
# )
# print(res.status_code, res.json())

# print("\n--- TEST 3: DUPLICATE MEMBER PHONE ---")
# res = session.post(
#     f"{BASE_URL}/api/members/",
#     json={"phone": "555-1234", "name": "Another Alex"}
# )
# print(res.status_code, res.json())

# print("\n--- TEST 4: WRONG LOGIN ---")
# bad_session = requests.Session()

# res = bad_session.post(
#     f"{BASE_URL}/api/auth/login",
#     json={"username": "cashier_1", "password": "wrongpassword"}
# )
# print(res.status_code, res.json())

# print("\n--- TEST 5: UNAUTHORIZED REQUEST ---")
# no_login = requests.Session()

# res = no_login.get(f"{BASE_URL}/api/members/")
# print(res.status_code, res.json())
#Test 3 — search, pagination and sorting

import requests

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

session.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "cashier_1", "password": "password123"}
)

print("\n--- TEST 1: SEARCH BY PHONE ---")
res = session.get(
    f"{BASE_URL}/api/members/",
    params={"search": "555-1234"}
)
print(res.status_code, res.json())

print("\n--- TEST 2: SEARCH BY NAME ---")
res = session.get(
    f"{BASE_URL}/api/members/",
    params={"search": "Alex"}
)
print(res.status_code, res.json())

print("\n--- TEST 3: PAGINATION ---")
res = session.get(
    f"{BASE_URL}/api/members/",
    params={"page": 1, "limit": 2}
)
print(res.status_code, res.json())

print("\n--- TEST 4: SORT BY POINTS ---")
res = session.get(
    f"{BASE_URL}/api/members/",
    params={
        "sort_by": "points",
        "order": "desc"
    }
)
print(res.status_code, res.json())

print("\n--- TEST 5: SORT BY NAME ---")
res = session.get(
    f"{BASE_URL}/api/members/",
    params={
        "sort_by": "name",
        "order": "asc"
    }
)
print(res.status_code, res.json())