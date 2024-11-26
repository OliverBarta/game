import pygame as pg
from random import *
import time

pg.init()

#pg.mixer.init()

WIDTH = 600#the width of the screen
HEIGHT = 600#the height of the screen

mouse_x = 0#the x coordinate of the mouse
mouse_y = 0#the y coordinate of the mouse

bomb_posibl = []
for x in range(1,101):
  bomb_posibl.append(x)
#hit_sound = pg.mixer.Sound("hit_sound.mp3")
#miss_sound = pg.mixer.Sound("miss_sound.mp3")
#victory_sound = pg.mixer.Sound("victory.mp3")
#defeat_sound = pg.mixer.Sound("defeat_sound.mp3")


left_clicked = False#if the user left clicks this is true
right_clicked = False#if the user right clicks this is true

num_left_clicks = 1#the number of left clicks

who_won = "nobody"#this is saving who won, either the computer or the player won

orientation = "side"#the orientation of a ship

screen = pg.display.set_mode((WIDTH,HEIGHT))#the screen set up
pg.display.set_caption("Battleship")#the caption set up

BebasNeue = pg.font.Font("BebasNeue Regular.otf", 40)#sets up the font

ship_num = 1#which ship we are placing

def remove_duplicates(list):
  """takes a list and returns that list with all duplicates in the list removed"""
  new_list = []
  for item in list:
    if item not in new_list:
      new_list.append(item)
  return new_list

def mouse_to_pos(x,y):
  """sets the position of a ship to allign with the grid and makes sure to keep the ship on the grid"""
  x = x-x%60
  y = y-y%60
  if x+(size*60) > 600 and orientation == "side" or y+(size*60) > 600 and orientation == "up":
    if orientation == "side":
      x = 540-((size-1)*60)
    if orientation == "up":
      y = 540-((size-1)*60)
  return (int(x),int(y))

class Board:
  """Creates a grid for the battle ship game to be played on and a background"""
  def __init__(self, num_grid_line = 10, color = "blue"):
    self.num_grid_line = num_grid_line#i added this variable for future customization but never be anything except 10. It doesn't need to be here but I'll leave it if I ever want to use it
    self.color = color#this deosn't decide the color just decides the image to use
  def draw_grid(self):
    """draws the grid and the background"""
    if self.color == "blue":#the user background (blue)
      blue_sharks = pg.image.load("water_with_sharks.jpg")
      blue_sharks = pg.transform.scale(blue_sharks, (600,600))
      screen.blit(blue_sharks, (0,0))
    elif self.color == "red":#the computer background (red)
      red_waves = pg.image.load("summer-background-red-water-waves-footage-088548081_prevstill_1.webp")
      red_waves = pg.transform.scale(red_waves, (600, 600))
      screen.blit(red_waves, (0,0))
    for x in range(self.num_grid_line):#draws the grid
      pg.draw.line(screen, (0,0,0), (((WIDTH/self.num_grid_line)*(x+1)),0), ((WIDTH/self.num_grid_line)*(x+1),HEIGHT))
      pg.draw.line(screen, (0,0,0), (0,((HEIGHT/self.num_grid_line)*(x+1))), (WIDTH,((HEIGHT/self.num_grid_line)*(x+1))))

class Ship:
  """creates, draws, hovers and returns info about the ships"""
  def __init__(self, siz, orient, posx, posy):
    self.siz = siz#the size of the ship
    self.orient = orient#the orientation of the ship
    self.posx = posx#the x coordinate of the top left of the ship
    self.posy = posy#the y coordinate of the top left of the ship

  def hover_ship(self):
    """hovers the ship, used when placing ships"""
    if self.orient == "side":#for horizontal ships
      pg.draw.rect(screen, (0,80,20), ((self.posx, self.posy),(self.siz*60,60)), border_radius = 30)
    elif self.orient == "up":#for vertical ships
      pg.draw.rect(screen, (0,80,20), ((self.posx, self.posy),(60,self.siz*60)), border_radius = 30)
  def place_ship(self, saved_pos):
    """places ships"""
    self.saved_pos = saved_pos
    if self.orient == "side":#for horizontal ships
      battle_ship = pg.image.load("battle_ship_top_down_edited.png")#loads image of ship
      battle_ship = pg.transform.scale(battle_ship, (self.siz*60,60))#scales image of ship for size
      screen.blit(battle_ship, (saved_pos[0],saved_pos[1]))
    elif self.orient == "up":#for vertical ships
      battle_ship = pg.image.load("battle_ship_top_down_edited.png")#loads image of ship
      battle_ship = pg.transform.rotate(battle_ship, 90)#rotates ship or else ship wouldn't be oriented correctly
      battle_ship = pg.transform.scale(battle_ship, (60,self.siz*60))#scales image of ship for size
      screen.blit(battle_ship, (saved_pos[0],saved_pos[1]))
  def pos(self):
    """returns the position of a ship"""
    return self.saved_pos
  def ship_square(self):
    """returns a list of the ships squares it is covering"""
    psiblx = []
    psibly = []
    final = []
    for x in range(10):
      psiblx.append(int(self.saved_pos[0]/60+1+10*x))
    for y in range(10):
      psibly.append(int(self.saved_pos[1]/60*10+y+1))
    for x in psiblx:
      for y in psibly:
        if x == y:
          final.append(x)
    if self.orient == "up":
      for y in range(self.siz-1):
        final.append(final[y]+10)
    elif self.orient == "side":
      for x in range(self.siz-1):
        final.append(final[x]+1)
    return final



size = 3#the size of a ship

Board1 = Board(color = "blue")#the players board
Board1.draw_grid()

while True:
  Board1.draw_grid()#draws the players board
  text = BebasNeue.render("Place your ships", False, (255,255,255))#sets up text
  text_rect = text.get_rect() #makes a rectangle for the "Place your ships" text
  text_rect.centerx = 600/2 #centers the "Place your ships" text
  screen.blit(text, text_rect)#places text
  if right_clicked == True: #makes it so that after the user right clicks it doesn't stay at right clicked forever
    right_clicked = False
  if left_clicked == True:#makes it so that after the user left clicks it doesn't stay at left clicked forever
    num_left_clicks += 1
    left_clicked = False
  for event in pg.event.get():#the code for the clicks
    if event.type == pg.MOUSEMOTION:
      mouse_x = pg.mouse.get_pos()[0]
      mouse_y = pg.mouse.get_pos()[1]
    if event.type == pg.MOUSEBUTTONDOWN:
      left_clicked = pg.mouse.get_pressed()[0]
      right_clicked = pg.mouse.get_pressed()[2]
  pressed_keys = pg.key.get_pressed()
  if pressed_keys[pg.K_UP]:#the code for the arrow keys (they change the size of a ship)
    size = 4
  elif pressed_keys[pg.K_DOWN]:
    size = 1
  elif pressed_keys[pg.K_RIGHT]:
    size = 3
  elif pressed_keys[pg.K_LEFT]:
    size = 2
  if num_left_clicks%2 == 0:#changes orientation based on numbers of left clicks
    orientation = "up"
  else:
    orientation = "side"

  if ship_num == 1:#hovers ship 1, when the user right clicks it places the ship and saves the location. The next 4 elifs do that with the other ships.
    ship1 = Ship(size,orientation, mouse_x, mouse_y)
    ship1.hover_ship()
    if right_clicked == True:
      saved_pos1 = (mouse_to_pos(mouse_x, mouse_y))
      ship1.place_ship(saved_pos1)
      ship_num+=1
  elif ship_num == 2:
    ship2 = Ship(size,orientation, mouse_x, mouse_y)
    ship2.hover_ship()
    ship1.place_ship(saved_pos1)
    if right_clicked == True:
      saved_pos2 = (mouse_to_pos(mouse_x, mouse_y))
      ship2.place_ship(saved_pos2)
      ship_num+=1
  elif ship_num == 3:
    ship3 = Ship(size,orientation, mouse_x, mouse_y)
    ship3.hover_ship()
    ship1.place_ship(saved_pos1)
    ship2.place_ship(saved_pos2)
    if right_clicked == True:
      saved_pos3 = (mouse_to_pos(mouse_x, mouse_y))
      ship3.place_ship(saved_pos3)
      ship_num+=1
  elif ship_num == 4:
    ship4 = Ship(size,orientation, mouse_x, mouse_y)
    ship4.hover_ship()
    ship1.place_ship(saved_pos1)
    ship2.place_ship(saved_pos2)
    ship3.place_ship(saved_pos3)
    if right_clicked == True:
      saved_pos4 = (mouse_to_pos(mouse_x, mouse_y))
      ship4.place_ship(saved_pos4)
      ship_num+=1
  elif ship_num == 5:
    ship5 = Ship(size,orientation, mouse_x, mouse_y)
    ship5.hover_ship()
    ship1.place_ship(saved_pos1)
    ship2.place_ship(saved_pos2)
    ship3.place_ship(saved_pos3)
    ship4.place_ship(saved_pos4)
    if right_clicked == True:
      saved_pos5 = (mouse_to_pos(mouse_x, mouse_y))
      ship5.place_ship(saved_pos5)
      ship_num+=1
      break
  pg.display.update()

def square_to_pos(square):
  """returns the grid position of a square"""
  square = int(square)
  extra = square%10
  if extra == 0:
    x = 540
  else:
    x = (extra-1)*60
  squarey = square-extra
  if x == 540:
    y = (squarey/10)-1
  else:
    y = squarey/10
  y = y*60
  return (int(x),int(y))

#lines 233-250 make lists of the ships positions on the grid and squares they occupy
ship_squares = []
ship_squares1 = []
ship_squares1.append(ship1.ship_square())
ship_squares1.append(ship2.ship_square())
ship_squares1.append(ship3.ship_square())
ship_squares1.append(ship4.ship_square())
ship_squares1.append(ship5.ship_square())

for square in ship_squares1:
  for x in square:
    ship_squares.append(x)


ship_squares = remove_duplicates(ship_squares)

ship_pos = []
for square in ship_squares:
  ship_pos.append(square_to_pos(square))


Board2 = Board(color = "red")#the computers board (with red image background)

enemy_ship_squares1 = []#a temporary list that holds the enemy ships squares

for x in range(5):#creates and places 5 randomly sized, oriented, and positioned enemy ships
  orientation = randint(1,2)
  if orientation == 1:
    orientation = "side"
  if orientation == 2:
    orientation = "up"
  size = randint(1,4)
  enemy_ship_pos = mouse_to_pos(randint(1,599),randint(1,599))
  if x == 0:
    enemy_ship_1 = Ship(size, orientation, enemy_ship_pos[0], enemy_ship_pos[1])
    enemy_ship_1.place_ship(enemy_ship_pos)
  elif x == 1:
    enemy_ship_2 = Ship(size, orientation, enemy_ship_pos[0], enemy_ship_pos[1])
    enemy_ship_2.place_ship(enemy_ship_pos)
  elif x == 2:
    enemy_ship_3 = Ship(size, orientation, enemy_ship_pos[0], enemy_ship_pos[1])
    enemy_ship_3.place_ship(enemy_ship_pos)
  elif x == 3:
    enemy_ship_4 = Ship(size, orientation, enemy_ship_pos[0], enemy_ship_pos[1])
    enemy_ship_4.place_ship(enemy_ship_pos)
  elif x == 4:
    enemy_ship_5 = Ship(size, orientation, enemy_ship_pos[0], enemy_ship_pos[1])
    enemy_ship_5.place_ship(enemy_ship_pos)

#lines 279-294 creat 2 lists one of enemy ship positions the other of enemy ship squares
enemy_ship_squares1.append(enemy_ship_1.ship_square())
enemy_ship_squares1.append(enemy_ship_2.ship_square())
enemy_ship_squares1.append(enemy_ship_3.ship_square())
enemy_ship_squares1.append(enemy_ship_4.ship_square())
enemy_ship_squares1.append(enemy_ship_5.ship_square())

enemy_ship_squares = []

for square in enemy_ship_squares1:
  for x in square:
    enemy_ship_squares.append(x)

enemy_ship_squares = remove_duplicates(enemy_ship_squares)
enemy_ship_positions = []
for square in enemy_ship_squares:
  enemy_ship_positions.append(square_to_pos(square))


def pos_to_60(x,y):
  """makes a position anywhere snap to the grid by putting it in the nearest top left corner of the grid square"""
  return (int(x-x%60),int(y-y%60))


player_turn = True#true if it is the players turn false if it is the computers turn
bombs_miss_pos = []#the grid positions of the bombs the player has lanched that have missed
bombs_hit_pos = []#the grid positions of the bombs the player has lanched that have hit

bom_mis_enemy = []#the squares of the bombs the computer has lanched that have missed
bom_hit_enemy = []#the sqaures of the bombs the computer has lanched that have hit
bomb_place = 101#where the next bomb is being placed
bom_hit_enemy_pos = []#the grid positions of the bombs the computer has lanched that have hit

while True:#this loop is the back and forth part of the game
  while player_turn:#this loop is for the players turn
    attacking = True#this allows the computer to attack when it is not the players turn
    Board2.draw_grid()#draws the computer grid
    for bom in bombs_miss_pos:#draws the bombs the player has missed
      pg.draw.circle(screen, (220,255,255),(bom[0]+30,bom[1]+30),20)
    for bom in bombs_hit_pos:#draws the bombs the player has hit
      fire_image = pg.image.load("fire_image.png")
      fire_image = pg.transform.scale(fire_image, (60,60))
      screen.blit(fire_image, (bom[0],bom[1]))
    text = BebasNeue.render("Attack!", True, (255,255,255))#the text for attacking
    screen.blit(text, text_rect)
    pg.display.update()
    if left_clicked:#makes it so that left_clicked isnt true forever after being clicked
      left_clicked = False
    for event in pg.event.get():#the code for the clicks
      if event.type == pg.MOUSEMOTION:
        mouse_x = pg.mouse.get_pos()[0]
        mouse_y = pg.mouse.get_pos()[1]
      if event.type == pg.MOUSEBUTTONDOWN:
        left_clicked = pg.mouse.get_pressed()[0]
    if left_clicked:#when the player attacks
      player_turn = False
      #len_miss = len(bombs_miss_pos)#this would run but its only use was for sound
      #len_hit = len(bombs_hit_pos)
      if pos_to_60(mouse_x, mouse_y) in bombs_miss_pos:#this makes it so that if you click on a square you have already missed on it doesn't use your turn
        player_turn = True
      else:
        for square in enemy_ship_squares:
          if pos_to_60(mouse_x,mouse_y) == square_to_pos(square):#if the player hit a square with a ship in it
            bombs_hit_pos.append(pos_to_60(mouse_x, mouse_y))#adds position to the hit list
            bombs_hit_pos = remove_duplicates(bombs_hit_pos)#removes duplacites
            bombs_miss_pos = remove_duplicates(bombs_miss_pos)
            if len(bombs_hit_pos) == len (enemy_ship_positions):#checking for win
              who_won = "player"
              break
            player_turn = True
          else:
            if square_to_pos(square) not in bombs_hit_pos and square_to_pos(square) not in bombs_miss_pos:#checking if this square has already been clicked
              bombs_miss_pos.append(pos_to_60(mouse_x, mouse_y))#adds position to miss list
              bombs_hit_pos = remove_duplicates(bombs_hit_pos)#removes duplicates
              bombs_miss_pos = remove_duplicates(bombs_miss_pos)

              if len(bombs_hit_pos) == len (enemy_ship_positions):#checking for win
                who_won = "player"
                break
            
      bombs_hit_pos = remove_duplicates(bombs_hit_pos)#removes duplicates
      bombs_miss_pos = remove_duplicates(bombs_miss_pos)
      #if len(bombs_hit_pos) > len_hit:
       # pg.mixer.Sound.play(hit_sound)
      #elif len(bombs_miss_pos) > len_miss:
       # pg.mixer.Sound.play(miss_sound)
      #else:
       # pg.mixer.Sound.play(miss_sound)
    pg.display.update()
  if len(bombs_hit_pos) == len (enemy_ship_positions):#checking for win
    who_won = "player"
    break
  start_time = time.time()#saves tge time when the computers turn is starting
  while player_turn == False:
    Board1.draw_grid()#draws the players grid and ships
    ship1.place_ship(saved_pos1)
    ship2.place_ship(saved_pos2)
    ship3.place_ship(saved_pos3)
    ship4.place_ship(saved_pos4)
    ship5.place_ship(saved_pos5)
    for bomb in bom_mis_enemy:#draws hit and missed bombs for computer
      pg.draw.circle(screen, (255,255,255), (square_to_pos(bomb)[0]+30,square_to_pos(bomb)[1]+30), 20)
    for bomb in bom_hit_enemy:
      fire_image = pg.image.load("fire_image.png")
      fire_image = pg.transform.scale(fire_image, (60,60))
      screen.blit(fire_image, (square_to_pos(bomb)[0],square_to_pos(bomb)[1]))
    text = BebasNeue.render("Computer Attacking", True, (255,255,255))#computer attacking text
    screen.blit(text, text_rect)
    pg.display.update()
    if time.time() >= start_time+1:#if it has been too long it ends the computers turn
      player_turn = True
    while attacking:#when the computer is attacking
      while bomb_place in bom_hit_enemy or bomb_place in bom_mis_enemy or bomb_place > 100 or bomb_place < 1:
        #this loop contains the code for the target selection for the computer, it makes the computer not brainless
        bomb_place = randint(1,100)
        if len(bom_hit_enemy) > 0:
          for hits in bom_hit_enemy:
            if (hits+1) not in bom_hit_enemy and (hits+1) not in bom_mis_enemy and hits%10 != 0:
              bomb_place = hits+1
              break
            elif (hits-1) not in bom_hit_enemy and (hits-1) not in bom_mis_enemy and hits%10 != 1:
              bomb_place = hits-1
              break
            elif (hits+10) not in bom_hit_enemy and (hits+10) not in bom_mis_enemy and hits < 90:
              bomb_place = hits+10
              break
            elif (hits-10) not in bom_hit_enemy and (hits-10) not in bom_mis_enemy and hits > 10:
              bomb_place = hits-10
              break
        if len(bom_hit_enemy_pos) == len(ship_pos):#checks for wins
          who_won = "computer"
          break
      if len(bom_hit_enemy_pos) == len(ship_pos):#checks for wins
        who_won = "computer"
        break
      if bomb_place in ship_squares:
        bom_hit_enemy.append(bomb_place)
        bom_hit_enemy_pos.append(square_to_pos(bomb_place))
        bom_mis_enemy = remove_duplicates(bom_mis_enemy)
        bom_hit_enemy = remove_duplicates(bom_hit_enemy)
        bom_hit_enemy_pos = remove_duplicates(bom_hit_enemy_pos)
        if len(bom_hit_enemy_pos) == len(ship_pos):#checks for wins
          who_won = "computer"
          break
      else:
        bom_mis_enemy.append(bomb_place)#adding bomb square to missed list
        bom_mis_enemy = remove_duplicates(bom_mis_enemy)#removing duplicates
        bom_hit_enemy = remove_duplicates(bom_hit_enemy)
        bom_hit_enemy_pos = remove_duplicates(bom_hit_enemy_pos)
        if len(bom_hit_enemy_pos) == len(ship_pos):#checks for wins
          who_won = "computer"
          break
        attacking = False
  bom_mis_enemy = remove_duplicates(bom_mis_enemy)#removing duplicates
  bom_hit_enemy = remove_duplicates(bom_hit_enemy)
  bom_hit_enemy_pos = remove_duplicates(bom_hit_enemy_pos)
  if len(bom_hit_enemy_pos) == len(ship_pos):#checks for wins
    who_won = "computer"
    break
  pg.display.update()

if who_won == "computer":#for computer win
  print("computer wins!")
  #pg.mixer.Sound.play(defeat_sound)
  while True:
    wins = pg.image.load("49125-gravity-brings-battleship-live-board-game-life.jpg")
    wins = pg.transform.scale(wins, (600,600))
    screen.blit(wins, (0,0))
    text = BebasNeue.render("Computer Wins!", True, (255,255,255))
    text_rect = text.get_rect() #makes a rectangle for the "You Win!" text
    text_rect.centerx = 600/2 #centers the "You Win!" text
    text_rect.centery = 600/2 #centers the "You Win!" text
    screen.blit(text, text_rect)
    pg.display.update()


elif who_won == "player":#for player win
  print("Player wins!")
  #pg.mixer.Sound.play(victory_sound)
  while True:
    wins = pg.image.load("49125-gravity-brings-battleship-live-board-game-life.jpg")
    wins = pg.transform.scale(wins, (600,600))
    screen.blit(wins, (0,0))
    text = BebasNeue.render("You Win!", True, (255,255,255))
    text_rect = text.get_rect() #makes a rectangle for the "You Win!" text
    text_rect.centerx = 600/2 #centers the "You Win!" text
    text_rect.centery = 600/2 #centers the "You Win!" text
    screen.blit(text, text_rect)
    pg.display.update()