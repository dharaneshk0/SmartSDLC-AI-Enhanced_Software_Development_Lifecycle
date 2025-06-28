import streamlit as st
import requests
import json
from datetime import datetime
import plotly.express as px
import pandas as pd

# Configure page
st.set_page_config(
    page_title="SmartSDLC - AI-Enhanced SDLC",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .chat-container {
        background: #f1f3f4;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 2rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# API Base URL
API_BASE_URL = "http://localhost:8000/api"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 SmartSDLC</h1>
        <h3>AI-Enhanced Software Development Lifecycle</h3>
        <p>Transform your development process with AI-powered automation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        ["🏠 Home", "📄 PDF Classifier", "💻 Code Generator", "🐛 Bug Fixer", "🧪 Test Generator"]
    )
    
    if page == "🏠 Home":
        show_home()
    elif page == "📄 PDF Classifier":
        show_pdf_classifier()
    elif page == "💻 Code Generator":
        show_code_generator()
    elif page == "🐛 Bug Fixer":
        show_bug_fixer()
    elif page == "🧪 Test Generator":
        show_test_generator()

def show_home():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Core Features</h3>
            <ul>
                <li><strong>📄 PDF Classifier:</strong> Convert unstructured PDFs into SDLC phases</li>
                <li><strong>💻 Code Generator:</strong> Generate production-ready code from requirements</li>
                <li><strong>🐛 Bug Fixer:</strong> Automatically detect and fix code issues</li>
                <li><strong>🧪 Test Generator:</strong> Create comprehensive test cases</li>
                <li><strong>🤖 AI Assistant:</strong> Real-time help and guidance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Get Started</h3>
            <p>Select a feature from the sidebar to begin automating your SDLC process.</p>
            <p><strong>Powered by IBM Watsonx AI</strong></p>
            <p>Experience the future of software development with our AI-enhanced tools.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback stats
    try:
        response = requests.get(f"{API_BASE_URL}/feedback/stats")
        if response.status_code == 200:
            stats = response.json()
            
            st.markdown("### 📊 Platform Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>{stats['total_feedback']}</h2>
                    <p>Total Feedback</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>{stats['average_rating']}/5</h2>
                    <p>Average Rating</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>{len(stats['features'])}</h2>
                    <p>Features Used</p>
                </div>
                """, unsafe_allow_html=True)
    except:
        pass
    
    # Floating AI Chatbot
    show_chatbot()

def show_pdf_classifier():
    st.title("📄 PDF Classifier")
    st.write("Upload a PDF document to classify its content into SDLC phases")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Classify PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{API_BASE_URL}/ai/upload-pdf", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success(f"Successfully processed: {result['filename']}")
                        
                        # Show extracted text preview
                        st.subheader("📝 Extracted Text Preview")
                        st.text_area("Text", result['extracted_text'], height=200)
                        
                        # Show classification
                        st.subheader("🔍 SDLC Classification")
                        try:
                            classification = json.loads(result['classification'])
                            for phase, sentences in classification.items():
                                if sentences:
                                    st.write(f"**{phase}:**")
                                    for sentence in sentences:
                                        st.write(f"- {sentence}")
                        except:
                            st.code(result['classification'])
                    else:
                        st.error("Failed to process PDF")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    show_feedback_section("PDF Classifier")

def show_code_generator():
    st.title("💻 Code Generator")
    st.write("Generate production-ready code from natural language requirements")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        prompt = st.text_area("Enter your requirement:", height=150, 
                            placeholder="Example: Create a function to calculate the factorial of a number")
    
    with col2:
        language = st.selectbox("Language:", ["python", "javascript", "java", "c++", "go"])
    
    if st.button("Generate Code"):
        if prompt:
            with st.spinner("Generating code..."):
                try:
                    data = {"prompt": prompt, "language": language}
                    response = requests.post(f"{API_BASE_URL}/ai/generate-code", json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("Code generated successfully!")
                        st.subheader("📋 Generated Code")
                        st.code(result['generated_code'], language=language)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Code",
                            data=result['generated_code'],
                            file_name=f"generated_code.{language}",
                            mime="text/plain"
                        )
                    else:
                        st.error("Failed to generate code")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a requirement")
    
    show_feedback_section("Code Generator")

def show_bug_fixer():
    st.title("🐛 Bug Fixer")
    st.write("Fix bugs and optimize your code with AI assistance")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        code = st.text_area("Paste your buggy code:", height=200,
                          placeholder="Paste your code here...")
    
    with col2:
        language = st.selectbox("Language:", ["python", "javascript", "java", "c++", "go"])
    
    if st.button("Fix Bugs"):
        if code:
            with st.spinner("Analyzing and fixing code..."):
                try:
                    data = {"code": code, "language": language}
                    response = requests.post(f"{API_BASE_URL}/ai/fix-bug", json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("Code analyzed and fixed!")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🔴 Original Code")
                            st.code(result['original_code'], language=language)
                        
                        with col2:
                            st.subheader("✅ Fixed Code")
                            st.code(result['fixed_code'], language=language)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Fixed Code",
                            data=result['fixed_code'],
                            file_name=f"fixed_code.{language}",
                            mime="text/plain"
                        )
                    else:
                        st.error("Failed to fix bugs")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please paste your code")
    
    show_feedback_section("Bug Fixer")

def show_test_generator():
    st.title("🧪 Test Generator")
    st.write("Generate comprehensive test cases for your code")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        code = st.text_area("Paste your code:", height=200,
                          placeholder="Paste the code you want to test...")
    
    with col2:
        language = st.selectbox("Language:", ["python", "javascript", "java", "c++", "go"])
    
    if st.button("Generate Tests"):
        if code:
            with st.spinner("Generating test cases..."):
                try:
                    data = {"code": code, "language": language}
                    response = requests.post(f"{API_BASE_URL}/ai/generate-tests", json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("Test cases generated successfully!")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📋 Original Code")
                            st.code(result['original_code'], language=language)
                        
                        with col2:
                            st.subheader("🧪 Generated Tests")
                            st.code(result['test_cases'], language=language)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Test Cases",
                            data=result['test_cases'],
                            file_name=f"test_cases.{language}",
                            mime="text/plain"
                        )
                    else:
                        st.error("Failed to generate tests")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please paste your code")
    
    show_feedback_section("Test Generator")

def show_chatbot():
    st.markdown("### 🤖 AI Assistant")
    
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about SDLC..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        data = {"message": prompt}
                        response = requests.post(f"{API_BASE_URL}/chat/chat", json=data)
                        
                        if response.status_code == 200:
                            result = response.json()
                            ai_response = result['response']
                        else:
                            ai_response = "Sorry, I'm having trouble responding right now."
                        
                        st.markdown(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.markdown(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_feedback_section(feature_name):
    st.markdown("---")
    st.subheader("💬 Feedback")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        rating = st.slider("Rate this feature:", 1, 5, 3)
    
    with col2:
        comment = st.text_area("Comments (optional):", height=100)
    
    if st.button("Submit Feedback"):
        try:
            data = {
                "feature": feature_name,
                "rating": rating,
                "comment": comment,
                "user_id": f"user_{datetime.now().strftime('%Y%m%d')}"
            }
            response = requests.post(f"{API_BASE_URL}/feedback/submit", json=data)
            
            if response.status_code == 200:
                st.success("Thank you for your feedback!")
            else:
                st.error("Failed to submit feedback")
                
        except Exception as e:
            st.error(f"Error submitting feedback: {str(e)}")

if __name__ == "__main__":
    main()