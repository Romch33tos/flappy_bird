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
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        background_path = os.path.join(script_dir, "game_files", "background.png")
        pipe_path = os.path.join(script_dir, "game_files", "pipe.png")
        bird_paths = [os.path.join(script_dir, "game_files", f"bird{i}.png") for i in range(1, 4)]
        
        self.background_img = Image.open(background_path).resize((self.width, self.height))
        self.background_img = ImageTk.PhotoImage(self.background_img)
        
        self.pipe_img = Image.open(pipe_path).resize((50, 400))
        self.pipe_img = ImageTk.PhotoImage(self.pipe_img)
        
        self.bird_frames = [
            ImageTk.PhotoImage(Image.open(path).resize((self.bird_width, self.bird_height)))
            for path in bird_paths
        ]
        self.current_frame = 0
        
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="skyblue")
        self.canvas.pack()
        
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.game_started = False
        self.bird = None
        self.pipes = []
        self.start_message = None
        self.score_text = None
        self.high_score_text = None
        
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
        self.bird_y_velocity = -self.jump_strength

    def show_start_message(self):
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_img)
        self.start_message = self.canvas.create_text(
            self.width // 2, self.height // 2,
            text="Кликни, чтобы начать игру!",
            font=("Arial", 14, "bold"), fill="white", justify="center"
        )

    def show_game_over_message(self):
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text="Конец игры!\nКликни для перезапуска!",
            font=("Arial", 14, "bold"), fill="white", justify="center"
        )

    def start_game(self):
        self.score = 0
        self.game_over = False
        self.bird_y_velocity = 0
        self.pipes.clear()
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_img)
        
        self.score_text = self.canvas.create_text(
            self.width - 40, 20,
            text=f"Счет: {self.score}",
            font=("Arial", 12, "bold"), fill="white",
            tags="score"
        )
        
        self.high_score_text = self.canvas.create_text(
            self.width - 50, 45,
            text=f"Рекорд: {self.high_score}",
            font=("Arial", 12, "bold"), fill="white",
            tags="score"
        )
        
        self.bird = self.canvas.create_image(
            50, self.height // 2,
            anchor=tk.NW,
            image=self.bird_frames[0]
        )
        
        self.create_pipe()
        self.canvas.tag_raise("score")
        self.animate_bird()
        self.update()

    def animate_bird(self):
        if not self.game_over:
            self.current_frame = (self.current_frame + 1) % len(self.bird_frames)
            self.canvas.itemconfig(self.bird, image=self.bird_frames[self.current_frame])
            self.master.after(100, self.animate_bird)

    def create_pipe(self):
        gap_start = random.randint(100, self.height - 200)
        top_pipe = self.canvas.create_image(
            self.width, gap_start - 400,
            anchor=tk.NW,
            image=self.pipe_img
        )
        bottom_pipe = self.canvas.create_image(
            self.width, gap_start + 150,
            anchor=tk.NW,
            image=self.pipe_img
        )
        self.pipes.append((top_pipe, bottom_pipe))
        self.canvas.tag_raise("score")

    def update(self):
        if not self.game_over:
            self.bird_y_velocity += self.gravity
            self.canvas.move(self.bird, 0, self.bird_y_velocity)
            
            for top_pipe, bottom_pipe in self.pipes:
                self.canvas.move(top_pipe, -3, 0)
                self.canvas.move(bottom_pipe, -3, 0)
            
            if self.pipes and self.canvas.coords(self.pipes[0][0])[0] < -50:
                top_pipe, bottom_pipe = self.pipes.pop(0)
                self.canvas.delete(top_pipe)
                self.canvas.delete(bottom_pipe)
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Счет: {self.score}")
                
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.canvas.itemconfig(self.high_score_text, text=f"Рекорд: {self.high_score}")
            
            if len(self.pipes) == 0 or self.canvas.coords(self.pipes[-1][0])[0] < self.width - 200:
                self.create_pipe()
            
            if self.check_collision():
                self.game_over = True
                self.show_game_over_message()
            
            self.master.after(15, self.update)

    def check_collision(self):
        bird_coords = self.canvas.coords(self.bird)
        if not bird_coords:
            return True
            
        bird_x, bird_y = bird_coords[0], bird_coords[1]
        
        for top_pipe, bottom_pipe in self.pipes:
            top_coords = self.canvas.coords(top_pipe)
            bottom_coords = self.canvas.coords(bottom_pipe)
            
            if (bird_x + self.bird_width > top_coords[0] and
                bird_x < top_coords[0] + 50 and
                bird_y < top_coords[1] + 400):
                return True
            
            if (bird_x + self.bird_width > bottom_coords[0] and
                bird_x < bottom_coords[0] + 50 and
                bird_y + self.bird_height > bottom_coords[1]):
                return True
        
        if bird_y < 0 or bird_y + self.bird_height > self.height:
            return True
        
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyBird(root)
    game.show_start_message()
    root.mainloop()
