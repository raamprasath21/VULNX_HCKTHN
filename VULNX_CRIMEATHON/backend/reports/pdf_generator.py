from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf_report(findings, output_path="vulnx_report.pdf"):
    doc = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    doc.setTitle("VulnX Security Assessment Report")
    doc.setFont("Helvetica-Bold", 18)
    doc.drawString(72, height - 72, "VulnX Security Assessment Report")
    doc.setFont("Helvetica", 11)
    doc.drawString(72, height - 96, "Evidence-backed findings overview")

    y = height - 140
    for index, finding in enumerate(findings, start=1):
        title = finding.get("title", "Finding")
        severity = finding.get("severity", "medium").upper()
        description = finding.get("description", "No description provided.")
        if y < 72:
            doc.showPage()
            y = height - 72
        doc.setFont("Helvetica-Bold", 12)
        doc.drawString(72, y, f"{index}. {title} [{severity}]")
        y -= 18
        doc.setFont("Helvetica", 10)
        wrapped = doc.beginText(90, y)
        wrapped.textLine(description[:180])
        doc.drawText(wrapped)
        y -= 28

    doc.save()
    return output_path
