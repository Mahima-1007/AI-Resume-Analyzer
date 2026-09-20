from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from io import BytesIO

def get_base_styles():
    styles = getSampleStyleSheet()
    return styles

def _template_modern(data, buffer):
    """Modern Professional: Blue accents, clean sans-serif layout."""
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = get_base_styles()
    
    name_style = ParagraphStyle('Name', parent=styles['Heading1'], fontSize=24, spaceAfter=8, textColor=colors.HexColor("#1e3a8a"), alignment=TA_CENTER)
    contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontSize=10, spaceAfter=20, textColor=colors.HexColor("#475569"), alignment=TA_CENTER)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=14, spaceBefore=16, spaceAfter=8, textColor=colors.HexColor("#1e3a8a"), borderPadding=2, borderType=2, borderColor=colors.HexColor("#1e3a8a"), borderStyle='solid')
    body_style = styles['Normal']
    
    elements = []
    
    # Header
    elements.append(Paragraph(data.get("name", "Your Name").upper(), name_style))
    contact_info = f"{data.get('email', '')} | {data.get('phone', '')}"
    elements.append(Paragraph(contact_info, contact_style))
    
    # Summary
    if data.get("summary"):
        elements.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
        elements.append(Paragraph(data["summary"], body_style))
        
    # Experience
    if data.get("experience"):
        elements.append(Paragraph("WORK EXPERIENCE", section_style))
        for exp in data["experience"]:
            elements.append(Paragraph(f"<b>{exp.get('role')}</b> | {exp.get('company')}", body_style))
            elements.append(Paragraph(f"<font color='#64748b'>{exp.get('duration')}</font>", ParagraphStyle('Dur', parent=body_style, fontSize=9, spaceAfter=4)))
            elements.append(Paragraph(exp.get('description', ''), body_style))
            elements.append(Spacer(1, 8))
            
    # Education
    if data.get("education"):
        elements.append(Paragraph("EDUCATION", section_style))
        for edu in data["education"]:
            elements.append(Paragraph(f"<b>{edu.get('degree')}</b>, {edu.get('institution')}", body_style))
            elements.append(Paragraph(f"<font color='#64748b'>{edu.get('year')}</font>", ParagraphStyle('Yr', parent=body_style, fontSize=9, spaceAfter=4)))
            elements.append(Spacer(1, 4))
            
    # Skills
    if data.get("skills"):
        elements.append(Paragraph("SKILLS", section_style))
        skills_text = " • ".join(data["skills"])
        elements.append(Paragraph(skills_text, body_style))
        
    # Projects
    if data.get("projects"):
        elements.append(Paragraph("PROJECTS", section_style))
        for proj in data["projects"]:
            elements.append(Paragraph(f"<b>{proj.get('title')}</b>", body_style))
            elements.append(Paragraph(proj.get('description', ''), body_style))
            if proj.get('technologies'):
                elements.append(Paragraph(f"<i>Tech: {proj['technologies']}</i>", ParagraphStyle('Tech', parent=body_style, textColor=colors.HexColor("#475569"))))
            elements.append(Spacer(1, 8))

    doc.build(elements)

def _template_minimal(data, buffer):
    """Minimal ATS: Strictly text, highly parsable, no borders just whitespace."""
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = get_base_styles()
    
    name_style = ParagraphStyle('Name', parent=styles['Heading1'], fontSize=20, spaceAfter=6, alignment=TA_CENTER)
    contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontSize=11, spaceAfter=24, alignment=TA_CENTER)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=12, spaceBefore=14, spaceAfter=6, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, leading=14)
    
    elements = []
    
    elements.append(Paragraph(data.get("name", "Your Name").upper(), name_style))
    contact_info = f"{data.get('email', '')} | {data.get('phone', '')}"
    elements.append(Paragraph(contact_info, contact_style))
    
    if data.get("summary"):
        elements.append(Paragraph("SUMMARY", section_style))
        elements.append(Paragraph(data["summary"], body_style))
        
    if data.get("skills"):
        elements.append(Paragraph("SKILLS", section_style))
        elements.append(Paragraph(", ".join(data["skills"]), body_style))
        
    if data.get("experience"):
        elements.append(Paragraph("EXPERIENCE", section_style))
        for exp in data["experience"]:
            elements.append(Paragraph(f"<b>{exp.get('role')}</b>, {exp.get('company')} ({exp.get('duration')})", body_style))
            elements.append(Paragraph(exp.get('description', ''), body_style))
            elements.append(Spacer(1, 10))
            
    if data.get("education"):
        elements.append(Paragraph("EDUCATION", section_style))
        for edu in data["education"]:
            elements.append(Paragraph(f"<b>{edu.get('institution')}</b> - {edu.get('degree')} ({edu.get('year')})", body_style))
            elements.append(Spacer(1, 8))
            
    if data.get("projects"):
        elements.append(Paragraph("PROJECTS", section_style))
        for proj in data["projects"]:
            elements.append(Paragraph(f"<b>{proj.get('title')}</b>", body_style))
            elements.append(Paragraph(proj.get('description', ''), body_style))
            elements.append(Spacer(1, 8))

    doc.build(elements)

def _template_two_column(data, buffer):
    """Two Column Professional: Left column for contact/skills, right for experience."""
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = get_base_styles()
    
    name_style = ParagraphStyle('Name', parent=styles['Heading1'], fontSize=26, textColor=colors.HexColor("#2C3E50"))
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=14, spaceBefore=12, spaceAfter=6, textColor=colors.HexColor("#2C3E50"), borderPadding=2, borderType=2, borderColor=colors.HexColor("#BFC9CA"), borderStyle='solid')
    sidebar_section_style = ParagraphStyle('SideSection', parent=styles['Heading2'], fontSize=12, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor("#34495E"))
    body_style = styles['Normal']
    sidebar_style = ParagraphStyle('SideBody', parent=styles['Normal'], fontSize=9, leading=12)
    
    elements = []
    
    # Header
    elements.append(Paragraph(data.get("name", "Your Name").upper(), name_style))
    elements.append(Spacer(1, 20))
    
    # Build Sidebar items
    side_elements = []
    side_elements.append(Paragraph("<b>CONTACT</b>", sidebar_section_style))
    side_elements.append(Paragraph(data.get("email", ""), sidebar_style))
    side_elements.append(Paragraph(data.get("phone", ""), sidebar_style))
    side_elements.append(Spacer(1, 10))
    
    if data.get("skills"):
        side_elements.append(Paragraph("<b>SKILLS</b>", sidebar_section_style))
        for skill in data["skills"]:
            side_elements.append(Paragraph(f"• {skill}", sidebar_style))
        side_elements.append(Spacer(1, 10))
            
    if data.get("education"):
        side_elements.append(Paragraph("<b>EDUCATION</b>", sidebar_section_style))
        for edu in data["education"]:
            side_elements.append(Paragraph(f"<b>{edu.get('degree')}</b>", sidebar_style))
            side_elements.append(Paragraph(edu.get('institution', ''), sidebar_style))
            side_elements.append(Paragraph(f"<font color='#7F8C8D'>{edu.get('year')}</font>", sidebar_style))
            side_elements.append(Spacer(1, 6))

    # Build Main items
    main_elements = []
    if data.get("summary"):
        main_elements.append(Paragraph("PROFILE", section_style))
        main_elements.append(Paragraph(data["summary"], body_style))
        
    if data.get("experience"):
        main_elements.append(Paragraph("EXPERIENCE", section_style))
        for exp in data["experience"]:
            main_elements.append(Paragraph(f"<b>{exp.get('role')}</b> at {exp.get('company')} | <font color='#7F8C8D'>{exp.get('duration')}</font>", body_style))
            main_elements.append(Paragraph(exp.get('description', ''), body_style))
            main_elements.append(Spacer(1, 8))
            
    if data.get("projects"):
        main_elements.append(Paragraph("PROJECTS", section_style))
        for proj in data["projects"]:
            main_elements.append(Paragraph(f"<b>{proj.get('title')}</b>", body_style))
            if proj.get('technologies'):
                main_elements.append(Paragraph(f"<i>[{proj['technologies']}]</i>", ParagraphStyle('Tech', parent=body_style, fontSize=9, textColor=colors.HexColor("#7F8C8D"))))
            main_elements.append(Paragraph(proj.get('description', ''), body_style))
            main_elements.append(Spacer(1, 8))
            
    # Combine into a table for 2 columns
    col_widths = [160, 360]
    # We must wrap lists in lists for table rows
    table_data = [[side_elements, main_elements]]
    layout_table = Table(table_data, colWidths=col_widths)
    layout_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('RIGHTPADDING', (0,0), (0,0), 20),
        ('LEFTPADDING', (1,0), (1,0), 20),
        ('LINEAFTER', (0,0), (0,0), 1, colors.HexColor("#E5E7EB"))
    ]))
    
    elements.append(layout_table)
    doc.build(elements)

def _template_compact(data, buffer):
    """Compact Fresher: Condensed spacing to fit 1 page easily."""
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = get_base_styles()
    
    name_style = ParagraphStyle('Name', parent=styles['Heading1'], fontSize=18, spaceAfter=4, alignment=TA_CENTER, fontName='Helvetica-Bold')
    contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontSize=9, spaceAfter=12, alignment=TA_CENTER)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=11, spaceBefore=8, spaceAfter=4, fontName='Helvetica-Bold', borderPadding=1, borderType=2, borderColor=colors.black, borderStyle='solid')
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=11)
    
    elements = []
    
    elements.append(Paragraph(data.get("name", "Your Name").upper(), name_style))
    contact_info = f"{data.get('email', '')} | {data.get('phone', '')}"
    elements.append(Paragraph(contact_info, contact_style))
    
    if data.get("summary"):
        elements.append(Paragraph("SUMMARY", section_style))
        elements.append(Paragraph(data["summary"], body_style))
        
    if data.get("education"):
        elements.append(Paragraph("EDUCATION", section_style))
        for edu in data["education"]:
            elements.append(Paragraph(f"<b>{edu.get('degree')}</b>, {edu.get('institution')} ({edu.get('year')})", body_style))
            
    if data.get("skills"):
        elements.append(Paragraph("SKILLS", section_style))
        elements.append(Paragraph(", ".join(data["skills"]), body_style))
        
    if data.get("experience"):
        elements.append(Paragraph("EXPERIENCE", section_style))
        for exp in data["experience"]:
            elements.append(Paragraph(f"<b>{exp.get('role')}</b> - {exp.get('company')} | {exp.get('duration')}", body_style))
            elements.append(Paragraph(exp.get('description', ''), body_style))
            elements.append(Spacer(1, 4))
            
    if data.get("projects"):
        elements.append(Paragraph("PROJECTS", section_style))
        for proj in data["projects"]:
            elements.append(Paragraph(f"<b>{proj.get('title')}</b> ({proj.get('technologies', '')})", body_style))
            elements.append(Paragraph(proj.get('description', ''), body_style))
            elements.append(Spacer(1, 4))

    doc.build(elements)

def _template_classic(data, buffer):
    """Classic Corporate: Traditional serif fonts, formal structure."""
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=60, leftMargin=60, topMargin=60, bottomMargin=60)
    styles = get_base_styles()
    
    name_style = ParagraphStyle('Name', parent=styles['Heading1'], fontName='Times-Bold', fontSize=22, spaceAfter=8, alignment=TA_CENTER)
    contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, spaceAfter=20, alignment=TA_CENTER)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontName='Times-Bold', fontSize=13, spaceBefore=14, spaceAfter=6, borderPadding=2, borderType=2, borderColor=colors.black, borderStyle='solid')
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Times-Roman', fontSize=11, leading=14)
    italic_style = ParagraphStyle('Italic', parent=body_style, fontName='Times-Italic')
    
    elements = []
    
    elements.append(Paragraph(data.get("name", "Your Name"), name_style))
    contact_info = f"{data.get('email', '')} | {data.get('phone', '')}"
    elements.append(Paragraph(contact_info, contact_style))
    
    if data.get("summary"):
        elements.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
        elements.append(Paragraph(data["summary"], body_style))
        
    if data.get("experience"):
        elements.append(Paragraph("EXPERIENCE", section_style))
        for exp in data["experience"]:
            elements.append(Paragraph(f"<b>{exp.get('company')}</b> — {exp.get('role')}", body_style))
            elements.append(Paragraph(exp.get('duration', ''), italic_style))
            elements.append(Paragraph(exp.get('description', ''), body_style))
            elements.append(Spacer(1, 8))
            
    if data.get("education"):
        elements.append(Paragraph("EDUCATION", section_style))
        for edu in data["education"]:
            elements.append(Paragraph(f"<b>{edu.get('institution')}</b>", body_style))
            elements.append(Paragraph(f"{edu.get('degree')} - {edu.get('year')}", body_style))
            elements.append(Spacer(1, 6))
            
    if data.get("skills"):
        elements.append(Paragraph("SKILLS & EXPERTISE", section_style))
        elements.append(Paragraph(", ".join(data["skills"]), body_style))
        
    if data.get("projects"):
        elements.append(Paragraph("NOTABLE PROJECTS", section_style))
        for proj in data["projects"]:
            elements.append(Paragraph(f"<b>{proj.get('title')}</b>", body_style))
            elements.append(Paragraph(proj.get('description', ''), body_style))
            elements.append(Spacer(1, 6))

    doc.build(elements)


def generate_resume_pdf(data: dict, template_id: str = "modern") -> bytes:
    """
    Generates a professional PDF resume from the provided data using the specified template.
    Supported templates: 'modern', 'minimal', 'twocolumn', 'compact', 'classic'
    """
    buffer = BytesIO()
    
    if template_id == "minimal":
        _template_minimal(data, buffer)
    elif template_id == "twocolumn":
        _template_two_column(data, buffer)
    elif template_id == "compact":
        _template_compact(data, buffer)
    elif template_id == "classic":
        _template_classic(data, buffer)
    else:
        _template_modern(data, buffer)
        
    pdf_value = buffer.getvalue()
    buffer.close()
    return pdf_value
