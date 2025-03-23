import sqlite3
import random
import tkinter as tk

def get_words(difficulty):
    
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("SELECT french, english FROM words WHERE id <= ? ORDER BY RANDOM() LIMIT 3", (difficulty*100,))
    words = [row for row in cursor.fetchall()]
    conn.close()
    
    return words
    
def update_word():
    
    is_french_to_english = random.choice([True, False])
    
    words = get_words(difficulty.get())
    
    i = random.randint(0,2)
    
    prompt = words[i][is_french_to_english]
    
    answer = words[i][1 - is_french_to_english]
    
    options = [x[1-is_french_to_english] for x in words]

    current_word = f"{['French','English'][is_french_to_english]}: {prompt}"

    word_label.config(text=current_word)
    
    for i, button in enumerate(option_buttons):
        button.config(text=options[i], bg="#444", fg="white", command=lambda opt=options[i]: check_answer(opt, answer))

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
        
    score_label.config(text=f"Rating: {100*(score_correct/(score_wrong+score_correct)):0.1f}%")
    
    if selected == correct:
        root.after(1000, update_word)  # Pause 1 seconds before updating
    else:
        root.after(3000, update_word)  # Pause 3 seconds before updating
        
# GUI Setup
root = tk.Tk()
root.title("French-English Quiz")
root.geometry("800x700")
root.configure(bg="#222")

score_correct = 0
score_wrong = 0

is_french_to_english = True
word_label = tk.Label(root, text="", font=("Arial", 40), bg="#222", fg="white")
word_label.pack(pady=40)

option_buttons = [tk.Button(root, text="", font=("Arial", 24), bg="#222", fg="white") for _ in range(3)]
for btn in option_buttons:
    btn.pack(fill=tk.X, padx=40, pady=10)

difficulty = tk.IntVar(value=2)  # Default difficulty, limits words to first 50 rows

difficulty_slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, variable=difficulty, length=600, tickinterval=1, bg="#222", fg="white", troughcolor="#666")
difficulty_slider.pack()

score_label = tk.Label(root, text="", font=("Arial", 24), bg="#222", fg="white")
score_label.pack(pady=40)

update_word()

root.mainloop()
