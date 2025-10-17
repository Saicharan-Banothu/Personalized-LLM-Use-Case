from typing import Dict, List, Any
import logging
from .gemini_client import GeminiClient
from .rpg_system import RPGSystemManager

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self, gemini_client: GeminiClient, rpg_manager: RPGSystemManager):
        self.gemini = gemini_client
        self.rpg_manager = rpg_manager
        self.generated_content = []
    
    def generate_content(self, content_type: str, user_input: str = "") -> Dict[str, Any]:
        try:
            system_prompt = self.rpg_manager.get_system_prompt(content_type, user_input)
            
            response = self.gemini.generate_response(
                prompt=user_input,
                system_message=system_prompt
            )
            
            content_item = {
                'type': content_type,
                'input': user_input,
                'content': response,
                'system': self.rpg_manager.current_system.name if self.rpg_manager.current_system else 'Unknown'
            }
            
            self.generated_content.append(content_item)
            
            if len(self.generated_content) > 15:
                self.generated_content = self.generated_content[-15:]
            
            return content_item
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return {
                'type': content_type,
                'input': user_input,
                'content': f"❌ Error: {str(e)}",
                'system': 'Error'
            }
    
    def generate_npc(self, description: str = ""):
        return self.generate_content('NPC', description)
    
    def generate_location(self, description: str = ""):
        return self.generate_content('Location', description)
    
    def generate_plot(self, description: str = ""):
        return self.generate_content('Plot', description)
    
    def generate_encounter(self, description: str = ""):
        return self.generate_content('Encounter', description)
    
    def generate_item(self, description: str = ""):
        return self.generate_content('Item', description)
    
    def get_recent_content(self, limit: int = 5):
        return self.generated_content[-limit:] if self.generated_content else []
    
    def clear_history(self):
        self.generated_content = []
        self.gemini.clear_conversation()