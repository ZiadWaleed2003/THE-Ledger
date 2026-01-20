THE-Ledger

What is this?

An AI-powered asset manager.

As a user, you can manage your assets with the help of THE-Ledger. You can chat with it for financial council, or even query your asset database using natural language. Our multi-agent system will handle the heavy work.


---

Usage

1. Simply clone this repository.


2. Create and populate the required environment files as described below.

---

Backend Configuration

Inside the backend directory, add the following file:

.env

CEREBRAS_API_KEY=YOUR-API-KEY
LANGSMITH_API_KEY=YOUR-API-KEY
LANGSMITH_TRACING=TRUE
LANGSMITH_PROJECT=anyname you would like for the project on langsmith


---

Frontend Configuration

Inside the frontend directory, add the following file:

.env

VITE_BACKEND_URL=http://localhost:8000


---



3. After creating and populating both .env files, from the root directory run:



docker compose up



Notes

This is not the full documentation. The complete documentation will be added soon.

