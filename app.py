import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


DATA_FILE = "quizzes.json"


def load_quizzes():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except:
        return {}


def save_quizzes(quizzes):
    with open(DATA_FILE, "w") as file:
        json.dump(quizzes, file, indent=4)


quizzes = load_quizzes()


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Quiz Platform")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.current_quiz = None
        self.current_question = 0
        self.score = 0
        self.selected_answer = tk.StringVar()

        self.show_home()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_screen()

        title = tk.Label(
            self.root,
            text="Online Quiz Platform",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=50)

        subtitle = tk.Label(
            self.root,
            text="Create, customize and take quizzes",
            font=("Arial", 15)
        )
        subtitle.pack(pady=10)

        tk.Button(
            self.root,
            text="Take Quiz",
            font=("Arial", 14),
            width=20,
            command=self.select_quiz
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Create Quiz",
            font=("Arial", 14),
            width=20,
            command=self.create_quiz
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Exit",
            font=("Arial", 14),
            width=20,
            command=self.root.destroy
        ).pack(pady=10)

    def select_quiz(self):
        self.clear_screen()

        tk.Label(
            self.root,
            text="Select a Quiz",
            font=("Arial", 24, "bold")
        ).pack(pady=40)

        if not quizzes:
            tk.Label(
                self.root,
                text="No quizzes available. Create a quiz first.",
                font=("Arial", 14)
            ).pack(pady=20)

            tk.Button(
                self.root,
                text="Create Quiz",
                font=("Arial", 13),
                command=self.create_quiz
            ).pack(pady=10)

            tk.Button(
                self.root,
                text="Back",
                font=("Arial", 13),
                command=self.show_home
            ).pack(pady=10)

            return

        self.quiz_choice = ttk.Combobox(
            self.root,
            values=list(quizzes.keys()),
            state="readonly",
            font=("Arial", 13),
            width=30
        )
        self.quiz_choice.pack(pady=20)

        tk.Button(
            self.root,
            text="Start Quiz",
            font=("Arial", 13),
            width=18,
            command=self.start_quiz
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 13),
            width=18,
            command=self.show_home
        ).pack(pady=10)

    def start_quiz(self):
        selected = self.quiz_choice.get()

        if not selected:
            messagebox.showwarning("Select Quiz", "Please select a quiz.")
            return

        self.current_quiz = selected
        self.current_question = 0
        self.score = 0

        self.show_question()

    def show_question(self):
        self.clear_screen()

        questions = quizzes[self.current_quiz]

        if self.current_question >= len(questions):
            self.show_result()
            return

        question = questions[self.current_question]

        tk.Label(
            self.root,
            text=self.current_quiz,
            font=("Arial", 24, "bold")
        ).pack(pady=25)

        tk.Label(
            self.root,
            text=f"Question {self.current_question + 1} of {len(questions)}",
            font=("Arial", 13)
        ).pack(pady=5)

        tk.Label(
            self.root,
            text=question["question"],
            font=("Arial", 18, "bold"),
            wraplength=750
        ).pack(pady=30)

        self.selected_answer.set("")

        for option in question["options"]:
            tk.Radiobutton(
                self.root,
                text=option,
                variable=self.selected_answer,
                value=option,
                font=("Arial", 14),
                anchor="w",
                width=40
            ).pack(pady=6)

        tk.Button(
            self.root,
            text="Next",
            font=("Arial", 13),
            width=18,
            command=self.next_question
        ).pack(pady=30)

    def next_question(self):
        answer = self.selected_answer.get()

        if not answer:
            messagebox.showwarning(
                "Select Answer",
                "Please select an answer before continuing."
            )
            return

        question = quizzes[self.current_quiz][self.current_question]

        if answer == question["correct"]:
            self.score += 1

        self.current_question += 1
        self.show_question()

    def show_result(self):
        self.clear_screen()

        total = len(quizzes[self.current_quiz])
        percentage = (self.score / total) * 100

        tk.Label(
            self.root,
            text="Quiz Completed!",
            font=("Arial", 28, "bold")
        ).pack(pady=50)

        tk.Label(
            self.root,
            text=f"Quiz: {self.current_quiz}",
            font=("Arial", 17)
        ).pack(pady=10)

        tk.Label(
            self.root,
            text=f"Score: {self.score} / {total}",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        tk.Label(
            self.root,
            text=f"Percentage: {percentage:.1f}%",
            font=("Arial", 18)
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Take Another Quiz",
            font=("Arial", 13),
            width=20,
            command=self.select_quiz
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Home",
            font=("Arial", 13),
            width=20,
            command=self.show_home
        ).pack(pady=10)

    def create_quiz(self):
        self.clear_screen()

        self.new_questions = []

        tk.Label(
            self.root,
            text="Create Your Quiz",
            font=("Arial", 24, "bold")
        ).pack(pady=25)

        tk.Label(
            self.root,
            text="Quiz Name",
            font=("Arial", 13)
        ).pack()

        self.quiz_name_entry = tk.Entry(
            self.root,
            font=("Arial", 13),
            width=40
        )
        self.quiz_name_entry.pack(pady=8)

        tk.Label(
            self.root,
            text="Question",
            font=("Arial", 13)
        ).pack(pady=(15, 0))

        self.question_entry = tk.Entry(
            self.root,
            font=("Arial", 13),
            width=70
        )
        self.question_entry.pack(pady=8)

        self.option_entries = []

        for i in range(4):
            tk.Label(
                self.root,
                text=f"Option {i + 1}",
                font=("Arial", 12)
            ).pack()

            entry = tk.Entry(
                self.root,
                font=("Arial", 12),
                width=60
            )
            entry.pack(pady=4)

            self.option_entries.append(entry)

        tk.Label(
            self.root,
            text="Correct Answer",
            font=("Arial", 12)
        ).pack(pady=(12, 0))

        self.correct_choice = ttk.Combobox(
            self.root,
            values=["Option 1", "Option 2", "Option 3", "Option 4"],
            state="readonly",
            font=("Arial", 12),
            width=18
        )
        self.correct_choice.pack(pady=8)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Add Question",
            font=("Arial", 12),
            width=15,
            command=self.add_question
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            button_frame,
            text="Save Quiz",
            font=("Arial", 12),
            width=15,
            command=self.save_quiz
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            button_frame,
            text="Back",
            font=("Arial", 12),
            width=15,
            command=self.show_home
        ).grid(row=0, column=2, padx=8)

        self.question_count_label = tk.Label(
            self.root,
            text="Questions added: 0",
            font=("Arial", 12)
        )
        self.question_count_label.pack()

    def add_question(self):
        quiz_name = self.quiz_name_entry.get().strip()
        question = self.question_entry.get().strip()
        options = [entry.get().strip() for entry in self.option_entries]
        correct = self.correct_choice.get()

        if not quiz_name:
            messagebox.showwarning(
                "Missing Quiz Name",
                "Please enter a quiz name."
            )
            return

        if not question:
            messagebox.showwarning(
                "Missing Question",
                "Please enter a question."
            )
            return

        if any(not option for option in options):
            messagebox.showwarning(
                "Missing Option",
                "Please fill all four options."
            )
            return

        if not correct:
            messagebox.showwarning(
                "Missing Answer",
                "Please select the correct answer."
            )
            return

        correct_index = int(correct.split()[-1]) - 1

        question_data = {
            "question": question,
            "options": options,
            "correct": options[correct_index]
        }

        self.new_questions.append(question_data)

        self.question_entry.delete(0, tk.END)

        for entry in self.option_entries:
            entry.delete(0, tk.END)

        self.correct_choice.set("")

        self.question_count_label.config(
            text=f"Questions added: {len(self.new_questions)}"
        )

        messagebox.showinfo(
            "Question Added",
            "Question added successfully."
        )

    def save_quiz(self):
        quiz_name = self.quiz_name_entry.get().strip()

        if not quiz_name:
            messagebox.showwarning(
                "Missing Quiz Name",
                "Please enter a quiz name."
            )
            return

        if not self.new_questions:
            messagebox.showwarning(
                "No Questions",
                "Please add at least one question."
            )
            return

        if quiz_name in quizzes:
            result = messagebox.askyesno(
                "Quiz Exists",
                "A quiz with this name already exists. Replace it?"
            )

            if not result:
                return

        quizzes[quiz_name] = self.new_questions
        save_quizzes(quizzes)

        messagebox.showinfo(
            "Quiz Saved",
            f"'{quiz_name}' saved successfully."
        )

        self.show_home()


root = tk.Tk()
app = QuizApp(root)
root.mainloop()