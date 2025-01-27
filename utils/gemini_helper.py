import google.generativeai as genai
from config import GOOGLE_API_KEY
import json
from .ai_provider import AIProvider

class GeminiProvider(AIProvider):
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def _format_prompt(self, topic: str, difficulty: str, num_questions: int) -> str:
        return f"""Generate exactly {num_questions} multiple choice questions about {topic} at {difficulty} difficulty level.
        
        Requirements for each question:
        1. Clear question text
        2. Exactly 4 options labeled as A), B), C), D)
        3. One correct answer
        4. Brief explanation
        
        Return the response in this exact JSON format:
        [
            {{
                "question": "Question text here",
                "options": [
                    "A) First option",
                    "B) Second option",
                    "C) Third option",
                    "D) Fourth option"
                ],
                "correct_answer": "A) First option",
                "explanation": "Explanation text here"
            }}
        ]
        
        Important:
        - Ensure the response is a valid JSON array
        - Each question must follow the exact format above
        - Options must start with A), B), C), D)
        - The correct_answer must match exactly with one of the options
        """
    
    def generate_questions(self, topic: str, difficulty: str, num_questions: int) -> list:
        try:
            prompt = self._format_prompt(topic, difficulty, num_questions)
            response = self.model.generate_content(prompt)
            
            # Check if response is valid
            if not response or not response.text:
                print("Empty response from Gemini")
                return self._generate_fallback_questions(num_questions)
                
            return self._parse_response(response)
            
        except Exception as e:
            print(f"Error generating questions with Gemini: {str(e)}")
            return self._generate_fallback_questions(num_questions)
    
    def _parse_response(self, response) -> list:
        try:
            # Clean the response text
            text = response.text.strip()
            if text.startswith('```json'):
                text = text[7:-3]  # Remove ```json and ``` markers
            elif text.startswith('```'):
                text = text[3:-3]  # Remove ``` markers
            
            # Parse JSON
            questions = json.loads(text)
            
            # Validate the structure
            if not isinstance(questions, list):
                raise ValueError("Response is not a list of questions")
            
            for q in questions:
                if not all(key in q for key in ['question', 'options', 'correct_answer', 'explanation']):
                    raise ValueError("Question missing required fields")
                if not isinstance(q['options'], list) or len(q['options']) != 4:
                    raise ValueError("Invalid options format")
                if q['correct_answer'] not in q['options']:
                    raise ValueError("Correct answer not in options")
            
            return questions
            
        except Exception as e:
            print(f"Error parsing Gemini response: {str(e)}\nResponse text: {response.text}")
            return self._generate_fallback_questions(1)
    
    def _generate_fallback_questions(self, num_questions: int) -> list:
        return [{
            "question": "What is the capital of France?",
            "options": [
                "A) Paris",
                "B) London",
                "C) Berlin",
                "D) Madrid"
            ],
            "correct_answer": "A) Paris",
            "explanation": "Paris is the capital city of France."
        }] * num_questions