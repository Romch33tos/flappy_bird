import tkinter as tk
import random
from PIL import Image, ImageTk
import os

class FlappyBird:
    def __init__(self, master):
        self.master = master
        self.master.title("Flappy Bird")
        self.master.resizable(False, False)
        
        self.width = 300
        self.height = 400
        self.gravity = 0.5
        self.jump_strength = 7.5
        self.bird_width = 50
        self.bird_height = 45
        
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="skyblue")
        self.canvas.pack()
        
        self.game_over = False
        self.game_started = False
        
        self.master.bind("<Button-1>", self.on_click)
        self.master.bind("<space>", self.on_space)

    def on_click(self, event):
        if not self.game_started:
            self.game_started = True
            self.start_game()
        elif self.game_over:
            self.start_game()

    def on_space(self, event):
        if not self.game_over and self.game_started:
            self.flap()

    def flap(self):
        pass

    def start_game(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyBird(root)
    root.mainloop()
