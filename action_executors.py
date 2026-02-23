"""
Action Executors - Executes actions based on command intent
"""
import subprocess
import platform
import logging
import os
import webbrowser
import datetime
from strands import Agent, tool
from strands_tools import current_time

logger = logging.getLogger(__name__)

# Try to import PIL for screenshot functionality
try:
    from PIL import ImageGrab
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("PIL/Pillow not available. Screenshot feature will use fallback method.")


# Define custom tools for Strands Agent

@tool
def open_application(app_name: str) -> str:
    """
    Opens an application on the user's computer.
    
    Args:
        app_name (str): The name of the application to open (e.g., "chrome", "notepad", "calculator", "spotify")
    
    Returns:
        str: Success or error message
    """
    if not app_name or not app_name.strip():
        return "Error: Application name is empty"
    
    system = platform.system()
    app_lower = app_name.lower()
    
    # Special case: YouTube should be opened in browser, not as an app
    if app_lower in ['youtube', 'yt']:
        return "Use open_youtube tool to open YouTube in browser"
    
    # Common application mappings for Windows
    app_mappings = {
        'chrome': 'chrome.exe',
        'google chrome': 'chrome.exe',
        'firefox': 'firefox.exe',
        'edge': 'msedge.exe',
        'microsoft edge': 'msedge.exe',
        'vscode': 'code.exe',
        'visual studio code': 'code.exe',
        'vs code': 'code.exe',
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'calc': 'calc.exe',
        'paint': 'mspaint.exe',
        'spotify': 'spotify.exe',
        'discord': 'discord.exe',
        'teams': 'teams.exe',
        'outlook': 'outlook.exe',
        'word': 'winword.exe',
        'microsoft word': 'winword.exe',
        'excel': 'excel.exe',
        'microsoft excel': 'excel.exe',
        'powerpoint': 'powerpnt.exe',
        'microsoft powerpoint': 'powerpnt.exe',
        'vlc': 'vlc.exe',
        'steam': 'steam.exe',
    }
    
    try:
        logger.info(f"Attempting to open {app_name} on {system}")
        
        if system == "Windows":
            # Get the executable name
            exe_name = app_mappings.get(app_lower, f"{app_name}.exe")
            
            # Try to launch using shell
            try:
                subprocess.Popen(exe_name, shell=True)
                logger.info(f"Successfully opened {app_name}")
                return f"Successfully opened {app_name}"
            except Exception as e:
                logger.error(f"Failed to open {app_name}: {e}")
                return f"Could not find or open {app_name}. Make sure it's installed."
                
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", app_name])
            return f"Successfully opened {app_name}"
            
        elif system == "Linux":
            subprocess.Popen([app_name])
            return f"Successfully opened {app_name}"
            
        else:
            return f"Unsupported operating system: {system}"
            
    except Exception as e:
        logger.error(f"Error opening application: {e}")
        return f"Failed to open {app_name}: {str(e)}"


@tool
def open_youtube() -> str:
    """
    Opens YouTube website in the default web browser.
    
    Returns:
        str: Success message
    """
    try:
        logger.info("Opening YouTube in browser")
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"
    except Exception as e:
        logger.error(f"Error opening YouTube: {e}")
        return f"Failed to open YouTube: {str(e)}"


@tool
def play_music_on_youtube(song_name: str) -> str:
    """
    Plays a song or music video on YouTube by opening it in the default web browser.
    
    Args:
        song_name (str): The name of the song or artist to search and play on YouTube
    
    Returns:
        str: Success or error message
    """
    if not song_name or not song_name.strip():
        return "Error: Song name is empty"
    
    try:
        logger.info(f"Playing {song_name} on YouTube")
        
        # Create YouTube search URL
        search_query = song_name.replace(' ', '+')
        youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
        
        # Open in default browser
        webbrowser.open(youtube_url)
        
        logger.info(f"Successfully opened YouTube search for {song_name}")
        return f"Opening YouTube to play {song_name}"
        
    except Exception as e:
        logger.error(f"Error playing music: {e}")
        return f"Failed to play {song_name} on YouTube: {str(e)}"


@tool
def take_screenshot(filename: str = None) -> str:
    """
    Takes a screenshot of all monitors and saves it as an image file.
    
    Args:
        filename (str, optional): The filename to save the screenshot as.
                                  Examples: "my_photo", "vacation", "screenshot1"
                                  If not provided, defaults to 'screenshot_YYYYMMDD_HHMMSS.png'
    
    Returns:
        str: Success message with file path or error message
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if filename is None or not filename.strip():
            filename = f"screenshot_{timestamp}.png"
        
        # Ensure .png extension
        if not filename.lower().endswith('.png'):
            filename += ".png"
        
        # Create screenshots directory in Pictures folder
        screenshots_dir = os.path.join(os.path.expanduser("~"), "Pictures", "VoiceAssistant")
        os.makedirs(screenshots_dir, exist_ok=True)
        
        filepath = os.path.join(screenshots_dir, filename)
        
        logger.info(f"Taking screenshot using PIL ImageGrab...")
        
        # Take screenshot using PIL ImageGrab
        screenshot = ImageGrab.grab()
        screenshot.save(filepath)
        
        logger.info(f"Screenshot saved successfully at {filepath}")
        return f"Screenshot saved at {filepath}"
   
    except Exception as e:
        logger.error(f"Screenshot capture failed: {e}")
        return f"Sorry, couldn't capture screenshot: {str(e)}"


class AppLauncher:
    """Launches applications using subprocess"""
    
    def __init__(self):
        self.system = platform.system()
        
        # Common application mappings for Windows
        self.app_mappings = {
            'chrome': ['chrome.exe', 'Google\\Chrome\\Application\\chrome.exe'],
            'firefox': ['firefox.exe', 'Mozilla Firefox\\firefox.exe'],
            'edge': ['msedge.exe', 'Microsoft\\Edge\\Application\\msedge.exe'],
            'vscode': ['code.exe', 'Microsoft VS Code\\Code.exe'],
            'visual studio code': ['code.exe', 'Microsoft VS Code\\Code.exe'],
            'notepad': ['notepad.exe'],
            'calculator': ['calc.exe'],
            'paint': ['mspaint.exe'],
            'spotify': ['spotify.exe', 'Spotify\\Spotify.exe'],
            'discord': ['discord.exe', 'Discord\\Discord.exe'],
            'teams': ['teams.exe', 'Microsoft\\Teams\\current\\Teams.exe'],
            'outlook': ['outlook.exe', 'Microsoft Office\\root\\Office16\\OUTLOOK.EXE'],
            'word': ['winword.exe', 'Microsoft Office\\root\\Office16\\WINWORD.EXE'],
            'excel': ['excel.exe', 'Microsoft Office\\root\\Office16\\EXCEL.EXE'],
            'powerpoint': ['powerpnt.exe', 'Microsoft Office\\root\\Office16\\POWERPNT.EXE'],
            'vlc': ['vlc.exe', 'VideoLAN\\VLC\\vlc.exe'],
            'steam': ['steam.exe', 'Steam\\steam.exe'],
        }
        
    def _find_app_windows(self, app_name: str) -> str:
        """
        Find application executable on Windows
        
        Args:
            app_name: Name of the application
            
        Returns:
            str: Path to executable or empty string if not found
        """
        app_lower = app_name.lower()
        
        # Check if we have a mapping for this app
        if app_lower in self.app_mappings:
            search_names = self.app_mappings[app_lower]
        else:
            # Try the app name directly
            search_names = [f"{app_name}.exe"]
        
        # Common installation directories
        search_paths = [
            os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files')),
            os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs'),
            os.path.join(os.environ.get('APPDATA', '')),
        ]
        
        # Search for the application
        for search_name in search_names:
            # Try direct execution first (for system apps)
            try:
                subprocess.Popen(search_name, shell=True)
                return search_name
            except:
                pass
            
            # Search in common directories
            for base_path in search_paths:
                if not base_path:
                    continue
                    
                full_path = os.path.join(base_path, search_name)
                if os.path.exists(full_path):
                    return full_path
                
                # Also try searching subdirectories
                try:
                    for root, dirs, files in os.walk(base_path):
                        if search_name.split('\\')[-1] in files:
                            potential_path = os.path.join(root, search_name.split('\\')[-1])
                            if os.path.exists(potential_path):
                                return potential_path
                        # Limit search depth to avoid taking too long
                        if root.count(os.sep) - base_path.count(os.sep) > 2:
                            break
                except:
                    continue
        
        return ""
        
    def launch_application(self, app_name: str) -> tuple[bool, str]:
        """
        Opens an application using subprocess
        
        Args:
            app_name: Name of the application to launch
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not app_name or not app_name.strip():
            return False, "Application name is empty"
        
        try:
            logger.info(f"Attempting to launch {app_name} on {self.system}")
            
            if self.system == "Windows":
                # Try to find and launch on Windows
                app_path = self._find_app_windows(app_name)
                
                if app_path:
                    try:
                        subprocess.Popen(app_path, shell=True)
                        return True, f"Opening {app_name}"
                    except Exception as e:
                        logger.error(f"Error launching {app_path}: {e}")
                        return False, f"Found {app_name} but couldn't launch it"
                else:
                    return False, f"Could not find application {app_name}. Try saying the full name."
                        
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", app_name])
                return True, f"Opening {app_name}"
                
            elif self.system == "Linux":
                subprocess.Popen([app_name])
                return True, f"Opening {app_name}"
                
            else:
                return False, f"Unsupported operating system: {self.system}"
                
        except Exception as e:
            logger.error(f"Error launching application: {e}")
            return False, f"Failed to open {app_name}. Please check the application name."


class MusicPlayer:
    """Plays music on YouTube"""
    
    def play_on_youtube(self, song_name: str) -> tuple[bool, str]:
        """
        Searches and plays music on YouTube using pywhatkit
        
        Args:
            song_name: Name of the song to play
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not song_name or not song_name.strip():
            return False, "Song name is empty"
        
        try:
            import pywhatkit as kit
            logger.info(f"Playing {song_name} on YouTube")
            kit.playonyt(song_name)
            return True, f"Playing {song_name} on YouTube"
            
        except Exception as e:
            logger.error(f"Error playing music: {e}")
            return False, f"Failed to play {song_name} on YouTube"


class QuestionAnswerer:
    """Answers questions and executes commands using Strands Agents LLM with custom tools"""
    
    def __init__(self):
        """Initializes the Strands Agents LLM client with all tools and system prompt"""
        try:
            # System prompt to configure agent behavior
            system_prompt = """You are a helpful voice assistant and Your name is AI Buddy. Follow these rules:
                    1. Give CONCISE one-line answers (maximum 15-20 words)
                    2. All times and dates should be in IST (Indian Standard Time) timezone
                    3. Be direct and to the point
                    4. When using tools, confirm the action briefly
                    5. No explanations unless asked
                    6. If you don't find anything then search on web and then give answers.
                    Examples:
                    - "What time is it?" -> "It's 3:45 PM IST"
                    - "Open chrome" -> "Opening Chrome"
                    - "Open YouTube" -> Use open_youtube tool -> "Opening YouTube"
                    - "Play music" -> "Playing [song name] on YouTube"
                    - "Take a screenshot" -> "Screenshot saved at [path]"
                    - "Take screenshot and save it as my_photo" -> Extract "my_photo" as filename parameter
                    - "Screenshot called vacation" -> Extract "vacation" as filename parameter
                    - "Save screenshot as desktop_image" -> Extract "desktop_image" as filename parameter
                """
            
            # Initialize agent with all tools and system prompt
            self.agent = Agent(
                tools=[current_time, open_application, open_youtube, play_music_on_youtube, take_screenshot],
                system_prompt=system_prompt
            )
            logger.info("Strands Agent initialized with open_youtube tool, screenshot tool, IST timezone and concise response mode")
        except Exception as e:
            logger.error(f"Error initializing Strands Agent: {e}")
            self.agent = None
    
    def answer_question(self, question: str) -> str:
        """
        Processes user input using Strands Agents LLM with tools
        The agent can answer questions, open applications, open YouTube, play music, and take screenshots
        
        Args:
            question: The user's input/question/command
            
        Returns:
            str: The response from the agent
        """
        if not question or not question.strip():
            return "I didn't catch that. Could you please repeat?"
        
        if self.agent is None:
            return "I'm having trouble connecting. Please try again later."
        
        try:
            logger.info(f"Processing user input: {question}")
            response = self.agent(question)
            logger.info(f"Agent response: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            return "I'm sorry, I couldn't process that. Please try again."
