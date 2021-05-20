import pygame
import sys
from pygame.locals import *
import random
import os


mainClock = pygame.time.Clock()

# initialization
pygame.init()
pygame.display.set_caption('Tic Tac Toe')
icon = pygame.image.load(os.path.join('imgs', 'icon.png'))
pygame.display.set_icon(icon)
WIDTH, HEIGHT = 700, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

# parameters

menu_font = pygame.font.SysFont('Century', 100)
options_font = pygame.font.SysFont('Century', 80)
font = pygame.font.SysFont('Century', 60)
font_me = pygame.font.SysFont('Century', 40, False, True)
font_try_again = pygame.font.SysFont('Century', 40)
WHITE = (235, 235, 235)
BLACK = (0, 0, 0)
RED = (206, 0, 0)
BLUE = (2, 95, 207)
PINK = (232, 127, 177)
ORANGE = (255, 100, 0)

# customizations for crosses and circles

cross = pygame.image.load(os.path.join("imgs","cross.png"))
circle = pygame.image.load(os.path.join("imgs", "circle.png"))


def change_cross(directory):
	global cross # why would I do that like this
	cross = pygame.image.load(os.path.join('imgs', directory))


def change_circle(directory):
	global circle
	circle = pygame.image.load(os.path.join('imgs', directory))


def draw_text(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)


def main_menu():
	click = False
	while True:

		screen.fill(WHITE)
		draw_text('Tic Tac Toe', menu_font, BLACK, screen, 100, 20)

		mx, my = pygame.mouse.get_pos()

		# buttons in menu
		# Rect(left, top, width, height)
		rect_width = 400
		rect_height = 80
		x = 150
		y = 170
		button_1 = pygame.Rect(x, y, rect_width, rect_height)
		button_2 = pygame.Rect(x, y+120, rect_width, rect_height)
		button_3 = pygame.Rect(x, y+240, rect_width, rect_height)

		if button_1.collidepoint((mx, my)):
			if click:
				player_1()
		if button_2.collidepoint((mx, my)):
			if click:
				player_2()
		if button_3.collidepoint((mx, my)):
			if click:
				options()

		pygame.draw.rect(screen, BLACK, button_1)
		pygame.draw.rect(screen, BLACK, button_2)
		pygame.draw.rect(screen, BLACK, button_3)
		draw_text('1 Player', font, WHITE, screen, x+85, y)
		draw_text('2 Players', font, WHITE, screen, x+85, y+120)
		draw_text('Options', font, WHITE, screen, x+85, y+240)

		draw_text('by MrJoeKr', font_me, BLACK, screen, 460, 500)

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.update()
		mainClock.tick(60)


# in-game functions


def create_cell(x, y, w, h):
	outline = pygame.Rect(x, y, w, h)
	cell_draw = pygame.Rect(x + 5, y + 5, w - 10, h - 10)
	pygame.draw.rect(screen, BLACK, outline)
	pygame.draw.rect(screen, WHITE, cell_draw)
	return pygame.Rect(x, y, w, h)


def create_board(x,y,w,h): #creates the board with 9 cells
	x1 = x
	y1 = y
	cells = []
	for row in range(3):
		x1 = x
		for col in range(3):
			cell = create_cell(x1, y1, w, h)
			x1 += w
			cells.append(cell)
		y1 += h
	return cells


def switch_turns(turn_X, turn_O):
	if turn_X:
		turn_X = False
		turn_O = True
	elif turn_O:
		turn_X = True
		turn_O = False

	return turn_X, turn_O



def check_for_win(board):
	# board is a dictionary
	win = False
	win_X = False
	for x in range(1, 10):
		# row check
		if x in [1,4,7]:
			if board[x] == board[x+1] and board[x+1] == board[x+2] and board[x] != '':
				if board[x] == 'X':
					win_X = True
				win = True

		# columns check
		if x < 4:
			if board[x] == board[x+3] and board[x+3] == board[x+6] and board[x] != '':
				if board[x] == 'X':
					win_X = True
				win = True


		#diagonal check
		elif board[1] == board[5] and board[5] == board[9] and board[1] != '':
			if board[1] == 'X':
				win_X = True
			win = True

		elif board[3] == board[5] and board[5] == board[7] and board[3] != '':
			if board[3] == 'X':
				win_X = True
			win = True

	# if win is True and win_X is False => Circle won
	return win, win_X 


def check_for_tie(board, turn_X):
	tie = False
	# count empty cells
	count = 0
	for k in board:
		if board[k] == '':
			count += 1
			# if count is one than it's ok
			empty_cell_pos = k


	# print(count)

	if count > 1:
		return tie
	
	if count == 1:
		win, win_X = check_for_win(board)

		# check whether X or O have turn to calculate if they can win
		if turn_X:
			board[empty_cell_pos] = 'X'
			win, win_X = check_for_win(board)
			board[empty_cell_pos] = ''
			if win:
				return tie


		elif not turn_X:
			board[empty_cell_pos] = 'O'
			win, win_X = check_for_win(board)
			board[empty_cell_pos] = ''
			if win:
				return tie


		if not win:
			tie = True
			draw_text("Draw!", font_try_again, (196, 4, 0), screen, WIDTH//2-60, 30)
			draw_text("Press SPACE for next round", font_try_again, PINK, screen, 125, HEIGHT-50)
		else:
			tie = False

	return tie


# Opponents

# baby AI - puts circles randomly
def easy_AI(board, player_O, turn_X, turn_O):
	choices = []
	# if not win and not tie:
	# 	draw_text("O's turn", font, RED, screen, WIDTH//2-100, 30)
	for num in board:
		if board[num] == '':
			choices.append(num)

	if choices:
		r = random.choice(choices)
		choices.remove(r)

	player_O.append(r)

	turn_X, turn_O = switch_turns(turn_X, turn_O)

	return board, player_O, turn_X, turn_O

# impossible AI - Mini-Max Algorithm

def minimax(board, depth, maximizingPlayer):

	# -10 - lose
	# 0 - tie
	# 10 - win

	# in our case, maximizingPlayer is 'O'
	if maximizingPlayer:
		turn_X = False
	else:
		turn_X = True

	# if it's game over
	# using turn_X, because that's what I used in these functions
	win, win_X = check_for_win(board)
	tie = check_for_tie(board, turn_X)
	if tie:
		return 0
	elif win_X:
		return -10
	elif win:
		return 10 - depth

	if maximizingPlayer:
		maxValue = -2
		# checking each move
		for k in board:
			if board[k] != '':
				continue
			board[k] = 'O'
			value = minimax(board, depth+1, False)
			maxValue = max(maxValue, value)
			board[k] = ''

		return maxValue
	else:
		minValue = 2
		for k in board:
			if board[k] != '':
				continue
			board[k] = 'X'
			value = minimax(board, depth+1, True)
			minValue = min(minValue, value)
			board[k] = ''

		return minValue


def findBestMove(board, turn_X):
	# if turn_X:
	# 	turn = 'X'
	# 	maximizingPlayer = False
	# else:
	# 	turn = 'O'
	# 	maximizingPlayer = True
	# maximizingPlayer is false cause we put turn for him and evaluate if it's good or not
	maximizingPlayer = False
	turn = 'O'

	bestMove = -100
	position = -1
	for k in board:		# k -> position of cell
		if board[k] != '':
			continue

		board[k] = turn
		move = minimax(board, 0, maximizingPlayer)
		# print(move, k)
		if move > bestMove:
			bestMove = move
			position = k
		board[k] = ''

	# print(bestMove)
	return position


# Considering 'O' as the AI
# using funcs: evaluate(), minimax(), findBestMove()
def impossible_AI(board):	
	# when activated, it's 'O's turn
	turn_X = False
	position = findBestMove(board, turn_X)
	board[position] = 'O'
	return position

# Function for drawing on board
def draw_on_board(board, cells):
	for k, v in board.items():

		draw_x = cells[k-1].x + 11
		draw_y = cells[k-1].y + 15

		if board[k] == 'X':
			draw_cross(draw_x + 5, draw_y + 5)
		elif board[k] == 'O':
			draw_circle(draw_x, draw_y)


def draw_line(x, y, w, h, color):
	line = pygame.Rect(x, y, w, h)
	pygame.draw.rect(screen, color, line)


def draw_win_line(board, x, y):

	for x in range(1,10):

		w = 440
		h = 10
		# print(x, x+1, x+2)

		# row check
		if x < 8:
			if board[x] == board[x+1] and board[x+1] == board[x+2] and board[x] != '':
				if x == 1:
					draw_line(x+125, y+50, w, h, BLUE)
				if x == 4:
					draw_line(x+125, y+175, w, h, BLUE)
				if x == 7:
					draw_line(x+125, y+300, w, h, BLUE)

		# columns check
		if x < 4:
			if board[x] == board[x+3] and board[x+3] == board[x+6] and board[x] != '':
				if x == 1:
					draw_line(x+230, y-50, h, w, BLUE)
				if x == 2:
					draw_line(x+230+110, y-50, h, w, BLUE)
				if x == 3:
					draw_line(x+230+2*110, y-50, h, w, BLUE)

		#diagonal check
		elif board[1] == board[5] and board[5] == board[9] and board[1] != '':
			pygame.draw.line(screen, RED, (x+125, y-30), (x+419+125, y+419-40), 10)

		elif board[3] == board[5] and board[5] == board[7] and board[3] != '':
			pygame.draw.line(screen, RED, (x+125, y+419-40), (x+419+125, y-30), 10)


def draw_cross(x, y, s=80):
	global cross
	cross = pygame.transform.scale(cross, (s, s))
	screen.blit(cross, (x, y))


def draw_own(img, x, y, scale):
	own = pygame.image.load('imgs' + "\\" + img)
	own = pygame.transform.scale(own, (scale, scale))
	screen.blit(own, (x, y))


def draw_circle(x, y, s=90):
	global circle
	circle = pygame.transform.scale(circle, (s, s))
	screen.blit(circle, (x, y))


# test func probably
def load(t):
	time.sleep(t)
	print('works')


def player_1():
	running = True
	click = False
	while running:

		screen.fill(WHITE)

		mx, my = pygame.mouse.get_pos()

		# buttons in menu
		rect_width = 400
		rect_height = 80
		x = 150
		y = 170

		button_1 = pygame.Rect(x, y, rect_width, rect_height)
		button_2 = pygame.Rect(x, y+120, rect_width, rect_height)

		# draw buttons and texts
		draw_text('Choose Difficulty:', options_font, BLACK, screen, 15, 25)


		
		pygame.draw.rect(screen, BLACK, button_1)
		pygame.draw.rect(screen, BLACK, button_2)
		draw_text('Easy', font, WHITE, screen, x+130, y)
		draw_text('Impossible', font, WHITE, screen, x+55, y+120)

		if button_1.collidepoint((mx, my)):
			if click:
				easy()
		if button_2.collidepoint((mx, my)):
			if click:
				impossible()

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.update()
		mainClock.tick(60)


def easy():
	# booting the game
	running = True
	click = False

	clicks = []

	board = {1: '', 2: '', 3: '',
			 4: '', 5: '', 6: '',
			 7: '', 8: '', 9: ''}

	score_X = 0
	score_O = 0

	# handling turns

	point = False
	end = False
	win = False
	win_X = False
	win_O = False
	turn_X = True
	turn_O = False
	turns = [i for i in range(1, 10)]

	empty_cells = [i for i in range(1, 10)]
	drawn_cells = []


	# lists of taken cells
	player_X = []
	player_O = []

	# if tie
	tie_list = []
	tie = False

	while running:

		# draw screen and board
		screen.fill(WHITE)

		# creating board
		x = 170
		y = 130
		w = 120
		h = w
		# create the cells and put them in a list
		cells = []
		cells = create_board(x, y, w, h)

		# show score

		global WIDTH
		draw_text("X: " + str(score_X), font, BLUE, screen, 25, 25)
		draw_text("O: " + str(score_O), font, RED, screen, WIDTH-140, 25)

		# showing who's turn

		if turn_X:
			if not win and not tie:
				draw_text("X's turn", font, BLUE, screen, WIDTH//2-110, 30)
		if turn_O:
			pass


		# interacting with cells
		# managing who's turn is

		#new
		if turn_X and not win or not tie:
			for cell in cells:
				for click in clicks:
					if cell.collidepoint(click):
						pos = cells.index(cell) + 1
						if pos in empty_cells:
							turn_X, turn_O = switch_turns(turn_X , turn_O)

							# adding to player x so it works
							player_X.append(pos)

							empty_cells.remove(pos)
							drawn_cells.append(pos)

						# print(turn_X, turn_O)


		# why is here the same as before
		if not end:

			win, win_X = check_for_win(board)

			# print(win)
			if win:
				end = True # not sure what end is but anyways...
				if not win_X:
					win_O = True

			#putting X and O into dictionary
			for i in player_X:
				board[i] = 'X'

			for i in player_O:
				board[i] = 'O'

		# checking if tie

		if not win:
			tie = check_for_tie(board, turn_X)


		# baby opponent
		win, win_X = check_for_win(board)
		if turn_O and not win and not tie:
			board, player_O, turn_X, turn_O = easy_AI(board, player_O, turn_X, turn_O)

		# check for circles to remove them from empty list
		for num in board:
			if board[num] == 'O':
				if num in empty_cells:
					empty_cells.remove(num)
					drawn_cells.append(num)


		# drawing crosses and circles

		draw_on_board(board, cells)


		# drawing lines when win

		x_line = 170
		y_line = 130
		draw_win_line(board, x_line, y_line)


		# adding point after win

		if win:
			if win_X and not point:
				score_X += 1
				point = True
			elif not win_X and not point:
				score_O += 1
				point = True

			if win_X:
				draw_text("X won!", font, (10, 98, 221), screen, WIDTH//2-100, 30)
			if not win_X:
				draw_text("O won!", font, (196, 4, 0), screen, WIDTH//2-100, 30)

			draw_text("SPACE for next round", font_try_again, PINK, screen, 150, 500)

		# controls and resetting variables
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
				if win or tie:
					if event.key == K_SPACE:

						# check who won
						turn_X = False
						turn_O = False
						if win_X:
							turn_O = True
						else:
							turn_X = True

						win = False
						tie = False
						win_X = False
						win_O = False
						end = False
						point = False
						player_X.clear()
						player_O.clear()
						clicks.clear()
						turns = [i for i in range(1, 10)]

						empty_cells = turns
						drawn_cells = []

						for i in board.keys():
							board[i] = ''

			if event.type == MOUSEBUTTONDOWN:
				if event.button == BUTTON_LEFT:
					mx, my = pygame.mouse.get_pos()
					clicks.append((mx, my))
				if win or tie:
					if event.button == BUTTON_LEFT:

						# check who won
						turn_X = False
						turn_O = False
						if win_X:
							turn_O = True
						else:
							turn_X = True

						win = False
						tie = False
						win_X = False
						win_O = False
						end = False
						point = False
						player_X.clear()
						player_O.clear()
						clicks.clear()
						turns = [i for i in range(1, 10)]

						empty_cells = turns
						drawn_cells = []

						for i in board.keys():
							board[i] = ''

		pygame.display.update()
		mainClock.tick(60)


def impossible():
	# booting the game
	running = True
	click = False

	clicks = []

	board = {1: '', 2: '', 3: '',
			 4: '', 5: '', 6: '',
			 7: '', 8: '', 9: ''}

	score_X = 0
	score_O = 0

	# handling turns

	point = False
	end = False
	win = False
	win_X = False
	win_O = False
	turn_X = True
	turn_O = False
	turns = [i for i in range(1, 10)]

	empty_cells = [i for i in range(1, 10)]
	drawn_cells = []


	# lists of taken cells
	player_X = []
	player_O = []

	# if tie
	tie_list = []
	tie = False

	while running:

		# draw screen and board
		screen.fill(WHITE)

		# creating board
		x = 170
		y = 130
		w = 120
		h = w
		# create the cells and put them in a list
		cells = []
		cells = create_board(x, y, w, h)

		# show score

		global WIDTH
		draw_text("X: " + str(score_X), font, BLUE, screen, 25, 25)
		draw_text("O: " + str(score_O), font, RED, screen, WIDTH-140, 25)

		# showing who's turn

		if turn_X:
			if not win and not tie:
				draw_text("X's turn", font, BLUE, screen, WIDTH//2-110, 30)
		if turn_O:
			pass


		# interacting with cells
		# managing who's turn is

		if turn_X and not win or not tie:
			for cell in cells:
				for click in clicks:
					if cell.collidepoint(click):
						pos = cells.index(cell) + 1
						if pos in empty_cells:
							turn_X, turn_O = switch_turns(turn_X , turn_O)

							# adding to player x so it works
							player_X.append(pos)

							empty_cells.remove(pos)
							drawn_cells.append(pos)

						# print(turn_X, turn_O)


		# why is here the same as before
		if not end:

			win, win_X = check_for_win(board)

			# print(win)
			if win:
				end = True # not sure what end is but anyways...
				if not win_X:
					win_O = True

			#putting X and O into dictionary
			for i in player_X:
				board[i] = 'X'

			for i in player_O:
				board[i] = 'O'

		# checking if tie
		
		if not win:
			tie = check_for_tie(board, turn_X)


		# STRONG opponent
		win, win_X = check_for_win(board)
		if turn_O and not win:
			impossible_AI(board)
			turn_X, turn_O = switch_turns(turn_X , turn_O)

			# player_O.append(pos)
			# empty_cells.remove(pos)
			# drawn_cells.append(pos)

		# check for circles to remove them from empty list
		for num in board:
			if board[num] == 'O':
				if num in empty_cells:
					empty_cells.remove(num)
					drawn_cells.append(num)


		# drawing crosses and circles

		draw_on_board(board, cells)


		# drawing lines when win

		x_line = 170
		y_line = 130
		draw_win_line(board, x_line, y_line)


		# adding point after win

		if win:
			if win_X and not point:
				score_X += 1
				point = True
			elif not win_X and not point:
				score_O += 1
				point = True

			if win_X:
				draw_text("X won!", font, (10, 98, 221), screen, WIDTH//2-100, 30)
			if not win_X:
				draw_text("O won!", font, (196, 4, 0), screen, WIDTH//2-100, 30)

			draw_text("SPACE for next round", font_try_again, PINK, screen, 150, 500)

		# controls and resetting variables
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
				if win or tie:
					if event.key == K_SPACE:

						# check who won
						turn_X = False
						turn_O = False
						if win_X:
							turn_O = True
						else:
							turn_X = True

						win = False
						tie = False
						win_X = False
						win_O = False
						end = False
						point = False
						player_X.clear()
						player_O.clear()
						clicks.clear()
						turns = [i for i in range(1, 10)]

						empty_cells = turns
						drawn_cells = []

						for i in board.keys():
							board[i] = ''

			if event.type == MOUSEBUTTONDOWN:
				if event.button == BUTTON_LEFT:
					mx, my = pygame.mouse.get_pos()
					clicks.append((mx, my))
				if win or tie:
					if event.button == BUTTON_LEFT:

						# check who won
						turn_X = False
						turn_O = False
						if win_X:
							turn_O = True
						else:
							turn_X = True

						win = False
						tie = False
						win_X = False
						win_O = False
						end = False
						point = False
						player_X.clear()
						player_O.clear()
						clicks.clear()
						turns = [i for i in range(1, 10)]

						empty_cells = turns
						drawn_cells = []

						for i in board.keys():
							board[i] = ''

		pygame.display.update()
		mainClock.tick(60)


def player_2():
	# booting the game
	running = True
	click = False

	clicks = []

	board = {1: '', 2: '', 3: '',
			 4: '', 5: '', 6: '',
			 7: '', 8: '', 9: ''}

	score_X = 0
	score_O = 0

	# handling turns

	point = False
	end = False
	win = False
	win_X = False
	win_O = False
	turn_X = True
	turn_O = False
	turns = [i for i in range(1, 10)]

	empty_cells = [i for i in range(1, 10)]
	drawn_cells = []


	# lists of taken cells
	player_X = []
	player_O = []

	# if tie
	tie_list = []
	tie = False

	while running:

		# draw screen and board
		screen.fill(WHITE)

		# creating board
		x = 170
		y = 130
		w = 120
		h = w
		# create the cells and put them in a list
		cells = []
		cells = create_board(x, y, w, h)

		# show score

		global WIDTH
		draw_text("X: " + str(score_X), font, BLUE, screen, 25, 25)
		draw_text("O: " + str(score_O), font, RED, screen, WIDTH-140, 25)

		# showing who's turn

		if turn_X:
			if not win and not tie:
				draw_text("X's turn", font, BLUE, screen, WIDTH//2-110, 30)
		if turn_O:
			if not win and not tie:
				draw_text("O's turn", font, RED, screen, WIDTH//2-110, 30)


		# interacting with cells
		# managing who's turn is

		if not win or not tie:
			for cell in cells:
				for click in clicks:
					if cell.collidepoint(click):
						pos = cells.index(cell) + 1
						if pos in empty_cells:
							turn_X, turn_O = switch_turns(turn_X , turn_O)

							# turns swapped
							if not turn_X:
								# adding to player x so it works
								player_X.append(pos)

							else:
								player_O.append(pos)

							empty_cells.remove(pos)
							drawn_cells.append(pos)


		# why is here the same as before
		if not end:

			win, win_X = check_for_win(board)

			# print(win)
			if win:
				end = True # not sure what end is but anyways...
				if not win_X:
					win_O = True

			#putting X and O into dictionary
			for i in player_X:
				board[i] = 'X'

			for i in player_O:
				board[i] = 'O'

		# checking if tie

		if not win:
			tie = check_for_tie(board, turn_X)


		# check for circles to remove them from empty list
		for num in board:
			if board[num] == 'O':
				if num in empty_cells:
					empty_cells.remove(num)
					drawn_cells.append(num)


		# drawing crosses and circles

		draw_on_board(board, cells)


		# drawing lines when win

		x_line = 170
		y_line = 130
		draw_win_line(board, x_line, y_line)


		# adding point after win

		if win:
			if win_X and not point:
				score_X += 1
				point = True
			elif not win_X and not point:
				score_O += 1
				point = True

			if win_X:
				draw_text("X won!", font, (10, 98, 221), screen, WIDTH//2-100, 30)
			if not win_X:
				draw_text("O won!", font, (196, 4, 0), screen, WIDTH//2-100, 30)

			draw_text("SPACE for next round", font_try_again, PINK, screen, 150, 500)

		# controls and resetting variables
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
				if win or tie:
					if event.key == K_SPACE:

						# check who won
						turn_X = False
						turn_O = False
						if win_X:
							turn_O = True
						else:
							turn_X = True

						win = False
						tie = False
						win_X = False
						win_O = False
						end = False
						point = False
						player_X.clear()
						player_O.clear()
						clicks.clear()
						turns = [i for i in range(1, 10)]

						empty_cells = turns
						drawn_cells = []

						for i in board.keys():
							board[i] = ''

			if event.type == MOUSEBUTTONDOWN:
				if event.button == BUTTON_LEFT:
					mx, my = pygame.mouse.get_pos()
					clicks.append((mx, my))
				if win or tie:
					if event.button == BUTTON_LEFT:

						# check who won
						turn_X = False
						turn_O = False
						if win_X:
							turn_O = True
						else:
							turn_X = True

						win = False
						tie = False
						win_X = False
						win_O = False
						end = False
						point = False
						player_X.clear()
						player_O.clear()
						clicks.clear()
						turns = [i for i in range(1, 10)]

						empty_cells = turns
						drawn_cells = []

						for i in board.keys():
							board[i] = ''

		pygame.display.update()
		mainClock.tick(60)


def select_skin_circle(x, y, directory):
	circle1 = pygame.Rect(x, y, 110, 110)
	pygame.draw.rect(screen, BLUE, circle1, 3)
	change_circle(directory)


def select_skin_cross(x, y, directory):
	circle1 = pygame.Rect(x, y, 110, 110)
	pygame.draw.rect(screen, RED, circle1, 3)
	change_cross(directory)


click_cross_x = 0
click_cross_y = 0
click_circle_x = 0
click_circle_y = 0


def options():
	running = True
	global click_cross_x
	global click_cross_y
	global click_circle_x
	global click_circle_y
	while running:

		# screen and text
		screen.fill(WHITE)
		draw_text('Options:', font, BLACK, screen, 10, 10)
		draw_text('Select skin:', font_me, BLACK, screen, 12, 110)

		# choosing skin
		x = 50
		y = 165
		w = 600
		h = 120
		circle_field = pygame.Rect(x, y, w, h)
		cross_field = pygame.Rect(x, y+140, w, h)
		pygame.draw.rect(screen, RED, circle_field, 5)
		pygame.draw.rect(screen, BLUE, cross_field, 5)

		# choosing skin for circles
		circle_black = pygame.Rect(x, y+5, 110, 110)
		circle_red = pygame.Rect(x+135, y+5, 110, 110)
		circle_orange = pygame.Rect(x+2*135, y+5, 110, 110)

		if circle_black.collidepoint((click_circle_x, click_circle_y)) or click_circle_x == 0:
			select_skin_circle(x+25, y+5, 'circle.png')

		if circle_red.collidepoint((click_circle_x, click_circle_y)):
			select_skin_circle(x+165, y+5, 'circlered.png')

		if circle_orange.collidepoint((click_circle_x, click_circle_y)):
			select_skin_circle(x+305, y+5, 'circleorange.png')

		draw_own('circle.png', 80, y+10, 100)
		draw_own('circlered.png', 220, y+10, 100)
		draw_own('circleorange.png', 360, y+10, 100)

		# choosing skin for crosses
		cross_black = pygame.Rect(x, y+145, 110, 110)
		cross_blue = pygame.Rect(x+135, y+145, 110, 110)
		cross_pink = pygame.Rect(x+2*135, y+145, 110, 110)

		if cross_black.collidepoint((click_cross_x, click_cross_y)) or click_cross_x == 0:
			select_skin_cross(x+25, y+145, 'cross.png')

		if cross_blue.collidepoint((click_cross_x, click_cross_y)):
			select_skin_cross(x+25+140, y+145, 'crossblue.png')

		if cross_pink.collidepoint((click_cross_x, click_cross_y)):
			select_skin_cross(x+25+2*140, y+145, 'crosspink.png')

		draw_own('cross.png', 80, y+150, 100)
		draw_own('crossblue.png', 220, y+150, 100)
		draw_own('crosspink.png', 360, y+150, 100)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == BUTTON_LEFT:
					mx, my = pygame.mouse.get_pos()
					if circle_field.collidepoint((mx, my)):
						click_circle_x = mx
						click_circle_y = my
					if cross_field.collidepoint((mx, my)):
						click_cross_x = mx
						click_cross_y = my

		pygame.display.update()
		mainClock.tick(60)


main_menu()
