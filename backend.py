# import fitz  # PyMuPDF
# import os
# from datetime import datetime
# # from markdownify import markdownify as md


# def encapsulate_in_shell(text):
#     # Use triple backticks with the shell keyword to encapsulate the text
#     encapsulated_text = f"```\n{text}\n```"
#     return encapsulated_text

# def get_file_content(info: dict):
#     # Hardcoded base folder path
#     base_folder = r"C:\Users\rotesh kumar\Desktop\sc court\Database"
    
#     # Extracting information from the input dictionary
#     diary_no = info['diary_no']
#     year = info['year']
#     doc_type = info['doc_type']
#     date = info['date']

#     # Convert the user-provided date (DD/MM/YYYY) to the document date format (DD-Mon-YYYY)
#     try:
#         date_object = datetime.strptime(date, "%d/%m/%Y")
#         formatted_date = date_object.strftime("%d-%b-%Y")
#     except ValueError:
#         if  doc_type == "case_status" or "judgement":
#             pass
#         else:
#             return "Invalid date format provided."

#     # Setting up the base directory structure
#     year_folder = os.path.join(base_folder, str(year))
#     diary_folder = os.path.join(year_folder, str(diary_no))

#     # Naming the file based on document type and formatted date
#     if doc_type == "daily_order":
#         file_name = f"Order_{formatted_date}.pdf"
#     elif doc_type == "judgement":
#         file_name = f"Judgement.pdf"
#     elif doc_type == "case_status":
#         file_name = "status.pdf"
#     elif doc_type == "office_report":
#         file_name = f"Report_{formatted_date}.pdf"
#     else:
#         return "Invalid document type specified."

#     # Construct the full file path
#     file_path = os.path.join(diary_folder, file_name)

#     # Check if the file exists
#     if not os.path.exists(file_path):
#         return "File does not exist for this case."

#     # Extract text from the PDF
#     try:
#         doc = fitz.open(file_path)
#         text = ""
#         for page in doc:
#             text += page.get_text()
#         doc.close()
#         # markdown = convert_to_markdown(text)
#         markdown = encapsulate_in_shell(text)
#         return markdown
#     except Exception as e:
#         return f"An error occurred while extracting text: {str(e)}"


import fitz  # PyMuPDF
import os
from datetime import datetime

def encapsulate_in_shell(text):
    # Use triple backticks with the shell keyword to encapsulate the text
    encapsulated_text = f"```\n{text}\n```"
    return encapsulated_text

def get_file_content(info: dict):
    # Hardcoded base folder path
    base_folder = "database"
    
    # Extracting information from the input dictionary
    diary_no = info['diary_no']
    year = info['year']
    doc_type = info['doc_type']
    date = info['date']

    # Setting up the base directory structure
    year_folder = os.path.join(base_folder, str(year))
    diary_folder = os.path.join(year_folder, str(diary_no))
    
    # Check if the folder exists
    if not os.path.exists(diary_folder):
        return "No documents found for the specified diary number and year."

    # Handle document type specific logic
    if doc_type == "daily_order" or doc_type == "office_report":
        # If a date is provided, convert it to the correct format
        if date!='00/00/0000':
            try:
                date_object = datetime.strptime(date, "%d/%m/%Y")
                formatted_date = date_object.strftime("%d-%b-%Y")
            except ValueError:
                return "Invalid date format provided."

            # Naming the file based on document type and formatted date
            if doc_type == "daily_order":
                file_name = f"Order_{formatted_date}.pdf"
            else:  # office_report
                file_name = f"Report_{formatted_date}.pdf"
            
            # Construct the full file path
            file_path = os.path.join(diary_folder, file_name)

            # Check if the file exists and return its content
            if os.path.exists(file_path):
                return extract_pdf_content(file_path)
            else:
                return f"File for {formatted_date} does not exist. Available dates are: {list_available_dates(diary_folder, doc_type)}"
        else:
            return f"No date provided. Available dates are: {list_available_dates(diary_folder, doc_type)}"
    elif doc_type == "judgement":
        file_name = "Judgement.pdf"
    elif doc_type == "case_status":
        file_name = "status.pdf"
    else:
        return "Invalid document type specified."

    # Construct the full file path for judgement or case_status
    file_path = os.path.join(diary_folder, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        return "File does not exist for this case."

    # Extract text from the PDF
    return extract_pdf_content(file_path)

def extract_pdf_content(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        markdown = encapsulate_in_shell(text)
        return markdown
    except Exception as e:
        return f"An error occurred while extracting text: {str(e)}"

def list_available_dates(folder_path, doc_type):
    available_dates = []
    for file in os.listdir(folder_path):
        if doc_type == "daily_order" and file.startswith("Order_"):
            date_str = file.split("_")[1].replace(".pdf", "")
            available_dates.append(date_str)
        elif doc_type == "office_report" and file.startswith("Report_"):
            date_str = file.split("_")[1].replace(".pdf", "")
            available_dates.append(date_str)
    return ", ".join(available_dates)
