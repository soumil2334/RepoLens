import markdown
from weasyprint import HTML

def save_as_pdf(tutorial_text: str, filename: str):
    # Convert markdown to HTML first
    html_content = markdown.markdown(
        tutorial_text,
        extensions=['fenced_code', 'tables', 'codehilite']
    )
    
    # Wrap in basic styled HTML
    styled_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
            pre  {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
            h1, h2, h3 {{ color: #2c3e50; }}
        </style>
    </head>
    <body>{html_content}</body>
    </html>
    """
    
    HTML(string=styled_html).write_pdf(filename)
    print(f"Saved to {filename}")
