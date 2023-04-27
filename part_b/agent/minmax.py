import copy
class Node:
    def __init__(self, board = None, parent = None):
        self.parent = parent
        self.value = 0
        self.action = None
        self.board = board
        self.child = None
        self.left =  None
        self.right = None

    
    def set_value(self, value):
        self.value = value

    def set_action(self, action):
        self.action = action
    def addchild(self, newchild):
        newchild.parent = self
        if (self.child == None):
            self.child = newchild
        else:
            self.child.left = newchild
            newchild.right = self.left



def get_cell(input_dic: dict[tuple: tuple], color: str) ->dict[tuple, tuple]:
    cell_dic = {}
    if (color == 'r'):
        for i in input_dic.keys():
            if (input_dic[i][0] == 'r'):
                cell_dic[i] = input_dic[i]
    if (color =='b'):
        for i in input_dic.keys():
            if (input_dic[i][0] == 'b'):
                cell_dic[i] = input_dic[i]
    return cell_dic

def if_goal(board: dict[tuple, tuple]):
    for i in board.keys():
        if board[i][0] == 'b':
            return False 
    return True 


def render_board(board: dict[tuple, tuple], ansi=False) -> str:
    """
    Visualise the Infexion hex board via a multiline ASCII string.
    The layout corresponds to the axial coordinate system as described in the
    game specification document.
    
    Example:

        >>> board = {
        ...     (5, 6): ("r", 2),
        ...     (1, 0): ("b", 2),
        ...     (1, 1): ("b", 1),
        ...     (3, 2): ("b", 1),
        ...     (1, 3): ("b", 3),
        ... }
        >>> print_board(board, ansi=False)

                                ..     
                            ..      ..     
                        ..      ..      ..     
                    ..      ..      ..      ..     
                ..      ..      ..      ..      ..     
            b2      ..      b1      ..      ..      ..     
        ..      b1      ..      ..      ..      ..      ..     
            ..      ..      ..      ..      ..      r2     
                ..      b3      ..      ..      ..     
                    ..      ..      ..      ..     
                        ..      ..      ..     
                            ..      ..     
                                ..     
    """
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


def evaluation(board: dict[tuple:tuple], colour: str):
    count = 0
    for cells in board.values():
        cell = list(cells)
        if (cell[0] == colour):
            count += cell[1]
    print(count)
    return count



def minmax(board: dict[tuple, tuple], colour: str):
    action_list = [0,0,0,0]
    directions = [[0,1],[-1,1],[-1,0],[0,-1],[1,-1],[1,0]]
    for position in board.keys():
        if board[position][0] == colour:
            parent = Node(board, None)
            action_list[0] = list(position)[0]
            action_list[1] = list(position)[1]
            for direction in directions:
                print("new direction\n")
                action_list[2] = direction[0]
                action_list[3] = direction[1]
                newboard = update_board(board, action_list, colour)
                c = Node(newboard, parent)
                c.action = direction
                c.value = evaluation(newboard, colour)
                parent.addchild(c)
                action_list = [0,0,0,0]
                for nposition in newboard.keys():
                    
                    if newboard[nposition][0] != colour:
                        print(nposition)
                        action_list[0] = list(nposition)[0]
                        action_list[1] = list(nposition)[1]
                        for ndirection in directions:
                            action_list[2] = ndirection[0]
                            action_list[3] = ndirection[1]
                            print(action_list)
                            nnboard = update_board(newboard, action_list, 'b')
                            nc = Node(nnboard, c)
                            nc.action = direction
                            nc.value = evaluation(nnboard, colour)
                            c.addchild(nc)
                        
                


def update_board(board:dict[tuple:tuple], action_list:list, colour: str) -> dict[tuple, tuple]:
    new_board = copy.deepcopy(board)
    power = -1
    r = action_list[0]
    q = action_list[1]
    
    if (r,q) in new_board and new_board[r,q][0] == colour:
        power = new_board[(r,q)][1]
        print(power)
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
                new_board[(r,q)] = (colour, 1)
            elif (r,q) in new_board:
                new_power = new_board[r,q][1]
                if new_board[r,q][1] == 6:
                    del new_board[(r,q)]
                else:
                    del new_board[(r,q)]
                    new_power += 1
                    new_board[r,q] = (colour, new_power)
    print(render_board(new_board, ansi=False))                

    return new_board   
def main():
    test_board = {(0,0):('b',5),(6,6):('r',1)}
    minmax(test_board, 'r')
    evaluation(test_board, 'r')
if __name__ == "__main__":
    main()