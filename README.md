# Multi-Agent System LLM for Educational Content Generation

## 📖 Overview

A web-based Multi-Agent System (MAS) powered by Large Language Models (LLM) that automatically generates high-quality educational materials including lecture notes, presentation slides, and quiz assessments. The system features a modern web interface built with Next.js and a robust FastAPI backend. Users simply need to log in and request the system to generate corresponding learning content. The system integrates Retrieval-Augmented Generation (RAG) technology to query and utilize knowledge from user-uploaded source documents such as textbooks and reference materials.

## ✨ Key Features

- **🌐 Web-based Interface**: Modern, responsive web application built with Next.js
- **⚡ FastAPI Backend**: High-performance API with automatic documentation
- **🔐 User Authentication**: Secure login system with user management
- **🎨 Intuitive UI/UX**: User-friendly interface for seamless content generation
- **🤖 Multi-Agent Architecture**: Specialized agents designed separately for each type of educational content
- **📚 RAG Integration**: Intelligent querying from knowledge base built from user documents
- **📝 Lecture Notes Generation**: Automatically create structured and detailed lecture notes
- **🎯 Slide Presentation**: Generate professional presentation slides with proper formatting
- **❓ Quiz Generation**: Create diverse multiple-choice questions with varying difficulty levels
- **📤 Document Upload**: Support for uploading and processing multiple document formats
- **🔍 Intelligent Retrieval**: Accurate search and extraction of relevant information

## 🏗️ System Architecture

![](/resources/multiagent_workflow.svg)

## 🚀 Getting Started

### System Requirements

- **Frontend**: Node.js 18+, npm/yarn
- **Backend**: Python 3.9+, FastAPI, Uvicorn
- **Database**: PostgreSQL 13+ (for user data), Vector DB (for embeddings)
- **Authentication**: JWT tokens, OAuth support
- **Storage**: Local/Cloud storage for document uploads
- **GPU**: Recommended for faster LLM processing

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/multi-agent-llm-education.git
cd multi-agent-llm-education
```

2. **Install dependencies**
```bash
# Backend (FastAPI)
cd backend
pip install -r requirements.txt

# Frontend (Next.js)
cd frontend
npm install
# or
yarn install
```

### Running the Application

**Direct execution:**
```bash
# Backend (FastAPI)
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Frontend (Next.js) - new terminal
cd frontend
npm run dev
# or
yarn dev
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Configuration

### LLM Models
The system supports multiple LLM provider:
- Google Gemini


## 🤖 Agents

### 1. Lecture Notes Agent
- **Function**: Generate structured lecture notes
- **Input**: Topic, learning objectives, source documents
- **Output**: Formatted lecture notes with headings, bullet points, examples

### 2. Slide Creator Agent  
- **Function**: Generate presentation slides
- **Input**: Content outline, presentation style
- **Output**: Slide deck with titles, content, transitions

### 3. Quiz Generator Agent
- **Function**: Create multiple-choice questions
- **Input**: Content area, difficulty level, question types
- **Output**: Multiple choice questions with answers and explanations

### 4. Content Reviewer Agent
- **Function**: Review and ensure content quality
- **Input**: Generated content from other agents
- **Output**: Reviewed and refined content

## 💻 Web Interface Usage

### 1. User Authentication
- **Sign Up**: Create a new account with email verification
- **Login**: Access your dashboard with email/password or OAuth
- **Dashboard**: View your generated content and manage documents

### 2. Document Upload
- Upload textbooks, PDFs, DOCX files through the web interface
- Real-time processing status with progress indicators
- Document preview and metadata extraction

### 3. Content Generation Workflow
```
Login → Upload Documents → Select Content Type → Configure Options → Generate → Download/Export
```

### 4. Interactive Features
- **Real-time Generation**: Live updates during content creation
- **Content Preview**: Review generated content before downloading
- **History Management**: Access previously generated materials
- **Export Options**: Multiple formats (PDF, DOCX, PPTX, Markdown)


## 📊 Sample Outputs

### Lecture Notes Sample
```markdown
# Machine Learning Fundamentals

## 1. Introduction
Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed...

## 2. Types of Machine Learning
### 2.1 Supervised Learning
- Definition and characteristics
- Common algorithms: Linear Regression, Decision Trees
- Applications: Classification, Regression

### 2.2 Unsupervised Learning
...
```

### Quiz Sample
```json
{
  "question": "What is the primary goal of supervised learning?",
  "options": [
    "A. To find hidden patterns in data",
    "B. To predict outcomes based on labeled training data",
    "C. To reduce dimensionality",
    "D. To cluster similar data points"
  ],
  "correct_answer": "B",
  "explanation": "Supervised learning uses labeled training data to learn a mapping function that can predict outcomes for new, unseen data."
}
```

## 📝 FastAPI Endpoints

### Authentication Endpoints
```http
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
```

### Document Management
```http
POST /api/documents/upload
GET  /api/documents/
GET  /api/documents/{document_id}
DELETE /api/documents/{document_id}
```

### Task Management
```http
GET  /api/tasks/{task_id}        # Get task status
GET  /api/tasks/                 # List user tasks
POST /api/tasks/{task_id}/cancel # Cancel running task
```

## 📊 Performance Metrics

- **Response Time**: 
- **Accuracy**: 
- **Throughput**: 
- **Storage**: 

## 🛠️ Development

### Project Structure
```
multi-agent-llm-education/
├── frontend/                    # Next.js application
│   ├── components/             # React components
│   │   ├── auth/              # Authentication components
│   │   ├── dashboard/         # Dashboard components
│   │   ├── generation/        # Content generation UI
│   │   └── common/            # Shared components
│   ├── pages/                 # Next.js pages
│   │   ├── api/              # API routes (if using Next.js API)
│   │   ├── auth/             # Authentication pages
│   │   ├── dashboard/        # Dashboard pages
│   │   └── generate/         # Generation pages
│   ├── styles/               # CSS/SCSS files
│   ├── utils/                # Utility functions
│   └── hooks/                # Custom React hooks
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── auth/         # Authentication routes
│   │   │   ├── documents/    # Document management
│   │   │   └── generate/     # Content generation
│   │   ├── agents/           # Agent implementations
│   │   ├── core/             # Core functionality
│   │   │   ├── auth.py       # Authentication logic
│   │   │   ├── database.py   # Database connection
│   │   │   └── config.py     # Configuration
│   │   ├── models/           # Pydantic models
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utility functions
│   ├── alembic/              # Database migrations
│   └── tests/                # Backend tests
├── shared/                     # Shared configurations
├── docker-compose.yml          # Docker setup
├── docs/                      # Documentation
└── scripts/                   # Setup scripts
```

## 📞 Support

If you encounter any issues or have questions:
- Create an [Issue](https://github.com/yourusername/multi-agent-llm-education/issues)
- Email: your.email@example.com

## 🔮 Roadmap

- [ ] **Enhanced UI/UX**: Dark mode, themes, accessibility improvements
- [ ] **Real-time Collaboration**: Multi-user document editing and sharing
- [ ] **Advanced Analytics**: Usage statistics and content performance metrics
- [ ] **Mobile App**: React Native mobile application
- [ ] **Integration APIs**: LMS integration (Moodle, Canvas, Blackboard)
- [ ] **AI Improvements**: Fine-tuned models for educational content
- [ ] **Multi-language Support**: Internationalization and localization
- [ ] **Advanced Export**: Interactive presentations, SCORM packages
- [ ] **Voice Integration**: Text-to-speech for generated content
- [ ] **Plagiarism Detection**: Content originality checking

---

⭐ **If this project helps you, please give it a star!** ⭐
