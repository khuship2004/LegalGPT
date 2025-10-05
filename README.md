# 🏛️ LegalGPT v2.0

**An AI-powered Legal Assistant for Indian Law** - Get instant, accurate legal guidance with proper source citations using Google Gemini AI.

![LegalGPT](https://img.shields.io/badge/LegalGPT-v2.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-brightgreen?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi)

---

## 🚀 Features

### 🤖 **AI-Powered Legal Assistant**
- **Google Gemini Integration** - Latest AI model for accurate responses
- **Source Citations** - Every answer includes proper legal references
- **Context-Aware** - Understands Indian legal framework

### ⚖️ **Comprehensive Legal Coverage**
- 🏛️ **Constitutional Law** - Articles, fundamental rights, PIL procedures
- ⚖️ **Criminal Law** - IPC sections, FIR procedures, court processes
- 📋 **Civil Law** - Contract law, property disputes, family matters
- 🛡️ **Consumer Protection** - Rights, complaint procedures, redressal
- 🏢 **Corporate Law** - Company registration, compliance, disputes
- 👨‍👩‍👧‍👦 **Family Law** - Marriage, divorce, adoption, surrogacy laws

### 💼 **Professional Features**
- 🔐 **User Authentication** - Secure JWT-based login system
- 💬 **Chat History** - Persistent conversation storage
- 📊 **Analytics Dashboard** - Track usage and performance
- 🔍 **Advanced Search** - Find previous legal queries
- 📱 **Responsive Design** - Works on desktop and mobile

---

## 🛠️ Tech Stack

**Backend:**
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - Database ORM with SQLite
- **Google Gemini API** - AI-powered responses
- **JWT Authentication** - Secure user sessions
- **Pydantic** - Data validation and serialization

**Frontend:**
- **React 18** - Modern UI framework
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icons

**Database:**
- **SQLite** - Lightweight, file-based database
- **6 Tables** - Users, sessions, queries, documents, feedback, analytics

---

## 📦 Installation & Setup

### **Prerequisites**
- **Python 3.9+** installed
- **Node.js 16+** and npm installed
- **Google Gemini API key** (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd legalGPT
```

### **2. Backend Setup**
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Edit .env file and add your Gemini API key
# GEMINI_API_KEY=your_api_key_here
```

### **3. Frontend Setup**
```bash
# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
npm install
```

---

## 🚀 Running the Application

### **Start Backend Server**
```bash
cd backend
uvicorn main:app --host 127.0.0.1 --port 8000

# Or alternatively:
python main.py
```

**Backend will be available at:** `http://127.0.0.1:8000`

### **Start Frontend Application**
```bash
cd frontend
npm start
```

**Frontend will be available at:** `http://localhost:3000`

### **🎯 Quick Start Commands**
```bash
# Terminal 1: Start Backend
cd legalGPT/backend && uvicorn main:app --host 127.0.0.1 --port 8000

# Terminal 2: Start Frontend  
cd legalGPT/frontend && npm start
```

---

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file in the `backend/` directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development

# Google Gemini API (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Security
SECRET_KEY=your-secret-key-change-in-production

# CORS
CORS_ORIGINS=http://localhost:3000

# Database (SQLite - auto-configured)
# DATABASE_URL=sqlite:///./legal_ai_database.db
```


## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---
