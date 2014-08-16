# This program displays prerendered visuals that move across the screen. On hitting the boundaries, the shapes randomly change their color.
# The software is intended to be used with appropriate eeg capture software and binaural beats audio playback.

from pygame import *
import random

BALL_SIZE = 0
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

FPS = 60

red_count = 0

class Ball(sprite.Sprite):
    def __init__(self, xy = (0,0), xm = 1, ym = 1):
        sprite.Sprite.__init__(self)
        rnd_nr = random.randint(1,3)
        self.img_load('img/monkey' + str(rnd_nr) + '.png')
        global red_count
        if rnd_nr == 1:
            red_count += 1

        self.rect.centerx, self.rect.centery = xy

        self.xmove = xm
        self.ymove = ym

    def update(self):
        self.move()
        self.ballBarrier()

    def move(self):
        self.rect.x += self.xmove
        self.rect.y += self.ymove

    def img_load(self, filename):
        self.image = image.load(filename)
        self.rect = self.image.get_rect()

    def img_update(self, filename):
        rect.centerx = self.rect.centerx
        rect.centery = self.rect.centery
        self.image = image.load(filename)
        self.rect.centerx = rect.centerx
        self.rect.centery = rect.centery

    def ballBarrier(self):
        """
        Checks to make sure ball is within bounds, adjusts movement speed if it's not
        """
        rnd_nr = random.randint(1,3)
        global red_count
        if self.rect.right > (SCREEN_WIDTH + BALL_SIZE):
            self.xmove = random.randint(-2, -1)
            self.img_update('img/monkey' + str(rnd_nr) + '.png')   
            if rnd_nr == 1:
                red_count += 1
        if self.rect.left < (0 - BALL_SIZE):
            self.xmove = random.randint(1, 2)
            self.img_update('img/monkey' + str(rnd_nr) + '.png')   
            if rnd_nr == 1:
                red_count += 1
        if self.rect.bottom > (SCREEN_HEIGHT + BALL_SIZE):
            self.ymove = random.randint(-2, -1)
            self.img_update('img/monkey' + str(rnd_nr) + '.png')   
            if rnd_nr == 1:
                red_count += 1
        if self.rect.top < (0 - BALL_SIZE):
            self.ymove = random.randint(1, 2)
            self.img_update('img/monkey' + str(rnd_nr) + '.png')   
            if rnd_nr == 1:
                 red_count += 1


class ball_manager():
    def __init__(self, numballs = 5, balls = []):      
        self.blist = balls

        if numballs > 0:
            self.multipleBalls(numballs) # moved this here so balls get init'd only once

    def update(self):
        """
        Update position of all balls
        """
        for ball in self.blist:
            self.ballMove(ball)

    def add_ball(self, xy = (0,0), xm = 1, ym = 1):
        self.blist.append(Ball(xy, xm, ym)) # appends a random ball

    def multipleBalls(self, numballs):
        for i in range(numballs):
            self.add_ball((random.randint(0, SCREEN_WIDTH),
                          random.randint(0, SCREEN_HEIGHT)),
                          random.choice([-2,-1,1,2]),
                          random.choice([-2,-1,1,2]))

class Game(object):
    def __init__(self):
        init()
        key.set_repeat(1, 30)
        self.screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg= Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg.fill((0,0,0))
        
        self.clock = time.Clock()
        display.set_caption('Game')


        event.set_allowed([QUIT, KEYDOWN, KEYUP])
        self.screen.blit(self.bg, (0,0))
        display.flip()

        self.sprites = sprite.RenderUpdates()

        self.balls = ball_manager(5)

        for ball in self.balls.blist:
            self.sprites.add(ball)

    def run(self):
        global red_count
        running = True
        while running == True:
            self.clock.tick(FPS)
            running = self.handleEvents()
            display.set_caption('game %d fps' % self.clock.get_fps())

            self.sprites.clear(self.screen, self.bg)

            for sprite in self.sprites:
                sprite.update()

            dirty = self.sprites.draw(self.screen)
            display.update(dirty)
        print("red count = " + str(red_count))


    def handleEvents(self):
        for e in event.get():
            if e.type == QUIT:
                return False

            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    return False
                if e.key == K_UP:
                    self.character.up()
                if e.key == K_DOWN:
                    self.character.down()
                if e.key == K_r:
                   self.sprites.add(Ball((random.randint(0, SCREEN_WIDTH),
                          random.randint(0, SCREEN_HEIGHT)),
                          random.randint(-2,2),
                          random.randint(-2,2))) 


        return True

def main():
    game = Game()
    game.run()
    quit()

main()
