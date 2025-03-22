import sqlite3
import random
import tkinter as tk

def get_random_word():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("SELECT french, english FROM words ORDER BY RANDOM() LIMIT 1")
    word = cursor.fetchone()
    conn.close()
    return word

def generate_options(correct, is_french_to_english):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    if is_french_to_english:
        cursor.execute("SELECT english FROM words WHERE english != ? ORDER BY RANDOM() LIMIT 2", (correct,))
    else:
        cursor.execute("SELECT french FROM words WHERE french != ? ORDER BY RANDOM() LIMIT 2", (correct,))
    incorrect = [row[0] for row in cursor.fetchall()]
    conn.close()
    options = incorrect + [correct]
    random.shuffle(options)
    return options

def update_word():
    global current_word, options, is_french_to_english, correct_answer
    is_french_to_english = random.choice([True, False])
    french, english = get_random_word()
    
    if is_french_to_english:
        current_word = french
        correct_answer = english
    else:
        current_word = english
        correct_answer = french
    
    options = generate_options(correct_answer, is_french_to_english)
    word_label.config(text=current_word)
    for i, button in enumerate(option_buttons):
        button.config(text=options[i], bg="lightgray", command=lambda opt=options[i]: check_answer(opt, correct_answer))

def check_answer(selected, correct):
    global score_correct,score_wrong
    for button in option_buttons:
        if button["text"] == correct:
            button.config(bg="green")
        elif button["text"] == selected:
            button.config(bg="red")
    
    if selected == correct:
        score_correct += 1
    else:
        score_wrong += 1
        
    score_label.config(text=f"Score: {score_correct} vs {score_wrong}")
    
    if selected == correct:
        root.after(1000, update_word)  # Pause 5 seconds before updating
    else:
        root.after(3000, update_word)  # Pause 5 seconds before updating
        
# GUI Setup
root = tk.Tk()
root.title("French-English Quiz")
root.geometry("800x600")

score_correct = 0
score_wrong = 0

is_french_to_english = True
word_label = tk.Label(root, text="", font=("Arial", 40))
word_label.pack(pady=40)

option_buttons = [tk.Button(root, text="", font=("Arial", 24)) for _ in range(3)]
for btn in option_buttons:
    btn.pack(fill=tk.X, padx=40, pady=10)

score_label = tk.Label(root, text="", font=("Arial", 24))
score_label.pack(pady=40)

update_word()

root.mainloop()
