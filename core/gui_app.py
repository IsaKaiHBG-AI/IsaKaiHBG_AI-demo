import sys, os, time, subprocess
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QProgressBar,
    QStackedWidget, QGraphicsOpacityEffect
)
import pygame
from agent_manager import AgentManager

# Initialize Pygame mixer for sounds
pygame.mixer.init()
PING_SOUND = "/home/IsaKai/NCPrime/IsaKaiHBG_AI/utils/ping.wav"
SEND_SOUND = "/home/IsaKai/NCPrime/IsaKaiHBG_AI/utils/send.wav"
REPLY_SOUND = "/home/IsaKai/NCPrime/IsaKaiHBG_AI/utils/reply.wav"

LOGO_PATH = "/home/IsaKai/NCPrime/IsaKaiHBG_AI/utils/E2217DEF-96B4-44F1-AF6F-BE92A3A5465A.png"
BRAND_TEXT = "IsaKai Holdings and Bookings Group LLC"

# Typing animation worker
class TypingWorker(QThread):
    update_text = pyqtSignal(str)
    finished = pyqtSignal()
    def __init__(self, full_text: str, color: str):
        super().__init__()
        self.full_text = full_text
        self.color = color
    def run(self):
        current = ""
        for char in self.full_text:
            current += char
            self.update_text.emit(f"<span style='color:{self.color};'>AI:</span> {current}")
            time.sleep(0.02)
        self.finished.emit()

# Rotating logo widget
class RotatingLogo(QLabel):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.speed = 1
        self.pixmap = QPixmap(LOGO_PATH)
        self.setScaledContents(True)
        self.setFixedSize(400, 400)
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate_logo)
        self.timer.start(50)
    def rotate_logo(self):
        transform = QTransform().rotate(self.angle)
        rotated = self.pixmap.transformed(transform, Qt.SmoothTransformation)
        self.setPixmap(rotated)
        self.angle = (self.angle + self.speed) % 360
    def boost_rotation(self, fast=False):
        self.speed = 12 if fast else 6
        QTimer.singleShot(3000, self.reset_speed)
    def reset_speed(self):
        self.speed = 1

# Loading worker for pitch deck
class LoadingWorker(QThread):
    progress_update = pyqtSignal(int)
    finished = pyqtSignal()
    def run(self):
        for i in range(101):
            time.sleep(0.05)
            self.progress_update.emit(i)
        self.finished.emit()

# Splash screen with fade
class SplashScreen(QWidget):
    def __init__(self, stacked_widget, chat_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.chat_widget = chat_widget
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.logo = RotatingLogo()
        self.logo.boost_rotation(fast=True)
        self.label = QLabel("Initializing IsaKaiHBG_AI...")
        self.label.setStyleSheet("color: #FFD700; font-size: 22px;")
        layout.addWidget(self.logo, alignment=Qt.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        try: pygame.mixer.Sound(PING_SOUND).play()
        except: pass
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_anim.setDuration(1000)
        QTimer.singleShot(3000, self.finish_boot)
    def finish_boot(self):
        self.opacity_anim.setStartValue(1)
        self.opacity_anim.setEndValue(0)
        self.opacity_anim.finished.connect(self.switch_to_chat)
        self.opacity_anim.start()
    def switch_to_chat(self):
        self.stacked_widget.setCurrentWidget(self.chat_widget)
        self.chat_widget.logo.boost_rotation(fast=False)

# Main chat GUI
class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IsaKaiHBG_AI - Multi-Agent AI")
        self.setGeometry(100, 100, 1400, 750)
        self.setStyleSheet("background-color: black; color: white;")
        self.agent_manager = AgentManager()
        layout = QHBoxLayout(self)

        # Chat layout
        chat_layout = QVBoxLayout()
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {background-color:#111;color:#EEE;font-family:Consolas;font-size:14px;
                       border:1px solid #444;border-radius:6px;padding:8px;}""")
        self.entry = QLineEdit()
        self.entry.setStyleSheet("""
            QLineEdit {background-color:#222;color:#FFF;font-family:Consolas;font-size:14px;
                       border-radius:6px;padding:6px;}""")
        self.entry.returnPressed.connect(self.process_message)
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background-color:#444;color:white;")
        self.send_button.clicked.connect(self.process_message)
        self.toggle_mode_button = QPushButton("Demo Mode (ON)")
        self.toggle_mode_button.setCheckable(True)
        self.toggle_mode_button.setStyleSheet("background-color:#222;color:yellow;")
        self.toggle_mode_button.setChecked(True)
        self.toggle_mode_button.clicked.connect(self.toggle_mode)
        self.mic_button = QPushButton("🎤")
        self.mic_button.setStyleSheet("background-color:#555;color:white;")
        self.mic_button.clicked.connect(self.voice_input)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.entry)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.toggle_mode_button)
        input_layout.addWidget(self.mic_button)
        chat_layout.addWidget(self.chat_display)
        chat_layout.addLayout(input_layout)

        # Quick demo buttons
        self.demo_gemma = QPushButton("Gemma Research")
        self.demo_wizard = QPushButton("Wizard Script")
        self.demo_mistral = QPushButton("Mistral Strategy")
        self.demo_pitch = QPushButton("Generate Pitch Deck")
        self.demo_gemma.clicked.connect(lambda: self.auto_demo("gemma summarize AI funding trends"))
        self.demo_wizard.clicked.connect(lambda: self.auto_demo("wizard make NAS100 trading script"))
        self.demo_mistral.clicked.connect(lambda: self.auto_demo("mistral $75 prop plan"))
        self.demo_pitch.clicked.connect(self.start_pitch_deck_animation)

        demo_layout = QHBoxLayout()
        demo_layout.addWidget(self.demo_gemma)
        demo_layout.addWidget(self.demo_wizard)
        demo_layout.addWidget(self.demo_mistral)
        demo_layout.addWidget(self.demo_pitch)
        chat_layout.addLayout(demo_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("QProgressBar {color:#0F0;background-color:#222;border:1px solid #555;}")
        self.progress_bar.hide()
        chat_layout.addWidget(self.progress_bar)

        # Logo/branding
        right_layout = QVBoxLayout()
        self.logo = RotatingLogo()
        self.brand = QLabel(BRAND_TEXT)
        self.brand.setStyleSheet("color:#FFD700;font-size:18px;font-weight:bold;")
        self.brand.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.logo, alignment=Qt.AlignCenter)
        right_layout.addWidget(self.brand, alignment=Qt.AlignBottom | Qt.AlignCenter)
        layout.addLayout(chat_layout, 3)
        layout.addLayout(right_layout, 1)

    def toggle_mode(self):
        new_status = self.agent_manager.toggle_mode()
        self.toggle_mode_button.setText(new_status)

    def process_message(self):
        user_text = self.entry.text().strip()
        if not user_text: return
        pygame.mixer.Sound(SEND_SOUND).play()
        self.chat_display.append(f"<b>You:</b> {user_text}")
        self.entry.clear()
        ai_response = self.agent_manager.handle_input(user_text)
        color = "#00FF00"
        if "Gemma" in ai_response: color = "#1E90FF"
        elif "Wizard" in ai_response: color = "#00FF7F"
        elif "Mistral" in ai_response: color = "#BA55D3"
        self.logo.boost_rotation()
        self.typing_worker = TypingWorker(ai_response, color)
        self.typing_worker.update_text.connect(lambda text: self.chat_display.append(text))
        self.typing_worker.finished.connect(lambda: pygame.mixer.Sound(REPLY_SOUND).play())
        self.typing_worker.start()

    def start_pitch_deck_animation(self):
        self.chat_display.append("<b>AI:</b> Building Pitch Deck...")
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.logo.boost_rotation(fast=True)
        self.loading_worker = LoadingWorker()
        self.loading_worker.progress_update.connect(self.progress_bar.setValue)
        self.loading_worker.finished.connect(self.finish_pitch_deck)
        self.loading_worker.start()

    def finish_pitch_deck(self):
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.colors import black, HexColor
        from reportlab.lib.units import inch
        from reportlab.lib.utils import ImageReader
        pdf_path = "/home/IsaKai/NCPrime/IsaKaiHBG_AI/utils/IsaKai_AI_PitchDeck.pdf"
        logo_path = LOGO_PATH
        width, height = letter
        gold = HexColor("#FFD700")
        c = canvas.Canvas(pdf_path, pagesize=letter)

        def footer(): c.setFont("Helvetica", 10); c.setFillColor(gold); c.drawCentredString(width/2, 20, BRAND_TEXT)
        def divider(y): c.setStrokeColor(gold); c.setLineWidth(1); c.line(40, y, width-40, y)
        def logo(): c.drawImage(ImageReader(logo_path),(width-1.5*inch)/2,0.5*inch,1.5*inch,1.5*inch,mask='auto')

        # Page content
        pages = [
            ("Sovereign Multi-Agent AI", ["By IsaKai Holdings and Bookings Group LLC",
             "A $60,000 Vision for a First-to-Market AI Ecosystem"]),
            ("Technology & Sovereignty", ["- Integrated Whisper + LLAMA.CP + Ollama",
             "- WireGuard & Yggdrasil networking (Firejail optional)",
             "- Multi-model orchestration (Gemma, Wizard, Mistral)"]),
            ("System Overview", ["IsaKaiHBG_AI combines 3 AI models:",
             "- Gemma 7B (Research & Summaries)","- WizardCoder 7B (Automation)",
             "- Mistral 7B (Trading Strategy)","Includes Whisper voice, PDF, networking."]),
            ("Hardware & Funding", ["$60,000 funding supports:",
             "- $20,000+ workstation (i9-14900K, RTX4090, 192GB DDR5)",
             "- WireGuard/Yggdrasil cluster scaling",
             "- Real-time investor-ready demos"]),
            ("Join Us in Building the Future", [
             "IsaKai Holdings & Bookings Group LLC is pioneering a sovereign AI ecosystem.",
             "This $60,000 investment will accelerate hardware and integrations.",
             "Now is the time to join us — help secure AI sovereignty and reap rewards."])
        ]
        for title, lines in pages:
            c.setFont("Helvetica-Bold", 24); c.setFillColor(gold)
            c.drawCentredString(width/2, height-100, title)
            divider(height-120)
            c.setFont("Helvetica", 14); c.setFillColor(black)
            y = height-180
            for line in lines:
                c.drawCentredString(width/2, y, line); y -= 30
            logo(); footer(); c.showPage()
        c.save()

        self.chat_display.append("<b>AI:</b> Professional Pitch Deck Ready! Opening...")
        self.progress_bar.hide()
        pygame.mixer.Sound(REPLY_SOUND).play()
        try: subprocess.Popen(["xdg-open", pdf_path])
        except Exception as e: self.chat_display.append(f"<b>Error:</b> Could not open PDF ({e})")

    def auto_demo(self, text): self.entry.setText(text); self.process_message()

    def voice_input(self):
        import whisper, sounddevice as sd, numpy as np
        duration, samplerate = 5, 16000
        self.chat_display.append("<i>Listening...</i>")
        rec = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
        sd.wait()
        audio = np.squeeze(rec)
        model = whisper.load_model("base")
        text = model.transcribe(audio, fp16=False)["text"].strip()
        self.entry.setText(text)
        self.process_message()

def main():
    app = QApplication(sys.argv)
    stacked = QStackedWidget()
    chat = ChatApp()
    splash = SplashScreen(stacked, chat)
    stacked.addWidget(splash)
    stacked.addWidget(chat)
    stacked.setCurrentWidget(splash)
    stacked.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
