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

### **Get Your Gemini API Key**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Create new API key
4. Copy and paste into `.env` file

---

## 📱 Usage Guide

### **1. User Registration & Login**
- Visit `http://localhost:3000`
- Create account or login with existing credentials
- Secure JWT authentication with password hashing

### **2. Ask Legal Questions**
- **Click blue suggestions** for quick queries
- **Type custom questions** about Indian law
- Get **instant AI responses** with source citations

### **3. Chat History**
- **View previous conversations** in sidebar
- **Resume old chats** or start new sessions
- **Auto-saved sessions** with descriptive names

### **4. Example Queries**
```
✅ "What is PIL in Indian law?"
✅ "How to file an FIR for theft?"
✅ "Consumer protection rights in India"
✅ "Marriage registration process"
✅ "Section 302 IPC punishment"
✅ "Property dispute resolution"
```

---

## 🏗️ Project Structure

```
legalGPT/
├── 📁 backend/
│   ├── 📁 auth/              # JWT authentication system
│   ├── 📁 database/          # Database connection & config
│   ├── 📁 models/            # SQLAlchemy database models
│   ├── 📁 routes/            # FastAPI API endpoints
│   │   ├── auth.py           # User authentication routes
│   │   └── chat.py           # Chat and legal query routes
│   ├── 📁 schemas/           # Pydantic data validation models
│   ├── 📁 services/          # Business logic & Gemini AI service
│   ├── 📄 main.py            # FastAPI application entry point
│   ├── 📄 requirements.txt   # Python dependencies
│   ├── 📄 .env               # Environment configuration
│   └── 📊 legal_ai_database.db # SQLite database file
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📁 components/    # React components
│   │   │   ├── AuthPage.js   # Login/Register component
│   │   │   └── ChatHistory.js # Chat sidebar component  
│   │   ├── 📄 App.js         # Main React application
│   │   └── 📄 index.js       # React entry point
│   ├── 📄 package.json       # Node.js dependencies
│   └── 📄 tailwind.config.js # Tailwind CSS configuration
├── 📄 README.md              # Project documentation
└── 📄 QUICKSTART.md          # Quick setup guide
```

---

## 🔌 API Endpoints

### **Authentication**
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### **Chat & Legal Queries**
- `POST /chat/message` - Send legal query and get AI response
- `GET /chat/sessions` - Get user's chat sessions
- `GET /chat/history/{session_id}` - Get specific chat history

### **System**
- `GET /` - API health check
- `GET /health` - Detailed system health

---

## 📊 Database Schema

The application uses **SQLite** with 6 main tables:

### **Users Table**
```sql
- id (Primary Key)
- email, username, full_name
- hashed_password (bcrypt)
- is_active, is_admin
- created_at, last_login
```

### **Legal Queries Table**  
```sql
- id (Primary Key)
- user_id, chat_session_id
- query_text, response_text
- query_category, ai_model_used
- response_sources (JSON)
- confidence_score, response_time_ms
```

**View Database:** Run `python backend/explore_database.py` to inspect data.

---

## 🔒 Security Features

- **🔐 JWT Authentication** - Secure token-based auth
- **🛡️ Password Hashing** - bcrypt with salt rounds
- **⚡ CORS Protection** - Configured for frontend domain
- **✅ Input Validation** - Pydantic schema validation
- **🔍 SQL Injection Prevention** - SQLAlchemy ORM protection

---

## 🚨 Troubleshooting

### **Common Issues**

**❌ "Module not found" errors**
```bash
# Ensure you're in the right directory and dependencies are installed
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

**❌ "Port already in use" errors**
```bash
# Kill processes on ports 3000/8000
npx kill-port 3000 8000

# Or use different ports
uvicorn main:app --port 8001
```

**❌ "Gemini API key invalid"**
- Check your API key in `.env` file
- Verify key is active at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Ensure no extra spaces in the key

**❌ Database connection issues**
```bash
# Reset database (will lose data)
rm backend/legal_ai_database.db
# Restart backend to recreate tables
```

### **Debug Mode**
```bash
# Run backend with debug logging
cd backend && uvicorn main:app --reload --log-level debug

# Check frontend console for errors
# Open browser DevTools → Console
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature-name`
3. **Make changes** and test thoroughly
4. **Commit**: `git commit -m "Add feature description"`
5. **Push**: `git push origin feature-name`
6. **Create Pull Request**

### **Development Guidelines**
- Follow **PEP 8** for Python code
- Use **ESLint** for JavaScript/React code
- Add **docstrings** to functions
- Write **unit tests** for new features
- Update **documentation** for API changes

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini AI** - Powering intelligent legal responses
- **FastAPI** - High-performance backend framework  
- **React** - Modern frontend development
- **Indian Legal System** - Comprehensive law coverage

---

## 📞 Support

**Having issues?** 
- 📧 **Email**: support@legalgpt.com
- 🐛 **Bug Reports**: Create an issue on GitHub
- 💡 **Feature Requests**: Submit via GitHub Issues
- 📖 **Documentation**: Check [QUICKSTART.md](QUICKSTART.md)

---

**⚖️ Legal Disclaimer**: LegalGPT provides information for educational purposes only. Always consult qualified legal professionals for specific legal advice.

---

<div align="center">

**Built with ❤️ for the Indian Legal Community**

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/legalGPT?style=social)](https://github.com/yourusername/legalGPT)
[![Follow](https://img.shields.io/twitter/follow/yourusername?style=social)](https://twitter.com/yourusername)

</div>