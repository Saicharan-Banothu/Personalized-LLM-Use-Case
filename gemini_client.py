import os
import google.generativeai as genai
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, model: str = None):
        self.api_key = os.getenv("GEMINI_API_KEY")
        # Try different models in order of preference
        self.available_models = [
            "gemini-2.0-flash-exp",  # Latest experimental
            "gemini-1.5-flash",      # Fast and reliable
            "gemini-1.5-pro"         # Most capable
        ]
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.model = None
        self.model_name = None
        
        # Try to initialize with available models
        for model_name in self.available_models:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(model_name)
                self.model_name = model_name
                
                # Test the model with a simple prompt
                test_response = self.model.generate_content("Hello")
                if test_response and test_response.text:
                    logger.info(f"✅ Successfully initialized with model: {model_name}")
                    break
                else:
                    logger.warning(f"❌ Model {model_name} returned empty response, trying next...")
                    continue
                    
            except Exception as e:
                logger.warning(f"❌ Failed to initialize model {model_name}: {e}, trying next...")
                continue
        
        if not self.model:
            raise ValueError("❌ Could not initialize any Gemini model. Please check your API key and quota.")
        
        self.conversation_history = []
        
        # Optimized generation config
        self.generation_config = {
            "temperature": 0.9,  # Higher for creative RPG content
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        # Balanced safety settings
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        ]
    
    def generate_response(self, prompt: str, system_message: str = "") -> str:
        try:
            # Create a more structured and engaging prompt
            full_prompt = f"""🎮 RPG CONTENT GENERATION REQUEST

GAME MASTER GUIDELINES:
{system_message}

PLAYER REQUEST:
"{prompt}"

CREATION INSTRUCTIONS:
1. Create immersive, detailed RPG content
2. Include game mechanics where relevant
3. Use vivid descriptions and storytelling
4. Make it immediately usable for game sessions
5. Be creative but consistent with the setting

READY TO CREATE MAGIC! 🪄"""
            
            # Generate content
            response = self.model.generate_content(
                full_prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            # Comprehensive response handling
            if not response:
                return "🎭 The creative well seems dry! Let's try a different approach or prompt."
            
            # Check for text in response
            if hasattr(response, 'text') and response.text:
                response_content = response.text.strip()
                if response_content and len(response_content) > 10:  # Ensure meaningful content
                    # Update conversation history
                    self.conversation_history.append({"role": "user", "content": prompt})
                    self.conversation_history.append({"role": "assistant", "content": response_content})
                    
                    # Keep history manageable
                    if len(self.conversation_history) > 10:
                        self.conversation_history = self.conversation_history[-10:]
                    
                    return response_content
            
            # Check candidates for more detailed error info
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'finish_reason'):
                    if candidate.finish_reason == "SAFETY":
                        return "🛡️ Content was filtered for safety. Let's try a different approach!"
                    elif candidate.finish_reason == "MAX_TOKENS":
                        return "📝 Response was too long! Let's try a more focused prompt."
                    elif candidate.finish_reason == "STOP":
                        return "⏹️ Generation stopped unexpectedly. Let's try again!"
            
            return "✨ The creative sparks aren't flying! Let's try a different prompt or approach."
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            error_msg = str(e).lower()
            
            if "quota" in error_msg:
                return "💳 API quota exceeded. Please check your Google AI Studio quota."
            elif "permission" in error_msg:
                return "🔑 API permission denied. Please verify your API key is correct."
            elif "model" in error_msg or "not found" in error_msg:
                return f"🤖 Model unavailable: {self.model_name}. Trying alternative approach..."
            elif "safety" in error_msg:
                return "🛡️ Content blocked by safety filters. Let's try a different prompt."
            else:
                return f"⚡ Technical hiccup: {str(e)[:100]}... Let's try again!"
    
    def clear_conversation(self):
        self.conversation_history = []
    
    def get_model_info(self):
        return f"Gemini {self.model_name}"