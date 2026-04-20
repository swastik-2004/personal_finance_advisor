# Personal Finance AI Advisor

A production-grade full-stack AI-powered personal finance application combining backend engineering, machine learning, and LLM-based RAG to help users track spending, get predictions, and receive personalized financial advice.

**Live Demo:** https://personal-finance-advisor-ovjk.onrender.com

---

## Features

- **Transaction Management** — Add income/expense transactions manually or via CSV upload
- **Auto Categorization** — TF-IDF + Logistic Regression classifier predicts category as you type the description
- **Spending Forecasting** — Predicts next month's expenses from historical monthly averages
- **Anomaly Detection** — Isolation Forest flags unusual spending patterns personalized to your data
- **AI Chatbot** — RAG-based assistant answers financial questions using your transaction data as context
- **Visual Analytics** — Category doughnut chart + monthly trend line chart (Chart.js)
- **CSV Export** — Download all transactions as a CSV file
- **Secure Auth** — JWT-based authentication with bcrypt password hashing

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (async) |
| Database | PostgreSQL via Supabase + SQLAlchemy (async) |
| DB Driver | asyncpg |
| Auth | JWT (python-jose) + passlib (bcrypt) |
| Validation | Pydantic v2 |
| ML — Classification | TF-IDF + Logistic Regression (scikit-learn Pipeline) |
| ML — Forecasting | Monthly average (pandas time-series groupby) |
| ML — Anomaly Detection | Isolation Forest (scikit-learn, fitted at inference time) |
| RAG — Retrieval | TF-IDF cosine similarity (LangGraph wired, FAISS upgrade in progress) |
| RAG — Orchestration | LangChain + LangGraph |
| LLM | Groq API (llama-3.3-70b-versatile) |
| Frontend | Vanilla JS + Chart.js 4.4 |
| Containerization | Docker |
| Deployment | Render |
| Server | Uvicorn (ASGI) |

---

## Architecture

```
Browser (HTML/JS)
      │
      ▼
FastAPI Backend
      │
      ├── /auth          → JWT login/register
      ├── /transactions  → CRUD + CSV
      ├── /ml            → TF-IDF predict, IsolationForest anomaly, forecast
      └── /chat          → LangGraph RAG → Groq LLM
            │
            ├── retrieve_node  → TF-IDF knowledge retrieval
            └── respond_node   → Groq LLM with user context
```

---

## Project Structure

```
finance-advisor-backend/
├── app/
│   ├── api/               # Route handlers (auth, transactions, ml, chat)
│   ├── auth/              # Auth dependencies (get_current_user)
│   ├── core/              # Config, security (JWT, password hashing)
│   ├── db/                # SQLAlchemy engine, session, base
│   ├── models/            # ORM models (User, Transaction)
│   ├── schemas/           # Pydantic request/response schemas
│   └── main.py            # FastAPI app factory + CORS
├── ml/
│   ├── train.py           # TF-IDF + LogisticRegression training pipeline
│   ├── predict.py         # Category inference + spending forecast
│   └── models/
│       └── classifier.pkl # Pre-trained TF-IDF pipeline (committed)
├── rag/
│   ├── ingest.py          # FAISS vector store builder (HuggingFace embeddings)
│   ├── retriever.py       # TF-IDF cosine retriever (current)
│   ├── chatbot.py         # Groq LLM prompt + response
│   └── graph.py           # LangGraph: retrieve → respond workflow
├── finance-advisor-frontend/
│   └── index.html         # Single-page frontend (auth, dashboard, charts)
├── Dockerfile
├── render.yaml
├── requirements.txt
└── .env                   # Not committed — see setup below
```

---

## Database Schema

### Users
| Column | Type |
|---|---|
| id | Integer (PK) |
| email | String (unique) |
| password_hash | String |
| first_name | String |
| last_name | String |
| is_active | Boolean |
| created_at | DateTime |

### Transactions
| Column | Type |
|---|---|
| id | Integer (PK) |
| user_id | Integer (FK → users.id) |
| amount | Numeric(10,2) |
| description | String |
| category | String |
| transaction_type | String (income / expense) |
| date | DateTime |

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, returns JWT |
| GET | `/auth/me` | Get current user info |

### Transactions
| Method | Endpoint | Description |
|---|---|---|
| POST | `/transactions` | Add a transaction |
| GET | `/transactions` | Get all transactions |
| DELETE | `/transactions/{id}` | Delete a transaction |

### ML
| Method | Endpoint | Description |
|---|---|---|
| GET | `/ml/predict/category?description=` | Predict category from description text |
| GET | `/ml/predict/forecast` | Forecast next month's spending |
| GET | `/ml/predicted/anomalies` | Detect anomalous transactions |

### Chatbot
| Method | Endpoint | Description |
|---|---|---|
| POST | `/chat` | Ask AI a financial question |

### Health
| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Server + DB status |

---

## Setup (Local)

### 1. Clone the repo
```bash
git clone https://github.com/swastik-2004/personal_finance_advisor.git
cd personal_finance_advisor
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root:
```
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GROQ_API_KEY=your-groq-api-key
```

### 5. Build the FAISS vector store
```bash
python -m rag.ingest
```

### 6. Run the server
```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

---

## ML Pipeline

```
Transaction Description (text)
        │
        ▼
TF-IDF Vectorizer (ngram 1-2)
        │
        ▼
Logistic Regression Classifier
        │
        ▼
Predicted Category (Food / Rent / Travel / Shopping / Health / Entertainment / Utilities / Other)
```

- **Classifier** — scikit-learn Pipeline (TfidfVectorizer + LogisticRegression), trained on 75 labeled samples, pre-trained pkl committed to repo
- **Forecasting** — groups transactions by month, returns mean monthly spend
- **Anomaly Detection** — Isolation Forest fitted at inference time on the user's own expense history (no pkl dependency, personalized per user)

---

## RAG Chatbot Pipeline

```
User Query
    │
    ▼
LangGraph: retrieve_node
    │  TF-IDF cosine similarity over financial knowledge base
    ▼
LangGraph: respond_node
    │  Groq LLM (llama-3.3-70b) with retrieved context + user transaction summary
    ▼
Response
```

> Retrieval uses FAISS with HuggingFace sentence embeddings (`all-MiniLM-L6-v2`) for semantic search — finds relevant knowledge even when query wording differs from the stored documents.

---

## Docker

```bash
docker build -t finance-advisor .
docker run -p 8000:8000 --env-file .env finance-advisor
```

---

## Roadmap

- [x] FastAPI project structure
- [x] PostgreSQL + SQLAlchemy async ORM
- [x] JWT Authentication (register / login / me)
- [x] Transaction CRUD endpoints
- [x] TF-IDF expense classifier with auto-predict UI
- [x] Monthly spending forecast
- [x] Isolation Forest anomaly detection
- [x] LangGraph RAG chatbot (Groq LLM)
- [x] Chart.js dashboard (doughnut + trend line)
- [x] CSV export
- [x] Docker + Render deployment
- [x] FAISS vector store (semantic retrieval) — local only, live demo uses in-memory retrieval
- [ ] GitHub Actions CI/CD
- [ ] Bank API integration (Plaid)

---

## Resume Description

> Built a production-grade AI-powered personal finance advisor using FastAPI, PostgreSQL (Supabase), and LangChain — integrating a TF-IDF + Logistic Regression expense classifier, Isolation Forest anomaly detection, and a LangGraph RAG chatbot powered by Groq (LLaMA 3.3 70B) for personalized financial insights. Deployed live on Render with Docker.
