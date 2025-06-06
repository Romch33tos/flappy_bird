import tkinter as tk
import random

class FlappyBird:
  def __init__(self, master):
    self.master = master
    self.master.title("Flappy Bird")
    self.width = 400
    self.height = 600
    self.gravity = 0.5
    self.jump_strength = 10
    self.score = 0
    self.game_over = False
    self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="skyblue")
    self.canvas.pack()
    self.bird = self.canvas.create_oval(50, self.height / 2, 70, self.height / 2 + 20, fill='yellow')
    self.bird_y_velocity = 0
    self.pipes = []
    self.pipe_height = 100
    self.pipe_gap = 150
    self.pipe_speed = 3
    self.create_pipe()
    self.master.bind("<ButtonPress-1>", self.flap)
    self.update()

  def create_pipe(self):
    gap_start = random.randint(100, self.height - 100 - self.pipe_gap)
    top_pipe = self.canvas.create_rectangle(self.width, 0, self.width + 50, gap_start, fill='green')
    bottom_pipe = self.canvas.create_rectangle(self.width, gap_start + self.pipe_gap, self.width + 50, self.height, fill='green')
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
      if self.canvas.coords(self.pipes[0][0])[2] < 0:
        self.pipes.pop(0)
        self.create_pipe()
        self.score += 1
        print("Score:", self.score)
      if self.check_collision():
        self.game_over = True
        print("Game Over! Your score was:", self.score)
      self.master.after(20, self.update)

  def check_collision(self):
    bird_coords = self.canvas.coords(self.bird)
    for top_pipe, bottom_pipe in self.pipes:
      top_coords = self.canvas.coords(top_pipe)
      bottom_coords = self.canvas.coords(bottom_pipe)
      if (bird_coords[2] > top_coords[0] and bird_coords[0] < top_coords[2] and
          (bird_coords[1] < top_coords[3] or bird_coords[3] > bottom_coords[1])):
        return True
    if bird_coords[1] < 0 or bird_coords[3] > self.height:
      return True
    return False

if __name__ == "__main__":
  root = tk.Tk()
  game = FlappyBird(root)
  root.mainloop()