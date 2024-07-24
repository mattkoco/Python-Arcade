import tkinter as tk
from tkinter import messagebox
import json
import os

# Create the main window
root = tk.Tk()
root.title("Python Arcade")
root.geometry("400x300")

# Function to view career stats
def view_stats():
    if os.path.exists('career_stats.json'):
        with open('career_stats.json', 'r') as file:
            stats = json.load(file)
            stats_message = f"Games Played: {stats['Games Played']}\n"
            stats_message += "Highest Scores:\n"
            for game, score in stats['Highest Scores'].items():
                stats_message += f"  {game}: {score}\n"
            stats_message += f"Favorite Game: {stats['Favorite Game']}"
            messagebox.showinfo("Career Stats", stats_message)
    else:
        messagebox.showinfo("Career Stats", "No stats available. Play some games first!")

# Function to select a game (currently a placeholder)
def select_game():
    messagebox.showinfo("Select Game", "Game selection coming soon!")

# Create buttons
view_stats_button = tk.Button(root, text="View Career Stats", command=view_stats)
select_game_button = tk.Button(root, text="Select Game", command=select_game)

# Place buttons in the window
view_stats_button.pack(pady=20)
select_game_button.pack(pady=20)

# Start the main loop
root.mainloop()
