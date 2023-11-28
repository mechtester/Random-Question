import pandas as pd
import random

def load_questions_from_sheet(file_path, selected_sheet):
    try:
        df = pd.read_excel(file_path, sheet_name=selected_sheet)
        s_no = df.iloc[:, 0].tolist()
        questions = df.iloc[:, 1].tolist()
        answers = df.iloc[:, 2].tolist()

        # Create a list of shuffled indices based on S.No
        shuffled_indices = sorted(range(len(s_no)), key=lambda k: s_no[k])

        # Use shuffled indices to get shuffled questions and answers
        shuffled_questions = [questions[i] for i in shuffled_indices]
        shuffled_answers = [answers[i] for i in shuffled_indices]

        return shuffled_questions, shuffled_answers
    except Exception as e:
        print(f"Error loading questions and answers from Excel: {str(e)}")
        return [], []
