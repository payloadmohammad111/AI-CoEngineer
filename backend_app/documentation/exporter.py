"""
Module: exporter
Provides functions to export generated documents (SRS, design docs, test plans, etc.)
"""


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_to_pdf(content: str, filename: str) -> None:
    """
    Export the given content to a PDF file.

    Args:
        content (str): The content to export.
        filename (str): The name of the output PDF file.

    Returns:
        None
    """
    try:
        # Create a canvas for the PDF
        pdf_canvas = canvas.Canvas(filename, pagesize=letter)
        
        # Set the starting position for the text
        text_object = pdf_canvas.beginText(50, 750)  # 50 points from the left, 750 points from the bottom
        
        # Add the content to the text object
        for line in content.split('\n'):
            text_object.textLine(line)
        
        # Draw the text object onto the canvas
        pdf_canvas.drawText(text_object)
        
        # Save the PDF file
        pdf_canvas.save()
        print(f"PDF file '{filename}' has been successfully created.")
    except Exception as e:
        print(f"An error occurred while exporting to PDF: {e}")


from docx import Document

def export_to_docx(content: str, filename: str) -> None:
    """
    Export the given content to a DOCX file.

    Args:
        content (str): The content to export.
        filename (str): The name of the output DOCX file.

    Returns:
        None
    """
    try:
        # Create a new Document
        doc = Document()
        
        # Add content to the document
        doc.add_paragraph(content)
        
        # Save the document to the specified filename
        doc.save(filename)
        print(f"DOCX file '{filename}' has been successfully created.")
    except Exception as e:
        print(f"An error occurred while exporting to DOCX: {e}")


def export_to_markdown(content: str, filename: str) -> None:
    """
    Export the given content to a Markdown file.

    Args:
        content (str): The content to export.
        filename (str): The name of the output Markdown file.

    Returns:
        None
    """
    try:
        with open(filename, 'w', encoding='utf-8') as markdown_file:
            markdown_file.write(content)
        print(f"Markdown file '{filename}' has been successfully created.")
    except Exception as e:
        print(f"An error occurred while exporting to Markdown: {e}")
