# Yash-Goyal-skit
# Café Rewards POS

## Project Overview
A lightning-fast, full-stack Point-of-Sale (POS) loyalty dashboard built specifically for café counters. It features an immutable transaction ledger to guarantee 100% accurate points calculations, automated tier upgrades (Base, Silver, Gold), and instant customer lookups with search, pagination, and sorting.

## Setup & Installation
1. Open the project in GitHub Codespaces.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## How to Run
1. Ensure your virtual environment is active: `source venv/bin/activate`
2. Start the backend server: `python app.py`
3. Click "Open in Browser" when Codespaces forwards Port 5000.

## How to Debug
- **Database Reset:** If you need to clear the data, simply delete the `instance/cafe_rewards.db` file and restart the server. The database will automatically rebuild itself.
- **Connection Refused:** If you see a port error, ensure `app.py` is running in an active terminal tab before running test scripts or opening the browser.
- **Frontend Errors:** Open the browser's Developer Tools (F12) and check the Console or Network tab to see exact API responses.

## API Endpoints
- `POST /api/auth/register` - Register a new staff account
- `POST /api/auth/login` - Authenticate staff (Session based)
- `POST /api/auth/logout` - Clear staff session
- `GET /api/members/` - Retrieve customers (supports `?search=`, `&page=`, `&sort_by=`)
- `POST /api/members/` - Add a new customer
- `POST /api/purchases/` - Log a purchase (auto-applies tier multipliers)
- `POST /api/redemptions/` - Deduct points for a reward