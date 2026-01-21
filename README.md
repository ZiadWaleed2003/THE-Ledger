# THE-Ledger

## What the heck is this?

An AI-powered asset manager.

As a user, you can manage your assets with the help of **THE-Ledger**. You can chat with it for financial council, or even query your asset database using natural language. Our multi-agent system will handle the heavy work.

- you can also chat with Mr Devin here for more details about the project --> [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ZiadWaleed2003/THE-Ledger)
- for the sake of simplicity I chose SQLite with SQLAlchemy (I mean it's simple and easy to use and at the end this is project is a POC only)
- also I used Langchain here to orchestrate the workflow of the 2 agents
 ![Untitled - Frame 1 (2)](https://github.com/user-attachments/assets/b5f41d61-894b-4d0e-9ef9-8597f2a18175)



---

## Usage

1. Simply clone this repository.
2. Create and populate the required environment files as described below.

---

### Backend Configuration

Inside the `backend` directory, add the following file:

**.env**

```
CEREBRAS_API_KEY=YOUR-API-KEY
LANGSMITH_API_KEY=YOUR-API-KEY
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=anyname you would like for the project on langsmith
```

---

### Frontend Configuration

Inside the `frontend` directory, add the following file:

**.env**

```
VITE_BACKEND_URL=http://localhost:8000
```

---
[<img width="80" height="80" alt="image" src="https://github.com/user-attachments/assets/cd0825c1-fa7d-43b0-8db1-fa6726f4e599" />](https://icons8.com/icon/zFAYIdFZlGxP/docker) 
## Docker
3. After creating and populating both `.env` files, from the root directory run:

```
docker compose up
```


