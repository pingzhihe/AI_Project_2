import copy
import sys
sys.path.append('C:\AI\AI_Project_2')
from referee.game import Board, SpawnAction, HexPos, SpreadAction, HexDir,Action
from referee.game.player import PlayerColor


def apply_ansi(str, bold=True, color=None):
    bold_code = "\033[1m" if bold else ""
    color_code = ""
    if color == "r":
        color_code = "\033[31m"
    if color == "b":
        color_code = "\033[34m"
    return f"{bold_code}{color_code}{str}\033[0m"


def spread_board(board:dict[tuple:tuple], action_list:tuple, color: str) -> dict[tuple, tuple]:
    new_board = copy.deepcopy(board)
    power = -1
    r = action_list[0]
    q = action_list[1]
    if (r,q) in new_board and new_board[(r,q)][0] == color:
        power = new_board[(r,q)][1]
        del new_board[(r,q)]
        for _ in range(power):
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
                new_board[(r,q)] = (color, 1)
            elif (r,q) in new_board:
                new_power = new_board[r,q][1]
                if new_board[r,q][1] == 6:
                    del new_board[(r,q)]
                else:
                    del new_board[(r,q)]
                    new_power += 1
                    new_board[r,q] = (color, new_power)
    return new_board   


def render_board(board: dict[tuple, tuple], ansi=False) -> str:
    
    dim = 7
    output = ""
    for row in range(dim * 2 - 1):
        output += "    " * abs((dim - 1) - row)
        for col in range(dim - abs(row - (dim - 1))):
            # Map row, col to r, q
            r = max((dim - 1) - row, 0) + col
            q = max(row - (dim - 1), 0) + col
            if (r, q) in board:
                color, power = board[(r, q)]
                text = f"{color}{power}".center(4)
                if ansi:
                    output += apply_ansi(text, color=color, bold=False)
                else:
                    output += text
            else:
                output += " .. "
            output += "    "
        output += "\n"
    return output

def spawn_board(board: dict[tuple: tuple], pos: tuple, color: str)-> dict[tuple, tuple]:
    new_board = copy.deepcopy(board)
    if pos not in new_board:
        new_board[pos] = (color,1)
    return new_board


def spread_convertor(dir: HexDir, pos: HexPos) -> tuple:
    r = pos.r
    q = pos.q
    dr = 0
    dq = 0
    match dir:
        case HexDir.Down:
            dr = -1
            dq = 1
        case HexDir.Up:
            dr = 1
            dq = -1
        case HexDir.UpRight:
            dr = 1
            dq = 0
        case HexDir.UpLeft:
            dr = 0
            dq = -1
        case HexDir.DownLeft:
            dr = -1
            dq = 0
        case _:
            dr = 0
            dq = 1

    return (r,q,dr,dq)

def spawn_convertor(pos:HexPos)-> tuple:
    r =pos.r
    q = pos.q
    return (r,q)

def spreadaction_convertor(action_tuple: tuple)->SpreadAction:
    r = action_tuple[0]
    q = action_tuple[1]
    dr = action_tuple[2]
    dq = action_tuple[3]
    pos = HexPos(r,q)
    dir = HexDir.Down
    match (dr, dq):
        case (1, -1):
            dir = HexDir.Up
        case (1,0):
            dir = HexDir.UpRight
        case (0,-1):
            dir = HexDir.UpLeft
        case (0,1):
            dir = HexDir.DownRight
        case (-1, 0):
            dir = HexDir.DownLeft
    print(dir)
    return (SpreadAction(pos,dir))

def spawnaction_convertor(pos:tuple)-> SpawnAction:
    r = pos[0]
    q = pos[1]
    pos = HexPos(r,q)
    return SpawnAction(pos)

def get_legal_spawn(board:dict[tuple: tuple]):
    can = []
    power = 0
    for value in board.values():
        power += value[1]
        if power >= 49:
            return []
    for r in range(7):
        for q in range(7):
            if (r,q) not in board:
                can.append((r,q))
    return can


def get_legal_spread(turn:str, state: dict[tuple, tuple]):
    spread_list = []
    direction_list = [(1,-1),(-1,1),(1,0),(0,1),(0,-1),(-1,0)]
    length = len(direction_list)
    if turn == 'r':
        for (r,q) in state:
            if state[(r,q)][0] == 'r':
                for i in range(length):
                    t = direction_list[i]
                    spread_list.append((r,q,t[0],t[1]))
    else:
        for (r,q) in state:
            if state[(r,q)][0] == 'b': 
                for i in range(length):
                    t = direction_list[i]
                    spread_list.append((r,q,t[0],t[1]))
    return spread_list



