import pygame


class Map:
    # создание поля
    def __init__(self, width, height):
        self.matrix = []
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for x in range(self.width):
            self.matrix.append([0 for i in range(self.height)])
        for x in range(self.width):
            for y in range(self.height):
                if self.matrix[x][y] == 0:
                    pygame.draw.rect(screen, (0, 0, 0), ((self.left + self.cell_size * x,
                                                          self.top + self.cell_size * y),
                                                         (self.cell_size, self.cell_size)), 0)
                    pygame.draw.rect(screen, (255, 255, 255), ((self.left + self.cell_size * x,
                                                                self.top + self.cell_size * y),
                                                               (self.cell_size, self.cell_size)), 1)
                elif self.matrix[x][y] == 1:
                    pygame.draw.rect(screen, (255, 0, 0), ((self.left + self.cell_size * x,
                                                            self.top + self.cell_size * y),
                                                           (self.cell_size, self.cell_size)), 0)
                    pygame.draw.rect(screen, (255, 255, 255), ((self.left + self.cell_size * x,
                                                                self.top + self.cell_size * y),
                                                               (self.cell_size, self.cell_size)), 1)
                else:
                    pygame.draw.rect(screen, (0, 0, 255), ((self.left + self.cell_size * x,
                                                            self.top + self.cell_size * y),
                                                           (self.cell_size, self.cell_size)), 0)
                    pygame.draw.rect(screen, (255, 255, 255), ((self.left + self.cell_size * x,
                                                                self.top + self.cell_size * y),
                                                               (self.cell_size, self.cell_size)), 1)

    def click(self, x1, y1):
        if x1 <= self.left + self.cell_size * self.width and y1 <= self.top + self.cell_size * self.height \
                and x1 >= self.left and y1 >= self.top:
            first_coord = (x1 - self.left) // self.cell_size
            second_coord = (y1 - self.top) // self.cell_size
            if self.matrix[first_coord][second_coord] == 0:
                self.matrix[first_coord][second_coord] = 1
            elif self.matrix[first_coord][second_coord] == 1:
                self.matrix[first_coord][second_coord] = 2
            else:
                self.matrix[first_coord][second_coord] = 0
            self.render(screen)
            return ''
        return None


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Mygame')
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))
    pygame.display.flip()
    board = Map(19, 15)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
                print(board.click(x1, y1))
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
