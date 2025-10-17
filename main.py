import gradio as gr
import os
import sys
import time
from typing import List
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from src.gemini_client import GeminiClient
from src.rpg_system import RPGSystemManager
from src.content_generator import ContentGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ultra Premium Professional CSS - Next-Gen Design
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

:root {
    --primary: #6366F1;
    --primary-dark: #4F46E5;
    --primary-light: #818CF8;
    --secondary: #10B981;
    --accent: #F59E0B;
    --accent-pink: #EC4899;
    --dark: #0F172A;
    --darker: #020617;
    --light: #F8FAFC;
    --gray: #64748B;
    --border: #E2E8F0;
    --success: #10B981;
    --warning: #F59E0B;
    --error: #EF4444;
    --card-bg: rgba(255, 255, 255, 0.05);
    --glass-bg: rgba(255, 255, 255, 0.08);
    --sidebar-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: var(--darker);
    overflow-x: hidden;
}

/* Animated Background */
.gradio-container {
    background: var(--darker) !important;
    min-height: 100vh;
    padding: 0 !important;
    position: relative;
    overflow: hidden;
}

.gradio-container::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: 
        radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(236, 72, 153, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 40% 20%, rgba(16, 185, 129, 0.1) 0%, transparent 50%);
    animation: gradientShift 15s ease infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes gradientShift {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    33% { transform: translate(5%, 5%) rotate(120deg); }
    66% { transform: translate(-5%, 5%) rotate(240deg); }
}

/* Main Layout */
.main-container {
    background: transparent !important;
    max-width: 100% !important;
    margin: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    position: relative;
    z-index: 1;
}

/* Header - Ultra Premium */
.header-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 4rem 3rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="%23ffffff" fill-opacity="0.05" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,165.3C1248,171,1344,149,1392,138.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>'),
        linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.2) 100%);
    background-size: cover;
    animation: headerWave 20s ease-in-out infinite;
}

@keyframes headerWave {
    0%, 100% { transform: translateX(0) translateY(0); }
    50% { transform: translateX(-50px) translateY(-10px); }
}

.header-title {
    font-size: 4rem !important;
    font-weight: 900 !important;
    margin: 0 !important;
    background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1 !important;
    text-shadow: 0 0 40px rgba(255, 255, 255, 0.3);
    position: relative;
    letter-spacing: -0.03em;
    animation: titleGlow 3s ease-in-out infinite;
    font-family: 'Space Grotesk', sans-serif;
}

@keyframes titleGlow {
    0%, 100% { filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.3)); }
    50% { filter: drop-shadow(0 0 40px rgba(255, 255, 255, 0.5)); }
}

.header-subtitle {
    font-size: 1.4rem !important;
    opacity: 0.95;
    margin: 1.5rem 0 0 0 !important;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.95) !important;
    position: relative;
    letter-spacing: 0.02em;
}

/* Main Content Grid */
.content-grid {
    display: grid;
    grid-template-columns: 420px 1fr;
    gap: 0;
    min-height: calc(100vh - 250px);
    background: transparent;
}

/* Sidebar - Ultra Premium Glass */
.sidebar {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(40px) saturate(180%);
    -webkit-backdrop-filter: blur(40px) saturate(180%);
    padding: 2.5rem;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    height: 100%;
    position: relative;
    overflow-y: auto;
}

.sidebar::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 0% 100%, rgba(236, 72, 153, 0.08) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

.sidebar > * {
    position: relative;
    z-index: 1;
}

/* Custom Scrollbar */
.sidebar::-webkit-scrollbar {
    width: 8px;
}

.sidebar::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}

.sidebar::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.5);
    border-radius: 10px;
    transition: all 0.3s ease;
}

.sidebar::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.8);
}

/* Glass Card - Enhanced */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1),
        0 0 0 1px rgba(0, 0, 0, 0.1);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, 
        transparent 0%, 
        rgba(255, 255, 255, 0.3) 50%, 
        transparent 100%);
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 
        0 20px 40px rgba(99, 102, 241, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.15),
        0 0 0 1px rgba(99, 102, 241, 0.2);
    border-color: rgba(99, 102, 241, 0.3);
}

.card-title {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: rgba(255, 255, 255, 0.95) !important;
    margin: 0 0 1.5rem 0 !important;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    letter-spacing: -0.01em;
    font-family: 'Space Grotesk', sans-serif;
}

/* Stats Grid - Enhanced */
.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: linear-gradient(135deg, 
        rgba(99, 102, 241, 0.9) 0%, 
        rgba(79, 70, 229, 0.9) 100%);
    backdrop-filter: blur(20px);
    color: white;
    padding: 1.75rem 1.5rem;
    border-radius: 20px;
    text-align: center;
    box-shadow: 
        0 8px 32px rgba(99, 102, 241, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.15);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.stat-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    animation: statGlow 3s ease-in-out infinite;
}

@keyframes statGlow {
    0%, 100% { transform: translate(0, 0); opacity: 0.5; }
    50% { transform: translate(10%, 10%); opacity: 1; }
}

.stat-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 
        0 16px 48px rgba(99, 102, 241, 0.5),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.stat-value {
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
    color: white;
    position: relative;
    z-index: 1;
}

.stat-label {
    font-size: 0.85rem;
    opacity: 0.95;
    margin: 0.5rem 0 0 0;
    font-weight: 600;
    color: white;
    position: relative;
    z-index: 1;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Controls - Enhanced */
.control-group {
    margin-bottom: 1.5rem;
}

.control-label {
    display: block;
    margin-bottom: 0.75rem;
    color: rgba(255, 255, 255, 0.9);
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: -0.01em;
}

.control-input, .control-select {
    width: 100%;
    padding: 1rem 1.25rem;
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    font-size: 1rem;
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.95);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-weight: 500;
}

.control-input:focus, .control-select:focus {
    outline: none;
    border-color: var(--primary);
    background: rgba(255, 255, 255, 0.08);
    box-shadow: 
        0 0 0 4px rgba(99, 102, 241, 0.15),
        0 8px 24px rgba(99, 102, 241, 0.2);
    transform: translateY(-2px);
}

.control-select {
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23ffffff'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 1rem center;
    background-size: 1.25rem;
    padding-right: 3rem;
}

/* Buttons - Next-Gen Design */
.btn {
    padding: 1.25rem 2rem;
    border: none;
    border-radius: 16px;
    font-weight: 700;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    width: 100%;
    position: relative;
    overflow: hidden;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 0.95rem;
}

.btn::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.btn:hover::before {
    width: 300px;
    height: 300px;
}

.btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.3);
}

.btn:active {
    transform: translateY(-1px);
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    box-shadow: 
        0 8px 32px rgba(99, 102, 241, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-primary:hover {
    box-shadow: 
        0 16px 48px rgba(99, 102, 241, 0.5),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.btn-secondary {
    background: linear-gradient(135deg, var(--secondary) 0%, #059669 100%);
    color: white;
    box-shadow: 
        0 8px 32px rgba(16, 185, 129, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-accent {
    background: linear-gradient(135deg, var(--accent) 0%, #D97706 100%);
    color: white;
    box-shadow: 
        0 8px 32px rgba(245, 158, 11, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Quick Prompts - Ultra Premium */
.quick-prompt-grid {
    display: grid;
    gap: 1rem;
    margin-top: 1rem;
}

.quick-prompt {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    text-align: left;
    color: rgba(255, 255, 255, 0.9);
    position: relative;
    overflow: hidden;
}

.quick-prompt::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 3px;
    height: 100%;
    background: linear-gradient(180deg, var(--primary) 0%, var(--accent-pink) 100%);
    transform: scaleY(0);
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    transform-origin: bottom;
}

.quick-prompt:hover {
    background: rgba(99, 102, 241, 0.15);
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateX(8px);
    box-shadow: 
        0 8px 32px rgba(99, 102, 241, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.quick-prompt:hover::before {
    transform: scaleY(1);
    transform-origin: top;
}

.quick-prompt-content {
    font-size: 0.95rem;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
    line-height: 1.5;
    font-weight: 500;
    position: relative;
    z-index: 1;
}

/* Main Content Area */
.main-content {
    background: rgba(15, 23, 42, 0.5);
    backdrop-filter: blur(20px);
    padding: 2.5rem;
    height: 100%;
}

/* Chat Interface - Next-Gen */
.chat-container {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    height: 500px;
    overflow-y: auto;
    padding: 2rem;
    box-shadow: 
        inset 0 2px 20px rgba(0, 0, 0, 0.3),
        0 8px 32px rgba(0, 0, 0, 0.2);
}

.chat-container::-webkit-scrollbar {
    width: 10px;
}

.chat-container::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.5);
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.8);
}

/* Chat Messages - Enhanced */
.user-message, .bot-message {
    padding: 1.5rem 1.75rem !important;
    border-radius: 20px !important;
    margin: 1.5rem 0 !important;
    max-width: 80% !important;
    line-height: 1.7 !important;
    position: relative;
    animation: messageSlide 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    word-wrap: break-word;
    font-size: 1rem;
}

@keyframes messageSlide {
    from {
        opacity: 0;
        transform: translateY(30px) scale(0.9);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.user-message {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    color: white !important;
    margin-left: auto !important;
    margin-right: 0 !important;
    border-bottom-right-radius: 8px !important;
    box-shadow: 
        0 8px 32px rgba(99, 102, 241, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.bot-message {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(20px);
    color: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    margin-right: auto !important;
    margin-left: 0 !important;
    border-bottom-left-radius: 8px !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

/* Status Bar - Enhanced */
.status-bar {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 1.25rem 1.75rem;
    font-size: 0.95rem;
    color: rgba(255, 255, 255, 0.9);
    text-align: center;
    margin-top: 1.5rem;
    font-weight: 600;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.status-success {
    background: rgba(16, 185, 129, 0.15);
    border-color: rgba(16, 185, 129, 0.4);
    color: #6EE7B7;
    box-shadow: 0 4px 24px rgba(16, 185, 129, 0.3);
}

.status-error {
    background: rgba(239, 68, 68, 0.15);
    border-color: rgba(239, 68, 68, 0.4);
    color: #FCA5A5;
    box-shadow: 0 4px 24px rgba(239, 68, 68, 0.3);
}

.status-generating {
    background: rgba(245, 158, 11, 0.15);
    border-color: rgba(245, 158, 11, 0.4);
    color: #FCD34D;
    box-shadow: 0 4px 24px rgba(245, 158, 11, 0.3);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.9; transform: scale(1.02); }
}

/* Input Area - Enhanced */
.input-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 2rem;
    margin-top: 1.5rem;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

/* Responsive Design */
@media (max-width: 1024px) {
    .content-grid {
        grid-template-columns: 1fr;
    }
    
    .sidebar {
        border-right: none;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .header-title {
        font-size: 3rem !important;
    }
    
    .header-subtitle {
        font-size: 1.2rem !important;
    }
}

@media (max-width: 768px) {
    .header-title {
        font-size: 2.5rem !important;
    }
    
    .header-subtitle {
        font-size: 1rem !important;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .glass-card {
        padding: 1.5rem;
    }
}
"""

class GMAssistantApp:
    def __init__(self):
        self.gemini_client = None
        self.rpg_manager = RPGSystemManager("src/data")
        self.content_generator = None
        self.initialized = False
        
        # Content types with better organization
        self.content_types = {
            "character": {"name": "🧙‍♂️ Character", "description": "NPCs, heroes, villains"},
            "location": {"name": "🏰 Location", "description": "Places, dungeons, cities"}, 
            "plot": {"name": "📖 Story", "description": "Quests, mysteries, narratives"},
            "encounter": {"name": "⚔️ Encounter", "description": "Battles, challenges, puzzles"},
            "item": {"name": "🎁 Item", "description": "Weapons, artifacts, treasure"}
        }
        
        # RPG Systems
        self.rpg_systems = {
            "ironsworn": "Ironsworn",
            "dnd": "Dungeons & Dragons 5E",
            "cyberpunk": "Cyberpunk RED",
            "cthulhu": "Call of Cthulhu",
            "starfinder": "Starfinder"
        }
        
        # Enhanced quick prompts
        self.quick_prompts = [
            {
                "text": "A mysterious wizard living in a crystal tower with a dark secret",
                "type": "character",
                "icon": "🧙‍♂️"
            },
            {
                "text": "An ancient forest temple guarded by magical spirits",
                "type": "location", 
                "icon": "🏰"
            },
            {
                "text": "A noble family's dark secret that threatens the entire kingdom",
                "type": "plot",
                "icon": "📖"
            },
            {
                "text": "A social encounter with a vain noble who loves puzzles",
                "type": "encounter",
                "icon": "⚔️"
            },
            {
                "text": "A sentient sword that grants power but demands blood sacrifices",
                "type": "item",
                "icon": "🎁"
            },
            {
                "text": "A dragon guarding a magical treasure in a mountain lair",
                "type": "encounter",
                "icon": "🐉"
            }
        ]
        
        self.initialize_app()
    
    def initialize_app(self):
        """Initialize the application"""
        try:
            print("🚀 Initializing Game Master Assistant...")
            
            # Initialize Gemini client
            self.gemini_client = GeminiClient()
            print("✅ Gemini client initialized")
            
            # Initialize content generator
            self.content_generator = ContentGenerator(self.gemini_client, self.rpg_manager)
            print("✅ Content generator initialized")
            
            # Load default system
            if self.rpg_manager.load_system("ironsworn"):
                print("✅ Ironsworn system loaded")
            
            self.initialized = True
            print("🎯 Application ready!")
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            self.initialized = False
    
    def generate_content(self, content_type: str, user_input: str, history: List):
        """Generate content and update history"""
        if not self.initialized:
            return history, "❌ System not initialized. Please check your API key.", "status-error"
        
        if not user_input.strip():
            return history, "❌ Please enter a prompt to generate content.", "status-error"
        
        try:
            # Add user message to history
            new_history = history + [[user_input, None]]
            yield new_history, "🔄 Generating your content... This may take a few seconds.", "status-generating"
            
            # Map content type to method
            content_map = {
                "character": self.content_generator.generate_npc,
                "location": self.content_generator.generate_location,
                "plot": self.content_generator.generate_plot,
                "encounter": self.content_generator.generate_encounter,
                "item": self.content_generator.generate_item
            }
            
            # Clean content type (remove emoji)
            clean_type = content_type.split(" ")[-1].lower() if " " in content_type else content_type.lower()
            
            if clean_type in content_map:
                start_time = time.time()
                result = content_map[clean_type](user_input)
                response = result['content']
                generation_time = time.time() - start_time
                
                # Update history with bot response
                new_history[-1][1] = response
                
                status = f"✅ Success! Generated in {generation_time:.1f} seconds"
                yield new_history, status, "status-success"
            else:
                new_history[-1][1] = f"❌ Unknown content type: {content_type}"
                yield new_history, "❌ Failed to generate content", "status-error"
                
        except Exception as e:
            error_msg = f"❌ Error generating content: {str(e)}"
            if history and history[-1][1] is None:
                new_history = history
                new_history[-1][1] = error_msg
            else:
                new_history = history + [[user_input, error_msg]]
            yield new_history, "❌ Generation failed", "status-error"
    
    def clear_chat(self):
        """Clear the chat history"""
        if self.content_generator:
            self.content_generator.clear_history()
        return [], "🗑️ Chat cleared. Ready for new content!", "status-success"
    
    def change_system(self, system_name: str):
        """Change RPG system"""
        try:
            system_key = system_name.lower().replace(" ", "").replace("&", "")
            system_key = next((k for k, v in self.rpg_systems.items() if v == system_name), system_key)
            
            success = self.rpg_manager.load_system(system_key)
            if success:
                return f"✅ Switched to {system_name}", "status-success"
            return f"❌ Failed to load {system_name}", "status-error"
        except Exception as e:
            return f"❌ Error: {str(e)}", "status-error"
    
    def quick_prompt_handler(self, prompt: str, content_type_key: str):
        """Handle quick prompt clicks, returns the prompt text and the full content type name."""
        content_name = self.content_types.get(content_type_key, {"name": "🧙‍♂️ Character"})["name"]
        return prompt, content_name

def main():
    """Main application entry point"""
    print("🎮 Game Master Assistant - Premium Edition")
    print("=" * 50)
    print("✨ AI-Powered RPG Content Creation")
    print("🔗 Powered by Google Gemini AI")
    print("🎲 Multiple Game Systems Supported")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in .env file")
        print("💡 Please add your Google Gemini API key to the .env file")
        print("🔑 Get your key from: https://aistudio.google.com/app/apikey")
        return
    
    # Create application
    app = GMAssistantApp()
    
    if not app.initialized:
        print("❌ Failed to initialize application")
        print("💡 Please check your API key and internet connection")
        return
    
    print("✅ Application initialized successfully!")
    print("🌐 Starting web interface...")
    print("📱 Open: http://localhost:7860")
    print("=" * 50)
    
    # Create interface
    with gr.Blocks(
        title="Game Master Assistant Pro",
        css=custom_css,
        theme=gr.themes.Soft()
    ) as interface:
        
        # Header Section
        with gr.Row(elem_classes="header-section"):
            gr.Markdown("""
            <div class="header-title">🎮 Game Master Assistant</div>
            <div class="header-subtitle">AI-Powered RPG Content Creation • Premium Edition</div>
            """)
        
        # Main Content Grid
        with gr.Row(elem_classes="content-grid"):
            # Left Sidebar - Controls
            with gr.Column(scale=0, min_width=420, elem_classes="sidebar"):
                # Stats Cards
                with gr.Row(elem_classes="stats-grid"):
                    with gr.Column(scale=1):
                        gr.Markdown("""
                        <div class="stat-card">
                            <div class="stat-value">🤖</div>
                            <div class="stat-label">Gemini 2.0</div>
                        </div>
                        """)
                    with gr.Column(scale=1):
                        gr.Markdown("""
                        <div class="stat-card">
                            <div class="stat-value">⚡</div>
                            <div class="stat-label">Premium</div>
                        </div>
                        """)
                
                # System Selection
                with gr.Group(elem_classes="glass-card"):
                    gr.Markdown("""<div class="card-title">🎲 Game System</div>""")
                    with gr.Column(elem_classes="control-group"):
                        gr.Markdown("""<div class="control-label">Select RPG System</div>""")
                        system_dropdown = gr.Dropdown(
                            choices=list(app.rpg_systems.values()),
                            value="Ironsworn",
                            elem_classes="control-select",
                            interactive=True
                        )
                
                # Content Type
                with gr.Group(elem_classes="glass-card"):
                    gr.Markdown("""<div class="card-title">🎨 Content Type</div>""")
                    with gr.Column(elem_classes="control-group"):
                        gr.Markdown("""<div class="control-label">What to Generate</div>""")
                        content_dropdown = gr.Dropdown(
                            choices=[ct["name"] for ct in app.content_types.values()],
                            value="🧙‍♂️ Character",
                            elem_classes="control-select",
                            interactive=True
                        )
                
                # Quick Prompts - Store button references for later
                quick_prompt_buttons = []
                with gr.Group(elem_classes="glass-card"):
                    gr.Markdown("""<div class="card-title">🚀 Quick Start</div>""")
                    with gr.Column(elem_classes="quick-prompt-grid"):
                        for prompt_data in app.quick_prompts:
                            prompt_btn = gr.Button(
                                value=f"{prompt_data['icon']} {prompt_data['text']}",
                                elem_classes="quick-prompt",
                                size="sm"
                            )
                            quick_prompt_buttons.append((prompt_btn, prompt_data))
                
                # Actions
                with gr.Group(elem_classes="glass-card"):
                    gr.Markdown("""<div class="card-title">⚡ Actions</div>""")
                    clear_btn = gr.Button(
                        "🗑️ Clear Chat History",
                        elem_classes="btn-accent"
                    )
            
            # Main Content Area
            with gr.Column(scale=1, elem_classes="main-content"):
                # Chat Interface
                with gr.Group(elem_classes="glass-card"):
                    gr.Markdown("""<div class="card-title">💬 Content Generator</div>""")
                    chatbot = gr.Chatbot(
                        label="",
                        show_label=False,
                        height=500,
                        elem_classes="chat-container"
                    )
                
                # Input Area
                with gr.Group(elem_classes="input-container"):
                    with gr.Row():
                        user_input = gr.Textbox(
                            label="",
                            placeholder="🎯 Describe what you want to create... (e.g., 'a dragon guarding a magical treasure in an ancient forest')",
                            lines=3,
                            max_lines=5,
                            show_label=False,
                            elem_classes="control-input",
                            scale=4
                        )
                        generate_btn = gr.Button(
                            "✨ Generate Content",
                            elem_classes="btn-primary",
                            scale=1,
                            size="lg"
                        )
                
                # Status Bar
                status_display = gr.Textbox(
                    label="",
                    value="✅ Ready to create amazing RPG content! Enter a prompt above to get started.",
                    show_label=False,
                    max_lines=2,
                    interactive=False,
                    elem_classes="status-bar"
                )
        
        # NOW set up quick prompt handlers AFTER all components are defined
        for prompt_btn, prompt_data in quick_prompt_buttons:
            prompt_btn.click(
                app.quick_prompt_handler,
                inputs=[
                    gr.State(prompt_data["text"]),
                    gr.State(prompt_data["type"])
                ],
                outputs=[user_input, content_dropdown]
            )
        
        # Event handlers
        generate_btn.click(
            app.generate_content,
            inputs=[content_dropdown, user_input, chatbot],
            outputs=[chatbot, status_display, status_display]
        )
        
        user_input.submit(
            app.generate_content,
            inputs=[content_dropdown, user_input, chatbot],
            outputs=[chatbot, status_display, status_display]
        )
        
        clear_btn.click(
            app.clear_chat,
            outputs=[chatbot, status_display, status_display]
        )
        
        system_dropdown.change(
            app.change_system,
            inputs=[system_dropdown],
            outputs=[status_display, status_display]
        )
    
    # Launch interface
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
        show_error=True
    )

if __name__ == "__main__":
    main()