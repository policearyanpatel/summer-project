import customtkinter as ctk
import random
from tkinter import messagebox
import os

# -----------------------------
# APP SETTINGS
# -----------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

HIGH_SCORE_FILE = "highscore.txt"


# -----------------------------
# HIGH SCORE FUNCTIONS
# -----------------------------

def load_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write("0")

    with open(HIGH_SCORE_FILE, "r") as file:
        return int(file.read())


def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


# -----------------------------
# MAIN GAME CLASS
# -----------------------------

class NumberGuessMaster:

    def __init__(self, root):

        self.root = root
        self.root.title("🎯 Number Guess Master Pro")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        self.high_score = load_high_score()

        self.secret_number = 0
        self.max_number = 100
        self.max_attempts = 7
        self.attempts_used = 0
        self.score = 100
        self.guess_history = []

        self.build_ui()
        self.start_new_game()


    # -----------------------------
    # UI DESIGN
    # -----------------------------

    def build_ui(self):

        self.title_label = ctk.CTkLabel(
            self.root,
            text="🎯 NUMBER GUESS MASTER PRO 🎯",
            font=("Arial", 32, "bold"),
            text_color="#FFD700"
        )
        
        self.title_label.pack(pady=20)

        self.top_frame = ctk.CTkFrame(self.root)
        self.top_frame.pack(fill="x", padx=20)

        self.left_panel = ctk.CTkFrame(
            self.top_frame,
            width=300
        )
        self.left_panel.pack(side="left", padx=10, pady=10)

        self.right_panel = ctk.CTkFrame(
            self.top_frame,
            width=600
        )
        self.right_panel.pack(side="right", padx=10, pady=10)

        # -------------------------
        # PLAYER STATS
        # -------------------------

        self.stats_title = ctk.CTkLabel(
            self.left_panel,
            text="🏆 PLAYER STATS",
            font=("Arial", 20, "bold")
        )
        self.stats_title.pack(pady=10)

        self.score_label = ctk.CTkLabel(
            self.left_panel,
            text="⭐ Score: 100",
            font=("Arial", 16)
        )
        self.score_label.pack(pady=5)

        self.rank_label = ctk.CTkLabel(
            self.left_panel,
            text="🥉 Rank: Beginner",
            font=("Arial", 16)
        )
        self.rank_label.pack(pady=5)

        self.high_score_label = ctk.CTkLabel(
            self.left_panel,
            text=f"🏆 High Score: {self.high_score}",
            font=("Arial", 16)
        )
        self.high_score_label.pack(pady=5)

        self.attempt_label = ctk.CTkLabel(
            self.left_panel,
            text="❤️ Attempts Left: 7",
            font=("Arial", 16)
        )
        self.attempt_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(
            self.left_panel,
            width=250
        )
        self.progress_bar.pack(pady=15)

        self.progress_bar.set(1)

        # -------------------------
        # GUESS HISTORY
        # -------------------------

        self.history_title = ctk.CTkLabel(
            self.left_panel,
            text="📜 Guess History",
            font=("Arial", 18, "bold")
        )
        self.history_title.pack(pady=10)

        self.history_box = ctk.CTkTextbox(
            self.left_panel,
            width=250,
            height=180
        )
        self.history_box.pack(pady=10)

        # -------------------------
        # GAME AREA
        # -------------------------

        self.game_title = ctk.CTkLabel(
            self.right_panel,
            text="🎮 Game Dashboard",
            font=("Arial", 24, "bold")
        )
        self.game_title.pack(pady=20)

        self.difficulty_menu = ctk.CTkOptionMenu(
            self.right_panel,
            values=["Easy", "Medium", "Hard"]
        )
        self.difficulty_menu.pack(pady=10)

        self.start_button = ctk.CTkButton(
            self.right_panel,
            text="🚀 Start New Game",
            command=self.start_new_game
        )
        self.start_button.pack(pady=10)

        self.guess_entry = ctk.CTkEntry(
            self.right_panel,
            width=250,
            placeholder_text="Enter your guess"
        )
        self.guess_entry.pack(pady=20)

        self.submit_button = ctk.CTkButton(
            self.right_panel,
            text="🎯 Submit Guess",
            command=self.check_guess
        )
        self.submit_button.pack(pady=10)

        self.hint_label = ctk.CTkLabel(
            self.right_panel,
            text="💡 Hints will appear here",
            font=("Arial", 18)
        )
        self.hint_label.pack(pady=30)

        self.result_label = ctk.CTkLabel(
            self.right_panel,
            text="",
            font=("Arial", 22, "bold")
        )
        self.result_label.pack(pady=20)
            # -----------------------------
    # START NEW GAME
    # -----------------------------

    def start_new_game(self):

        difficulty = self.difficulty_menu.get()

        if difficulty == "Easy":
            self.max_number = 50
            self.max_attempts = 10

        elif difficulty == "Medium":
            self.max_number = 100
            self.max_attempts = 7

        else:
            self.max_number = 200
            self.max_attempts = 5

        self.secret_number = random.randint(
            1,
            self.max_number
        )

        self.attempts_used = 0
        self.score = 100
        self.guess_history = []

        self.progress_bar.set(1)

        self.history_box.delete(
            "1.0",
            "end"
        )

        self.result_label.configure(
            text=""
        )

        self.hint_label.configure(
            text=f"🎯 Guess a number between 1 and {self.max_number}"
        )

        self.score_label.configure(
            text="⭐ Score: 100"
        )

        self.rank_label.configure(
            text="🥉 Rank: Beginner"
        )

        self.attempt_label.configure(
            text=f"❤️ Attempts Left: {self.max_attempts}"
        )

        self.guess_entry.delete(
            0,
            "end"
        )


    # -----------------------------
    # RANK SYSTEM
    # -----------------------------

    def get_rank(self):

        if self.attempts_used == 1:
            return "Legendary 🏆"

        elif self.attempts_used <= 3:
            return "Expert 🥇"

        elif self.attempts_used <= 5:
            return "Pro 🥈"

        else:
            return "Beginner 🥉"


    # -----------------------------
    # MAIN GAME LOGIC
    # -----------------------------

    def check_guess(self):

        try:

            guess = int(
                self.guess_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid number."
            )

            return

        self.attempts_used += 1

        self.guess_history.append(
            str(guess)
        )

        self.history_box.delete(
            "1.0",
            "end"
        )

        self.history_box.insert(
            "end",
            "\n".join(self.guess_history)
        )

        attempts_left = (
            self.max_attempts
            - self.attempts_used
        )

        self.attempt_label.configure(
            text=f"❤️ Attempts Left: {attempts_left}"
        )

        progress = attempts_left / self.max_attempts

        self.progress_bar.set(progress)

        self.score = max(
            100 - (self.attempts_used * 10),
            10
        )

        self.score_label.configure(
            text=f"⭐ Score: {self.score}"
        )

        difference = abs(
            self.secret_number - guess
        )

        # -------------------------
        # DISTANCE HINTS
        # -------------------------

        if difference <= 5:
            distance_hint = "🔥 VERY CLOSE!"

        elif difference <= 15:
            distance_hint = "👍 CLOSE!"

        else:
            distance_hint = "❄️ FAR AWAY!"

        # -------------------------
        # HIGH / LOW HINTS
        # -------------------------

        if guess < self.secret_number:

            direction_hint = "⬆ TOO LOW"

        elif guess > self.secret_number:

            direction_hint = "⬇ TOO HIGH"

        else:

            direction_hint = "🎉 CORRECT!"

        # -------------------------
        # EVEN ODD HINT
        # -------------------------

        even_odd_hint = ""

        if self.attempts_used >= 3:

            if self.secret_number % 2 == 0:

                even_odd_hint = "\n💡 Number is EVEN"

            else:

                even_odd_hint = "\n💡 Number is ODD"

        self.hint_label.configure(
            text=f"{distance_hint}\n{direction_hint}{even_odd_hint}"
        )
                # -------------------------
        # WIN CONDITION
        # -------------------------

        if guess == self.secret_number:

            rank = self.get_rank()

            self.rank_label.configure(
                text=f"🏆 Rank: {rank}"
            )

            # Save High Score
            if self.score > self.high_score:

                self.high_score = self.score

                save_high_score(
                    self.high_score
                )

                self.high_score_label.configure(
                    text=f"🏆 High Score: {self.high_score}"
                )

            self.result_label.configure(
                text=
                f"""
🏆🏆🏆 YOU WON! 🏆🏆🏆

🎯 Correct Number : {self.secret_number}

⭐ Score : {self.score}

🥇 Rank : {rank}
"""
            )

            messagebox.showinfo(
                "Victory!",
                f"""
Congratulations!

Correct Number : {self.secret_number}

Score : {self.score}

Rank : {rank}
"""
            )

            return

        # -------------------------
        # GAME OVER
        # -------------------------

        if self.attempts_used >= self.max_attempts:

            self.result_label.configure(
                text=
                f"""
💀💀💀 GAME OVER 💀💀💀

Correct Number :
{self.secret_number}

😢 Better Luck Next Time!
"""
            )

            messagebox.showwarning(
                "Game Over",
                f"""
Game Over!

Correct Number :
{self.secret_number}
"""
            )

            return
        # --------------------------------
# APP START
# --------------------------------

if __name__ == "__main__":

    root = ctk.CTk()
    root.state("zoomed")
    root.minsize(1200, 700)

    app = NumberGuessMaster(root)

    root.mainloop()