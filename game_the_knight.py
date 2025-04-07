import pygame
import random
import time

pygame.init()

# Funkcja do inicjalizacji rozdzielczości ekranu
def initialize_screen():
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    return screen_width, screen_height

# Stałe dotyczące rozdzielczości
screen_width, screen_height = initialize_screen()

# Tworzymy okno
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('The Knight')

# Załadowanie obrazków
def load_image(path):
    return pygame.image.load(path)

background = load_image(r'C:\Users\robak\VSCode\pythonGamesLearning\castle.jpg')
knight_image = load_image(r'C:\Users\robak\VSCode\pythonGamesLearning\Knight.bmp')
dragon_image = load_image(r'C:\Users\robak\VSCode\pythonGamesLearning\dragon.bmp')
fire_image = load_image(r'C:\Users\robak\VSCode\pythonGamesLearning\firebullet.bmp')
princess_image = load_image(r'C:\Users\robak\VSCode\pythonGamesLearning\princess.bmp')

# Zmiana rozmiaru tła
background = pygame.transform.scale(background, (screen_width, screen_height))

# Ustawienie kolorów białych na przezroczyste
dragon_image.set_colorkey((255, 255, 255)) 
princess_image.set_colorkey((0, 0, 0))

# Klasa rycerza
class Knight(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = knight_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 100)
        self.speed = 5
        self.is_jumping = False
        self.jump_height = 15
        self.vel_y = 0
        self.original_y = self.rect.bottom
        self.hit_count = 0  # Licznik trafień

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.image = pygame.transform.flip(knight_image, True, False)

        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.image = knight_image

        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.vel_y = -self.jump_height

        if self.is_jumping:
            self.vel_y += 1
            self.rect.y += self.vel_y
            if self.rect.bottom >= self.original_y:
                self.rect.bottom = self.original_y
                self.is_jumping = False
                self.vel_y = 0

    def hit(self):
        """Zwiększa licznik trafień i sprawdza, czy gra powinna zostać zakończona"""
        self.hit_count += 1
        if self.hit_count >= 50:
            return True  # Gra powinna zostać zakończona
        return False

# Klasa kuli ognia
class FireBullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        self.image = pygame.transform.scale(fire_image, (fire_image.get_width() // 2, fire_image.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.vel_y = 5

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.bottom > screen_height - 100:
            self.rect.bottom = screen_height - 100
            self.vel_y = 0
            self.kill()

        # Sprawdzanie kolizji z rycerzem
        if self.rect.colliderect(knight.rect):  # Jeśli kula ognia trafia w rycerza
            if knight.hit():  # Jeśli liczba trafień przekroczyła 5
                global running
                running = False  # Zakończenie gry
            self.kill()  # Usuwamy kulę ognia po trafieniu

# Klasa bazowa dla smoków
class DragonBase(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        self.image = dragon_image
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.speed = 5
        self.moving_right = True
        self.fire_rate = 0

    def update(self):
        if self.moving_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.right > screen_width:
            self.moving_right = False
            self.image = pygame.transform.flip(dragon_image, True, False)
        elif self.rect.left <= 0:
            self.moving_right = True
            self.image = pygame.transform.flip(dragon_image, False, False)

        if self.fire_rate == 0:
            fire_bullet = FireBullet(self.rect.centerx, self.rect.centery)
            all_sprites.add(fire_bullet)
            self.fire_rate = 60
        else:
            self.fire_rate -= 1

# Klasy smoków dziedziczące po DragonBase
class Dragon(DragonBase):
    def __init__(self):
        super().__init__(90, 100)

class SecondDragon(DragonBase):
    def __init__(self):
        super().__init__(screen_width - 90, 300)

# Klasa księżniczki
class Princess(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(princess_image, (princess_image.get_width() // 2, princess_image.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect.y = knight.rect.y  # Księżniczka pojawia się na wysokości rycerza
        self.visible_time = random.randint(4, 5)  # Czas, przez jaki księżniczka będzie widoczna
        self.time_visible = time.time()  # Czas rozpoczęcia widoczności księżniczki

        # Losowa pozycja na osi X
        self.rect.x = random.randint(0, screen_width - self.rect.width)

    def update(self):
        global caught_princess_count

        # Sprawdzanie, czy minął czas wyświetlania księżniczki
        if time.time() - self.time_visible > self.visible_time:
            self.kill()  # Księżniczka znika po czasie

        # Sprawdzanie kolizji z rycerzem
        if self.rect.colliderect(knight.rect):  # Jeśli księżniczka jest złapana przez rycerza
            caught_princess_count += 1  # Zwiększ liczbę złapanych księżniczek
            self.kill()  # Księżniczka znika

# Funkcja do sprawdzenia i wyświetlania liczby złapanych księżniczek
def display_caught_princesses():
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Caught Princesses: {caught_princess_count}', True, (255, 255, 255))
    screen.blit(text, (10, 10))  # Wyświetlanie w lewym górnym rogu

# Funkcja do pokazania komunikatu Game Over i zapytania o wznowienie gry
def game_over_screen():
    font = pygame.font.SysFont(None, 74)
    text = font.render('Game Over!', True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2 - 50)
    screen.blit(text, text_rect)

    font = pygame.font.SysFont(None, 48)
    restart_text = font.render('Press Y to Restart or N to Quit', True, (255, 255, 255))
    restart_rect = restart_text.get_rect()
    restart_rect.center = (screen_width // 2, screen_height // 2 + 50)
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # Restart gry
                    return True
                elif event.key == pygame.K_n:  # Zakończenie gry
                    pygame.quit()
                    quit()

    return False

# Tworzenie grupy sprite'ów
all_sprites = pygame.sprite.Group()

# Dodawanie duszków do grupy
knight = Knight()
dragon = Dragon()
second_dragon = SecondDragon()

all_sprites.add(knight, dragon, second_dragon)

# Zmienna do kontrolowania księżniczki
princess_timer = 0  # Czas na pojawienie się księżniczki
caught_princess_count = 0  # Liczba złapanych księżniczek

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Zaktualizuj wszystkie sprite'y
    all_sprites.update()

    # Sprawdzanie, czy księżniczka powinna się pojawić
    if time.time() - princess_timer > random.randint(5, 10):  # Losowy czas pojawienia się
        princess = Princess()
        all_sprites.add(princess)
        princess_timer = time.time()  # Resetujemy czas na pojawienie się kolejnej księżniczki

    # Rysowanie tła i sprite'ów
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    # Wyświetlanie liczby złapanych księżniczek
    display_caught_princesses()

    pygame.display.flip()

    pygame.time.Clock().tick(60)

    if not running:
        if game_over_screen():  # Jeśli użytkownik wybierze wznowienie
            knight = Knight()
            dragon = Dragon()
            second_dragon = SecondDragon()

            all_sprites.empty()
            all_sprites.add(knight, dragon, second_dragon)

            running = True  # Wznawiamy grę
