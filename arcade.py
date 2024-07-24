import tkinter as tk
from tkinter import messagebox
import json
import os
import random

# File for storing stats
STATS_FILE = 'career_stats.json'

def update_stats(game, score):
    if not os.path.exists(STATS_FILE):
        stats = {
            'Games Played': 0,
            'Highest Scores': {},
            'Favorite Game': None
        }
    else:
        with open(STATS_FILE, 'r') as file:
            stats = json.load(file)

    # Update games played
    stats['Games Played'] += 1

    # Update highest score for the specifec game
    if game in stats['Highest Scores']:
        if score > stats['Highest Scores'][game]:
            stats['Highest Scores'][game] = score
    else:
        stats['Highest Scores'][game] = score

    # Write the updated stats back to the file
    with open(STATS_FILE, 'w') as file:
        json.dump(stats, file, indent=4)

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()
        
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.food = (200, 200)
        self.direction = "Right"
        self.running = True
        self.score = 0
        
        self.draw_snake()
        self.draw_food()
        self.update_score()
        
        self.root.bind("<KeyPress>", self.change_direction)
        self.run_game()

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0]+10, segment[1]+10, fill="green", tags="snake")

    def draw_food(self):
        self.canvas.delete("food")
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0]+10, self.food[1]+10, fill="red", tags="food")

    def update_score(self):
        self.canvas.delete("score")
        self.canvas.create_text(200, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 12), tags="score")

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.direction = event.keysym

    def run_game(self):
        if self.running:
            self.move_snake()
            self.check_collision()
            self.root.after(100, self.run_game)
        else:
            self.canvas.create_text(200, 200, text=f"Game Over\nScore: {self.score}", fill="white", font=("Arial", 24))
            update_stats('Snake Game', self.score)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= 10
        elif self.direction == "Down":
            head_y += 10
        elif self.direction == "Left":
            head_x -= 10
        elif self.direction == "Right":
            head_x += 10
        
        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]
        self.draw_snake()

    def check_collision(self):
        head = self.snake[0]
        if head == self.food:
            self.snake.append(self.snake[-1])
            self.food = (random.randint(0, 39) * 10, random.randint(0, 39) * 10)
            self.draw_food()
            self.score += 10
            self.update_score()
        
        if head in self.snake[1:] or head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 400:
            self.running = False

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Arcade")
        self.root.geometry("400x300")

        self.view_stats_button = tk.Button(root, text="View Career Stats", command=self.view_stats)
        self.select_game_button = tk.Button(root, text="Select Game", command=self.select_game)

        self.view_stats_button.pack(pady=20)
        self.select_game_button.pack(pady=20)

    def view_stats(self):
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r') as file:
                stats = json.load(file)
                stats_message = f"Games Played: {stats['Games Played']}\n"
                stats_message += "Highest Scores:\n"
                for game, score in stats['Highest Scores'].items():
                    stats_message += f"  {game}: {score}\n"
                stats_message += f"Favorite Game: {stats['Favorite Game']}"
                messagebox.showinfo("Career Stats", stats_message)
        else:
            messagebox.showinfo("Career Stats", "No stats available. Play some games first!")

    def select_game(self):
        self.select_game_window = tk.Toplevel(self.root)
        self.select_game_window.title("Select Game")
        self.select_game_window.geometry("300x200")
        
        tk.Button(self.select_game_window, text="Snake Game", command=self.start_snake_game).pack(pady=20)

    def start_snake_game(self):
        self.snake_window = tk.Toplevel(self.root)
        self.snake_app = SnakeGame(self.snake_window)

root = tk.Tk()
menu = MainMenu(root)

root.mainloop()
