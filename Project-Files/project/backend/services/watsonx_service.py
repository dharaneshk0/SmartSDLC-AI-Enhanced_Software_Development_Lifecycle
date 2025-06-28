import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
import json

load_dotenv()

class WatsonxService:
    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("PROJECT_ID")
        self.url = os.getenv("WATSONX_URL")
        self.model_id = os.getenv("MODEL_ID", "ibm/granite-20b-code-instruct")
        
        self.credentials = {
            "url": self.url,
            "apikey": self.api_key
        }
        
        self.parameters = {
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MAX_NEW_TOKENS: 1000,
            GenParams.TEMPERATURE: 0.1,
            GenParams.TOP_P: 1.0,
            GenParams.TOP_K: 50
        }
    
    def get_model(self):
        try:
            model = Model(
                model_id=self.model_id,
                params=self.parameters,
                credentials=self.credentials,
                project_id=self.project_id
            )
            return model
        except Exception as e:
            print(f"Error creating model: {str(e)}")
            return None
    
    def generate_response(self, prompt: str):
        try:
            model = self.get_model()
            if model is None:
                return "Error: Could not initialize Watson model"
            
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def classify_sdlc_phases(self, text: str):
        prompt = f"""
        Analyze the following text and classify each sentence into SDLC phases.
        Phases: Requirements, Design, Development, Testing, Deployment, Maintenance
        
        Text: {text}
        
        Format the response as JSON with the following structure:
        {{
            "Requirements": ["sentence1", "sentence2"],
            "Design": ["sentence3"],
            "Development": ["sentence4"],
            "Testing": ["sentence5"],
            "Deployment": ["sentence6"],
            "Maintenance": ["sentence7"]
        }}
        
        Response:
        """
        return self.generate_response(prompt)
    
    def generate_code(self, prompt: str, language: str = "python"):
        code_prompt = f"""
        Generate clean, production-ready {language} code for the following requirement:
        
        Requirement: {prompt}
        
        Please provide only the code with proper comments and best practices.
        
        Code:
        """
        return self.generate_response(code_prompt)
    
    def fix_bug(self, code: str, language: str = "python"):
        bug_prompt = f"""
        Analyze the following {language} code and fix any bugs or issues:
        
        Code:
        {code}
        
        Please provide the corrected code with explanations of what was fixed:
        
        Fixed Code:
        """
        return self.generate_response(bug_prompt)
    
    def generate_test_cases(self, code: str, language: str = "python"):
        test_prompt = f"""
        Generate comprehensive test cases for the following {language} code:
        
        Code:
        {code}
        
        Please provide unit tests using appropriate testing framework:
        
        Test Cases:
        """
        return self.generate_response(test_prompt)
    
    def chat_response(self, message: str):
        chat_prompt = f"""
        You are an AI assistant specialized in Software Development Lifecycle (SDLC).
        Answer the following question with helpful, accurate information:
        
        Question: {message}
        
        Answer:
        """
        return self.generate_response(chat_prompt)

# Global instance
watsonx_service = WatsonxService()