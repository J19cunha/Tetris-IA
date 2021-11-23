import pprint
def main():

    map = [[4, 27], [3, 28], [4, 28], [3, 29], [4, 25], [4, 26], [5, 26], [5, 27], [4, 22], [4, 23], [4, 24], [5, 24]]

    # cols = {}
    # heights = []
    # for x in range(1,9):
    #     cols[x] = sorted(column for column in map if column[0] == x)
    #     if cols[x] != []:
    #         heights.append(min(column[1] for column in cols[x]))
    #     else:
    #         heights.append(0)   
    
    # print(heights)

    # print(sum(heights))

    board=[[0 for i in range(1,9)] for j in range(1,30)]

    for coords in map:
        board[coords[1]-1][coords[0]-1] = 1

    pprint.pprint(board)

if __name__ == '__main__':
    main()