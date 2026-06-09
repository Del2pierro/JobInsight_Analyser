from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from typing import Dict, Any
from app.agents.base import BaseAgent

class ReportAgent(BaseAgent):
    """
    Reporting Agent.
    Generates professional PDF reports summarizing market analysis.
    
    Analogy: The 'Designer' who takes all the raw data and charts 
    to create a beautiful, printable magazine for the board.
    """

    def __init__(self):
        super().__init__(name="ReportAgent")

    def generate_market_report(self, trends: Dict[str, Any]) -> BytesIO:
        """
        Creates a PDF report from trend data.
        """
        self.log_start("generate_pdf_report")
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Title
        p.setFont("Helvetica-Bold", 24)
        p.drawString(100, height - 100, "Rapport du Marché de l'Emploi")
        
        # Date
        p.setFont("Helvetica", 12)
        import datetime
        p.drawString(100, height - 130, f"Généré le : {datetime.datetime.now().strftime('%d/%m/%Y')}")

        # Top Skills
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 180, "Top 10 Compétences Demandées")
        
        p.setFont("Helvetica", 12)
        y = height - 210
        for skill in trends.get("top_skills", []):
            p.drawString(120, y, f"• {skill['name']} ({skill['count']} offres)")
            y -= 20
            if y < 100: break

        # Vibe
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, y - 40, f"Indicateur de Tendance : {trends.get('market_vibe')}")

        p.showPage()
        p.save()
        
        buffer.seek(0)
        self.log_end("generate_pdf_report")
        return buffer

# Singleton
report_agent = ReportAgent()
