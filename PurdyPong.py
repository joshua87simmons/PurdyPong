import pygame,sys,math,random
from pygame.locals import *

pygame.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN.fill((0,0,0))
pygame.display.set_caption("PurdyPong")
clock = pygame.time.Clock()
P_SCORE = 0
C_SCORE = 0


""" COMPONENTS """

class Position:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Size:
  def __init__(self, w, h):
    self.width = w
    self.height = h

class Velocity:
  def __init__(self, s, x, y):
    self.speed = s
    self.dirX = x
    self.dirY = y

class Controller:
  def __init__(self):
    self.isControllable = True

class Sound:
  def __init__(self, file):
#    self.sound = pygame.getsoundfile(...)
    pass



""" NODES """

class Moveable:
  def __init__(self, pos, vel):
    self.position = pos
    self.velocity = vel

class Renderable:
  def __init__(self, pos, size):
    self.position = pos
    self.size = size

class Audible:
  def __init__(self):
    pass



""" ENTITIES """

class Player:
  def __init__(self):
    self.size = Size(20,80)
    self.position = Position(20, (SCREEN_HEIGHT/2 - self.size.height/2))
    self.velocity = Velocity(20, 0, 0)

class Computer:
  def __init__(self):
    self.size = Size(20,80)
    self.position = Position((SCREEN_WIDTH - 20 - self.size.width), (SCREEN_HEIGHT/2 - self.size.height/2))
    self.velocity = Velocity(20, 0, 0)

class Ball:
  def __init__(self):
    self.size = Size(20,20)
    self.position = Position((SCREEN_WIDTH/2 - self.size.width/2), (SCREEN_HEIGHT/2 - self.size.height/2))
    self.velocity = Velocity(5, -1, -1)

  



""" SYSTEMS """

class InputSystem:
  def __init__(self, player):
    self.player = player
  def process(self, key):
    if key == K_UP:
      self.player.velocity.dirY = -1
    elif key == K_DOWN:
      self.player.velocity.dirY = 1
    else:
      self.player.velocity.dirY = 0

class BallCollisionSystem:
  def __init__(self, ball, paddles):
    self.ball = ball
    self.paddles = paddles
  def process(self):
    ballRect = Rect(self.ball.position.x, self.ball.position.y, self.ball.size.width, self.ball.size.height)
    # if collide with top or bottom wall
    if self.ball.position.y <= 0 or (self.ball.position.y + self.ball.size.height) >= SCREEN_HEIGHT:
      self.ball.velocity.dirY *= -1
    # if collide with paddle
    for p in self.paddles:
      paddleRect = Rect(p.position.x, p.position.y, p.size.width, p.size.height)
      if paddleRect.colliderect(ballRect):
        self.ball.velocity.dirX *= -1

class PaddleCollisionSystem:
  def __init__(self, paddles):
    self.paddles = paddles
  def process(self):
    for p in self.paddles:
      if p.position.y <= 0:
        p.position.y = 0
      if (p.position.y + p.size.height) >= SCREEN_HEIGHT:
        p.position.y = SCREEN_HEIGHT - p.size.height
    
class ScoreSystemP:
  def __init__(self, ball, P):
    self.ball = ball
    self.P = P
  def process(self, P):
    global P_SCORE
    if (self.ball.position.x + self.ball.size.width) >= SCREEN_WIDTH:
      self.ball.position.x = SCREEN_WIDTH/2 - self.ball.size.width/2
      self.ball.position.y = SCREEN_HEIGHT/2 - self.ball.size.height/2
      P_SCORE += 1
      return P_SCORE
class ScoreSystemC:
  def __init__(self, ball, C):
    self.ball = ball
    self.C = C
  def process(self):
    global C_SCORE
    # if collide with left or right wall
    if self.ball.position.x <= 0:
      self.ball.position.x = SCREEN_WIDTH/2 - self.ball.size.width/2
      self.ball.position.y = SCREEN_HEIGHT/2 - self.ball.size.height
      C_SCORE += 1
      return C_SCORE

class MovementSystem:
  def __init__(self, nodes):
    self.nodes = nodes
  def process(self):
    for n in self.nodes:
      n.position.x += n.velocity.dirX * n.velocity.speed
      n.position.y += n.velocity.dirY * n.velocity.speed

class RenderSystem:
  def __init__(self, nodes):
    self.nodes = nodes
  def process(self):
    SCREEN.fill((0,0,0))
    SCREEN.fill((255, 255, 255), ((SCREEN_WIDTH/2) - 10, 0, 10, SCREEN_HEIGHT))
    for n in self.nodes:
      surf = pygame.Surface((n.size.width, n.size.height))
      surf.fill((255,255,255))
      #pygame.Surface.blit(surf, SCREEN, (n.position.x, n.position.y, n.size.width, n.size.height))
      pygame.draw.rect(SCREEN, (255,255,255), (n.position.x, n.position.y, n.size.width, n.size.height))

class ScoreRenderSystem:
  def __init__(self, P, C):
    self.P = P
    self.C = C
  def process(self):
    global P_SCORE
    global C_SCORE
    p_font = pygame.font.Font(None, 100)
    p_text = p_font.render(str(P_SCORE), 1, (255, 255, 255))
    p_textpos = SCREEN.get_rect(center=((SCREEN_WIDTH) - 75, SCREEN_HEIGHT / 2))
    SCREEN.blit(p_text, p_textpos)
  
    c_font = pygame.font.Font(None, 100)
    c_text = c_font.render(str(C_SCORE), 1, (255, 255, 255))
    c_textpos = SCREEN.get_rect(center=((SCREEN_WIDTH + 28, SCREEN_HEIGHT / 2)))
    SCREEN.blit(c_text, c_textpos)
class AISystem:
  def __init__(self, ball, computer):
    self.computer = computer
    self.ball = ball
  def process(self):
    if self.ball.velocity.dirX < 0:
      if (self.computer.position.y + (self.computer.size.height / 2)) > (245):
        self.computer.position.y -= 10
      elif (self.computer.position.y + (self.computer.size.height / 2)) < (235):
        self.computer.position.y += 10
      else:
        self.computer.velocity.dirY = 0
    else:
      self.computer.position.y = self.ball.position.y - (self.computer.size.height / 2)
        



class NodeManager:
  def __init__(self, entities):
    self.moveables = []
    self.renderables = []
    for e in entities:
      if e.position and e.velocity:
        self.moveables.append(e)
      if e.position and e.size:
        self.renderables.append(e)



def main():
  player = Player()
  computer = Computer()
  ball = Ball()

  nm = NodeManager([player, computer, ball])
  inputSystem = InputSystem(player)
  ballCollisionSystem = BallCollisionSystem(ball, (player, computer))
  paddleCollisionSystem = PaddleCollisionSystem((player, computer))
  scoreSystemP = ScoreSystemP(ball, 0)
  scoreSystemC = ScoreSystemC(ball, 0)
  movementSystem = MovementSystem(nm.moveables)
  renderSystem = RenderSystem(nm.renderables)
  scoreRenderSystem = ScoreRenderSystem(scoreSystemP.P, scoreSystemC.C)
  aiSystem = AISystem(ball, computer)
  
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
        running = False
      elif event.type == KEYDOWN:
        inputSystem.process(event.key)
      elif event.type == KEYUP:
        player.velocity.dirY = 0
    ballCollisionSystem.process()
    paddleCollisionSystem.process()
    scoreSystemP.process(P_SCORE)
    scoreSystemC.process()
    movementSystem.process()
    renderSystem.process()
    aiSystem.process()
    scoreRenderSystem.process()
    pygame.display.update()
    clock.tick(30)
    

  pygame.quit()
  sys.exit()

if __name__ == "__main__": main()
