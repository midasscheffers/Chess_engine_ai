
"""
This is the game file responsible for game drawing and such
"""


import pygame
from main import *




# pygame setup
pygame.init()
size = 100
screen = pygame.display.set_mode((8*size, 8*size))
clock = pygame.time.Clock()
running = True


dark = (0,50, 100)
light = (240, 230,200)
hi_dark = (100,50,0)
hi_light = (240, 50,50)

# load board
b = Board()
# load images
piece_imgs={}
for p in ["king", "queen", "rook", "bishop", "knight", "pawn"]:
    for c in ["white", "black"]:
        img = pygame.image.load(f"imgs/{c}_{p}.png").convert_alpha()
        img = pygame.transform.scale(img, (size*0.5, size))
        piece_imgs[f"{c}_{p}"]  = img

hover_piece = []
highlight_sqrs = []



def draw_piece(screen, x, y, piece):
    c = "white" if Piece.piece_color(piece) == Piece.White else "black"
    type_to_str_dict = {Piece.King:"king", Piece.Pawn:"pawn", Piece.Knight:"knight", Piece.Bishop:"bishop", Piece.Rook:"rook", Piece.Queen:"queen"}
    p = type_to_str_dict[Piece.piece_type(piece)]
    img = piece_imgs[f"{c}_{p}"]
    screen.blit(img, [x,y])



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()
            mx,my = mx//(size), my//(size)
            hover_piece = [b.squares[mx+my*8], mx, my]
            moves = b.get_moves()
            for m in moves:
                if m.start == mx+8*my:
                    highlight_sqrs.append(m.target)
        
        if event.type == pygame.MOUSEBUTTONUP:
            mx,my = pygame.mouse.get_pos()
            mx,my = mx//(size), my//(size)
            if (mx+8*my) in highlight_sqrs:
                b.make_move(Move(hover_piece[1]+hover_piece[2]*8, mx+8*my))
            hover_piece = []
            highlight_sqrs = []

    screen.fill("black")

    for sq in range(64):
        x,y = sq%8,sq//8
        # draw square
        if sq in highlight_sqrs:
            color = hi_light if (x+y)%2==0 else hi_dark
        else:
            color = light if (x+y)%2==0 else dark
        pygame.draw.rect(screen, color, [x*size, y*size, size, size])
        # draw piece
        if not Piece.piece_type(b.squares[sq]) == Piece.Empty:
            if not [b.squares[sq], x,y] == hover_piece:
                draw_piece(screen, x*100+size/4,y*100, b.squares[sq])
        if not hover_piece == []:
            mx, my = pygame.mouse.get_pos()
            draw_piece(screen, mx-size/4,my-(size*0.75), hover_piece[0])
    


    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()





