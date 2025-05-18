## 🤖 AI Research Assistant Chatbot

A modular, containerized multi-agent system for personalized Q/A, research guidance, and reasoning—built using:

* 🧠 **Agno Agents** for multi-step task orchestration
* 🧾 **FastAPI** for high-performance backend
* 🖼 **Streamlit** for interactive chat UI
* 🧠 **Mem0 AI** for session-based short-term memory
* 📦 **Vector DB** for long-term semantic memory (e.g., Weaviate)
* 🧮 **PostgreSQL** for user profile & metadata storage
* 🔐 **JWT-based authentication**
* 🧠 **Reasoning strategies**: Chain of Thought, Tree of Thought, Graph of Thought
* 📄 **PDF ingestion** and embedding for custom knowledge bases

---

## 📁 Project Structure

```
research-chatbot/
├── backend/                 # FastAPI backend
│   ├── app/                # Core backend logic
│   │   ├── core/           # Config, logging, security
│   │   ├── api/            # API routers (auth, chat, pdf)
│   │   ├── db/             # SQLAlchemy session, models, schemas, CRUD
│   │   ├── agents/         # Agno multi-agent implementations
│   │   └── utils/          # Helper functions (PDFs, embeddings)
│   ├── Dockerfile
│   ├── .env
│   └── requirements.txt
├── frontend/               # Streamlit frontend
│   ├── streamlit_app/      # App code and components
│   ├── Dockerfile
│   ├── .env
│   └── requirements.txt
├── docker-compose.yml      # Orchestrates backend, frontend, DBs
├── .env                    # (Optional) shared config
└── README.md
```

---

## ⚙️ Features

✅ **Multi-Agent Task Orchestration**
✅ **Upload and Embed PDFs** for custom research
✅ **Memory Layer**

* Short-Term: session memory with Mem0
* Long-Term: vector DB + summarization
  ✅ **User Profiles & Progress** tracked in PostgreSQL
  ✅ **Authentication** with JWT tokens
  ✅ **Interactive UI** built in Streamlit
  ✅ **Switchable Reasoning Modes**:
* Chain of Thought (CoT)
* Tree of Thought (ToT)
* Graph of Thought (GoT)
  ✅ **Logging** and custom error handling

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/research-chatbot.git
cd research-chatbot
```

### 2. Configure Environment Variables

#### `backend/.env`

```env
DATABASE_URL=postgresql://user:password@postgres:5432/chatbot
SECRET_KEY=super-secret-key
VECTOR_DB_URL=http://vectordb:8080
```

#### `frontend/.env`

```env
API_URL=http://backend:8000
```

### 3. Build & Run with Docker Compose

```bash
docker-compose up --build
```

### 4. Access the App

| Component    | URL                                                      |
| ------------ | -------------------------------------------------------- |
| Frontend UI  | [http://localhost:8501](http://localhost:8501)           |
| FastAPI Docs | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Vector DB    | [http://localhost:8080/v1](http://localhost:8080/v1)     |
| PostgreSQL   | localhost:5432 (internal only)                           |

---

## 🧠 How It Works

### 🎯 Reasoning Modes

Choose between different cognitive reasoning tools:

* **Chain of Thought** – step-by-step logic
* **Tree of Thought** – branching reasoning with backtracking
* **Graph of Thought** – node/state based reasoning paths

### 📥 PDF Upload

1. Upload research papers via the sidebar.
2. PDFs are parsed, chunked, embedded, and stored in the vector DB.
3. Relevant chunks are retrieved for Q/A during chat.

### 🧬 Memory System

* **Short-term memory**: Mem0 keeps session state.
* **Long-term memory**: Periodically summarized and embedded into vector DB.
* **Personalization**: User profile tracks interests, past topics, and progress.

---

## 🔒 Authentication

JWT-based login and registration via `/auth/login` and `/auth/register`.

---

## 🧪 Example API Requests

### Login

```http
POST /auth/login
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Chat

```http
POST /chat
Headers: Authorization: Bearer <token>
{
  "message": "What is the transformer architecture?",
  "mode": "chain"
}
```

---

## 🛠 Dev Scripts

Run backend locally:

```bash
cd backend
uvicorn app.main:app --reload
```

Run frontend locally:

```bash
cd frontend
streamlit run streamlit_app/app.py
```

---

## ✅ To Do

* [ ] Implement OAuth login (e.g. GitHub, Google)
* [ ] Add LangChain agent interface
* [ ] Expand PDF source types (arXiv, web scrapers)
* [ ] Track weekly user progress analytics
* [ ] Add CI/CD pipeline for tests and Docker build

---

## 🧠 Tech Stack

| Tool       | Purpose                          |
| ---------- | -------------------------------- |
| FastAPI    | REST API backend                 |
| Agno       | Multi-agent orchestration        |
| Mem0       | Short-term memory                |
| Streamlit  | Frontend web UI                  |
| PostgreSQL | User profile & progress tracking |
| Vector DB  | Long-term memory (e.g. Weaviate) |
| Docker     | Containerized deployment         |

---

## 📄 License

MIT License © 2025 Taufeeq Ahmad

---

