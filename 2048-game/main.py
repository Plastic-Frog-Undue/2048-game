import pygame
import random
import math

pygame.init()

FPS = 60

WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_color(self):
        if self.value <= 0:
            return BACKGROUND_COLOR
        color_index = min(int(math.log2(self.value)) - 1, len(self.COLORS) - 1)
        return self.COLORS[color_index]

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        if self.value > 0:
            text = FONT.render(str(self.value), 1, FONT_COLOR)
            window.blit(
                text,
                (
                    self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                    self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
                ),
            )

    def set_pos(self):
        self.row = round(self.y / RECT_HEIGHT)
        self.col = round(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)
    pygame.display.update()


def get_random_pos(tiles):
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)
        if f"{row}{col}" not in tiles:
            return row, col


def move_tiles(window, tiles, clock, direction):
    # Define movement logic based on direction
    sort_func, reverse, delta, boundary_check, get_next_tile = None, None, None, None, None

    if direction == "left":
        sort_func = lambda t: t.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda t: t.col == 0
        get_next_tile = lambda t: tiles.get(f"{t.row}{t.col - 1}")

    elif direction == "right":
        sort_func = lambda t: t.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda t: t.col == COLS - 1
        get_next_tile = lambda t: tiles.get(f"{t.row}{t.col + 1}")

    elif direction == "up":
        sort_func = lambda t: t.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda t: t.row == 0
        get_next_tile = lambda t: tiles.get(f"{t.row - 1}{t.col}")

    elif direction == "down":
        sort_func = lambda t: t.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda t: t.row == ROWS - 1
        get_next_tile = lambda t: tiles.get(f"{t.row + 1}{t.col}")

    blocks = set()
    updated = True

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for tile in sorted_tiles:
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
                updated = True
            elif next_tile.value == tile.value and next_tile not in blocks:
                next_tile.value *= 2
                tiles.pop(f"{tile.row}{tile.col}")
                blocks.add(next_tile)
                updated = True

            tile.set_pos()

        draw(window, tiles)


def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return tiles


def main(window):
    clock = pygame.time.Clock()
    tiles = generate_tiles()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_tiles(window, tiles, clock, "left")
                elif event.key == pygame.K_RIGHT:
                    move_tiles(window, tiles, clock, "right")
                elif event.key == pygame.K_UP:
                    move_tiles(window, tiles, clock, "up")
                elif event.key == pygame.K_DOWN:
                    move_tiles(window, tiles, clock, "down")

        draw(window, tiles)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)



