import sys
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import black
from datetime import datetime



# Define inch manually as 72 points
inch = 72

# Basically turns the csv into what it needs to be 
# Need to improve it but not entirely sure how

def clean_csv_data(csv):
    """
    Takes the default parq csv and returns the same file as a cleaned version
    param csv: name of csv file
    return: Same csvfile? (i forget how this shit works sometimes)
    """
    # Name	Age	Gender	Event city	Event date	Weight	Previous experience	Medical info 	Medical condition	Medical rejection

    # csvCleanColumns = ['Name', 'Date of birth', 'Gender', 'Event city', 'Event date', 'Weight', 'Previous experience', 'Medical info', 'Medical condition', 'Medical rejection']
    csvCleanColumns = ['Name', 'Date of birth', 'Gender', 'Event city', 'Event date', 'Weight', 'Previous experience', 'Medical details']
    # csvCleanColumns = ['Name','Event city', 'Weight', 'Previous experience', 'Medical info']

    # read csv
    parq = pd.read_csv(csv)

    # created new column name and combines fname and lname
    parq["Name"] = parq["First name"] + " " + parq["Last name"]

    # drops the first and last name columns
    parq.drop(columns=["First name", "Last name"], inplace=True)

    # column renaming options
    # columnMapping = { "Medical details":"Medical info" }
    columnMapping = { "Medical Conditions":"Medical info" }


    # function that renames the specified columns 
    parq.rename(columns=columnMapping, inplace=True ) 

    # variable is set equal to new temp csv
    parq_filtered = parq[csvCleanColumns]

    # saves csv
    parq_filtered.to_csv("cleaned_data.csv", index=False)
    # parq_filtered.to_csv("aspire-match-up-clean.csv", index=False)



def draw_wrapped_text(pdf, text, x, y, max_width, font_size, extra_space=5, line_spacing=12):
    """
    Draws wrapped text at a specific position on the PDF with extra space below the last line.
    
    :param pdf: The canvas object
    :param text: The text to be wrapped and drawn
    :param x: The x-coordinate for drawing text
    :param y: The y-coordinate for drawing text
    :param max_width: Maximum width of the text line
    :param font_size: Font size of the text
    :param extra_space: Extra space below the last line of text
    :param line_spacing: Space between lines of text
    :return: The updated y-coordinate after drawing the text
    """
    pdf.setFont("Helvetica", font_size)
    
    # Break text into lines that fit within max_width 

    lines = []
    words = text.split(' ')
    current_line = ''
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        text_width = pdf.stringWidth(test_line, "Helvetica", font_size)
        
        if text_width > max_width:
            # Add the current line to the lines list and start a new line
            if current_line:  # Avoid adding empty lines
                lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    
    if current_line:
        lines.append(current_line)
    
    # Draw each line and add extra space after the last line
    for i, line in enumerate(lines):
        pdf.drawString(x, y, line)
        y -= line_spacing  # Move to the next line position
        # Add extra space only after the last line of wrapped text
        if i == len(lines) - 1:
            y -= extra_space

    return y  # Return the updated y-coordinate




# Mainly for headers to draw a border around and behind the text
def draw_bold_highlighted_text(pdf, text, x, y, max_width, font_size, bg_gray=0.9, padding=5):
    """
    Draws bold text with a full-width grey background.
    
    :param pdf: The canvas object
    :param text: The text to be drawn
    :param x: X-coordinate
    :param y: Y-coordinate (baseline of text)
    :param max_width: Maximum width of the grey background
    :param font_size: Font size
    :param bg_gray: Background color (0 = black, 1 = white)
    :param padding: Padding around text
    :return: Updated y-coordinate after drawing text
    """
    
    # Set font and calculate text height
    pdf.setFont("Helvetica-Bold", font_size)
    text_height = font_size * 1.5  # Estimate text height (with line spacing)

    # Adjust Y position so the rectangle covers the text
    rect_y = y - padding - 2  # Move background up to align with text

    # Draw full-width grey background rectangle
    pdf.setFillGray(bg_gray)
    pdf.rect(x - padding, rect_y, max_width + 2 * padding, text_height, fill=1, stroke=0)

    # Reset text color to black and draw text on top
    pdf.setFillColor(black)
    pdf.drawString(x, y, text)

    return y - text_height - 5  # Return new y-position (leaves space after)



def create_pdf_from_csv(csv_filename, pdf_filename):
    """
    Creates PDF from given csv

    Parameters
    - csv_filename: name of the csv file
    - pdf_filename: name of the pdf file
    """

    # Get absoloute data points for each part so can allocate to different areas better


    df = pd.read_csv(csv_filename)

    # altering csv to better match PARQ
    df["Name"] = df["First name"] + " " + df["Last name"]
    df.drop(columns=["First name", "Last name"], inplace=True)
    col_name = df.pop("Name")
    df.insert(0, "Name", col_name)

    
    # Create a PDF document
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    
    
    # Define margins and font size
    margin = 1 * inch
    font_size = 12
    max_width = width - 2 * margin
    text_x = margin
    text_y_start = height - margin - 50
    
    # Process each row in the DataFrame
    for index, row in df.iterrows():

        pdf.drawInlineImage('static/ultra-events-white-bg.png', 430, 700, width=150,height=50)

        # This isn't the actual loop
        current_y = text_y_start

        # Add row number as title
        pdf.setFont("Helvetica-Bold", 16)
        
        # Calculate text width
        title_text = "Participant Information"
        text_width = pdf.stringWidth(title_text, "Helvetica-Bold", 16)
        
        # Calculate X position for center alignment
        center_x = (width - text_width) / 2
        
        # Draw centered title
        pdf.drawString(center_x, current_y, title_text)
        
        current_y -= font_size * 3  # Add space after title
        
        # Process each column - THE ACTUAL LOOP
        for column, value in row.items():   

            # Checks to see if any vals are blank or smthn
            if pd.isna(value):
                value = ""

            if column == "Name":
                pdf.setFont("Helvetica-Bold", 14)
                column = "Participant"
                # Prepare the text for the current column
                column_text = f"{column}: {value}"
                # Draw wrapped text with additional space and get updated y position
                # current_y = draw_wrapped_text(pdf, column_text, text_x, current_y, max_width, font_size+1, extra_space=10, line_spacing=font_size + 4)
                pdf.drawString(text_x, current_y, column_text)
                # Add extra space between columns
                current_y -= font_size * 1.5

            elif column == "Date of birth":
                column = "Age"
                # Define the birth date string
                birth_date_str = value  # Assuming MM/DD/YYYY format
                # Convert string to datetime object
                birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y")
                # Get today's date
                today = datetime.today()
                # Calculate age
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                #Reset the value to the new age value
                value = age
                # Prepare the text for the current column
                column_text = f"{column}: {value}"
                # Draw wrapped text with additional space and get updated y position
                current_y = draw_wrapped_text(pdf, column_text, text_x, current_y, max_width, font_size, extra_space=10, line_spacing=font_size + 4)
                # Add extra space between columns
                current_y -= font_size * -0.5

            elif column == "Previous experience":
                # Adds an extra space between larger column blocks
                current_y = draw_wrapped_text(pdf, "", text_x, current_y, max_width, font_size, extra_space=10, line_spacing=font_size + 4)
                current_y -= font_size * 1
                current_y = draw_bold_highlighted_text(pdf, "Previous Experience", text_x, current_y, max_width, 13, bg_gray=0.9, padding=3) 
                current_y -= font_size * 0.5
                current_y = draw_wrapped_text(pdf, value, text_x, current_y, max_width, font_size, extra_space=10, line_spacing=font_size + 4)
                # current_y -= font_size * 0.5

            # elif column == "Medical info ":
            elif column == "Medical details":                
                current_y = draw_wrapped_text(pdf, "", text_x, current_y, max_width, font_size, extra_space=10, line_spacing=font_size + 4)
                current_y -= font_size * 0.5
                current_y = draw_bold_highlighted_text(pdf, "Medical information", text_x, current_y, max_width, 13, bg_gray=0.9, padding=3) 
                current_y -= font_size * 0.5
                current_y = draw_wrapped_text(pdf, value, text_x, current_y, max_width, font_size, extra_space=10, line_spacing=font_size + 4)
                # current_y -= font_size * 0.5

            else:
                # Prepare the text for the current column
                column_text = f"{column}: {value}"
                # Draw wrapped text with additional space and get updated y position
                current_y = draw_wrapped_text(pdf, column_text, text_x, current_y, max_width, font_size, extra_space=10, line_spacing=font_size + 4)
                # Add extra space between columns
                current_y -= font_size * -0.5

        
        # Two final lines for scoring and additional comments
        pdf.setFont("Helvetica", font_size)
        # Add a scoring section after the initial spreadsheet
        current_y -= font_size * 2
        # current_y = draw_wrapped_text(pdf, "Scoring:", text_x, current_y, max_width, font_size, extra_space=10, line_spacing=font_size + 4)
        current_y = draw_bold_highlighted_text(pdf, "Scoring", text_x, current_y, max_width, 13, bg_gray=0.9, padding=3)


        # Add a comments area at the end of the page
        comments = "Additional Comments"
        current_y -= font_size * 4.5  # Ensure there's space before adding comments
        # current_y = draw_wrapped_text(pdf, comments, text_x, current_y, max_width, font_size, extra_space=10, line_spacing=font_size + 4)
        current_y = draw_bold_highlighted_text(pdf, comments, text_x, current_y, max_width, 13, bg_gray=0.9, padding=3) 
        
        
        # Finish the current page
        pdf.showPage()
    
    # Save the PDF
    pdf.save()


# CSV to pdf fields that are checked   
# Name
# Date of birth
# Previous experience
# Medical info 



# clean_csv_data('manchester-mma-2025-parq-info.csv')
# clean_csv_data('aspire-match-up.csv')
# clean_csv_data('salford-match-up-sheets.csv')

# base function for testing
# create_pdf_from_csv('chester-sheet.csv', 'chester-sheet.pdf')
# create_pdf_from_csv('salford-match-up-sheets.csv', 'salford-match-up-sheets.pdf')