import numpy as np
import pygame
import math
import tkinter as tk

board = np.zeros((6, 7))
height = len(board) - 1
turn = 0

pygame.init()

# Open window
size = (700, 600)
screen = pygame.display.set_mode(size)


# Make Board
def create_board():
  background_color = (0, 0, 180)
  screen.fill(background_color)
  y_val = 50
  for number in range(1, 7):
    x_val = 50
    for number in range(1, 8):
      pygame.draw.circle(screen, (255, 255, 255), (x_val, y_val), 40)
      x_val += 100
    y_val += 100


# Highlights column that mouse is hovering
highlighted = True
def highligt_row(x, y):
  transparent_rect = pygame.Surface((100, 600))  # the size of your rect
  transparent_rect.fill((255, 0, 0))  # this fills the entire surface
  transparent_rect.set_alpha(100)
  global highlighted

  screen.blit(transparent_rect, (math.floor(x/100) * 100, 0))



# Returns the lowest empty row in the given column.
def first_empty_row(board, column):
  for y in range(height, -1, -1):
    if board[y][column] == 0:
      return y
  return -1

def player_win(piece):
  rows = len(board[0])
  columns = len(board)
  # check horizontal spaces
  for y in range(rows):
    for x in range(columns - 3):
      if board[x][y] == piece and board[x + 1][y] == piece and board[x + 2][y] == piece and board[x + 3][y] == piece:
        return True

  # check vertical spaces
  for x in range(columns):
    for y in range(rows - 3):
      if board[x][y] == piece and board[x][y + 1] == piece and board[x][y + 2] == piece and board[x][y + 3] == piece:
        return True

  # check / diagonal spaces
  for x in range(columns - 3):
    for y in range(3, rows):
      if board[x][y] == piece and board[x + 1][y - 1] == piece and board[x + 2][y - 2] == piece and board[x + 3][
        y - 3] == piece:
        return True

  # check \ diagonal spaces
  for x in range(columns - 3):
    for y in range(rows - 3):
      if board[x][y] == piece and board[x + 1][y + 1] == piece and board[x + 2][y + 2] == piece and board[x + 3][
        y + 3] == piece:
        return True

  return False

create_board()
pygame.display.update()

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.MOUSEMOTION:
      #highligt_row(event.pos[0], event.pos[1])
      pygame.display.update()

    # Adds piece to board that player wants
    if event.type == pygame.MOUSEBUTTONDOWN:
      column = math.floor(event.pos[0]/100)
      row = first_empty_row(board, column)
      if turn % 2 == 0 and row >= 0:
        board[row,column] = 1
        pygame.draw.circle(screen, (255, 0, 0), ((column * 100) + 50, (row * 100) + 50), 40)
        turn += 1
        if player_win(1):
          running = False
      elif row >= 0:
        board[row, column] = 2
        pygame.draw.circle(screen, (255, 255, 0), ((column * 100) + 50, (row * 100) + 50), 40)
        turn += 1
        if player_win(2):
          running = False
      pygame.display.update()

    #



