import asyncio
import getpass
import json
import pprint
import os
import random
from typing import Match

import websockets

# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)



def check_figure(piece):

    if piece:
        if[piece[0][0]+1, piece[0][1]] in piece and [piece[0][0], piece[0][1]+1] in piece and [piece[0][0]+1, piece[0][1]+1] in piece:
            return "O","1"

        
        elif[piece[0][0]+1, piece[0][1]] in piece and [piece[0][0]+2, piece[0][1]] in piece and [piece[0][0]+3,piece[0][1]] in piece:
            return "I","1"
        elif[piece[0][0], piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+2] in piece and [piece[0][0],piece[0][1]+3] in piece:
            return "I","2"


        elif[piece[0][0], piece[0][1]+1] in piece and [piece[0][0]+1, piece[0][1]+1] in piece and [piece[0][0]+1, piece[0][1]+2] in piece:
            return "S","1"
        elif[piece[0][0]+1, piece[0][1]] in piece and [piece[0][0]-1, piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+1] in piece:
            return "S","2"
            

        elif[piece[0][0]-1,piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+1] in piece and [piece[0][0]-1, piece[0][1]+2] in piece:
            return "Z","1"
        elif[piece[0][0]+1,piece[0][1]] in piece and [piece[0][0]+1, piece[0][1]+1] in piece and [piece[0][0]+2, piece[0][1]+1] in piece:
            return "Z","2"


        elif[piece[0][0]+1,piece[0][1]] in piece and [piece[0][0], piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+2] in piece :
            return "J","1"
        elif[piece[0][0]+1,piece[0][1]] in piece and [piece[0][0]+2, piece[0][1]] in piece and [piece[0][0]+2, piece[0][1]+1] in piece :
            return "J","2"
        elif[piece[0][0],piece[0][1]+1] in piece and [piece[0][0]-1, piece[0][1]+2] in piece and [piece[0][0], piece[0][1]+2] in piece :
            return "J","3"
        elif[piece[0][0],piece[0][1]+1] in piece and [piece[0][0]+1, piece[0][1]+1] in piece and [piece[0][0]+2, piece[0][1]+1] in piece :
            return "J","4"


        elif[piece[0][0],piece[0][1]+1] in piece and [piece[0][0]+1, piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+2] in piece :
            return "T","1"
        elif[piece[0][0]+1,piece[0][1]] in piece and [piece[0][0]+2, piece[0][1]] in piece and [piece[0][0]+1, piece[0][1]+1] in piece :
            return "T","2"
        elif[piece[0][0]-1,piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+2] in piece :
            return "T","3"
        elif[piece[0][0]-1,piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+1] in piece and [piece[0][0]+1, piece[0][1]+1] in piece :
            return "T","4"
        

        elif[piece[0][0],piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+2] in piece and [piece[0][0]+1, piece[0][1]+2] in piece :
            return "L","1"
        elif[piece[0][0]+1,piece[0][1]] in piece and [piece[0][0]+2, piece[0][1]] in piece and [piece[0][0], piece[0][1]+1] in piece :
            return "L", "2"
        elif[piece[0][0]+1,piece[0][1]] in piece and [piece[0][0]+1, piece[0][1]+1] in piece and [piece[0][0]+1, piece[0][1]+2] in piece :
            return "L", "3"
        elif[piece[0][0]-2,piece[0][1]+1] in piece and [piece[0][0]-1, piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+1] in piece :
            return "L", "4"

        


def possibilities(piece,game):
    # meter a peça à esquerda
    a = [piece[0][0],piece[1][0],piece[2][0],piece[3][0]]
    minvalue = min(a)
    b= [piece[0][1],piece[1][1],piece[2][1],piece[3][1]]
    miny=min(b)
    newpiece = [[piece[0][0]-minvalue+1,piece[0][1]-miny+1],[piece[1][0]-minvalue+1,piece[1][1]-miny+1],[piece[2][0]-minvalue+1,piece[2][1]-miny+1],[piece[3][0]-minvalue+1,piece[3][1]-miny+1]]
    listp=[]
    aux = newpiece
   

    for x in range(1,9,1):
        newpiece = [ [aux[0][0]+x-1,aux[0][1]],[aux[1][0]+x-1,aux[1][1]],[aux[2][0]+x-1,aux[2][1]],[aux[3][0]+x-1,aux[3][1]]]
        xx= [newpiece[0][0],newpiece[1][0],newpiece[2][0],newpiece[3][0]]
        maxX=max(xx)
        if maxX == 9:
            break
        else:
            for y in range (1,30,1):
                newpiece = [ [newpiece[0][0],newpiece[0][1]+1],[newpiece[1][0],newpiece[1][1]+1],[newpiece[2][0],newpiece[2][1]+1],[newpiece[3][0],newpiece[3][1]+1]]
                y= [newpiece[0][1],newpiece[1][1],newpiece[2][1],newpiece[3][1]]
                maxY=max(y)
                #print(f'peca:{newpiece}')
                #print(f'game:{game}\n-------\n')
                flag=0
                for cord in newpiece:
                    if cord in game: #colisão
                        possibility = [[newpiece[0][0],newpiece[0][1]-1],[newpiece[1][0],newpiece[1][1]-1],[newpiece[2][0],newpiece[2][1]-1],[newpiece[3][0],newpiece[3][1]-1]]
                        listp.append(possibility)
                        flag=1
                        break
                if flag==1:
                    break
                else:
                    if maxY==29:
                        listp.append(newpiece)
                        break
        
    game_possibilities=[]
    for piecee in listp:
        #print(piecee)
        newGame= game+piecee
        game_possibilities.append(newGame) 
        

    return game_possibilities

def get_board(game):
    
    board=[[0 for i in range(1,9)] for j in range(1,30)]

    for coords in game:
        board[coords[1]-1][coords[0]-1] = 1
    
    
    # for piecee in game:
    return board
        


def agregate_height(board):

    height2=0

    for x in range (1,9):    
        for y in range (1,30):
            if(board[y-1][x-1]==1):
                height2+=(30-y)
                break
    
    return height2
  
def number_of_holes(board):
    holes=0

    for column in zip(*board):
         i=0
         while i<29 and column[i] != 1:
             i+=1

         holes += len([x for x in column[i+1:] if x == 0])


    return holes



def bumpiness(board):

    height=[]
    total_bumpiness=0

    for x in range (1,9):    
        for y in range (1,30):
            if(board[y-1][x-1]==1):
                height.append(30-y)
                break
            else:
                if(y==29):
                    height.append(0)
   


    for i in range(len(height)-1):
        bumpiness = abs(height[i] -height[i+1])
        total_bumpiness += bumpiness

    return total_bumpiness





def complete_lines(board):
    
    comp_lines = 0
    for y in range(28, -1, -1):
        if sum(board[y]) == 8:
            comp_lines += 1
    return comp_lines



def cost(height, bumpiness,number_holes, complines):

    return (-0.510066)*height + (-0.184483)*bumpiness + (-0.35663)*number_holes + (0.760666)*complines


def best_possibility(custos,game_possibilities):

    max_cost=max(custos)
    indice=0

    for a in range(len(custos)):
        if(max_cost==custos[a]):
            indice=a

    return game_possibilities[indice], indice

                        
def rotate(piece):

    rotation_point=[piece[0][0], piece[0][1]]

    x=piece[0][0]
    y=piece[0][1]
    form,type= check_figure(piece)

    if form=="O":
        return piece

    elif form =="I":
        if type =="1":
            piece=[[x,y],[x,y+1],[x,y+2],[x,y+3]]
        elif type =="2":
            piece=[[x,y],[x-1,y],[x-2,y],[x+1,y]]

    elif form == "S":
        if type == "1":
            piece=[[x,y],[x+1,y],[x-1,y+1],[x,y+1]]
        elif type=="2":
            piece=[[x,y],[x,y+1],[x+1,y+1],[x+1,y+2]]

    elif form=="Z":
        if type=="1":
            piece=[[x,y],[x+1,y],[x+1,y+1],[x+2,y+1]]
        elif type == "2":
            piece=[[x,y],[x-1,y+1],[x,y+1],[x-1,y+2]]
        
    
    elif form=="J":
        if type == "1":
            piece=[[x,y],[x+1,y],[x+2,y],[x+2,y+1]]
        elif type == "2":
            piece=[[x,y],[x,y+1],[x-1,y+2],[x,y+2]]
        elif type == "3":
            piece=[[x,y],[x,y+1],[x+1,y+1],[x+2,y+1]]
        elif type == "4":
            piece=[[x,y],[x+1,y],[x,y+1],[x-1,y+2]]

    elif form == "T":
        if type == "1":
            piece=[[x,y],[x+1,y],[x+2,y],[x+1,y+1]]
        elif type == "2":
            piece = [[x,y],[x-1,y+1],[x,y+1],[x,y+2]]
        elif type == "3":
            piece = [[x,y],[x-1,y+1],[x,y+1],[x+1,y+1]]
        elif type == "4":
            piece = [[x,y],[x,y+1],[x+1,y+1],[x,y+2]]

    elif form == "L":
        if type == "1":
            piece=[[x,y],[x+1,y],[x+2,y],[x,y+1]]
        elif type == "2":
            piece = [[x,y],[x+1,y],[x+1,y+1],[x+1,y+2]]
        elif type == "3":
            piece = [[x,y],[x-2,y+1],[x-1,y+1],[x,y+1]]
        elif type == "4":
            piece = [[x,y],[x,y+1],[x,y+2],[x+1,y+2]]

    
    return piece


def possibilities_rotation(piece, game):
    peca, tipo =check_figure(piece)
    allmapas = []
    if peca == 'I':
        numrotation=2
    elif peca=='S':
        numrotation=2
    elif peca =="Z":
        numrotation=2
    elif peca =="J":
        numrotation=4
    elif peca=="T":
        numrotation=4
    elif peca=="L":
        numrotation=4
    else:
        numrotation=1

    newpiece = piece

    for rotation in range(numrotation):
        anothergame = possibilities(newpiece,game)
        allmapas+=anothergame
        newpiece = rotate(newpiece)
    return allmapas


    

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        msg = await websocket.recv()
        game_properties = json.loads(msg)

        # Next 3 lines are not needed for AI agent
        # SCREEN = pygame.display.set_mode((299, 123))
        # SPRITES = pygame.image.load("data/pad.png").convert_alpha()
        # SCREEN.blit(SPRITES, (0, 0))
        rotacao =0
        start = 1
        listafinal=[]

        

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                key=""
                game=state['game']
                piece=state['piece']
                #next_piece=state['next_pieces'][0]
                
                if start:  
                    if piece:
                        #print("\n")

                        

                        
                        rodou=0 
                        figure = check_figure(piece)
                        #print("GAME ATUAL", game)
                        #game_possiblidades = possibilities(piece, game)
                        game_possiblidades = possibilities_rotation(piece,game)
                        #print("GAME_POSSIBLIDADES", game_possiblidades)

                        board_possiblidades =[]

                        #print(len(game_possiblidades))
                        for i in range(len(game_possiblidades)):
                            #print(game_possiblidades[i])
                            board_possiblidades.append(get_board(game_possiblidades[i]))
                            #pprint.pprint(board_possiblidades)
                          

                        custos=[]

                        for a in range(len(board_possiblidades)):
                            Height = agregate_height(board_possiblidades[a])
                            number_holes = number_of_holes(board_possiblidades[a])
                            Bumpiness= bumpiness(board_possiblidades[a])
                            Comp_lines = complete_lines(board_possiblidades[a])
                            custos.append(cost(Height,Bumpiness,number_holes,Comp_lines))

                        BestGame,indice=best_possibility(custos, game_possiblidades)
                     
                        best_piece_position=[]
                        
                        best_piece_position=[BestGame[-4], BestGame[-3], BestGame[-2], BestGame[-1]]
                        
                     


                        start = 0
                if not piece:
                    start = 1
                
                if piece :



                    xBest= [best_piece_position[0][0],best_piece_position[1][0],best_piece_position[2][0],best_piece_position[3][0]]
                    minvalueBest = min(xBest)
                    

                    xActual = [piece[0][0],piece[1][0],piece[2][0],piece[3][0]]
                    minvalueActual = min(xActual)
                    peca, tipo =check_figure(piece)
                   


                   
                    if( peca=="I"):
                        if(indice < 5):
                            rotacao=0
                        else:
                            rotacao=1

                    elif( peca=="S"):
                        if(indice < 7):
                            rotacao=0
                        else:
                            rotacao=1

                    elif( peca=="Z"):
                        if(indice < 7):
                            rotacao=0
                        else:
                            rotacao=1

                    elif(peca =="J"):
                        if(indice < 7):
                            rotacao=0
                        elif indice >= 7 and indice <13:
                            rotacao=1
                        elif indice >= 13 and indice <20:
                            rotacao=2
                        else:
                            rotacao=3

                    elif(peca =="T"):
                        if(indice < 7):
                            rotacao=0
                        elif indice >= 7 and indice <13:
                            rotacao=1
                        elif indice >= 13 and indice <20:
                            rotacao=2
                        else:
                            rotacao=3

                    elif(peca =="L"):
                        if(indice < 7):
                            rotacao=0
                        elif indice >= 7 and indice <13:
                            rotacao=1
                        elif indice >= 13 and indice <20:
                            rotacao=2
                        else:
                            rotacao=3
                    
                    else: rotacao=0

                    
                    if(rodou != rotacao):
                        key="w"
                        rodou +=1

                    else:
                        if(minvalueActual < minvalueBest):
                            key="d"

                        elif(minvalueActual > minvalueBest):
                            key="a"

                        elif(minvalueActual==minvalueBest):
                            key="s"
                    
                        
                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )
              

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return
            except: pass

            # Next line is not needed for AI agent
            #pygame.display.flip()


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))