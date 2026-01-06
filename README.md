# AI Healthcare Chatbot API

An intelligent healthcare support chatbot API built with FastAPI, featuring Retrieval-Augmented Generation (RAG) for document-based Q&A, user authentication, and intent-based responses.

## 🚀 Features

- **User Authentication**: Secure login and registration with JWT tokens
- **Intent Classification**: AI-powered intent detection for customer queries
- **Document Q&A**: RAG system for answering questions from healthcare documents
- **Database Integration**: SQLite/PostgreSQL support for user and equipment data
- **CORS Support**: Configured for frontend integration
- **Modular Architecture**: Clean separation of concerns with handlers, services, and models

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Setup](#database-setup)
- [Document Ingestion](#document-ingestion)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🛠 Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/venkateswari2754/ai-healthcare-chatbot-api.git
   cd ai-healthcare-chatbot-api
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here  # Optional, uses simple embeddings if not provided
   DATABASE_URL=sqlite:///./healthcare.db  # Or PostgreSQL URL
   SECRET_KEY=your_secret_key_here
   ```

## ⚙️ Configuration

### Environment Variables
- `OPENAI_API_KEY`: For advanced embeddings (optional)
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key
- `CHROMA_DIR`: Directory for ChromaDB storage (default: .chroma)
- `CHROMA_COLLECTION`: ChromaDB collection name (default: specs)

## 🚀 Usage

### Running the Server
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

The API will be available at `http://127.0.0.1:8001`

### Interactive API Documentation
Visit `http://127.0.0.1:8001/docs` for Swagger UI documentation.

## 📡 API Endpoints

### Authentication
- `POST /register`: User registration
- `POST /login`: User login (returns JWT token)

### Chat
- `POST /chat`: Send chat messages (requires authentication)

### Request Examples

#### Login
```bash
curl -X POST "http://127.0.0.1:8001/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password"}'
```

#### Chat
```bash
curl -X POST "http://127.0.0.1:8001/chat" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is the warranty period?"}'
```

## 🗄️ Database Setup

### Initialize Database
Run the seed script to populate initial data:
```bash
python seed.py
```

This creates:
- User accounts
- Equipment records
- Warranty and AMC contracts

## 📄 Document Ingestion

To add documents for RAG:
1. Place PDF/txt files in the `docs/` directory
2. Run the ingestion script:
   ```bash
   python scripts/ingest_docs.py
   ```

Supported formats: PDF, TXT

## 🧪 Testing

### Unit Tests
```bash
pytest
```

### Manual Testing
Use the `/docs` endpoint or tools like Postman for API testing.

## 🚢 Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Deployment
- Use a production WSGI server like Gunicorn
- Set up reverse proxy with Nginx
- Configure environment variables securely
- Use PostgreSQL for production database

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues, please open an issue on GitHub.

## 🔄 Recent Updates

- Integrated RAG for document-based Q&A
- Improved intent classification
- Enhanced error handling
- Added comprehensive API documentation