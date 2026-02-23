"""
UI Manager - Manages Tkinter interface with HUD animation and conversation history
"""
import tkinter as tk
from tkinter import scrolledtext
import math
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class UIManager:
    """Manages the Tkinter UI with futuristic HUD animation and conversation history"""
    
    def __init__(self, root: tk.Tk):
        """
        Initializes the Tkinter window
        
        Args:
            root: The Tkinter root window
        """
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg="#000000")
        
        # Animation variables
        self.angle = 0
        self.animation_running = False
        self.pulse = 0
        
        # Create canvas for HUD animation
        self.canvas = tk.Canvas(
            self.root,
            width=800,
            height=400,
            bg="#000000",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # HUD elements
        center_x = 400
        center_y = 200
        
        # Outer ring
        self.outer_ring = self.canvas.create_oval(
            center_x - 100, center_y - 100,
            center_x + 100, center_y + 100,
            outline="#00ffff",
            width=2
        )
        
        # Middle ring
        self.middle_ring = self.canvas.create_oval(
            center_x - 70, center_y - 70,
            center_x + 70, center_y + 70,
            outline="#00ccff",
            width=2
        )
        
        # Inner ring
        self.inner_ring = self.canvas.create_oval(
            center_x - 40, center_y - 40,
            center_x + 40, center_y + 40,
            outline="#0099ff",
            width=2
        )
        
        # Center dot
        self.center_dot = self.canvas.create_oval(
            center_x - 5, center_y - 5,
            center_x + 5, center_y + 5,
            fill="#00ffff",
            outline=""
        )
        
        # Rotating lines (4 lines at 90 degree intervals)
        self.rotating_lines = []
        for i in range(4):
            line = self.canvas.create_line(
                center_x, center_y,
                center_x + 80, center_y,
                fill="#00ffff",
                width=1
            )
            self.rotating_lines.append(line)
        
        # Arc segments
        self.arcs = []
        for i in range(8):
            arc = self.canvas.create_arc(
                center_x - 85, center_y - 85,
                center_x + 85, center_y + 85,
                start=i * 45,
                extent=30,
                outline="#00ffff",
                width=1,
                style=tk.ARC
            )
            self.arcs.append(arc)
        
        # Create conversation history frame
        history_frame = tk.Frame(self.root, bg="#000000", height=200)
        history_frame.pack(fill=tk.BOTH, side=tk.BOTTOM)
        history_frame.pack_propagate(False)
        
        # Create scrolled text widget for conversation
        self.conversation_text = scrolledtext.ScrolledText(
            history_frame,
            wrap=tk.WORD,
            bg="#000000",
            fg="#00ffff",
            font=("Consolas", 10),
            padx=10,
            pady=10,
            insertbackground="#00ffff"
        )
        self.conversation_text.pack(fill=tk.BOTH, expand=True)
        self.conversation_text.config(state=tk.DISABLED)
        
        # Message counter for history limit
        self.message_count = 0
        self.max_messages = 100
        
        # Status label for listening indicator
        self.status_label = tk.Label(
            self.root,
            text="● READY",
            bg="#000000",
            fg="#00ffff",
            font=("Consolas", 12, "bold")
        )
        self.status_label.place(x=10, y=10)
        
        logger.info("UI initialized with HUD animation")
    
    def start_animation(self) -> None:
        """Starts the HUD animation"""
        if not self.animation_running:
            self.animation_running = True
            self._animate()
            logger.info("HUD animation started")
    
    def _animate(self) -> None:
        """Internal animation loop for HUD"""
        if not self.animation_running:
            return
        
        # Update angle
        self.angle += 2
        if self.angle >= 360:
            self.angle = 0
        
        # Update pulse for glow effect
        self.pulse += 0.1
        if self.pulse >= 2 * math.pi:
            self.pulse = 0
        
        # Calculate center position
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        center_x = canvas_width // 2 if canvas_width > 1 else 400
        center_y = canvas_height // 2 if canvas_height > 1 else 200
        
        # Update rings position
        self.canvas.coords(self.outer_ring, center_x - 100, center_y - 100, center_x + 100, center_y + 100)
        self.canvas.coords(self.middle_ring, center_x - 70, center_y - 70, center_x + 70, center_y + 70)
        self.canvas.coords(self.inner_ring, center_x - 40, center_y - 40, center_x + 40, center_y + 40)
        self.canvas.coords(self.center_dot, center_x - 5, center_y - 5, center_x + 5, center_y + 5)
        
        # Rotate the lines
        for i, line in enumerate(self.rotating_lines):
            angle_rad = math.radians(self.angle + i * 90)
            line_end_x = center_x + 80 * math.cos(angle_rad)
            line_end_y = center_y + 80 * math.sin(angle_rad)
            self.canvas.coords(line, center_x, center_y, line_end_x, line_end_y)
        
        # Update arcs
        for i, arc in enumerate(self.arcs):
            start_angle = (self.angle + i * 45) % 360
            self.canvas.itemconfig(arc, start=start_angle)
            self.canvas.coords(arc, center_x - 85, center_y - 85, center_x + 85, center_y + 85)
        
        # Pulse effect on center dot
        pulse_size = 5 + int(3 * math.sin(self.pulse))
        self.canvas.coords(
            self.center_dot,
            center_x - pulse_size, center_y - pulse_size,
            center_x + pulse_size, center_y + pulse_size
        )
        
        # Schedule next frame (60 FPS = ~16ms)
        self.root.after(16, self._animate)
    
    def add_user_message(self, text: str) -> None:
        """
        Adds user question to conversation history
        
        Args:
            text: The user's message
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"[{timestamp}] You: {text}\n"
        
        self.conversation_text.config(state=tk.NORMAL)
        
        # Limit conversation history to max_messages
        self.message_count += 1
        if self.message_count > self.max_messages:
            # Delete oldest message (first line)
            self.conversation_text.delete("1.0", "2.0")
        
        self.conversation_text.insert(tk.END, message)
        self.conversation_text.config(state=tk.DISABLED)
        self.conversation_text.see(tk.END)
        
        logger.info(f"Added user message: {text}")
    
    def add_assistant_message(self, text: str) -> None:
        """
        Adds assistant response to conversation history
        
        Args:
            text: The assistant's response
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"[{timestamp}] Assistant: {text}\n\n"
        
        self.conversation_text.config(state=tk.NORMAL)
        
        # Limit conversation history to max_messages
        self.message_count += 1
        if self.message_count > self.max_messages:
            # Delete oldest message (first line)
            self.conversation_text.delete("1.0", "2.0")
        
        self.conversation_text.insert(tk.END, message)
        self.conversation_text.config(state=tk.DISABLED)
        self.conversation_text.see(tk.END)
        
        logger.info(f"Added assistant message: {text}")
    
    def update(self) -> None:
        """Updates the UI (called in main loop)"""
        self.root.update()
    
    def close(self) -> None:
        """Closes the UI window"""
        self.animation_running = False
        self.root.quit()
        logger.info("UI closed")

    
    def set_listening_status(self, is_listening: bool) -> None:
        """
        Updates the listening status indicator
        
        Args:
            is_listening: True if listening, False otherwise
        """
        if is_listening:
            self.status_label.config(text="● LISTENING", fg="#ff0066")
            # Make HUD glow red when listening
            self.canvas.itemconfig(self.outer_ring, outline="#ff0066")
            self.canvas.itemconfig(self.middle_ring, outline="#ff0066")
            self.canvas.itemconfig(self.inner_ring, outline="#ff0066")
            self.canvas.itemconfig(self.center_dot, fill="#ff0066")
            for line in self.rotating_lines:
                self.canvas.itemconfig(line, fill="#ff0066")
            for arc in self.arcs:
                self.canvas.itemconfig(arc, outline="#ff0066")
        else:
            self.status_label.config(text="● READY", fg="#00ffff")
            # Restore cyan color
            self.canvas.itemconfig(self.outer_ring, outline="#00ffff")
            self.canvas.itemconfig(self.middle_ring, outline="#00ccff")
            self.canvas.itemconfig(self.inner_ring, outline="#0099ff")
            self.canvas.itemconfig(self.center_dot, fill="#00ffff")
            for line in self.rotating_lines:
                self.canvas.itemconfig(line, fill="#00ffff")
            for arc in self.arcs:
                self.canvas.itemconfig(arc, outline="#00ffff")
