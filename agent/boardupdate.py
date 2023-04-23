import copy
from referee.game import HexDir, HexPos
def update_board(board:dict[tuple:tuple], action_list:tuple) -> dict[tuple, tuple]:
    new_board = copy.deepcopy(board)
    power = -1
    r = action_list[0]
    q = action_list[1]
    if (r,q) in new_board and new_board[r,q][0] == 'r':
        power = new_board[(r,q)][1]
        del new_board[(r,q)]
        for i in range(power):
            r += action_list[2]
            q += action_list[3]
            if r == 7:
                r = 0
            if q == 7:
                q = 0
            if r == -1:
                r = 6
            if q == -1:
                q = 6
            if (r,q) not in new_board:
                new_board[(r,q)] = ('r', 1)
            elif (r,q) in new_board:
                new_power = new_board[r,q][1]
                if new_board[r,q][1] == 6:
                    del new_board[(r,q)]
                else:
                    del new_board[(r,q)]
                    new_power += 1
                    new_board[r,q] = ('r', new_power)
    return new_board   

