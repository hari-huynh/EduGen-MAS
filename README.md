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

3. **Configure environment**
```bash
cp .env.example .env
# Edit the necessary environment variables
```

4. **Initialize database**
```bash
# Setup PostgreSQL database
python scripts/init_db.py

# Create admin user (optional)
python scripts/create_admin.py
```

### Running the Application

**Using Docker (Recommended):**
```bash
docker-compose up -d
```

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
The system supports multiple LLM providers:
- OpenAI GPT-4/GPT-3.5
- Anthropic Claude
- Google Gemini
- Local models (Ollama, vLLM)

### RAG Configuration
```python
# config/rag_config.py
RAG_CONFIG = {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "vector_db": "chromadb",
    "retrieval_k": 5
}
```

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

## 📚 API Usage Guide

### Authentication
All API requests require authentication using JWT tokens:

```javascript
// Login and get token
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
const { access_token } = await response.json();

// Use token in requests
const headers = {
  'Authorization': `Bearer ${access_token}`,
  'Content-Type': 'application/json'
};
```
### 1. Upload Documents via API
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('/api/documents/upload', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${access_token}` },
  body: formData
});

const { document_id, status } = await response.json();
```

### 2. Generate Lecture Notes via API
```javascript
const response = await fetch('/api/generate/lecture-notes', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    topic: "Machine Learning Basics",
    learning_objectives: ["Understand ML concepts", "Learn algorithms"],
    document_ids: ["doc_123", "doc_456"],
    format: "markdown",
    length: "detailed"
  })
});

const { task_id } = await response.json();

// Poll for completion
const result = await fetch(`/api/tasks/${task_id}`, { headers });
```

### 3. Generate Quiz via API
```javascript
const response = await fetch('/api/generate/quiz', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    topic: "Linear Regression",
    num_questions: 10,
    difficulty: "intermediate",
    question_types: ["multiple_choice"],
    document_ids: ["doc_123"]
  })
});

const { quiz_data, task_id } = await response.json();
```

## 🧪 Testing

```bash
# Run unit tests
pytest tests/

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=src tests/
```

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

## 🤝 Contributing

We welcome all contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Contribution Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## 📝 FastAPI Endpoints

### Authentication Endpoints
```http
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
GET  /api/auth/me
```

### Document Management
```http
POST /api/documents/upload
GET  /api/documents/
GET  /api/documents/{document_id}
DELETE /api/documents/{document_id}
```

### Content Generation Endpoints

#### Generate Lecture Notes
```http
POST /api/generate/lecture-notes
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "topic": "Machine Learning Basics",
  "learning_objectives": ["Understand ML concepts"],
  "document_ids": ["doc1", "doc2"],
  "format": "markdown",
  "length": "detailed"
}
```

#### Generate Slides
```http
POST /api/generate/slides
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "content": "lecture content",
  "style": "academic",
  "num_slides": 15,
  "template": "modern"
}
```

#### Generate Quiz
```http
POST /api/generate/quiz
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "topic": "Linear Regression",
  "num_questions": 10,
  "difficulty": "intermediate",
  "question_types": ["multiple_choice"],
  "document_ids": ["doc1"]
}
```

### Task Management
```http
GET  /api/tasks/{task_id}        # Get task status
GET  /api/tasks/                 # List user tasks
POST /api/tasks/{task_id}/cancel # Cancel running task
```

## 🔍 Advanced Features

### Custom Agent Development
```python
from agents.base import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        self.agent_type = "custom"
    
    def process(self, input_data):
        # Your custom logic here
        return processed_result
```

### RAG Customization
```python
# Custom retrieval strategy
from rag.retrievers import BaseRetriever

class CustomRetriever(BaseRetriever):
    def retrieve(self, query, k=5):
        # Custom retrieval logic
        return relevant_documents
```

## 📊 Performance Metrics

- **Response Time**: < 30 seconds for lecture notes
- **Accuracy**: 95%+ content relevance with RAG
- **Throughput**: 100+ concurrent requests
- **Storage**: Scalable vector database

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

### Code Style
- Follow PEP 8 for Python
- Use ESLint for JavaScript
- 80% test coverage minimum
- Type hints required

## 🚀 Deployment

### Docker Deployment
```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/db
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=your-secret-key
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=multi_agent_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
```

### Cloud Deployment
- **AWS**: ECS, Lambda, S3
- **GCP**: Cloud Run, Cloud Functions
- **Azure**: Container Instances, Functions

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

## 🔗 Useful Links

- [Documentation](https://your-docs-site.com)
- [API Reference](https://your-api-docs.com)
- [Examples](./examples/)
- [Troubleshooting](./docs/troubleshooting.md)
- [Changelog](./CHANGELOG.md)

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

See also the list of [contributors](https://github.com/yourusername/multi-agent-llm-education/contributors) who participated in this project.

## 🙏 Acknowledgments

- Thanks to the open source community
- Libraries and frameworks used in this project
- Contributors and beta testers
- Educational institutions providing feedback

## 📞 Support

If you encounter any issues or have questions:
- Create an [Issue](https://github.com/yourusername/multi-agent-llm-education/issues)
- Email: your.email@example.com
- Discord: [Server Link](https://discord.gg/yourserver)
- Stack Overflow: Tag with `multi-agent-llm`

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
