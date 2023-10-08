import pandas as pd
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Load questions from the selected sheet in the Excel file
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

class QuestionApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Random Question")
        self.root.attributes("-zoomed", True)

        self.original_questions = []
        self.original_answers = []
        self.questions = []
        self.answers = []
        self.current_question_index = -1
        self.remaining_label = tk.Label(root, text="", font=("Ubuntu Mono", 14))
        self.remaining_label.pack()
        self.question_display = tk.Label(root, text=""":::: Interview Preparation ::::
 \U0001F60E""", font=("Ubuntu Mono", 24), wraplength=900)
        self.question_display.pack(expand=True)

        button_frame = tk.Frame(root)
        button_frame.pack()

        # Upload File button
        self.upload_file_button = tk.Button(
            button_frame,
            text="Upload File",
            command=self.upload_and_populate_sheets,  # Updated command
            font=("Ubuntu Mono", 18)
        )
        self.upload_file_button.pack(side="left")

        # Dropdown menu to select the sheet
        self.sheet_var = tk.StringVar()
        self.sheet_dropdown = ttk.Combobox(
            button_frame,
            textvariable=self.sheet_var,
            values=[],
            state='readonly'
        )
        self.sheet_dropdown.pack(side="left")

        # Select Sheet button
        self.select_sheet_button = tk.Button(
            button_frame,
            text="Select Sheet",
            command=self.load_questions_from_selected_sheet,  # New method for selecting and loading sheet
            font=("Ubuntu Mono", 18)
        )
        self.select_sheet_button.pack(side="left")

        # Next Question
        self.next_button = tk.Button(
            button_frame,
            text="Next Question",
            command=self.next_question,
            font=("Ubuntu Mono", 18),
            bg="#FF5733"
        )
        self.next_button.pack(side="left")

        # Show Answer
        self.show_answer_button = tk.Button(
            button_frame,
            text="Show Answer",
            command=self.show_answer,
            font=("Ubuntu Mono", 18),
            bg="#7AB7F5"
        )
        self.show_answer_button.pack(side="left")

        # Reset
        self.reset_button = tk.Button(
            button_frame, text="Reset", command=self.reset, font=("Ubuntu Mono", 18)
        )
        self.reset_button.pack(side="left")

        # Instructions
        self.instructions_button = tk.Button(
            button_frame, text="Instructions", command=self.display_instructions,
            font=("Ubuntu Mono", 18)
        )
        self.instructions_button.pack(side="left")

        # About
        self.about_button = tk.Button(
            button_frame, text="About", command=self.about_content,
            font=("Ubuntu Mono", 18)
        )
        self.about_button.pack(side="left")

        self.answer_display = tk.Label(root, text="", font=("Ubuntu Mono", 18), wraplength=900)
        self.answer_display.pack(expand=True)

    def upload_and_populate_sheets(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])

        if self.file_path:
            excel_file = pd.ExcelFile(self.file_path)
            self.sheet_dropdown['values'] = excel_file.sheet_names
            self.sheet_var.set("")  # Clear the selected sheet
            self.original_questions = []
            self.original_answers = []
            self.questions = []
            self.answers = []
            self.current_question_index = -1
            self.display_question()
        else:
            messagebox.showinfo("Alert", "Please upload an Excel file.")

    def about_content(self):
        aboutt = """
         About This Tool:
         This tool is designed to help you prepare for interviews by providing a random selection of questions and answers.
         Simply upload an Excel sheet with questions and answers, and start practicing!

         Enjoy your interview preparation!
         Github Link = https://github.com/mechtester/Random-Question-Generator
         ** Created By :: Vigneshkumar **
         """
        messagebox.showinfo("About", aboutt)

    def display_instructions(self):
        instructions = """
        Instructions:
        * Uploaded Excel sheet First column for S.No
        * Second column for questions.
        * Third column for answers.

        Enjoy your interview preparation!
        """
        messagebox.showinfo("Instructions", instructions)

    def load_questions_from_selected_sheet(self):
        selected_sheet = self.sheet_var.get()

        if not selected_sheet:
            messagebox.showinfo("Alert", "Please select a sheet name.")
            return

        if not self.file_path:
            messagebox.showinfo("Alert", "Please upload an Excel file first.")
            return

        # Use the selected sheet name to load questions from the existing Excel file
        self.original_questions, self.original_answers = load_questions_from_sheet(self.file_path, selected_sheet)

        if self.original_questions:
            self.answers = []  # Reset the answers list
            self.answer_display.config(text="")  # Clear the answer display
            self.shuffle_questions_and_answers()
            self.current_question_index = -1
            self.display_question()
        else:
            messagebox.showinfo("Alert", "No questions found in the selected sheet.")

    def shuffle_questions_and_answers(self):
        # Shuffle the questions and answers while maintaining their correspondence
        combined = list(zip(self.original_questions, self.original_answers))
        random.shuffle(combined)
        self.questions, self.answers = zip(*combined)

    def update_remaining_label(self):
        remaining_count = len(self.questions) - self.current_question_index
        self.remaining_label.config(text=f"Remaining Questions: {remaining_count}")

    def display_question(self):
        if self.questions:
            if self.current_question_index == -1:
                # Start with the first question
                self.current_question_index = 0
            random_question = self.questions[self.current_question_index]
            self.question_display.config(text=random_question)
            self.update_remaining_label()

    def next_question(self):
        if not self.questions:
            messagebox.showinfo("Alert", "Please upload a question file.")
            return

        if self.current_question_index < len(self.questions) - 1:
            # Move to the next question
            self.current_question_index += 1

            # Update the displayed question
            random_question = self.questions[self.current_question_index]
            self.question_display.config(text=random_question)
            self.update_remaining_label()

            # Clear the answer display
            self.answer_display.config(text="")

    def reset(self):
        if not self.questions:
            messagebox.showinfo("Alert", "Please upload a question file.")
            return

        # Shuffle the questions and answers again
        self.shuffle_questions_and_answers()

        # Reset the current question index to start from the beginning
        self.current_question_index = -1

        # Clear the displayed question and answer
        self.question_display.config(text="")
        self.answer_display.config(text="")
        self.update_remaining_label()

        # Display a random question
        self.next_question()

    def show_answer(self):
        if not self.questions:
            messagebox.showinfo("Alert", "Please upload a question file.")
            return

        if self.current_question_index >= 0 and self.current_question_index < len(self.answers):
            # Display the answer for the current question
            answer = self.answers[self.current_question_index]
            self.answer_display.config(text=answer)
        else:
            messagebox.showinfo("Alert", "No answer available for the current question.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionApp(root)
    root.mainloop()
