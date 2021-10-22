import numpy as np
import pygame
import math
import random as rand

board = np.zeros((6, 7))
height = len(board) - 1
rows = len(board[0])
columns = len(board)
turn = rand.randint(0,1)

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


# Returns the lowest empty row in the given column.
def first_empty_row(board, column):
  for y in range(height, -1, -1):
    if board[y][column] == 0:
      return y
  return -1


def player_win(piece):
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

# Columns that are not filled
def valid_locations(board):
  valid_locations = []
  for col in range(7):
    if board[0][col] == 0:
      valid_locations.append(col)
  return valid_locations

# Score Rules
def score_rules(window, piece, opp_piece):
  score = 0

  if window.count(piece) == 4:
    score += 1000
  elif window.count(piece) == 3 and window.count(None) == 1:
    score += 5
  elif window.count(piece) == 2 and window.count(0) == 2:
    score += 2

  if window.count(opp_piece) == 2 and window.count(0) == 2:
    score -= 2
  elif window.count(opp_piece) == 3 and window.count(0) == 1:
    score -= 4
  elif window.count(opp_piece) == 4:
    score -= 1000

  return score


# Finds score of each possible board
def evaluate_board(board, piece, opp_piece):
  score = 0

  center_array = [int(i) for i in list(board[:, 3])]
  center_count = center_array.count(piece)
  score += center_count * 3

  for row in range(rows-1):
    start_column = 0
    row_array = [int(i) for i in list(board[row, :])]
    for number in range(4):
      window = row_array[start_column: start_column + 4]
      score += score_rules(window, piece, opp_piece)
      start_column += 1

  for column in range(columns + 1):
    start_row = 0
    col_array = [int(i) for i in list(board[:, column])]
    for number in range(3):
      window = col_array[start_row:start_row + 4]
      score += score_rules(window, piece, opp_piece)
      start_row += 1

  for row in range(3):
    for column in range(columns - 3):
      window = [board[row + i][column + i] for i in range(4)]
      score += score_rules(window, piece, opp_piece)

  for row in range(3):
    for column in range(columns - 3):
      window = [board[row + 3 - i][column + i] for i in range(4)]
      score += score_rules(window, piece, opp_piece)

  return score



transposition_table = {}
def minimax(board, depth_node, alpha=-10000, beta=10000, maximizing=True):
  if board.tostring() in transposition_table:
    tt_entry = transposition_table[board.tostring()]
    if tt_entry[1] == 'EXACT':
      return tt_entry[0]
    elif tt_entry[1] == 'LOWERCASE':
      alpha = max(alpha, tt_entry[0][1])
    elif tt_entry[1] == 'UPPERCASE':
      beta = min(beta, tt_entry[0][1])

    if alpha >= beta:
      return tt_entry[0]

  # Terminal Condition
  if depth_node == 0:
    return(None, evaluate_board(board, 2, 1))
  elif player_win(2):
    return (None, 10000)
  elif player_win(1):
    return (None, -10000)
  elif len(valid_locations(board)) == 0:
    return (None, 0)

  if maximizing:
    value = -math.inf
    for column in valid_locations(board):
      board_copy = board.copy()
      copy_row = first_empty_row(board, column)
      board_copy[copy_row][column] = 2
      new_score = minimax(board_copy, depth_node - 1, alpha, beta, False)[1]
      if new_score > value:
        value = new_score
        best_column = column
      alpha = max(alpha, value)
      if alpha >= beta:
        break
    return best_column, value

  else:
    value = math.inf
    for column in valid_locations(board):
      board_copy = board.copy()
      copy_row = first_empty_row(board, column)
      board_copy[copy_row][column] = 1
      new_score = minimax(board_copy, depth_node - 1, alpha, beta, True)[1]
      if new_score < value:
        value = new_score
        best_column = column
      beta = min(beta, value)
      if alpha >= beta:
        break
    return best_column, value



create_board()
pygame.display.update()

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    # Adds piece to board that player wants
    if event.type == pygame.MOUSEBUTTONDOWN:
      if turn % 2 == 0:
        column2 = math.floor(event.pos[0] / 100)
        row = first_empty_row(board, column2)
        board[row, column2] = 1
        pygame.draw.circle(screen, (255, 0, 0), ((column2 * 100) + 50, (row * 100) + 50), 40)
        turn += 1
        if player_win(1):
          # running = False
          print("Red wins")
        pygame.display.update()
    elif turn % 2 == 1:
      ai_column = minimax(board, 5)[0]
      row = first_empty_row(board, ai_column)
      pygame.time.wait(500)
      board[row, ai_column] = 2
      pygame.draw.circle(screen, (255, 255, 0), ((ai_column * 100) + 50, (row * 100) + 50), 40)
      turn += 1
      print(evaluate_board(board, 2, 1))
      if player_win(2):
        # running = False
        print("Yellow wins")
    pygame.display.update()
