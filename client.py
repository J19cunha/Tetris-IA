import asyncio
import getpass
import json
import pprint
import os
from typing import Match

import websockets

# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)



def check_figure(piece):
    
    if[piece[0][0]+1, piece[0][1]] in piece and [piece[0][0], piece[0][1]+1] in piece and [piece[0][0]+1, piece[0][1]+1] in piece:
        return "o"
    elif[piece[0][0]+1, piece[0][1]] in piece and [piece[0][0]+2, piece[0][1]] in piece and [piece[0][0]+3,piece[0][1]] in piece:
        return "i"
    elif[piece[0][0], piece[0][1]+1] in piece and [piece[0][0]+1, piece[0][1]+1] in piece and [piece[0][0]+1, piece[0][1]+2] in piece:
        return "S"
    elif[piece[0][0]-1,piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+1] in piece and [piece[0][0]-1, piece[0][1]+2] in piece:
        return "Z"
    elif[piece[0][0]+1,piece[0][1]] in piece and [piece[0][0], piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+2] in piece :
        return "J"
    elif[piece[0][0],piece[0][1]+1] in piece and [piece[0][0]+1, piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+2] in piece :
        return "T"
    elif[piece[0][0],piece[0][1]+1] in piece and [piece[0][0], piece[0][1]+2] in piece and [piece[0][0]+1, piece[0][1]+2] in piece :
        return "L"





def possibilities(piece,game):
    # meter a peça à esquerda
    a = [piece[0][0],piece[1][0],piece[2][0],piece[3][0]]
    minvalue = min(a)
    b= [piece[0][1],piece[1][1],piece[2][1],piece[3][1]]
    miny=min(b)
    newpiece = [[piece[0][0]-minvalue+1,piece[0][1]-miny+1],[piece[1][0]-minvalue+1,piece[1][1]-miny+1],[piece[2][0]-minvalue+1,piece[2][1]-miny+1],[piece[3][0]-minvalue+1,piece[3][1]-miny+1]]
    listp=[]
    aux = newpiece
    #print(f"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa    {aux}")
    #print(maxY)  


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
        
    # print("GAME: ",game_possibilities)
    # b=len(game_possibilities)
    # a=game_possibilities[0]
    # print("FIRST",a)
    # print("NUMERO", b)

    #numero_possiblidades=8-larguradapeça+1

    return game_possibilities

def get_board(game):
    
    board=[[0 for i in range(1,9)] for j in range(1,30)]

    for coords in game:
        board[coords[1]-1][coords[0]-1] = 1
    
    
    # for piecee in game:
    return board
        


def max_height(board):
    height=[]
    for x in range (1,9):    
        for y in range (1,30):
            if(board[y-1][x-1]==1):
                height.append(30-y)
                break

    return max(height, default=0)
  
def number_of_holes(board):
    holes=0

    for column in zip(*board):
         i=0
         while i<29 and column[i] != 1:
             i+=1

         holes += len([x for x in column[i+1:] if x == 0])

    #print(holes)
    return holes



def bumpiness(board):

    height=[]
    total_bumpiness=0
    max_bumpiness=0

    for x in range (1,9):    
        for y in range (1,30):
            if(board[y-1][x-1]==1):
                height.append(30-y)
                break


    for i in range(len(height)-1):
        bumpiness = abs(height[i] -height[i+1])
        max_bumpiness = max(bumpiness, max_bumpiness)
        total_bumpiness += abs(height[i] - height[i+1])

    return total_bumpiness

#só para testar
def decision(board):
    key = ''
    for y in range(28, -1, -1):
        if sum(board[y]) == 0:
            return 'a'
        else:   
            return 'd'

def complete_lines(board):
    
    comp_lines = 0
    for y in range(28, -1, -1):
        if sum(board[y]) == 8:
            comp_lines += 1
    return comp_lines
    

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        msg = await websocket.recv()
        game_properties = json.loads(msg)

        # Next 3 lines are not needed for AI agent
        SCREEN = pygame.display.set_mode((299, 123))
        SPRITES = pygame.image.load("data/pad.png").convert_alpha()
        SCREEN.blit(SPRITES, (0, 0))
    
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
                next_piece=state['next_pieces'][0]
                
                if start:           
                    figure = check_figure(piece)
                    lista = possibilities(piece, game)
                    #print(lista)
                    #print("-----------------------------------------")
                    #lista=height(game)
                    # lista =get_board(piece,game)
                    # print(lista)
                    board = get_board(game)
                    Height = max_height(board)
                    #pprint.pprint(board)
                    #print(Height)
                    number_holes = number_of_holes(board)
                    bumpinessssss= bumpiness(board)
                    comp_lines = complete_lines(board)
                    start = 0
                if not piece:
                    start = 1

                key = decision(board)
                
                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )
                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                # key = ""
                # for event in pygame.event.get():
                #     if event.type == pygame.QUIT:
                #         pygame.quit()

                #     if event.type == pygame.KEYDOWN:
                #         if event.key == pygame.K_UP:
                #             key = "w"
                #         elif event.key == pygame.K_LEFT:
                #             key = "a"
                #         elif event.key == pygame.K_DOWN:
                #             key = "s"
                #         elif event.key == pygame.K_RIGHT:
                #             key = "d"

                #         elif event.key == pygame.K_d:
                #             import pprint

                #             pprint.pprint(state)

                #         await websocket.send(
                #             json.dumps({"cmd": "key", "key": key})
                #         )  # send key command to server - you must implement this send in the AI agent
                #         break

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return

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