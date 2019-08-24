import sys, pygame, pygame.mixer, pygame.locals, pygame.gfxdraw, random
pygame.init()

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png')]

CwalkRight = [pygame.image.load('CR1.png'), pygame.image.load('CR2.png'), pygame.image.load('CR3.png'), pygame.image.load('CR4.png')]
CwalkLeft = [pygame.image.load('CL1.png'), pygame.image.load('CL2.png'), pygame.image.load('CL3.png'), pygame.image.load('CL4.png')]

driveRight = pygame.image.load('SOCR.png')
driveLeft = pygame.image.load('SOCL.png')

bg = pygame.image.load('bg.png')
dead = pygame.image.load('dead.png')
size = width, height = 1080, 720
display = pygame.display.set_mode(size)
score = 0

class time(object):
    last = pygame.time.get_ticks()
    cooldown = random.randint(0, 500)
    
class etime(object):
    last = pygame.time.get_ticks()
    cooldown = 500    
    
class btime(object):
    last = pygame.time.get_ticks()
    cooldown = 200



#MUSIC & SOUND
pygame.mixer.music.load('Kalimba.wav')
pygame.mixer.music.play(-1)
shot = pygame.mixer.Sound('shot.wav')
deadSound = pygame.mixer.Sound('dead.wav')

class player1(object):
    def __init__(self, x, y, charWidth, charHeight):
        self.x = x
        self.y = y
        self.charWidth = charWidth
        self.charHeight = charHeight
        self.vel = 20
        self.isJump = False
        self.jumpCount = 10
        self.lastCharPos = True
        self.crouch = False
        self.left = False
        self.right = True
        self.walkCount = 0
        self.cy = 0
        self.hitx = 70
        self.hity = 100
        self.hitbox = (self.x + 15, self.y + self.cy, self.hitx, self.hity)
        self.dead = False
        
    def draw(self, display):
        if self.walkCount + 1 >= 24:
            self.walkCount = 0
         
        if self.crouch:
            self.vel = 10
            self.cy = 75
            self.hitx = 70
            self.hity = 25            
            if not(self.lastCharPos):
                if self.left:
                    display.blit(CwalkLeft[self.walkCount//6], (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    display.blit(CwalkRight[self.walkCount//6], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    display.blit(CwalkRight[1], (self.x, self.y))
                else:
                    display.blit(CwalkLeft[1], (self.x, self.y))
        elif not(self.lastCharPos):
            self.vel = 20
            self.cy = 0
            self.hitx = 70
            self.hity = 100
            if self.left:
                display.blit(walkLeft[self.walkCount//6], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                display.blit(walkRight[self.walkCount//6], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                display.blit(walkRight[1], (self.x, self.y))
            else:
                display.blit(walkLeft[1], (self.x, self.y))
        self.hitbox = (self.x + 15, self.y + self.cy, self.hitx, self.hity)
        pygame.draw.rect(display, (0, 0, 255), self.hitbox, -1)
        
    def hit(self):
        self.dead = True
        
class player2(object):
    def __init__(self, x, y, charWidth, charHeight):        
        self.x = x
        self.y = y
        self.charWidth = charWidth
        self.charHeight = charHeight
        self.vel = 50
        self.left = False
        self.right = True
        self.hitbox = (self.x + 0, self.y + 15, 100, 65)
        
    def draw(self, display):
        if self.right:
            display.blit(driveRight, (self.x, self.y))
        elif self.left:
            display.blit(driveLeft, (self.x, self.y))            
        self.hitbox = (self.x + 0, self.y + 15, 100, 65)
        pygame.draw.rect(display, (0, 0, 255), self.hitbox, -1)
        
    def hit(self):
        print("chit")    


clock = pygame.time.Clock()

pygame.display.set_caption("Squid 3")

class projectile(object):
    def __init__(self, x, y, charWidth, charHeight, lastCharPos):
        self.x = x
        self.y = y
        self.charHeight = charHeight
        self.charWidth = charWidth
        self.lastCharPos = lastCharPos
        self.vel = 30* lastCharPos
        self.bullet = pygame.image.load('bullet.png')
        self.hitbox = (self.x, self.y, 20, 20)
        
    def draw(self, display):
        display.blit(self.bullet, (self.x, self.y))
        
        self.hitbox = (self.x, self.y, 20, 20)
        pygame.draw.rect(display, (0, 0, 255), self.hitbox, -1)        
        
    def hit(self):    
        bullets.pop(bullets.index(bullet))

class enemy1(object):
    walkRight = [pygame.image.load('SR1.png'), pygame.image.load('SR2.png')]
    walkLeft = [pygame.image.load('SL1.png'), pygame.image.load('SL2.png')]
    
    def __init__(self, x, y, charWidth, charHeight, end):
        self.x = x
        self.y = y
        self.charWidth = charWidth
        self.charHeight = charHeight
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 20
        self.hitbox = (self.x + 15, self.y, 70, 100)
        
    def draw(self, display):
        self.move()
        if self.walkCount + 1 >= 4:
            self.walkCount = 0
        if self.vel > 0:
            display.blit(self.walkRight[self.walkCount //2], (self.x, self.y))
            self.walkCount += 1
        else:
            display.blit(self.walkLeft[self.walkCount //2], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = (self.x + 15, self.y, 70, 100)
        pygame.draw.rect(display, (0, 0, 255), self.hitbox, -1)
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0                
        else:
            if self.x - self.vel > 0:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
                
    def hit(self):
        squids.pop(squids.index(squid))
                
                
class enemy2(object):
    def __init__(self, x, y, charWidth, charHeight):
        self.x = x
        self.y = y
        self.charWidth = charWidth
        self.charHeight = charHeight
        self.rock = pygame.image.load('razorspeed.png')
        self.vel = 25
        self.hitbox = (self.x + 0, self.y + 15, 100, 70)
        
    def draw(self, display):
        self.move()
        display.blit(self.rock, (self.x, self.y))
        self.hitbox = (self.x + 0, self.y + 15, 100, 70)
        pygame.draw.rect(display, (0, 0, 255), self.hitbox, -1)        
    
    def move(self):
        self.y = self.y + self.vel
        
    def hit(self):
        speeds.pop(speeds.index(speed))    

        
def redraw():
    
    display.blit(bg, (0,0))
    
    char.draw(display)
    
    car.draw(display)
    
    for speed in speeds:
        speed.draw(display)
    
    for squid in squids:
        squid.draw(display)
        
    for bullet in bullets:
        bullet.draw(display)
        
    if char.dead == True:
        display.blit(dead, (0,0))
        
    text = scoreFont.render('Score: ' + str(score), 1, (255, 255, 255))
    
    display.blit(text, (880, 10))
        
    pygame.display.update()
    
    
#The MAIN LOOP
scoreFont = pygame.font.SysFont('comicsans', 30, True)
char = player1(510, 620, 100, 100)
car = player2(510, 400, 100, 100)
bullets = []
squids = []
speeds = []
run = True
while run:
    clock.tick(24)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False   

#Squids
    now = pygame.time.get_ticks()
    if now - time.last >= time.cooldown:
        time.last = now
        if len(squids) < 3:
            randPos = random.randint(1,2)
            if randPos == 1:
                squids.append(enemy1(0, 620, 100, 100 ,980))
            else:
                squids.append(enemy1(980, 620, 100, 100 ,980))
#Razors
    enow = pygame.time.get_ticks()
    if enow - etime.last >= etime.cooldown:
        etime.last = now
        if len(speeds) < 100:
            speeds.append(enemy2(random.randint(0,980), 0, 100, 100))
    for speed in speeds:
        if speed.y > 720:
            speeds.pop(speeds.index(speed))
            
#Player1 BOOLETS
    if char.dead == False:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:           
                if char.left:
                    lastCharPos = -1
                elif char.right:
                    lastCharPos = 1
                if len(bullets) < 1000:
                    shot.play()
                    bnow = pygame.time.get_ticks()
                    if bnow - btime.last >= btime.cooldown:
                        btime.last = bnow
                        bullets.append(projectile(round(char.x + char.charWidth //2), round(char.y + char.charHeight //2), 6, (209, 219, 30), lastCharPos))

    for squid in squids:
        for bullet in bullets:
            if bullet.hitbox[1] < squid.hitbox[1] + squid.hitbox[3] and bullet.hitbox[1] + bullet.hitbox[3] > squid.hitbox[1]:
                if bullet.hitbox[0] + bullet.hitbox[2] > squid.hitbox[0] and bullet.hitbox[0] < squid.hitbox[0] + squid.hitbox[2]:
                    bullet.hit()
                    squid.hit()
                    score += 10

    for bullet in bullets:   
        if bullet.x < 1080 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    
    keys = pygame.key.get_pressed()
 
#Player1 Hitscan
    for squid in squids:
        if char.hitbox[1] < squid.hitbox[1] + squid.hitbox[3] and char.hitbox[1] + char.hitbox[3] > squid.hitbox[1]:
            if char.hitbox[0] + char.hitbox[2] > squid.hitbox[0] and char.hitbox[0] < squid.hitbox[0] + squid.hitbox[2]:
                char.hit()
                
    for speed in speeds:
        if char.hitbox[1] < speed.hitbox[1] + speed.hitbox[3] and char.hitbox[1] + char.hitbox[3] > speed.hitbox[1]:
            if char.hitbox[0] + char.hitbox[2] > speed.hitbox[0] and char.hitbox[0] < speed.hitbox[0] + speed.hitbox[2]:
                char.hit()
            
#Player1 movement
    if keys[pygame.K_a] and char.x > char.vel:
        char.x -= char.vel
        char.left = True
        char.right = False
        char.lastCharPos = False
    elif keys[pygame.K_d] and char.x < 1080 - char.charWidth - char.vel:
        char.x += char.vel
        char.right = True
        char.left = False
        char.lastCharPos = False
    else:
        char.lastCharPos = True
        char.walkCount = 0
        
    if keys[pygame.K_s]:
        char.crouch = True
    else:
        char.crouch = False
        
    if keys[pygame.K_w]:
        char.isJump = True
        char.walkCount = 0
    if (char.isJump):
        if char.jumpCount >= -10:
            neg = 1
            if char.jumpCount < 0:
                neg = -1
            char.y -= (char.jumpCount ** 2) * 0.75 * neg
            char.jumpCount -= 1
        else:
            char.isJump = False
            char.jumpCount = 10

            
#Player2 movement 

    if keys[pygame.K_LEFT] and car.x > car.vel:
        car.x -= car.vel
        car.left = True
        car.right = False
    elif keys[pygame.K_RIGHT] and car.x < 1080 - car.charWidth - car.vel:
        car.x += car.vel
        car.right = True
        car.left = False  
        
    if keys[pygame.K_UP] and car.y > car.vel:
        car.y -= car.vel
        
    if keys[pygame.K_DOWN] and car.y < 600 - car.charHeight - car.vel:
        car.y += car.vel
        
#Player2 HitScan
    if char.dead == False:
        for speed in speeds:
            if car.hitbox[1] < speed.hitbox[1] + speed.hitbox[3] and car.hitbox[1] + car.hitbox[3] > speed.hitbox[1]:
                if car.hitbox[0] + car.hitbox[2] > speed.hitbox[0] and car.hitbox[0] < speed.hitbox[0] + speed.hitbox[2]:
                    score += 10
                    speeds.pop(speeds.index(speed))
    
    if char.dead == True:
        deadSound.play()
        pygame.mixer.music.pause()
        if keys[pygame.K_RETURN]:
            score = 0
            char = player1(510, 620, 100, 100)
            car = player2(510, 400, 100, 100)
            bullets.clear()
            squids.clear()
            speeds.clear()   
            pygame.mixer.music.unpause()
            char.dead = False
            deadSound.stop()
    redraw()


#Music
#Kalimba by Mr Scruff
#[Merlin] Ninja Tune Ltd (on behalf of Ninja Tune); Audiam (Publishing), CMRRA, Abramus Digital, SOLAR Music Rights Management, ASCAP, LatinAutor - PeerMusic, Third Side Music, BMI - Broadcast Music Inc., UBEM, EMI Music Publishing, LatinAutor, LatinAutor - SonyATV, and 16 Music Rights Societies