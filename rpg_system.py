import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class RPGSystem:
    name: str
    rules_text: str
    prompts: Dict[str, str]
    
    @classmethod
    def load_from_files(cls, system_name: str, rules_file: str, prompts_dir: str) -> 'RPGSystem':
        """Load an RPG system from files"""
        try:
            # Load rules
            with open(rules_file, 'r', encoding='utf-8') as f:
                rules_text = f.read()
            
            # Load prompts
            prompts = {}
            prompt_files = {
                'npc': 'npc_prompts.txt',
                'location': 'location_prompts.txt', 
                'plot': 'plot_prompts.txt',
                'item': 'item_prompts.txt',
                'encounter': 'encounter_prompts.txt'
            }
            
            for prompt_type, filename in prompt_files.items():
                filepath = os.path.join(prompts_dir, filename)
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        prompts[prompt_type] = f.read()
                else:
                    prompts[prompt_type] = f"Generate {prompt_type} content for {system_name}"
                    logger.warning(f"Prompt file {filepath} not found, using default")
            
            return cls(system_name, rules_text, prompts)
            
        except Exception as e:
            logger.error(f"Error loading RPG system: {e}")
            return cls(system_name, "Default rules", {})

class RPGSystemManager:
    def __init__(self, resources_dir: str = "src/data"):
        self.resources_dir = resources_dir
        self.systems: Dict[str, RPGSystem] = {}
        self.current_system: Optional[RPGSystem] = None
        
    def load_system(self, system_name: str) -> bool:
        """Load a specific RPG system"""
        try:
            rules_file = os.path.join(self.resources_dir, f"{system_name.lower()}_rules.txt")
            prompts_dir = os.path.join(self.resources_dir, "prompts")
            
            if not os.path.exists(rules_file):
                logger.error(f"Rules file not found: {rules_file}")
                return False
            
            system = RPGSystem.load_from_files(system_name, rules_file, prompts_dir)
            self.systems[system_name] = system
            self.current_system = system
            return True
            
        except Exception as e:
            logger.error(f"Error loading system {system_name}: {e}")
            return False
    
    def get_system_prompt(self, content_type: str, user_input: str = "") -> str:
        """Get a formatted prompt for content generation"""
        if not self.current_system:
            return f"Generate {content_type}: {user_input}"
        
        base_prompt = self.current_system.prompts.get(content_type, f"Generate {content_type} content")
        
        system_context = f"""You are an expert Game Master for the {self.current_system.name} RPG system.

CORE RULES CONTEXT:
{self.current_system.rules_text[:1500]}  # Limit context length

USER REQUEST: {user_input}

INSTRUCTIONS:
{base_prompt}

IMPORTANT: Be creative but stay true to the system's mechanics, tone, and setting. Provide well-structured, game-ready content that a GM can immediately use.
"""
        
        return system_context
    
    def get_available_systems(self) -> List[str]:
        """Get list of available RPG systems"""
        systems = []
        if os.path.exists(self.resources_dir):
            for filename in os.listdir(self.resources_dir):
                if filename.endswith('_rules.txt'):
                    system_name = filename.replace('_rules.txt', '').title()
                    systems.append(system_name)
        return systems