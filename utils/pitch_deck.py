import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

LOGO_PATH = "/home/IsaKai/NCPrime/IsaKaiHBG_AI/utils/E2217DEF-96B4-44F1-AF6F-BE92A3A5465A.png"
PDF_PATH = "/home/IsaKai/NCPrime/IsaKaiHBG_AI/utils/Sovereign_AI_PitchDeck.pdf"

LEFT_MARGIN = 60
RIGHT_MARGIN = 540

def draw_watermark(c, width, height):
    """Draw a centered logo watermark at 60% opacity for stronger branding."""
    try:
        c.saveState()
        c.translate(width/2, height/2)
        c.rotate(30)
        c.setFillAlpha(0.60)  # Increased visibility
        c.drawImage(LOGO_PATH, -2.5*inch, -2.5*inch, 5*inch, 5*inch, mask='auto')
        c.restoreState()
    except:
        pass

def draw_title(c, text, y, size=34, color=colors.black):
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(color)
    c.drawCentredString(415, y, text)

def draw_body_text(c, text, x, y, width_limit=RIGHT_MARGIN, font_size=16, line_height=22):
    """Wraps text within safe margins for readability."""
    c.setFont("Helvetica", font_size)
    c.setFillColor(colors.black)
    words = text.split()
    line = ""
    for word in words:
        test_line = (line + " " + word).strip()
        if c.stringWidth(test_line, "Helvetica", font_size) < width_limit - x:
            line = test_line
        else:
            c.drawString(x, y, line)
            y -= line_height
            line = word
    if line:
        c.drawString(x, y, line)
    return y

def make_pitch_deck():
    c = canvas.Canvas(PDF_PATH, pagesize=letter)
    width, height = letter

    # Cover Page
    draw_watermark(c, width, height)
    draw_title(c, "Sovereign Multi-Agent AI", height-180)
    c.setFont("Helvetica", 20)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height-230, "Sovereign AI by IsaKai Holdings and Bookings Group LLC")
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.gold)
    c.drawCentredString(width/2, height-280, "A $60,000 Vision for a First-to-Market AI Ecosystem")
    c.showPage()

    # System Overview
    draw_watermark(c, width, height)
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(colors.black)
    c.drawString(LEFT_MARGIN, height-100, "System Overview")
    body = (
        "IsaKaiHBG_AI merges three core AI models into a sovereign ecosystem:\n\n"
        "• Gemma 7B – Research and rapid summarization\n"
        "• WizardCoder 7B – Automated coding and script generation\n"
        "• Mistral 7B – Real-time trading strategies and analytics\n\n"
        "This combination enables fast development, market analytics, and trading — "
        "all while maintaining full data privacy and sovereignty."
    )
    draw_body_text(c, body, LEFT_MARGIN, height-150)
    c.showPage()

    # Technology & Sovereignty
    draw_watermark(c, width, height)
    draw_title(c, "Technology & Sovereignty", height-100, size=28)
    tech_left = (
        "- Whisper + LLaMA.cpp + Ollama for offline AI reasoning\n"
        "- WireGuard & Yggdrasil for decentralized secure networking\n"
        "- Firejail optional sandboxing for hardened runtime\n"
    )
    tech_right = (
        "- Intel i9-14900K, 192GB DDR5 RAM, RTX 4090\n"
        "- 2TB Samsung 980 Pro NVMe SSD RAID\n"
        "- Baseline $20K stack, scalable to $60K enterprise build"
    )
    draw_body_text(c, tech_left, 80, height-180, width_limit=280)
    draw_body_text(c, tech_right, 330, height-180, width_limit=540)
    c.showPage()

    # Funding Request
    draw_watermark(c, width, height)
    draw_title(c, "Funding Request: $60,000", height-100, size=28, color=colors.gold)
    funding = (
        "The $60K round scales IsaKaiHBG_AI from our $20K prototype stack to an "
        "enterprise-ready, sovereign AI system capable of handling 24/7 trading, "
        "automated coding, and live research support for global clients.\n\n"
        "ROI projections: 3–5x return in Year One via trading profits, SaaS licensing, "
        "and consulting packages."
    )
    draw_body_text(c, funding, LEFT_MARGIN, height-150)
    c.showPage()

    # Call-to-Action
    draw_watermark(c, width, height)
    draw_title(c, "Join the Future of Sovereignty", height-100)
    call_text = (
        "IsaKaiHBG_AI isn’t just another AI platform — it’s the future of ownership and "
        "independence. We’re empowering individuals and companies to harness AI "
        "without Big Tech dependency.\n\n"
        "This $60,000 investment will fuel not just infrastructure, but a movement: "
        "a profitable, private, and sovereign AI ecosystem designed to thrive for years.\n\n"
        "Invest today and become a partner in reshaping the AI landscape — not just "
        "to profit, but to lead a revolution in how AI serves humanity."
    )
    draw_body_text(c, call_text, LEFT_MARGIN, height-150)
    c.showPage()

    c.save()
    print(f"Pitch Deck built: {PDF_PATH}")

if __name__ == "__main__":
    make_pitch_deck()

