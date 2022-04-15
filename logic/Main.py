# Driver file
# Handling user input & displaying current GameState

import pygame as p
from Engine import GameState, Move

p.init()
WIDTH = HEIGHT = 512  # 400 other option
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

# Init global dictionary of images. Called once in main


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wQ",
              "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"img/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def draw_board(screen):
    colors = [p.Color("white"), p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(
                    c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# Responsible for all graphics within current gamestate
def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


# Main driver for our code. Handle user input & updating graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    # screen.fill(p.Color("White"))
    gs = GameState()

    validMoves = gs.get_valid_moves()
    moveMade = False  # flag variable for made move

    load_images()

    sqSelected = ()  # last click of the user
    playerClicks = []  # Keep track of clicks [(6,4), (4,4)]

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.make_move(move)
                        print(move.get_chess_notation())
                        moveMade = True
                        sqSelected = ()  # reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u:
                    gs.undo_move()
                    moveMade = True
        if moveMade:
            validMoves = gs.get_valid_moves()
            moveMade = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
