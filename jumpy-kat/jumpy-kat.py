import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def create_bread():
    random_bread_pos = random.choice(bread_height)
    bottom_bread = bread_surface.get_rect(midtop = (700,random_bread_pos ))
    top_bread = bread_surface.get_rect(midbottom=(700, random_bread_pos - 300))
    return bottom_bread, top_bread

def move_bread(breads):
    for bread in breads:
        bread.centerx -= 5
    return breads

def draw_bread(breads):
    for bread in breads:
        if bread.bottom >= 1024:
            screen.blit(bread_surface,bread)
        else:
            flip_bread = pygame.transform.flip(bread_surface,False,True)
            screen.blit(flip_bread,bread)

def check_collision(breads):
    for bread in breads:
        if cat_rect.colliderect(bread):
            death_sound.play()
            return False

    if cat_rect.top <= -100 or cat_rect.bottom >= 900:
        death_sound.play()
        return False

    return True

def rotate_cat(cat):
    new_cat = pygame.transform.rotozoom(cat,-cat_movement*3,1)
    return new_cat

def cat_animation():
    new_cat = cat_frames[cat_index]
    new_cat_rect = new_cat.get_rect(center = (100,cat_rect.centery))
    return new_cat, new_cat_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,800))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576,1024))
keys = pygame.key.get_pressed()
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)

# Game Variables
gravity = 0.15
cat_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/bg-sunset.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/pink.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

cat_norm = pygame.transform.scale2x(pygame.image.load('assets/norm.png').convert_alpha())
cat_jump = pygame.transform.scale2x(pygame.image.load('assets/up.png').convert_alpha())
cat_glide = pygame.transform.scale2x(pygame.image.load('assets/upper.png').convert_alpha())
cat_frames = [cat_norm, cat_jump, cat_glide]
cat_index = 0
cat_surface = cat_frames[cat_index]
cat_rect = cat_surface.get_rect(center=(100, 512))

CATJUMP = pygame.USEREVENT + 1
pygame.time.set_timer(CATJUMP, 200)

#cat_surface = pygame.image.load('assets/upper.png').convert_alpha()
#cat_surface = pygame.transform.scale2x(cat_surface)
#cat_rect = cat_surface.get_rect(center = (100,512))

bread_surface = pygame.image.load('assets/bread.png')
bread_surface = pygame.transform.scale2x(bread_surface)
bread_list = []
SPAWNBREAD = pygame.USEREVENT
pygame.time.set_timer(SPAWNBREAD, 1200)
bread_height = [400,600,800]

game_over_surface = pygame.image.load('assets/intro3.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (288,512))

game_over_line = pygame.image.load('assets/game_over.png').convert_alpha()
game_over_line_rect = game_over_line.get_rect(center = (288,512))

jump_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                cat_movement = 0
                cat_movement -= 8
                jump_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                bread_list.clear()
                cat_rect.center = (100,512)
                cat_movement = 0
                score = 0

        if event.type == SPAWNBREAD:
            bread_list.extend(create_bread())

        if event.type == CATJUMP:
            if cat_index < 2:
                cat_index += 1
            else:
                cat_index = 0

            cat_surface, cat_rect = cat_animation()

    screen.blit(bg_surface,(0,0))

    if game_active:
        # Cat
        cat_movement += gravity
        rotated_cat = rotate_cat(cat_surface)
        cat_rect.centery += cat_movement
        screen.blit(rotated_cat,cat_rect)
        game_active = check_collision(bread_list)

        # Bread
        bread_list = move_bread(bread_list)
        draw_bread(bread_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        # screen.blit(game_over_line,game_over_line_rect)
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')



    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0





    pygame.display.update()
    clock.tick(120)
