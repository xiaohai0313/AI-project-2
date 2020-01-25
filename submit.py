import queue
import os

from collections import OrderedDict
f1 = open("input.txt","r")
All_line = f1.readlines()
Task = []
for line in All_line:
    temp = line.strip('\n')
    temp = line.split('\t')
    temp = line.strip('\n')
    Task.append(temp)

Gametype = Task[0]
color = Task[1]
Time = Task[2]
grid = [n for n in Task[3:20]]
f1.close()
#print(grid)
Black_camp = [
    [0,0],[0,1],[0,2],[0,3],[0,4],
    [1,0],[1,1],[1,2],[1,3],[1,4],
    [2,0],[2,1],[2,2],[2,3],
    [3,0],[3,1],[3,2],
    [4,0],[4,1]]            # This is row col order!!

White_camp = [
    [15,15],[15,14],[15,13],[15,12],[15,11],
    [14,15],[14,14],[14,13],[14,12],[14,11],
    [13,15],[13,14],[13,13],[13,12],
    [12,15],[12,14],[12,13],
    [11,15],[11,14]]
mode = 0
white_camp_check = [[-1,0],[0,-1],[-1,-1]]
black_camp_check = [[1,0],[0,1],[1,1]]
#is_end = [False,0,None]          #end at which depth
#terminate = False

arrive_num = [0]

class node():
    def __init__(self,x):
        self.stack = x
        self.child = None
        self.parent = None
        self.movement = None            #[value,type,x,y,ToX,ToY]
        self.fl = 0
        self.sl = 0
        #self.depth = 0
        self.path = []


def output(res):
    result = []
    for path in res:
        if path[1] == 'E':
            result.append('E {},{} {},{}'.format(path[3],path[2],path[5],path[4]))                   # 1 is J
        elif path[1] == 'J':                                                               #[0 , x , y , x + row , y + col]
            result.append('J {},{} {},{}'.format(path[3],path[2],path[5],path[4]))

    return result

def single_mode_check_jump(x,y,camp,move,potential,visited,originalX,originalY,camp_check,enemy_camp,path):
    for row in range(-1, 2, 1):
        for col in range(-1, 2, 1):
            if 0 <= x <= 15 and 0 <= y <= 15 and 0 <= x + row <= 15 and 0 <= y + col <= 15 and 0 <= x + row * 2 <= 15 and 0 <= y + col * 2 <= 15 and (row != 0 or col != 0):

                if (grid[x + row][y + col] == 'W' or grid[x + row][y + col] == 'B') and grid[x + row * 2][y + col * 2] == '.' and [x + row * 2][y + col * 2] not in visited:  # maybe can jump
                    if ([originalX, originalX] in enemy_camp and [x + 2 * row, y + 2 * col] in enemy_camp) or [originalX, originalX] not in enemy_camp:
                        if [x + row * 2, y + col * 2] not in camp:
                            target = path + [0,'J', x, y, x + row * 2, y + col * 2]
                            move.append([target])
                            return
                        elif [row, col] in camp_check:
                            potential.append([path + [0,'J', x, y, x + row * 2, y + col * 2]])
                        else:
                            single_mode_check_jump(x + row * 2, y + col * 2, camp, move, potential, [[x, y],[x + row * 2,y + col * 2]], originalX, originalY, camp_check,enemy_camp,path + [0,'J', x, y, x + row * 2, y + col * 2])

def check_how_many_arrive(cur_grid):
    mycounter = 0
    target_camp = Black_camp if color == 'WHITE' else White_camp
    cur_color = 'W' if color == 'WHITE' else 'B'
    for num in target_camp:
        if cur_grid[num[0]][num[1]] == cur_color:
            mycounter+=1
    return mycounter

def check_validation(x,y,move,camp,potential):      #check point has valid move possible
    #return turn type [J/E , start y , start x , To y , To x]
    camp_check = white_camp_check if color == 'WHITE' else black_camp_check
    enemy_camp = White_camp if color == 'WHITE' else Black_camp
    if [x,y] in camp:
        for row in range(-1, 2, 1):
            for col in range(-1, 2, 1):
                if 0 <= x <= 15 and 0 <= y <= 15 and 0 <= x + row <= 15 and 0 <= y + col <= 15 and (x!= 0 or y != 0) and grid[x+row][y+col] == '.':                      # is valid place
                    if [x, y] in enemy_camp and [x + row, y + col] in enemy_camp or [x, y] not in enemy_camp:
                        if [x + row , y+col] not in camp:                                   #empty place can be move to
                            target =[0,'E' , x , y , x + row , y + col]
                            move.append([target])
                            return
                        elif [row,col] in camp_check:
                            potential.append([[0,'E' , x , y , x + row , y + col]])
                if 0 <= x <= 15 and 0 <= y <= 15 and 0 <= x + row <= 15 and 0 <= y + col <= 15 and 0 <= x + row * 2 <= 15 and 0 <= y + col * 2 <= 15 and (x!= 0 or y != 0) \
                        and (grid[x+row][y+col] == 'W' or grid[x+row][y+col] == 'B') and grid[x + row * 2][y + col * 2] == '.':       #maybe can jump
                    if [x + row * 2,y + col * 2] not in camp:
                        target = [0,'J', x, y, x + row * 2, y + col * 2]
                        move.append([target])
                        return
                    elif [row, col] in camp_check:
                        potential.append([[0,'J', x, y, x + row * 2, y + col * 2]])
                    else:
                        single_mode_check_jump(x + row * 2, y + col * 2,camp,move,potential,[[x,y],[x + row * 2,y + col * 2]],x,y,camp_check,enemy_camp,[0,'J', x, y, x + row * 2, y + col * 2])
                        if move != []:
                            return

    else:
        for row in range(-1,2,1):
            for col in range(-1,2,1):
                if 0 <= x + row <= 15 and 0 <= y + col <= 15 and  [x + row , y+col] not in camp and (row != 0 or col != 0):                      # is valid place
                        #check never go back camp rule
                    if grid[x+row][y+col] == '.':                                   #empty place can be move to
                        if ([x, y] in enemy_camp and [x + row, y + col] in enemy_camp) or [x, y] not in enemy_camp:
                            target = [0,'E' , x , y , x + row , y + col]
                            move.append([target])
                            return
                    elif (grid[x+row][y+col] == 'W' or grid[x+row][y+col] == 'B') and 0 <= x + row * 2 <= 15 and 0 <= y + col * 2 <= 15:       #maybe can jump
                        if grid[x + row * 2][y + col * 2] == '.' and  [x + row * 2,y + col * 2] not in camp:
                            if ([x, y] in enemy_camp and [x + 2 * row, y + 2 * col] in enemy_camp) or [x, y] not in enemy_camp:
                                target = [0,'J', x, y, x + row * 2, y + col * 2]
                                move.append([target])                         #差如果返回camp最后跳出来的情况
                                return

def single_mode():
    move = []
    potential = []
    some_in_camp = 0
    if color == 'BLACK':
        camp = Black_camp
        cur_color = 'B'
    else:
        camp = White_camp
        cur_color = 'W'
    for coor in camp:       #clean all camp first
        if grid[coor[0]][coor[1]] == 'B' and color == 'BLACK' or grid[coor[0]][coor[1]] == 'W' and color == 'WHITE':
            check_validation(coor[0], coor[1], move, camp, potential)
            if move != []:
                return move[0]
            some_in_camp += 1
    if some_in_camp != 0 and potential != []:
        return potential[0]

    if color == 'WHITE':
        #start search from bot right
        for row in range(0,16,1):
            for col in range(0,16,1):
                if grid[row][col] == 'W':
                    check_validation(row,col, move, camp,potential)
                    if move != []:
                        return move[0]

    elif color == 'BLACK':
        #start search from top left
        for row in range(15,0,-1):
            for col in range(15,0,-1):              #need check here
                if grid[row][col] == 'B':
                    check_validation(row,col,move,camp,potential)
                    if move != []:
                        return move[0]
    return potential[0]

def check_last_seven_node(my_grid):
    q = queue.PriorityQueue()
    if color == 'WHITE':
        for row in range(15,-1,-1):
            for col in range(15,-1,-1):
                if my_grid[row][col]=='W':
                    v = (15-row + 15 - col)
                    q.put([v,row,col])
    if color == 'BLACK':
        for row in range(0,16,1):
            for col in range(0,16,1):
                if my_grid[row][col]=='B':
                    v = (row + col)
                    q.put([v,row,col])

    re = []
    i = 0
    if mode == 3:
        i = 12
    elif mode == 2:
        i = 5
    while q.qsize() > 0 and i > 0:
        re.append(q.get()[1:])
        i -= 1
    return re

def if_can_jump(mynode,x,y,cur_color,camp,visited,originalX,originalY,depth,end_depth,move,potential,enemy_camp,terminate,final_result,cur_path,cur_arrive):                                     #orix,y to maintain the start jump point
    for row in range(-1, 2, 1):
        for col in range(-1, 2, 1):
            if (row != 0 or col != 0) and 0 <= x <= 15 and 0 <= y <= 15 and 0 <= x + 2 * row <= 15 and 0 <= y + 2 * col <= 15 and 0 <= x + row <= 15 and 0 <= y + col <= 15 and [x + row * 2, y + col * 2] not in visited:          # maybe can jump
                if (mynode.stack[x + row][y + col] == 'W' or mynode.stack[x + row][y + col] == 'B') and mynode.stack[x + row * 2][y + col * 2] == '.':

                    tempee = mynode.stack[:]  # is new replace
                    tempee[originalX] = tempee[originalX][:originalY] + '.' + tempee[originalX][originalY + 1:]                   # x -> oriX  10/20
                    tempee[x + 2 * row] = tempee[x + 2 * row][:y + 2 * col] + cur_color + tempee[x + 2 * row][y + 2 * col + 1:]
                    new_node = node(tempee)
                    value = ((x + 2 * row) + (y + 2 * col)) - (originalX + originalY) if cur_color == 'B' else (originalX + originalY) - (x + 2 * row + y + 2 * col)
                    if depth % 2 == 0:                  #0,2,4 depth
                        new_node.fl = mynode.fl + value
                        new_node.sl = mynode.sl
                    else:                               #1,3,5 depth
                        new_node.sl = mynode.sl + value
                        new_node.fl = mynode.fl
                    if mode == 6 and depth == end_depth:
                        value = new_node.sl - new_node.fl
                    elif (mode == 1 or mode == 3 or mode == 5 or mode == 2)and depth == end_depth:
                        value = new_node.sl + new_node.fl
                    '''if cur_arrive[0] > 16 and depth == end_depth:
                        if [originalX,originalY] in enemy_camp:
                            value -= 100
                        if [originalX,originalY] not in enemy_camp:
                            value += 500'''
                    new_node.movement = [value,'J', x,y, x + 2 * row, y + 2 *col]                             #[value,type,x,y,ToX,ToY]   10/23
                    new_node.path = cur_path + [new_node.movement]              #10/23
                    if cur_arrive[0] >= 8 and check_how_many_arrive(tempee) > cur_arrive[0]:
                    #if check_how_many_arrive(new_node.stack) > cur_arrive[0]:
                        new_node.movement[0] += 10000

                        new_node.parent = mynode
                        final_result[0] = [True, depth, new_node]
                        terminate[0] = [True]
                        return
                    if [originalX, originalY] in camp:
                        if [x + 2 * row, y + 2 * col] not in camp: #and firsttime == 0:

                            move.append([mynode,new_node])
                        elif mynode.child == None and move == [] and [x + 2 * row, y + 2 * col] in camp:
                            if cur_color == 'B' and x + 2 * row >= originalX and y + 2 * col >= originalY or cur_color == 'W' and x + 2 * row <= originalX and y + 2 * col <= originalY:


                                potential.append([mynode,new_node])
                    elif [x + 2 * row, y + 2 * col] not in camp and [originalX,originalY] not in enemy_camp and [x,y] not in enemy_camp:
                        new_node.parent = mynode
                        mynode.child.append(new_node)

                        if depth == end_depth:  # and final_result != []:

                            if new_node.movement[0] > final_result[0][2].movement[0]:
                                final_result[0] = [True, depth, new_node]
                        #visited.append([x + 2 * row, y + 2 * col])
                    elif [originalX,originalY] in enemy_camp and [x + 2 * row,y + 2 * col] in enemy_camp:
                        new_node.parent = mynode
                        mynode.child.append(new_node)

                        if depth == end_depth:  # and final_result != []:

                            if new_node.movement[0] > final_result[0][2].movement[0]:
                                final_result[0] = [True, depth, new_node]
                        #visited.append([x + 2 * row, y + 2 * col])
                    visited.append([x + 2 * row, y + 2 * col])
                    if_can_jump(mynode,x + 2 * row , y + 2 * col , cur_color ,camp,visited,originalX,originalY,depth,end_depth,move,potential,enemy_camp,terminate,final_result,new_node.path,cur_arrive)         #temp not camp anymore
    return

def game_mode_move_search(mynode,x,y,cur_color,depth,end_depth,move,potential,terminate,final_result,cur_arrive,visited):                          #seach algorithm          fl = first level sl = second level
    if cur_color == 'B':
        camp = Black_camp
    else:
        camp = White_camp
    enemy_camp = White_camp if color == 'BLACK' else Black_camp
    for row in range(-1, 2, 1):           # x y is valid, for move check one box around, for jump check 2 box around
        for col in range(-1, 2, 1):
            if 0 <= x + row <= 15 and 0 <= y + col <= 15 and (row != 0 or col != 0): #and (not node_in_camp and [x+row,y+col] in forward):

                if mynode.stack[x + row][y + col] == '.':#and [x+row,y+col] not in visited:                                                                                                      # check never go back camp rule empty place can be move to
                    tempe = mynode.stack[:] # is new replace
                    tempe[x] = tempe[x][:y] + '.' + tempe[x][y+1:]
                    tempe[x + row] = tempe[x + row][:y + col] + cur_color + tempe[x + row ][y+col+1:]
                    new_node = node(tempe)
                    value = ((x + row) + (y + col)) - (x + y) if cur_color == 'B' else (x + y) - (x + row + y + col)

                    if depth % 2 == 0:                                          # 0,2,4 depth
                        new_node.fl = mynode.fl + value
                        new_node.sl = mynode.sl
                    else:                                                       # 1,3,5 depth
                        new_node.sl = mynode.sl + value
                        new_node.fl = mynode.fl
                    if mode == 6 and depth == end_depth:
                        value = new_node.sl - new_node.fl
                    elif (mode == 1 or mode == 3 or mode == 5 or mode == 2) and depth == end_depth:
                        value = new_node.sl + new_node.fl
                    '''if cur_arrive[0] > 16 and depth == end_depth:
                        if [x,y] in enemy_camp:
                            value -= 100
                        elif [x,y] not in enemy_camp:
                            value += 500'''
                    new_node.movement = [value,'E',x,y,x+row,y+col]

                    new_node.path = [new_node.movement]
                    if cur_arrive[0] >= 8 and check_how_many_arrive(new_node.stack) > cur_arrive[0]:
                    #if check_how_many_arrive(new_node.stack) > cur_arrive[0]:
                        new_node.movement[0] += 10000

                        new_node.parent = mynode

                        final_result[0] = [True, depth, new_node]
                        terminate[0] = [True]
                        return


                    camp_check = white_camp_check if color == 'WHITE' else black_camp_check
                    if [x,y] in camp:
                        if [x + row, y + col] not in camp:

                            move.append([mynode,new_node])
                        elif mynode.child == None and move == [] and [x+row,y+col] in camp and [row,col] in camp_check:

                            potential.append([mynode,new_node])

                    elif [x + row, y + col] not in camp and [x,y] not in enemy_camp and [row, col] in camp_check:

                        if depth == end_depth:  # and final_result != []:

                            if new_node.movement[0] > final_result[0][2].movement[0]:
                                final_result[0] = [True, depth, new_node]

                        new_node.parent = mynode
                        mynode.child.append(new_node)
                    elif [x,y] in enemy_camp and [x + row, y + col] in enemy_camp:

                        if depth == end_depth:  # and final_result != []:

                            if new_node.movement[0] > final_result[0][2].movement[0]:
                                final_result[0] = [True, depth, new_node]

                        new_node.parent = mynode
                        mynode.child.append(new_node)


                elif 0 <= x + 2 * row <= 15 and 0 <= y + 2 * col <= 15 and (mynode.stack[x + row][y + col] == 'B' or mynode.stack[x + row][y + col] == 'W'):  # maybe can jump
                    if mynode.stack[x + row * 2][y + col * 2] == '.' and [x + row * 2,y + col * 2] not in visited:          #1942
                        if_can_jump(mynode,x,y,cur_color,camp,visited,x,y,depth,end_depth,move,potential,enemy_camp,terminate,final_result,mynode.path,cur_arrive)
    return

def black_search(mynode,depth,end_depth,terminate,final_result):                                           #each search call
    changes = 0
    move = []
    potential = []
    search = []
    visited = []
    for nodes in Black_camp:
        if mynode.stack[nodes[0]][nodes[1]] == 'B':
            game_mode_move_search(mynode, nodes[0],nodes[1], 'B', depth, end_depth, move, potential,terminate,final_result,arrive_num,visited)
            changes += 1
    if mynode.child == None:
        mynode.child = []
    if len(move) != 0:
        for nodes in move:
            #if mynode.child == None:
             #   mynode.child = []

            nodes[0].child.append(nodes[1])
            nodes[1].parent = nodes[0]
            if depth == end_depth:  # and final_result != []:
                if nodes[1].movement[0] > final_result[0][2].movement[0]:       #1024
                    final_result[0] = [True, depth, nodes[1]]
    elif len(move)==0 and len(potential) != 0: #and mynode.child == None:
        #if mynode.child == None:
            #mynode.child = []
        for nodes in potential:

            nodes[0].child.append(nodes[1])
            nodes[1].parent = nodes[0]
            if depth == end_depth:  # and final_result != []:
                if nodes[1].movement[0] > final_result[0][2].movement[0]:       #1024
                    final_result[0] = [True, depth, nodes[1]]
    elif mode == 3 or mode == 2:
        search = check_last_seven_node(mynode.stack)
        for cur_node in search:
            if mynode.stack[cur_node[0]][cur_node[1]] == 'B':
                game_mode_move_search(mynode,cur_node[0],cur_node[1],'B',depth,end_depth, move, potential,terminate,final_result,arrive_num,visited)

    else:
        for row in range(0, 16, 1):
            for col in range(0, 16, 1):
                if mynode.stack[row][col] == 'B':
                    game_mode_move_search(mynode,row,col,'B',depth,end_depth, move, potential,terminate,final_result,arrive_num,visited)
    return

def white_search(mynode,depth,end_depth,terminate,final_result):
    changes = 0
    move = []
    potential = []
    visited = []
    for nodes in White_camp:
        if mynode.stack[nodes[0]][nodes[1]] == 'W':
            changes += 1
            game_mode_move_search(mynode, nodes[0],nodes[1], 'W', depth, end_depth, move, potential,terminate,final_result,arrive_num,visited)

    if mynode.child == None:
        mynode.child = []
    if len(move) != 0:
        for nodes in move:
            #if mynode.child == None:
            #    mynode.child = []
            nodes[0].child.append(nodes[1])
            nodes[1].parent = nodes[0]
            if depth == end_depth:  # and final_result != []:
                if nodes[1].movement[0] > final_result[0][2].movement[0]:       #1024
                    final_result[0] = [True, depth, nodes[1]]
    elif len(move) == 0 and len(potential) != 0:
        #if mynode.child == None:
        #    mynode.child = []
        for nodes in potential:
            nodes[0].child.append(nodes[1])
            nodes[1].parent = nodes[0]
            if depth == end_depth:  # and final_result != []:
                if nodes[1].movement[0] > final_result[0][2].movement[0]:       #1024
                    final_result[0] = [True, depth, nodes[1]]
    #if changes == 0:
    elif mode == 3 or mode == 2:
        search = check_last_seven_node(mynode.stack)

        for cur_node in search:
            if mynode.stack[cur_node[0]][cur_node[1]] == 'W':
                game_mode_move_search(mynode, cur_node[0], cur_node[1], 'W', depth, end_depth, move, potential,terminate, final_result,arrive_num,visited)

    else:
        for row in range(15, -1, -1):
            for col in range(15, -1, -1):  # need check here
                if mynode.stack[row][col] == 'W':
                    game_mode_move_search(mynode,row,col,'W',depth,end_depth, move, potential,terminate,final_result,arrive_num,visited)
    return

def minimax(mynode):
    #if color == 'BLACK':
    action = max_test(mynode,float('-INF'),float('INF'))
    #elif color == 'WHITE':
    #    action = max_test(mynode, float('-INF'), float('INF'))
    return action

def max_test(mynode,alpha,beta):
    if mynode.child == None:
        return mynode
    value = node([])
    value.movement = [float('-INF')]
    for x in mynode.child:
        if mode == 1 or mode == 3 or mode == 5 or mode == 2 or mode == 4:
            tempe = max_test(x, alpha, beta)
        else:
            tempe = min_test(x,alpha,beta)
        value = value if value.movement[0] > tempe.movement[0] else tempe
        if value.movement[0] > beta:
            return value
        alpha = max(alpha,value.movement[0])
    return value            #需要返回node 而不是值

def min_test(mynode,alpha,beta):
    if mynode.child == None:
        return mynode
    value = node([])
    value.movement = [float('INF')]
    for x in mynode.child:
        tempe = max_test(x, alpha, beta)

        value = value if value.movement[0] < tempe.movement[0] else tempe
        if value.movement[0] < alpha:
            return value
        beta = min(beta, value.movement[0])

    return value

def game_mode(terminate,final_result):                                                    #level search frame
    #[0 , x , y , x + row , y + col]
    if mode == 1:                   #only consider myself, in later game, move forward fast is the only condition
        if color == 'WHITE':
            mynode = node(grid)
            white_search(mynode,1,3,terminate,final_result)    #current depth, end depth
            for x in mynode.child:
                if not terminate[0]:
                    white_search(x,2,3,terminate,final_result)
                else:
                    return
            for y in mynode.child:
                for z in y.child:
                    if not terminate[0]:
                        white_search(z,3,3,terminate,final_result)
            return mynode
        elif color == 'BLACK':
            mynode = node(grid)
            black_search(mynode,1,3,terminate,final_result)
            for x in mynode.child:
                if not terminate[0]:
                    black_search(x,2,3,terminate,final_result)
                else:
                    return
            for y in mynode.child:
                for z in y.child:
                    if not terminate[0]:
                        black_search(z,3,3,terminate,final_result)
                    else:
                        return
            return mynode
        return

    elif mode == 2:                 #in middle only run depth 2, python suck for depth 3=-=
        if color == 'WHITE':
            mynode = node(grid)
            white_search(mynode,1,3,terminate,final_result)         ##10/24/2025
            for x in mynode.child:
                white_search(x,2,3,terminate,final_result)
            for y in mynode.child:
                for z in y.child:
                    white_search(z,3,3,terminate,final_result)
            return mynode
        elif color == 'BLACK':
            mynode = node(grid)
            black_search(mynode,1,3,terminate,final_result)
            for x in mynode.child:
                black_search(x,2,3,terminate,final_result)
            for y in mynode.child:
                for z in y.child:
                    black_search(z,3,3,terminate,final_result)
            return mynode
        return

    elif mode == 3:                   #only consider myself, in later game, move forward fast is the only condition
        if color == 'WHITE':
            mynode = node(grid)
            white_search(mynode,1,3,terminate,final_result)    #current depth, end depth
            for x in mynode.child:
                white_search(x,2,3,terminate,final_result)
            for y in mynode.child:
                for z in y.child:
                    white_search(z,3,3,terminate,final_result)
            return mynode
        elif color == 'BLACK':
            mynode = node(grid)
            black_search(mynode,1,3,terminate,final_result)
            for x in mynode.child:
                black_search(x,2,3,terminate,final_result)
            for y in mynode.child:
                for z in y.child:
                    black_search(z,3,3,terminate,final_result)
            return mynode
        return

    elif mode == 4:                     #depth 3 for test
        if color == 'WHITE':
            mynode = node(grid)
            white_search(mynode,1,1,terminate,final_result)                                  # 3 need - 2 value
            return mynode
        elif color == 'BLACK':
            mynode = node(grid)
            black_search(mynode,1,1,terminate,final_result)
            return mynode
        return
    elif mode == 5:                   #only consider myself, in later game, move forward fast is the only condition
        if color == 'WHITE':
            mynode = node(grid)                                                                         #1024 2031
            white_search(mynode,1,3,terminate,final_result)    #current depth, end depth
            for x in mynode.child:
                white_search(x,2,3,terminate,final_result)
            for y in mynode.child:
                for z in y.child:
                   white_search(z,3,3,terminate,final_result)
            return mynode
        elif color == 'BLACK':
            mynode = node(grid)
            black_search(mynode,1,3,terminate,final_result)
            for x in mynode.child:
                black_search(x,2,3,terminate,final_result)
            for y in mynode.child:
                for z in y.child:
                    black_search(z,3,3,terminate,final_result)
            return mynode
        return
    elif mode == 6:                   #only consider myself, in later game, move forward fast is the only condition
        if color == 'WHITE':
            mynode = node(grid)
            white_search(mynode,1,2,terminate,final_result)    #current depth, end depth
            for x in mynode.child:
                black_search(x,2,2,terminate,final_result)
            for y in mynode.child:
                for z in y.child:
                   white_search(z,3,3,terminate,final_result)
            return mynode
        elif color == 'BLACK':
            mynode = node(grid)
            black_search(mynode,1,2,terminate,final_result)
            for x in mynode.child:
                black_search(x,2,2,terminate,final_result)
            for y in mynode.child:
                for z in y.child:
                    black_search(z,3,3,terminate,final_result)
            return mynode
        return

def initial_step_for_GAME_mode(steps):
    result = []
    white_start = [[12,13],[14,15],[11,15],[14,12],
                   [12,14],[13,15],[13,12],[13,14],
                   [15,14],[15,13],[12,15],[13,13]]

    w_check_white = [[[]],[[13,14],[11,12]],[[11,14],[11,12],[10,11]],[[13,12],[11,12],[10,11]],
                     [[13,13],[13,12],[11,12],[9,11]],[[12,15],[11,14],[11,12],[10,10],[8,10]],
                     [[]],[[13,13],[12,11],[10,10],[8,10]],[[14,13],[12,11],[10,10],[9,11]],
                     [[14,14],[12,15],[11,14],[11,12],[10,10]],[[11,14],[9,12],[7,10]],[[]]]

    w_check_dot = [[[11,12]],[[12,13],[10,11]],[[11,13],[11,11],[9,11]],[[12,12],[10,12],[10,10]],
                   [[14,12],[12,12],[10,12],[8,10]],[[11,15],[11,13],[11,11],[9,9],[7,11]],
                   [[12,11]],[[13,12],[11,10],[9,10],[7,10]],[[13,12],[11,10],[9,10],[9,12]],
                   [[13,15],[11,15],[11,13],[11,11],[9,9]],[[10,13],[8,11],[6,9]],[[12,12]]]

    w_print_out = [[[0,'E',12,13,11,12]],
                   [[0,'J',14,15,12,13],[0,'J',12,13,10,11]],
                   [[0,'J',11,15,11,13],[0,'J',11,13,11,11],[0,'J',11,11,9,11]],
                   [[0,'J',14,12,12,12],[0,'J',12,12,10,12],[0,'J',10,12,10,10]],
                   [[0,'J',12,14,14,12],[0,'J',14,12,12,12],[0,'J',12,12,10,12],[0,'J',10,12,8,10]],
                   [[0,'J',13,15,11,15],[0,'J',11,15,11,13],[0,'J',11,13,11,11],[0,'J',11,11,9,9],[0,'J',9,9,7,11]],
                   [[0,'E',13,12,12,11]],
                   [[0,'J',13,14,13,12],[0,'J',13,12,11,10],[0,'J',11,10,9,10],[0,'J',9,10,7,10]],
                   [[0,'J',15,14,13,14],[0,'J',13,14,13,12],[0,'J',13,12,11,10],[0,'J',11,10,9,10],[0,'J',9,10,9,12]],
                   [[0,'J',15,13,13,15],[0,'J',13,15,11,15],[0,'J',11,15,11,13],[0,'J',11,13,11,11],[0,'J',11,11,9,9]],
                   [[0,'J',12,15,10,13],[0,'J',10,13,8,11],[0,'J',8,11,6,9]],
                   [[0,'E',13,13,12,12]]]





    ''' white_end = [[11,12],[10,11],[9,11],[10,10],
                 [8,10],[7,11],[12,11],[7,10],
                 [9,12],[9,9],[6,9]]
    '''
    black_start = [[3, 2], [1, 0], [4, 0], [1, 3],
                   [3, 1], [2, 0], [2, 3], [2, 1],
                   [0, 1], [0, 2],[3,0],[2,2]]

    b_check_black = [[[]], [[2, 1], [4, 3]], [[4, 1], [4, 3], [5, 4]], [[2, 3], [4, 3], [6, 4]],
                     [[2, 2], [2, 3], [4, 3], [5, 4]], [[3, 0], [4, 1], [4, 3], [5, 5], [7, 5]],
                     [[]], [[2, 2], [3, 4], [5, 5], [7, 5]], [[1, 2], [3, 4], [5, 5], [6, 4]],
                     [[1, 1], [3, 0], [4, 1], [4, 3], [5, 5]],[[4,1],[6,3],[8,5]],[[]]]

    b_check_dot = [[[4, 3]], [[3, 2], [5, 4]], [[4, 2], [4, 4], [6, 4]], [[3,3], [5, 3], [7, 5]],
                   [[1, 3], [3, 3], [5, 3], [5, 5]], [[4, 0], [4, 2], [4, 4], [6, 6], [8, 4]],
                   [[3,4]], [[2, 3], [4, 5], [6, 5], [8, 5]], [[2, 3], [4, 5], [6, 5], [6, 3]],
                   [[2, 0], [4, 0], [4, 2], [4, 4],[6,6]],[[5,2],[7,4],[9,6]],[[3,3]]]

    b_print_out = [[[0,'E',3,2,4,3]],
                   [[0,'J',1,0,3, 2], [0,'J',3,2,5, 4]],
                   [[0,'J',4,0,4, 2], [0,'J',4,2,4, 4], [0,'J',4,4,6, 4]],
                   [[0,'J',1,3,3,3], [0,'J',3,3,5, 3], [0,'J',5,3,7, 5]],
                   [[0,'J',3,1,1, 3], [0,'J',1,3,3, 3], [0,'J',3,3,5, 3], [0,'J',5,3,5, 5]],
                   [[0,'J',2,0,4, 0], [0,'J',4,0,4, 2], [0,'J',4,2,4, 4], [0,'J',4,4,6, 6], [0,'J',6,6,8, 4]],
                   [[0,'E',2,3,3,4]],
                   [[0,'J',2,1,2, 3], [0,'J',2,3,4, 5], [0,'J',4,5,6, 5], [0,'J',6,5,8, 5]],
                   [[0,'J',0,1,2, 3], [0,'J',2,3,4, 5], [0,'J',4,5,6, 5], [0,'J',6,5,6, 3]],
                   [[0,'J',0,2,2, 0], [0,'J',2,0,4, 0], [0,'J',4,0,4, 2], [0,'J',4,2,4, 4],[0,'J',4,4,6,6]],
                   [[0,'J',3,0,5,2],[0,'J',5,2,7,4],[0,'J',7,4,9,6]],
                   [[0,'E',2,2,3,3]]]
   # work_type = ['E','J','J','J','J','J','E','J','J','J','J']

    '''black_end = [[4, 3], [5, 4], [6, 4], [7, 5],
                 [5, 5], [8, 4], [3,4], [8, 5],
                 [6, 3], [6, 6],[9,6]]

    '''
    checker = None
    if color == 'WHITE':
        check_start = white_start[steps]
        check_color = w_check_white[steps]
        check_dot = w_check_dot[steps]
       # check_end = white_end[steps]
        checker = 'W'
        cur_print_out = w_print_out[steps]
        #cur_type = work_type[steps]
    else:
        check_start = black_start[steps]
        check_color = b_check_black[steps]
        check_dot = b_check_dot[steps]
        #check_end = black_end[steps]
        checker = 'B'
        cur_print_out = b_print_out[steps]
        #cur_type = work_type[steps]
    if grid[check_start[0]][check_start[1]] == checker:
        for num1 in check_color:
            if num1 != []:
                if grid[num1[0]][num1[1]] == 'W' or grid[num1[0]][num1[1]] == 'B':
                    continue
                else:
                    result = [False]
                    return result
        for num2 in check_dot:
            if num2 != []:
                if grid[num2[0]][num2[1]] == '.':
                    continue
                else:
                    result = [False]
                    return result
    else:
        result = [False]
        return result
    #result = [True,cur_type,check_start[0],check_start[1],check_dot[-1][0],check_dot[-1][1]]
    result = [True,cur_print_out]
    return result

def if_have_node_in_camp():
    if color == 'WHITE':
        for nodes in White_camp:
            if grid[nodes[0]][nodes[1]] == 'W':
                return True
    elif color == 'BLACK':
        for nodes in Black_camp:
            if grid[nodes[0]][nodes[1]] == 'B':
                return True
    return False

def last_one_step_in(mygrid):
    if color == 'WHITE':
        check_list = [[5,0],[5,1],[4,2],[3,3],[2,4],[1,5],[0,5]]
        forward = [[-1,0],[-1,-1],[0,-1]]
        for coor in check_list:
            if mygrid[coor[0]][coor[1]] == 'W':
                return [False]
        for col in range(15,0,-1):
            for row in range(0,15,1):
                if grid[row][col] == 'W':
                    for x in forward:
                        if 0 <= row+x[0] <= 15 and 0 <= col+x[1] <= 15 and grid[row+x[0]][col+x[1]] == '.':
                            return [True,[[0,'E',row,col,row+x[0],col+x[1]]]]

    else:
        check_list = [[15,10],[14,10],[13,11],[12,12],[11,13],[10,14],[10,15]]
        forward = [[1, 0], [1, 1], [0, 1]]
        for coor in check_list:
            if mygrid[coor[0]][coor[1]] == 'B':
                return [False]
        for col in range(0, 15, 1):
            for row in range(15, 0, -1):
                if grid[row][col] == 'B':
                    for x in forward:
                        if 0 <= row+x[0] <= 15 and 0 <= col+x[1] <= 15 and grid[row + x[0]][col + x[1]] == '.':
                            return [True,[[0, 'E', row, col, row + x[0], col + x[1]]]]
    return [False]


if __name__=="__main__":
    counter = 0
    terminate = [False]
    initial_node = node(grid)
    initial_node.movement = [0]
    final_result = [[False,0,initial_node]]
    res = None
    if Gametype == 'SINGLE':
        res = single_mode()
    else:
        if os.path.isfile("playdata.txt"):
            fo = open("playdata.txt", "r")
            Steps = fo.readlines()
            counter = int(Steps[0])
            fo.close()
            if counter <= 11:
                result = initial_step_for_GAME_mode(counter)
                if result[0] == True:
                    res = result[1]
                else:
                    mode = 5
                    mynode = game_mode(terminate,final_result)
                    res = final_result[0][2]
                    for num in range(final_result[0][1] - 1):  # True,depth,new_node
                        res = res.parent
                    # res = res.movement[1:]
                    res = res.path
                    #bottom = minimax(mynode)
                    #res = bottom.parent.parent.path
            else:
                #mode = 1 if if_have_node_in_camp() else 3
                arrive_num[0] = check_how_many_arrive(grid)
                if arrive_num[0] == 18 and last_one_step_in(grid)[0] == True:
                    res = last_one_step_in(grid)[1]
                elif arrive_num[0] >= 12:
                    mode = 1                   #3 check last 12
                elif 14 <= counter <= 17:
                    mode = 1                   #1235 BBB WWW
                elif 21 <= counter <= 25 or 31 <= counter <= 35:# or 44 <= counter <= 55:
                    mode = 3                    #4 B W  last 4 3

                elif 26 <= counter <= 30 or 36 <= counter <= 47:
                    mode = 2                    #2 check last 4 1506 1024 2
                else:
                    mode = 5

                #elif counter % 2 != 0:
                #    mode = 5                    #2 BWB WBW
                #else:                           #5 BB WW
                #    mode = 4
                mynode = game_mode(terminate,final_result)
                #mode = 6
                #if terminate[0] == False and mode == 6:
                #    bottom = minimax(mynode)
                #    res = bottom.parent.parent.movement[1:]
                if terminate[0] or mode == 3 or mode == 1 or mode == 5 or mode == 4 or mode == 2:
                    res = final_result[0][2]
                    for num in range(final_result[0][1] - 1):          #True,depth,new_node
                        res = res.parent
                    res = res.path

            fp = open("playdata.txt", "w")
            #if color == 'WHITE':
            counter += 1            #MUST DELETE BEFORE SUBMIT TEST ONLY !!!!!!!!!!!!!!!!!!!!!!
            fp.write(str(counter))
            fp.close()
        else:
            result = initial_step_for_GAME_mode(0)
            if result[0] == True:
                res = result[1]
            else:
                mode = 5
                mynode = game_mode(terminate, final_result)
                res = final_result[0][2]
                for num in range(final_result[0][1] - 1):  # True,depth,new_node
                    res = res.parent
                res = res.path
            fp = open("playdata.txt", "w")
            fp.write(str(1))
            fp.close()



    #print(mode)
    #print(counter)
    #print(res)
    final = output(res)
    print_out , rlength = '' , 0
    for x in final:
        print_out += x
        if rlength < len(final) - 1:
            print_out += '\n'
            rlength += 1
    #print(print_out)
    f = open("output.txt", "w")
    for x in print_out:
        f.write(x)
    #print(output(res)[0])
    f.close()