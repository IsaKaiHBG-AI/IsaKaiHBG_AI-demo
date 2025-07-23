from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, HexColor
import os

LOGO = "/home/IsaKai/NCPrime/IsaKaiHBG_AI/utils/E2217DEF-96B4-44F1-AF6F-BE92A3A5465A.png"
PDF_PATH = "/home/IsaKai/NCPrime/IsaKaiHBG_AI/utils/IsaKai_Preview_PitchDeck.pdf"

def draw_logo(c, width, height):
    """Draws the logo as a smaller cube at the bottom center (85% opacity simulated)."""
    logo_size = 120
    x = (width - logo_size) / 2
    y = 40
    c.drawImage(LOGO, x, y, width=logo_size, height=logo_size, mask='auto')

def make_preview_pitch_deck():
    c = canvas.Canvas(PDF_PATH, pagesize=landscape(letter))
    width, height = landscape(letter)

    # PAGE 1: COVER
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(HexColor("#FFD700"))
    c.drawCentredString(width / 2, height - 200, "Sovereign Multi-Agent AI")
    c.setFont("Helvetica", 22)
    c.setFillColor(black)
    c.drawCentredString(width / 2, height - 250, 
        "By IsaKai Holdings & Bookings Group LLC")
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height - 280, 
        "A $60,000 Vision for a First-to-Market AI Ecosystem")
    draw_logo(c, width, height)
    c.showPage()

    # PAGE 2: SYSTEM OVERVIEW
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(black)
    c.drawString(50, height - 100, "System Overview")
    c.setFont("Helvetica", 18)
    text_lines = [
        "IsaKaiHBG_AI is a cutting-edge, multi-model AI stack designed",
        "for rapid development, sovereign data security, and market-scale operations.",
        "Core AI Models:",
        "- Gemma 7B (Research & Summarization)",
        "- WizardCoder 7B (Automation & Code)",
        "- Mistral 7B (Trading Strategy & Execution)",
        "",
        "This integrated system can deliver trading, coding, and research solutions faster",
        "than any centralized AI provider, ensuring full sovereign control."
    ]
    for i, line in enumerate(text_lines):
        c.drawString(60, height - 150 - (i * 28), line)
    draw_logo(c, width, height)
    c.showPage()

    # PAGE 3: TECHNOLOGY & SOVEREIGNTY
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(black)
    c.drawString(50, height - 100, "Technology & Sovereignty")
    c.setFont("Helvetica", 18)
    tech_lines = [
        "- Integrated Whisper voice control for seamless input.",
        "- LLaMA.cpp + Ollama for on-device inference.",
        "- WireGuard & Yggdrasil networking (Firejail optional).",
        "- Real-time orchestration of Gemma, Wizard, and Mistral.",
        "",
        "With this stack, IsaKaiHBG_AI offers unmatched speed, privacy, and autonomy."
    ]
    for i, line in enumerate(tech_lines):
        c.drawString(60, height - 150 - (i * 28), line)
    draw_logo(c, width, height)
    c.showPage()

    # PAGE 4: FUNDING BREAKDOWN
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(black)
    c.drawString(50, height - 100, "Funding Breakdown - $60,000 Request")
    c.setFont("Helvetica", 18)
    funding_lines = [
        "Hardware & Infrastructure ($20,000):",
        "- 192GB DDR5 workstation (RTX 4090, i9-14900K).",
        "- Dedicated networking & GPU acceleration.",
        "",
        "Platform Development ($25,000):",
        "- Advanced agent orchestration and AI tuning.",
        "- Whisper, Ollama, and LLaMA.cpp integration.",
        "",
        "Scaling & Launch ($15,000):",
        "- Secure network expansion.",
        "- Investor demos and scaling the trading/coding stack."
    ]
    for i, line in enumerate(funding_lines):
        c.drawString(60, height - 150 - (i * 28), line)
    draw_logo(c, width, height)
    c.showPage()

        # PAGE 5: CALL TO ACTION (Redesigned)
    c.setFillColor(HexColor("#FFD700"))
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(width / 2, height - 80, "Join Us in Building the Future")

    # Top divider line
    c.setStrokeColor(HexColor("#FFD700"))
    c.setLineWidth(2)
    c.line(40, height - 100, width - 40, height - 100)

    # Body text (left column)
    c.setFont("Helvetica", 18)
    c.setFillColor(black)
    paragraphs = [
        "IsaKai Holdings & Bookings Group LLC is pioneering a sovereign AI ecosystem that gives full control to its operators. With your support, we will revolutionize trading, coding, and research automation while ensuring complete data privacy.",
        "This $60,000 investment will empower our advanced hardware stack, integrate cutting-edge AI models (Gemma, Wizard, Mistral), and scale a platform built to outperform centralized AI providers.",
        "Join us now to secure a future where AI sovereignty drives innovation — and investors share in the rewards of leading a new market standard."
    ]
    y = height - 150
    for para in paragraphs:
        for line in para.splitlines():
            c.drawString(60, y, line)
            y -= 30
        y -= 20

    # Logo at bottom-right (cube)
    logo_size = 120
    c.drawImage(LOGO, width - logo_size - 50, 40, width=logo_size, height=logo_size, mask='auto')

    # Footer branding
    c.setFont("Helvetica-Oblique", 14)
    c.setFillColor(HexColor("#999999"))
    c.drawCentredString(width / 2, 30, "IsaKai Holdings & Bookings Group LLC")

    c.showPage()

    c.save()
    print(f"Preview deck saved to: {PDF_PATH}")

if __name__ == "__main__":
    make_preview_pitch_deck()
