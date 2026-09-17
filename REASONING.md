# Architectural Reasoning & Implementation

## Design Decisions
- **Tech Stack:** Python, Flask, SQLite, Vanilla JS, and Tailwind CSS. This stack was chosen to eliminate complex build steps, Node module bloat, and hydration errors, allowing for ultra-fast execution within the 2.5-hour time limit.
- **Immutable Ledger System:** Instead of updating a static "points" integer on a user's profile, points are calculated dynamically by summing up a `Transaction` table. This prevents data corruption during simultaneous earning/spending and ensures the balance is mathematically foolproof.
- **Automated Tiers:** To remove manual work for cashiers, tiers (Base, Silver, Gold) are automatically evaluated on the backend based on `lifetime_earned` points whenever a purchase is logged.

## Implementation Approach
- **Backend-Heavy Logic:** Sorting, pagination, and math are all handled by the Flask/SQLite backend to keep the frontend completely lightweight and lightning-fast for the cashier.
- **Componentized Routes:** Flask Blueprints were used to separate Auth, Members, Purchases, and Redemptions into different files to keep the codebase clean and maintainable.

## Testing
- Logic was verified using an automated Python `requests` script to simulate a cashier workflow.
- Tested tier thresholds to ensure a user crossing 500 lifetime points instantly triggered the 1.5x Silver multiplier on their *next* purchase.
- Verified negative constraints (e.g., throwing an error if a member tries to redeem a 50-point item when they only have 40 points).

## Problems & Bugs Encountered
- **Bug:** Encountered a `[Errno 111] Connection refused` error when running the automated API test script.
- **Fix:** The issue occurred because the test script was trying to ping Port 5000 before the Flask application had bound to it. This was fixed by utilizing a dual-terminal workflow in Codespaces: running the server continuously in Tab 1, and executing tests in Tab 2.