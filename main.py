import pygame, sys, random
from time import sleep, time


def make_floor():
	screen.blit(floor, (floor_x,600))
	screen.blit(floor, (floor_x + 500,600))

def make_pipe():
	random_height = random.choice(pipe_height)
	bottom_pipe = pipe.get_rect(midtop = (700, random_height))
	top_pipe = pipe.get_rect(midbottom = (700, random_height - 250))
	return bottom_pipe, top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 2
	return pipes

def draw_pipes(pipes):
	for pipe_loc in pipes:
		if pipe_loc.bottom >= 700:
			screen.blit(pipe, pipe_loc)
		else:
			flipped_pipe = pygame.transform.flip(pipe, False, True)
			screen.blit(flipped_pipe, pipe_loc)


def if_collision(pipes):
	for pipe in pipes:
		if ball_rect.colliderect(pipe):
			return False
	if ball_rect.top <= -100 or ball_rect.bottom >= 600:
		return False
	return True

def rotate_ball(ball):
	ball_falling = pygame.transform.rotozoom(ball, -ball_move *5,1)
	return ball_falling

def show_score(score):
	score_display = text.render('Score: ' + str(int(score)), True, (255,255,255))
	score_rect = score_display.get_rect(center = (55, 30))
	screen.blit(score_display, score_rect)

	score_display = text.render('High Score: ' + str(int(high_score)), True, (255,255,255))
	score_rect = score_display.get_rect(center = (80, 58))
	screen.blit(score_display, score_rect)

def update_high_score(score,high_score):
	if score > high_score:
		high_score = score
	return high_score

alive = True				

pygame.init()
screen = pygame.display.set_mode((500, 700))
clock = pygame.time.Clock()
bg = pygame.image.load('project/background2.png').convert()
text = pygame.font.Font('project/Pixeboy-z8XGD.ttf', 25)
game_over = pygame.font.Font('project/Pixeboy-z8XGD.ttf', 45)

gravity = 0.25
ball_move = 0

score = 0
high_score = 0

#FLOOR VAR
floor = pygame.image.load('project/floor.png').convert()
floor = pygame.transform.scale(floor, (800, 150))
floor_x = 0

#BALL VAR
ball = pygame.image.load('project/ball.png').convert_alpha()
ball = pygame.transform.scale(ball,(40,40))
ball_rect = ball.get_rect(center = (70, 300))


#PIPES
pipe = pygame.image.load('project/pipe.png').convert_alpha()
pipe = pygame.transform.scale(pipe, (70, 450))
pipe_list = []
MAKEPIPE = pygame.USEREVENT
pygame.time.set_timer(MAKEPIPE, 1200)
pipe_height = [300, 400, 500, 650]


last_time = time() 

while True:
	for event in pygame.event.get(): #pygame looks for all events happening right now
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				ball_move = 0
				ball_move -= 7  

			if event.key == pygame.K_SPACE and alive == False:
				pipe_list = []
				ball_rect.center = (70, 300)
				bird_movement = 0
				score = 0
				alive = True
				last_time = time() - 1



		if event.type == MAKEPIPE:
			pipe_list.extend(make_pipe()) 

	screen.blit(bg, (0,0))

	if alive:
		#BIRD MOVE
		ball_move += gravity
		falling = rotate_ball(ball)

		ball_rect.centery += ball_move
		screen.blit(falling, ball_rect)


		#PIPE MOVE
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)
		show_score(score)
		high_score = update_high_score(score, high_score)
		if time()-last_time > 3:
			score += 0.008

		alive = if_collision(pipe_list)


	if not alive:
		game_over_text = game_over.render('GAME OVER', True, (255,255,255))
		go_rect = game_over_text.get_rect(center = (250, 220))
		screen.blit(game_over_text, go_rect)

		end_text = text.render('PRESS SPACE TO PLAY AGAIN', True, (255,255,255))
		end_text_rect = end_text.get_rect(center = (250, 250))
		screen.blit(end_text, end_text_rect)

		score_display = text.render('Score: ' + str(int(score)), True, (255,255,255))
		score_rect = score_display.get_rect(center = (250, 300))
		screen.blit(score_display, score_rect)

		score_display = text.render('High Score: ' + str(int(high_score)), True, (255,255,255))
		score_rect = score_display.get_rect(center = (250, 320))
		screen.blit(score_display, score_rect)

	floor_x -= 1
	make_floor()
	if floor_x <= -500:
		floor_x = 0

	pygame.display.update() #takes anything from the while loop and draws it
	clock.tick(120)