from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def generate_questions(self, topic: str, difficulty: str, num_questions: int) -> list:
        """Generate questions using the AI model"""
        pass
    
    @abstractmethod
    def _format_prompt(self, topic: str, difficulty: str, num_questions: int) -> str:
        """Format the prompt for the AI model"""
        pass
    
    @abstractmethod
    def _parse_response(self, response) -> list:
        """Parse the AI model response into a standardized format"""
        pass