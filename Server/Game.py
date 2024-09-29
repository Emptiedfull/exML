import numpy as np
import pygame
import random

boardtypes = [
    [
        "############################",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#o####.#####.##.#####.####o#",
        "#.####.#####.##.#####.####.#",
        "#..........................#",
        "#.####.##.########.##.####.#",
        "#.####.##.########.##.####.#",
        "#......##....##....##......#",
        "######.##### ## #####.######",
        "######.##### ## #####.######",
        "######.##          ##.######",
        "######.## ###  ### ##.######",
        "######.## #a b   # ##.######",
        " p ..  ## # c  d # ##       ",
        "######.## #      # ##.######",
        "######.## ######## ##.######",
        "######.##          ##.######",
        "######.## ######## ##.######",
        "######.## ######## ##.######",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#.####.#####.##.#####.####.#",
        "#o..##................##..o#",
        "###.##.##.########.##.##.###",
        "###.##.##.########.##.##.###",
        "#......##....##....##......#",
        "#.##########.##.##########.#",
        "#.##########.##.##########.#",
        "#..........................#",
        "############################"],
    [
        "############################",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#.####.#####.##.#####.####.#",
        "#.####.#####.##.#####.####.#",
        "#..........................#",
        "#.####.##.########.##.####.#",
        "#.####.##.########.##.####.#",
        "#......##....##....##......#",
        "######.##### ## #####.######",
        "######.### c   b  ###.######",
        "######.## a     d  ##.######",
        "######.## ###--### ##.######",
        "#............p.............#",
        "######.## ########## ##.####",
        "######.## ########## ##.####",
        "######.##            ##.####",
        "######.## ########## ##.####",
        "######.## ########## ##.####",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#.####.#####.##.#####.####.#",
        "#......##............##....#",
        "############################"
    ], ["###############################",
        "#.....#.................#.....#",
        "#.###.#.###.#######.###.#.....#",
        "#.#...#.#......#......#.#.....#",
        "#...###.#.####.#.####...###...#",
        "###.#.#.#.#......#..#.#...#.###",
        "#...#.###.#.### ###.#.###.#...#",
        "#.###.......#a b c#.......###.#",
        "#.###.......#   d #.......###.#",
        "#...#.#####.#######.#.###.#...#",
        "###.#...#.#....#....#.#...#.###",
        "#...###.#.####.#.####.#.###...#",
        "#.......#......#......#.....#.#",
        "#.....#.###.#######.###.#.###.#",
        "#.....#........p....#...#.....#",
        "###############################"]
]

cell_size = 20
rows, cols = 31, 28
screen_width = cols * cell_size
screen_height = rows * cell_size
class Player:
    
    def __init__(self,player_pos):
        self.points = 0
        self.x = player_pos[0]
        self.y = player_pos[1]
        self.player_pos = [self.x, self.y]

    def __getitem__(self, index):
        return self.player_pos[index]
    
    def move(self,board,move):
       
        if move == "up":
            if board[self.x-1,self.y] in "abcd":
                   return 'death'
            
            if board[self.x-1,self.y] != '#':
                if board[self.x-1,self.y] == '.':
                    self.points += 1
                board[self.x,self.y] = ' '
                self.x -= 1
                board[self.x,self.y] = 'p'
                if board[self.x,self.y] == '.':
                    self.points += 1
               
        if move == "down":
            
            if board[self.x+1,self.y] in "abcd":
                    return 'death'
            elif board[self.x+1,self.y] != '#':
                if board[self.x+1,self.y] == '.':
                    self.points += 1
                board[self.x,self.y] = ' '
                self.x += 1
                board[self.x,self.y] = 'p'
                
                
        if move == "left":
            if board[self.x,self.y-1] in "abcd":
                   return 'death'
            elif board[self.x,self.y-1] != '#':
                if board[self.x,self.y-1] == '.':
                    self.points += 1
                board[self.x,self.y] = ' '
                self.y -= 1
                board[self.x,self.y] = 'p'
               
                
        if move == "right":
            if board[self.x,self.y+1] in "abcd":
                     return 'death'
            elif board[self.x,self.y+1] != '#':
                if board[self.x,self.y+1] == '.':
                    self.points += 1 
                board[self.x,self.y] = ' '
                self.y += 1
                board[self.x,self.y] = 'p'
                
                

class Ghost:
    
    def __init__(self,ghost_pos,id):
        self.x = ghost_pos[0]
        self.y = ghost_pos[1]
        self.id = id
        self.position = [self.x,self.y]
        self.last_block = ' '


   

    def move(self,board,move):
        
        if move == "up":
            if board[self.x-1,self.y] == 'p':
                return 'death'
            elif board[self.x-1,self.y] not in "abcd#":
                
                board[self.x,self.y] = self.last_block
                self.last_block = board[self.x-1,self.y]
                self.x -= 1
                board[self.x,self.y] = self.id
           
        if move == "down":
            if board[self.x+1,self.y] == 'p':
                return 'death'
            elif board[self.x+1,self.y] not in "abcd#":
                
              
                board[self.x,self.y] = self.last_block
                self.last_block = board[self.x+1,self.y]
                self.x += 1
                board[self.x,self.y] = self.id
                
            
        if move == "left":
            if board[self.x,self.y-1] == 'p':
               return 'death'
            elif board[self.x,self.y-1] not in "abcd#":
                board[self.x,self.y] = self.last_block
                self.last_block = board[self.x,self.y-1]
                self.y -= 1
                board[self.x,self.y] = self.id
           
        if move == "right":
            if board[self.x,self.y+1] == 'p':
                return 'death'
            elif board[self.x,self.y+1] not in "abcd#":
                
                board[self.x,self.y] = self.last_block
                self.last_block = board[self.x,self.y+1]
                self.y += 1
                board[self.x,self.y] = self.id
              
           

        
class Board:
    def __init__(self):
        global rows,cols
        rand = random.randint(0,boardtypes.__len__()-1)
        arr = boardtypes[rand]
        self.rand = rand
        np_board = np.array([list(row) for row in arr])
        self.board = np_board
        self.row, self.col = self.board.shape
        self.positions = self.get_positions()
        rows,cols = self.row,self.col

        
       
    def display(self):
      return self.board

    def __getitem__(self, index):
        return self.board[index]
    
    def __setitem__(self,index,value):
        
        self.board[index] = value

    def get_positions(self):
        
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i,j] == 'p':
                    player_pos = [i,j]
                if self.board[i,j] == 'a':
                    ghost1_pos = [i,j]
                if self.board[i,j] == 'b':
                    ghost2_pos = [i,j]
                if self.board[i,j] == 'c':
                    ghost3_pos = [i,j]
                if self.board[i,j] == 'd':
                    ghost4_pos = [i,j] 

        return player_pos, ghost1_pos, ghost2_pos, ghost3_pos, ghost4_pos        
                   
    def get_board(self):
        return self.board.tolist() 
                

    # def draw(self, screen, cell_size):
    #     for i in range(self.row):
    #          for j in range(self.col):
    #             color = (0, 0, 0)  # Default color for empty cells
    #             if self.board[i, j] == '#':
    #                 color = (0, 0, 255)  # Blue color for walls
    #                 pygame.draw.rect(screen, color, pygame.Rect(
    #                     j * cell_size, i * cell_size, cell_size, cell_size))
    #             elif self.board[i, j] == '.':
    #                 color = (255, 255, 255)
    #                 pygame.draw.circle(screen, color, (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2),
    #                                    cell_size // 10) 
    #             elif self.board[i, j] == 'a':
    #                 color = (255, 0, 0)
    #                 pygame.draw.circle(screen, color, (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2),
    #                                    cell_size // 4)
    #             elif self.board[i, j] == 'b':
    #                 color = (255, 100, 0)
    #                 pygame.draw.circle(screen, color, (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2),
    #                                    cell_size // 4)
                                       
    #             elif self.board[i, j] == 'c':
    #                 color = (0, 255, 0)
    #                 pygame.draw.circle(screen, color, (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2),
    #                                    cell_size // 4)
                
    #             elif self.board[i, j] == 'd':
    #                 color = (0, 0, 255)
    #                 pygame.draw.circle(screen, color, (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2),
    #                                    cell_size // 4)
    #             elif self.board[i,j] == 'p':
    #                 color = (255, 255, 0)
    #                 pygame.draw.circle(screen, color, (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2),
    #                                    cell_size // 4)
                   


# pygame.init()

# Screen dimensions



# screen = pygame.display.set_mode((screen_width, screen_height))


# # Create the board and setup the level
# board = Board()
# player = Player()
# Ghost1 = Ghost(ghost1_pos[0],ghost1_pos[1],'a')




# # Game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             key = event.key
#             if key == pygame.K_UP:
#                 player.move(board,'up')
#             elif key == pygame.K_DOWN:
#                 player.move(board,'down')
#             elif key == pygame.K_LEFT:
#                 player.move(board,'left')
#             elif key == pygame.K_RIGHT:
#                 player.move(board,'right')

#     # Clear the screen
#     screen.fill((0, 0,0))

#     # Draw the board
#     board.draw(screen, cell_size)

#     # Update the display
#     pygame.display.flip()

# pygame.quit()


