import os
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from io import BytesIO

# Setup Jinja2 Environment pointing to the templates folder
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def format_resume_data(raw_data: dict) -> dict:
    """
    Ensures resume data follows a consistent structure.
    """
    return {
        "name": raw_data.get("name", "N/A"),
        "title": raw_data.get("title", ""),
        "email": raw_data.get("email", "N/A"),
        "phone": raw_data.get("phone", "N/A"),
        "linkedin": raw_data.get("linkedin", ""),
        "github": raw_data.get("github", ""),
        "summary": raw_data.get("summary", ""),
        "education": raw_data.get("education", []),
        "skills": raw_data.get("skills", []),
        "experience": raw_data.get("experience", []),
        "projects": raw_data.get("projects", []),
        "internships": raw_data.get("internships", []),
        "certifications": raw_data.get("certifications", [])
    }

def generate_resume_html(data: dict, template_id: str = "modern") -> str:
    """
    Renders the Jinja2 template with the given data and returns the HTML string.
    """
    template_filename = f"{template_id}.html"
    try:
        template = env.get_template(template_filename)
    except Exception:
        # Fallback if invalid template_id
        template = env.get_template("modern.html")
        
    formatted_data = format_resume_data(data)
    rendered_html = template.render(**formatted_data)
    return rendered_html

def create_resume_file(data: dict, template_id: str = "modern") -> bytes:
    """
    Generates the PDF bytes for a resume from the HTML template using xhtml2pdf.
    """
    html_content = generate_resume_html(data, template_id)
    pdf_buffer = BytesIO()
    
    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        src=html_content,
        dest=pdf_buffer,
        encoding='utf-8'
    )
    
    if pisa_status.err:
        raise Exception("Failed to generate PDF from HTML")
        
    return pdf_buffer.getvalue()
