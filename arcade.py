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

    # Update highest score for the specific game
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
            update_stats('Snake Game', self.score)  # Update stats when game ends

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
            self.score += 10  # Increment score
            self.update_score()  # Update score display
        
        if head in self.snake[1:] or head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 400:
            self.running = False

# Minesweeper Game Class
class MinesweeperGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper Game")
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.grid_size = 10
        self.num_mines = 10
        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.mines = set()
        self.revealed = set()
        self.mine_positions = []

        self.setup_grid()
        self.place_mines()
        self.calculate_numbers()
        self.game_over = False

    def setup_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                button = tk.Button(self.frame, width=4, height=2, command=lambda x=i, y=j: self.reveal(x, y))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def place_mines(self):
        self.mines.clear()
        while len(self.mines) < self.num_mines:
            x, y = random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)
            if (x, y) not in self.mines:
                self.mines.add((x, y))
                self.mine_positions.append((x, y))

    def calculate_numbers(self):
        self.numbers = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for x, y in self.mines:
            for i in range(max(0, x-1), min(self.grid_size, x+2)):
                for j in range(max(0, y-1), min(self.grid_size, y+2)):
                    if (i, j) != (x, y):
                        self.numbers[i][j] += 1

    def reveal(self, x, y):
        if (x, y) in self.revealed or self.game_over:
            return

        if (x, y) in self.mines:
            self.end_game(False)
            return

        self.revealed.add((x, y))
        self.buttons[x][y].config(text=self.numbers[x][y] if self.numbers[x][y] > 0 else '', relief=tk.SUNKEN, state=tk.DISABLED)
        
        if len(self.revealed) == self.grid_size * self.grid_size - len(self.mines):
            self.end_game(True)
            return

        if self.numbers[x][y] == 0:
            for i in range(max(0, x-1), min(self.grid_size, x+2)):
                for j in range(max(0, y-1), min(self.grid_size, y+2)):
                    self.reveal(i, j)
    
    def end_game(self, won):
        self.game_over = True
        for x, y in self.mines:
            self.buttons[x][y].config(text='*', relief=tk.SUNKEN, state=tk.DISABLED)
        messagebox.showinfo("Game Over", "You Won!" if won else "Game Over! You Hit a Mine")
        update_stats('Minesweeper', len(self.revealed))  # Update stats

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Arcade")
        self.root.geometry("400x300")

        # Create buttons
        self.view_stats_button = tk.Button(root, text="View Career Stats", command=self.view_stats)
        self.select_game_button = tk.Button(root, text="Select Game", command=self.select_game)

        # Place buttons in the window
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
        
        tk.Button(self.select_game_window, text="Snake Game", command=self.start_snake_game).pack(pady=10)
        tk.Button(self.select_game_window, text="Minesweeper", command=self.start_minesweeper_game).pack(pady=10)

    def start_snake_game(self):
        self.snake_window = tk.Toplevel(self.root)
        self.snake_app = SnakeGame(self.snake_window)

    def start_minesweeper_game(self):
        self.minesweeper_window = tk.Toplevel(self.root)
        self.minesweeper_app = MinesweeperGame(self.minesweeper_window)

# Create main window
root = tk.Tk()
menu = MainMenu(root)

# Start the main loop
root.mainloop()
