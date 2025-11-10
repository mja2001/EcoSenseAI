from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf_report(data: list) -> str:
    doc = SimpleDocTemplate("compliance_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("EcoSenseAI Compliance Report", styles['Title']))

    # Data table
    table_data = [["Timestamp", "CO2 (ppm)", "Temp (°C)", "Prediction"]]
    for item in data[-10:]:  # Last 10 entries
        table_data.append([item.get('timestamp'), item.get('co2'), item.get('temp'), item.get('prediction')])
    story.append(Table(table_data))

    doc.build(story)
    return "compliance_report.pdf"