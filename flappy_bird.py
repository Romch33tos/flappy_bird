import tkinter as tk
import random
from PIL import Image, ImageTk

class FlappyBird:
  def __init__(self, master):
    self.master = master
    self.master.title("Flappy Bird")
    self.pipe_image = Image.open("Python/Программы/Игры/FB/game_files/p1.png")
    self.pipe_image = self.pipe_image.resize((50, 400))
    self.pipe_image = ImageTk.PhotoImage(self.pipe_image)
    self.bird_image = Image.open("Python/Программы/Игры/FB/game_files/b.png")
    self.bird_image = self.bird_image.resize((50, 50))
    self.bird_image = ImageTk.PhotoImage(self.bird_image)
    self.width = 400
    self.height = 600
    self.gravity = 0.5
    self.jump_strength = 8.5
    self.score = 0
    self.game_over = False
    self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="skyblue")
    self.canvas.pack()
    self.bird = self.canvas.create_image(50, self.height / 2, anchor=tk.NW, image=self.bird_image)
    self.bird_y_velocity = 0
    self.pipes = []
    self.pipe_gap = 150
    self.pipe_speed = 3
    self.create_pipe()
    self.master.bind("<ButtonPress-1>", self.flap)
    self.update()

  def create_pipe(self):
    gap_start = random.randint(100, self.height - 200)
    top_pipe = self.canvas.create_image(self.width, gap_start - 400, anchor=tk.NW, image=self.pipe_image)
    bottom_pipe = self.canvas.create_image(self.width, gap_start + self.pipe_gap, anchor=tk.NW, image=self.pipe_image)
    self.pipes.append((top_pipe, bottom_pipe))

  def flap(self, event):
    if not self.game_over:
      self.bird_y_velocity = -self.jump_strength

  def update(self):
    if not self.game_over:
      self.bird_y_velocity += self.gravity
      self.canvas.move(self.bird, 0, self.bird_y_velocity)
      for top_pipe, bottom_pipe in self.pipes:
        self.canvas.move(top_pipe, -self.pipe_speed, 0)
        self.canvas.move(bottom_pipe, -self.pipe_speed, 0)
      if self.pipes and self.canvas.coords(self.pipes[0][0])[0] < 0:
        top_pipe, bottom_pipe = self.pipes.pop(0)
        self.canvas.delete(top_pipe)
        self.canvas.delete(bottom_pipe)
        self.create_pipe()
        self.score += 1
        print("Score:", self.score)
      if self.check_collision():
        self.game_over = True
        print("Game Over! Your score was:", self.score)
      self.master.after(20, self.update)

  def check_collision(self):
    bird_coords = self.canvas.coords(self.bird)
    bird_x = bird_coords[0]
    bird_y = bird_coords[1]
    bird_width = 50
    bird_height = 30
    for top_pipe, bottom_pipe in self.pipes:
      top_coords = self.canvas.coords(top_pipe)
      bottom_coords = self.canvas.coords(bottom_pipe)
      if (bird_x + bird_width > top_coords[0] and bird_x < top_coords[0] + 50 and
          bird_y < top_coords[1] + 400):
        return True
      if (bird_x + bird_width > bottom_coords[0] and bird_x < bottom_coords[0] + 50 and
          bird_y + bird_height > bottom_coords[1]):
        return True
    if bird_y < 0 or bird_y + bird_height > self.height:
      return True
    return False

if __name__ == "__main__":
  root = tk.Tk()
  game = FlappyBird(root)
  root.mainloop()
