import json
import os
import traceback

import PyPDF2


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            traceback.print_exc()
            raise Exception(f"Error reading the PDF file: {e}")

    elif file.name.endswith(".txt"):
        try:
            return file.read().decode("utf-8")
        except Exception as e:
            traceback.print_exc()
            raise Exception(f"Error reading the text file: {e}")
    else:
        raise Exception("Unsupported file format, only PDF and text files are supported.")

def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        for key, value in quiz_dict.items():
            # Check if the required keys ('mcq', 'options', 'correct') are in the quiz item
            if 'mcq' not in value or 'options' not in value or 'correct' not in value:
                raise KeyError(f"Missing key in quiz item: {key}. Required keys are 'mcq', 'options', and 'correct'.")
            
            question = value["mcq"]
            options_dict = value["options"]
            correct_option = value["correct"]
            
            # Format the options for display
            formatted_options = " || ".join([f"{opt_key}: {opt_val}" for opt_key, opt_val in options_dict.items()])
            
            # Append the data for this question to the quiz table data list
            quiz_table_data.append({
                "Question ID": key,
                "Question": question,
                "Options": formatted_options,
                "Correct Option": correct_option
            })
        return quiz_table_data
    except json.JSONDecodeError as e:
        traceback.print_exc()
        raise Exception(f"Error parsing quiz data as JSON: {e}")
    except KeyError as e:
        traceback.print_exc()
        raise Exception(f"Data format error: {e}")
    except Exception as e:
        traceback.print_exc()
        raise Exception(f"Unexpected error processing quiz data: {e}")
