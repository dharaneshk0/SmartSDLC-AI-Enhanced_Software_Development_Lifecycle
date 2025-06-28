# SmartSDLC - AI-Enhanced Software Development Lifecycle

A comprehensive AI-powered platform that automates key stages of the Software Development Lifecycle using IBM Watsonx AI and modern web technologies.

## 🚀 Features

### Core Functionality
1. **📄 PDF Classifier**: Upload unstructured PDF documents and automatically classify content into SDLC phases
2. **💻 Code Generator**: Generate production-ready code from natural language requirements
3. **🐛 Bug Fixer**: Automatically detect and fix bugs in your code
4. **🧪 Test Generator**: Create comprehensive test cases for quality assurance
5. **🤖 AI Assistant**: Real-time conversational support with feedback system

## 🛠 Technology Stack

### Backend
- **FastAPI**: High-performance web framework
- **IBM Watsonx AI**: Advanced AI model integration
- **PyMuPDF**: PDF text extraction
- **Python 3.10+**: Core runtime

### Frontend
- **Streamlit**: Interactive web application framework
- **Plotly**: Data visualization
- **Custom CSS**: Enhanced UI styling

## 📋 Prerequisites

- Python 3.10+
- IBM Watsonx AI account and API key
- Git (optional)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smartsdlc-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   WATSONX_URL=https://eu-de.ml.cloud.ibm.com
   WATSONX_API_KEY=your_api_key_here
   PROJECT_ID=your_project_id_here
   ACCESS_TOKEN=your_access_token_here
   MODEL_ID=ibm/granite-20b-code-instruct
   ```

## 🚀 Running the Application

### Option 1: Using the run scripts

1. **Start the backend server**
   ```bash
   python run_backend.py
   ```

2. **Start the frontend (in a new terminal)**
   ```bash
   python run_frontend.py
   ```

### Option 2: Manual startup

1. **Backend**
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Frontend**
   ```bash
   cd frontend
   streamlit run Home.py --server.port 8501
   ```

## 📖 Usage

1. **Access the application**: Open your browser and navigate to `http://localhost:8501`

2. **PDF Classifier**: Upload PDF documents to extract and classify content into SDLC phases

3. **Code Generator**: Enter natural language requirements to generate code in multiple programming languages

4. **Bug Fixer**: Paste buggy code to get automatically fixed and optimized versions

5. **Test Generator**: Input your code to generate comprehensive test cases

6. **AI Assistant**: Use the chat interface for real-time help and guidance

## 🏗 Architecture

```
smartsdlc-app/
MultipleFiles/
├── __init__.cpython-313.pyc
├── chat_routes.cpython-313.pyc
├── ai_routes.cpython-313.pyc
├── feedback_routes.cpython-313.pyc
├── ai_routes.py
├── __init__.py
├── feedback_routes.py
├── chat_routes.py
├── pdf_service.cpython-313.pyc
├── watsonx_service.cpython-313.pyc
├── __init__.cpython-313.pyc
├── pdf_service.py
├── watsonx_service.py
├── __init__.py
├── main.cpython-313.pyc
├── feedback_data.json
├── main.py
├── server.js
├── Home.py
├── FloatingChatbot.tsx
├── Navbar.tsx
├── CodeGenerator.tsx
├── PDFClassifier.tsx
├── BugFixer.tsx
├── Home.tsx
├── TestGenerator.tsx
├── mockApi.ts
├── App.tsx
├── index.css
├── main.tsx
├── vite-env.d.ts
├── config.json
├── .env
├── prompt
├── .gitignore
├── tailwind.config.js
├── package-lock.json
├── eslint.config.js
├── tsconfig.json
├── tsconfig.node.json
├── README.md
├── postcss.config.js
├── tsconfig.app.json
├── index.html
├── run_backend.py
├── requirements.txt
├── package.json
├── vite.config.ts
└── run_frontend.py

## 🔐 Security

- API keys are stored securely in environment variables
- CORS is properly configured for development
- Input validation is implemented across all endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions and support, please create an issue in the repository or contact the development team.

## 🙏 Acknowledgments

- IBM Watsonx AI for powerful AI capabilities
- Streamlit community for excellent documentation
- FastAPI team for the robust web framework