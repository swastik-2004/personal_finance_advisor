# Personal Finance AI Advisor

A production-grade full-stack AI-powered personal finance application that combines backend engineering, machine learning, and LLM-based RAG to help users track spending, get predictions, and receive personalized financial advice.

---

## Features

- **Transaction Management** — Upload CSV or manually add income/expense transactions
- **Auto Categorization** — ML model classifies transactions (Food, Rent, Travel, etc.)
- **Spending Forecasting** — Predicts next month's expenses using time-series models
- **Anomaly Detection** — Flags unusual spending patterns
- **AI Chatbot** — RAG-based assistant answers financial questions using your own data
- **Secure Auth** — JWT-based authentication with bcrypt password hashing

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL + SQLAlchemy (async) |
| DB Driver | asyncpg |
| Migrations | Alembic |
| Auth | JWT (python-jose) + passlib (bcrypt) |
| Validation | Pydantic v2 |
| ML | scikit-learn, XGBoost, Prophet |
| RAG | LangChain, LangGraph, FAISS, Sentence Transformers |
| LLM | OpenAI GPT / HuggingFace |
| Server | Uvicorn (ASGI) |

---

## Project Structure

```
finance-advisor-backend/
├── app/
│   ├── api/               # Route handlers (auth, transactions, ML, chat)
│   ├── auth/              # Auth dependencies (get_current_user)
│   ├── core/              # Config, security (JWT, hashing)
│   ├── db/                # SQLAlchemy engine, session, base
│   ├── models/            # ORM models (User, Transaction)
│   ├── schemas/           # Pydantic request/response schemas
│   └── main.py            # FastAPI app factory
├── ml/
│   ├── train.py           # Training pipeline
│   ├── predict.py         # Inference
│   └── models/            # Saved model files
├── rag/
│   ├── ingest.py          # Document ingestion into vector DB
│   ├── retriever.py       # FAISS vector search
│   ├── chatbot.py         # LLM interaction
│   └── graph.py           # LangGraph workflow
├── db/
│   └── schema.sql         # Raw SQL schema reference
├── config/                # Extra configuration files
├── requirements.txt
├── run.py                 # Entry point
└── .env                   # Environment variables (not committed)
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
| category | String (nullable) |
| transaction_type | String (income/expense) |
| date | DateTime |

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, returns JWT |

### Transactions
| Method | Endpoint | Description |
|---|---|---|
| POST | `/transactions` | Add a transaction |
| GET | `/transactions` | Get all transactions |
| DELETE | `/transactions/{id}` | Delete a transaction |

### ML
| Method | Endpoint | Description |
|---|---|---|
| GET | `/predict/expenses` | Forecast next month spend |
| GET | `/anomaly/check` | Detect anomalies |

### Chatbot
| Method | Endpoint | Description |
|---|---|---|
| POST | `/chat` | Ask AI a financial question |

### Health
| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Server + DB status |

---

## Setup

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
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/finance_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
OPENAI_API_KEY=your-openai-key
```

### 5. Set up PostgreSQL
- Create a database named `finance_db`
- Run Alembic migrations (once configured):
```bash
alembic upgrade head
```

### 6. Run the server
```bash
python run.py
```

API available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

---

## ML Pipeline

```
Raw Transactions → Cleaning → Feature Engineering → Model Training → Saved Model
                                                                          ↓
                                                               Inference via API
```

Models:
- **Classification** — XGBoost categorizes transaction descriptions
- **Forecasting** — Prophet predicts monthly spending
- **Anomaly Detection** — Isolation Forest flags unusual transactions

---

## RAG Chatbot Pipeline

```
User Query → Embedding → FAISS Vector Search → Top-K Context → LLM → Response
```

- Embeddings: Sentence Transformers
- Vector DB: FAISS
- Orchestration: LangChain + LangGraph
- LLM: OpenAI GPT-4 / HuggingFace

---

## Roadmap

- [x] Project structure & environment setup
- [x] Database models (User, Transaction)
- [x] JWT Authentication
- [ ] Transaction CRUD endpoints
- [ ] Alembic migrations
- [ ] ML expense classifier
- [ ] Spending forecasting
- [ ] Anomaly detection
- [ ] RAG chatbot
- [ ] Docker + deployment (AWS EC2 + Nginx)

---

## Resume Description

> Built a production-grade AI-powered personal finance advisor using FastAPI, PostgreSQL, and LangChain — integrating ML models (XGBoost, Prophet) for expense classification and forecasting with a RAG-based chatbot (FAISS + GPT-4) for personalized financial insights.
