import pdfkit
import markdown as md_converter
from pathlib import Path

def save_as_pdf(tutorial_text: str, filename: Path):
    # Convert markdown to HTML
    html_content = md_converter.markdown(
        tutorial_text,
        extensions=['fenced_code', 'tables', 'codehilite']
    )
    
    styled_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
            pre  {{ background: #f4f4f4; padding: 15px; border-radius: 5px; }}
            h1, h2, h3 {{ color: #2c3e50; }}
        </style>
    </head>
    <body>{html_content}</body>
    </html>
    """

    # Point to wkhtmltopdf install location
    config = pdfkit.configuration(
        wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    )
    
    save_path=Path(filename)
    save_path.mkdir(parents=True, exist_ok=True)
    repo_pdf=save_path/'repo.pdf'

    pdfkit.from_string(
    styled_html, 
    repo_pdf, 
    configuration=config,
    options={
        'encoding': 'UTF-8',
        'enable-local-file-access': None
    }
)
    print(f"Saved to {save_path}")