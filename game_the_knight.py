import pygame

pygame.init()

# Uzyskanie rozdzielczości ekranu
info = pygame.display.Info()
screen_width = info.current_w  # Szerokość ekranu
screen_height = info.current_h  # Wysokość ekranu

# Tworzymy okno z rozmiarem odpowiadającym ekranowi, ale z możliwością zamknięcia (bez pełnego ekranu)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # Okno jest teraz zmienne, ale nie pełnoekranowe
pygame.display.set_caption('The Knight')

# Załadowanie i skalowanie obrazka jako tła
background = pygame.image.load(r'C:\Users\robak\VSCode\pythonGamesLearning\castle.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))

# Ładowanie obrazów duszków (sprites)
knight_image = pygame.image.load(r'C:\Users\robak\VSCode\pythonGamesLearning\Knight.bmp')

# Ładowanie obrazu smoka i ustawienie białego tła na przezroczyste
dragon_image = pygame.image.load(r'C:\Users\robak\VSCode\pythonGamesLearning\dragon.bmp')
dragon_image.set_colorkey((255, 255, 255))  # Ustawienie białego koloru na przezroczysty

# Ładowanie ognia
fire_image = pygame.image.load(r'C:\Users\robak\VSCode\pythonGamesLearning\firebullet.bmp')

# Ładowanie księżniczki
princess_image = pygame.image.load(r'C:\Users\robak\VSCode\pythonGamesLearning\princess.bmp')
princess_image.set_colorkey((0, 0, 0))  # Tu też ustawienie białego koloru na przezroczysty

# Tworzenie klasy dla rycerza
class Knight(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = knight_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 100)  # Pozycja początkowa
        self.speed = 5  # Szybkość poruszania się
        self.is_jumping = False  # Flaga informująca, czy rycerz skacze
        self.jump_height = 15  # Wysokość skoku
        self.vel_y = 0  # Prędkość poruszania się rycerza w pionie (w górę lub w dół)
        self.original_y = self.rect.bottom  # Początkowa pozycja y (ziemia)

    def update(self):
        # Obsługa ruchu klawiaturą
        keys = pygame.key.get_pressed()

        # Poruszanie w lewo
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed  # Poruszanie w lewo
            self.image = pygame.transform.flip(knight_image, True, False)  # Obracanie w lewo

        # Poruszanie w prawo
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed  # Poruszanie w prawo
            self.image = knight_image  # Normalna orientacja (twarzą w prawo)

        # Skakanie
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.vel_y = -self.jump_height  # Prędkość skoku w górę

        if self.is_jumping:
            self.vel_y += 1  # Przyspieszenie grawitacyjne
            self.rect.y += self.vel_y  # Zmiana pozycji pionowej

            # Kiedy rycerz wróci na ziemię
            if self.rect.bottom >= self.original_y:  # Jeśli dotrze na ziemię
                self.rect.bottom = self.original_y  # Ustawiamy go dokładnie na poziomie ziemi
                self.is_jumping = False
                self.vel_y = 0  # Reset prędkości pionowej

        # Detekcja kolizji z księżniczką
        if self.rect.colliderect(princess.rect):
            princess.rect.center = (dragon.rect.centerx, dragon.rect.centery) # Ponowne ustawienie księżniczki

# Tworzenie klasy smoka
class Dragon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dragon_image
        self.rect = self.image.get_rect()
        self.rect.center = (90, 100)  # Pozycja początkowa smoka
        self.speed = 5  # Szybkość poruszania się
        self.moving_right = True  # Zmienna kontrolująca kierunek ruchu smoka

    def update(self):
        if self.moving_right:
            self.rect.x += self.speed  # Ruch smoka w prawo
        else:
            self.rect.x -= self.speed  # Ruch smoka w lewo

        # Sprawdzamy, czy smok zniknął z prawej strony ekranu
        if self.rect.right > screen_width:  # Jeśli smok opuścił ekran po prawej stronie
            self.moving_right = False  # Zmieniamy kierunek na lewy
            self.image = pygame.transform.flip(dragon_image, True, False)  # Obracamy smoka w lewo

        # Sprawdzamy, czy smok zniknął z lewej strony ekranu
        elif self.rect.left <= 0:  # Jeśli smok opuścił ekran po lewej stronie
            self.moving_right = True  # Zmieniamy kierunek na prawy
            self.image = pygame.transform.flip(dragon_image, False , False)  # Obracamy smoka w prawo

# Tworzenie klasy drugiego smoka
class SecondDragon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dragon_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width - 90, 220)  # Pozycja początkowa smoka
        self.speed = 5  # Szybkość poruszania się
        self.moving_right = False  # Zmienna kontrolująca kierunek ruchu smoka

    def update(self):
        if self.moving_right:
            self.rect.x += self.speed  # Ruch smoka w prawo
            self.image = pygame.transform.flip(dragon_image, False, False)  # Obraz smoka zwrócony w prawo
        else:
            self.rect.x -= self.speed  # Ruch smoka w lewo
            self.image = pygame.transform.flip(dragon_image, True, False)  # Obraz smoka zwrócony w lewo

        # Sprawdzamy, czy smok zniknął z prawej strony ekranu
        if self.rect.right > screen_width:  # Jeśli smok opuścił ekran po prawej stronie
            self.moving_right = False  # Zmieniamy kierunek na lewy
            self.image = pygame.transform.flip(dragon_image, True, False)  # Obracamy smoka w lewo

        # Sprawdzamy, czy smok zniknął z lewej strony ekranu
        elif self.rect.left <= 0:  # Jeśli smok opuścił ekran po lewej stronie
            self.moving_right = True  # Zmieniamy kierunek na prawy
            self.image = pygame.transform.flip(dragon_image, False , False)  # Obracamy smoka w prawo

# Tworzenie klasy księżniczki
class Princess(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(princess_image, (princess_image.get_width() // 2, princess_image.get_height() // 2)) # Zmniejszenie księżniczki 
        self.rect = self.image.get_rect()
        self.rect.center = (dragon.rect.centerx, dragon.rect.centery)  # Początkowa pozycja księżniczki nad smokiem
        self.start_y = 150  # Ustawienie pozycji początkowej księżniczki
        self.vel_y = 0  # Prędkość opadania

    def update(self):
        # Księżniczka leci w dół, prędkość opadania
        self.vel_y += 0.5  # Grawitacja
        self.rect.y += self.vel_y

        # Sprawdzamy, czy księżniczka opadła na ziemię
        if self.rect.bottom > screen_height - 100:  # Jeśli księżniczka dotknęła ziemi
            self.rect.bottom = screen_height - 100  # Ustawiamy ją na ziemi
            self.vel_y = 0  # Resetujemy prędkość opadania

            # Księżniczka znika i zaczyna opadać od nowa
            self.rect.center = (dragon.rect.centerx, self.start_y)  # Ponownie ustawiamy ją nad smokiem

# Tworzenie grupy sprite'ów
all_sprites = pygame.sprite.Group()

# Dodawanie duszków do grupy
knight = Knight()
dragon = Dragon()
princess = Princess()
second_dragon = SecondDragon()  # Dodanie drugiego smoka
all_sprites.add(knight, dragon, princess, second_dragon)

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Zaktualizuj sprite'y (ruch rycerza i smoka)
    all_sprites.update()

    # Zaktualizuj tło (w przypadku zmiany rozdzielczości ekranu)
    background = pygame.transform.scale(background, (screen_width, screen_height))

    # Zaktualizuj ekran
    screen.blit(background, (0, 0))

    # Rysowanie sprite'ów na ekranie
    all_sprites.draw(screen)

    # Zaktualizuj ekran        
    pygame.display.flip()

    # Kontrola liczby klatek na sekundę
    pygame.time.Clock().tick(60)  # Ograniczanie liczby klatek na sekundę

pygame.quit()
