import copy
import time

class Team17():
    def __init__(self):
        self.flag = ""
        self.count_plyr = 0
        self.count_opp = 0
        self.depth_limit = 3
        self.max = 10000000000000
        self.timer = 15
        self.startTime = ""
        self.utility_matrix = []

    def move(self, board, old_move, player_flag):
        self.startTime = time.time()
        self.flag = player_flag
        self.utility_matrix = [0,-1,-10,-100,-1000,1,0,0,100,0,10,0,0,0,0,100,0,0,0,0,1000,0,0,0,0]

        if old_move == (-1, -1):
            return (8, 8)

        opp_flag = 'o' if self.flag == 'x' else 'x'

        temp_board = copy.deepcopy(board)
        temp_block = copy.deepcopy(board.block_status)
        available_moves = board.find_valid_move_cells(old_move)

        for i in range(4):
            for j in range(4):
                if temp_block[i][j] == player_flag:
                    self.count_plyr += 1
                elif temp_block[i][j] == opp_flag:
                    self.count_opp += 1

        blocks_available = []
        for move in available_moves:
            x, y = move[0]/4, move[1]/4
            if [x,y] not in blocks_available:
                blocks_available.append([x,y])
        #print blocks_available

        plyr_win_block = self.check_win_block(temp_board, blocks_available, player_flag)
        if plyr_win_block != (-1 ,-1):
            return (plyr_win_block[0], plyr_win_block[1])

        opp_win_block = self.check_win_block(temp_board, blocks_available, opp_flag)
        if opp_win_block != (-1 ,-1):
            return (opp_win_block[0], opp_win_block[1])

        tentative_move, max_depth = (0,0,0), 2

        while time.time() - self.startTime < self.timer:
            best_move = tentative_move
            tentative_move = self.minimax(temp_board, old_move, True, player_flag, opp_flag, 0, -self.max, self.max, -1,-1, max_depth)
            max_depth += 1

        available_moves = board.find_valid_move_cells(old_move)
        if (best_move[1], best_move[2]) in available_moves:
            return (best_move[1], best_move[2])
        else:
            return random.choice(available_moves)

    def minimax(self, board, old_move, is_max, player_sign, opponent_sign, depth, alpha, beta, best_row, best_col, max_depth):
        if time.time() - self.startTime > self.timer:
            return (0, best_row, best_col)

        available_moves = board.find_valid_move_cells(old_move)

        if depth == max_depth or len(available_moves) == 0:
            utility = self.utility_get(board, player_sign, opponent_sign)
            return (utility, best_row, best_col)

        if len(available_moves) > 20 and depth == 0:
            self.depth_limit = min(2, self.depth_limit)

        if is_max:
            for move in available_moves:
                temp_board = copy.deepcopy(board)
                temp_board.update(old_move, move, player_sign)
                utility = self.minimax(temp_board, move, not is_max, player_sign, opponent_sign, depth+1 , alpha, beta, best_row, best_col, max_depth) # agains call minimax
                tent_val = utility[0]
                if tent_val > alpha:
                    alpha , best_row, best_col = utility[0], move[0], move[1]

                if alpha > beta:
                    break

                if time.time() - self.startTime > self.timer:
                    return (utility, best_row, best_col)

            return (alpha, best_row, best_col)

        else:
            for move in available_moves:
                temp_board = copy.deepcopy(board)
                temp_board.update(old_move, move, opponent_sign)
                utility = self.minimax(temp_board, move, is_max, player_sign, opponent_sign, depth+1 , alpha, beta, best_row, best_col, max_depth)
                tent_val = utility[0]
                if tent_val < beta:
                    beta, best_row, best_col = utility[0], move[0], move[1]

                if alpha > beta:
                    break;

                if time.time() - self.startTime > self.timer:
                    return (utility, best_row, best_col)

            return (beta, best_row, best_col)

    def check_win_block(self, temp_board, blocks_available, flag):
        for k in blocks_available:
            board_x, board_y = 4*k[0], 4*k[1]
            for i in range(4):
                count_plyr , empty = 0, 0
                for j in range(4):
                    if temp_board.board_status[board_x + i][board_y + j] == flag:
                        count_plyr +=1
                    elif temp_board.board_status[board_x + i][board_y + j] == '-':
                        empty, tent_x, tent_y = 1, board_x + i, board_y + j
                if count_plyr == 3 and empty == 1:
                    return (tent_x, tent_y)

            for i in range(4):
                count_plyr , empty = 0, 0
                for j in range(4):
                    if temp_board.board_status[board_x + j][board_y + i] == flag:
                        count_plyr +=1
                    elif temp_board.board_status[board_x + j][board_y + i] == '-':
                        empty, tent_x, tent_y = 1, board_x + j, board_y + i
                if count_plyr == 3 and empty == 1:
                    return (tent_x, tent_y)

            #DIAMOND1
            count_plyr , empty = 0, 0

            if temp_board.board_status[board_x + 1][board_y + 0] == flag:
                count_plyr +=1

            elif temp_board.board_status[board_x + 1][board_y + 0] == '-':
                empty, tent_x, tent_y = 1, board_x + 1, board_y + 0

            if temp_board.board_status[board_x + 0][board_y + 1] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 0][board_y + 1] == '-':
                empty, tent_x, tent_y = 1, board_x + 0, board_y + 1

            if temp_board.board_status[board_x + 2][board_y + 1] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 2][board_y + 1] == '-':
                empty, tent_x, tent_y = 1, board_x + 2, board_y + 1

            if temp_board.board_status[board_x + 1][board_y + 2] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 1][board_y + 2] == '-':
                empty, tent_x, tent_y = 1, board_x + 1, board_y + 2

            if count_plyr == 3 and empty == 1:
                return (tent_x, tent_y)


            #DIAMOND2
            count_plyr , empty = 0, 0

            if temp_board.board_status[board_x + 1][board_y + 1] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 1][board_y + 1] == '-':
                empty, tent_x, tent_y = 1, board_x + 1, board_y + 1

            if temp_board.board_status[board_x + 0][board_y + 2] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 0][board_y + 2] == '-':
                empty, tent_x, tent_y = 1, board_x + 0, board_y + 2

            if temp_board.board_status[board_x + 2][board_y + 2] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 2][board_y + 2] == '-':
                empty, tent_x, tent_y = 1, board_x + 2, board_y + 2

            if temp_board.board_status[board_x + 1][board_y + 3] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 1][board_y + 3] == '-':
                empty, tent_x, tent_y = 1, board_x + 1, board_y + 3

            if count_plyr == 3 and empty == 1:
                return (tent_x, tent_y)

            #DIAMOND3
            count_plyr , empty = 0, 0

            if temp_board.board_status[board_x + 2][board_y + 0] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 2][board_y + 0] == '-':
                empty, tent_x, tent_y = 1, board_x + 2, board_y + 0

            if temp_board.board_status[board_x + 1][board_y + 1] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 1][board_y + 1] == '-':
                empty, tent_x, tent_y = 1, board_x + 1, board_y + 1

            if temp_board.board_status[board_x + 3][board_y + 1] == flag:
                count_plyr += 1
            elif temp_board.board_status[board_x + 3][board_y + 1] == '-':
                empty, tent_x, tent_y = 1, board_x + 3, board_y + 1

            if temp_board.board_status[board_x + 2][board_y + 2] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 2][board_y + 2] == '-':
                empty, tent_x, tent_y = 1, board_x + 2, board_y + 2

            if count_plyr == 3 and empty == 1:
                return (tent_x, tent_y)

            #DIAMOND4
            count_plyr , empty = 0, 0

            if temp_board.board_status[board_x + 2][board_y + 1] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 2][board_y + 1] == '-':
                empty, tent_x, tent_y = 1, board_x + 2, board_y + 1

            if temp_board.board_status[board_x + 1][board_y + 2] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 1][board_y + 2] == '-':
                empty, tent_x, tent_y = 1, board_x + 1, board_y + 2

            if temp_board.board_status[board_x + 3][board_y + 2] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 3][board_y + 2] == '-':
                empty, tent_x, tent_y = 1, board_x + 3, board_y + 2

            if temp_board.board_status[board_x + 2][board_y + 3] == flag:
                count_plyr +=1
            elif temp_board.board_status[board_x + 2][board_y + 3] == '-':
                empty, tent_x, tent_y = 1, board_x + 2, board_y + 3

            if count_plyr == 3 and empty == 1:
                return (tent_x, tent_y)

        return (-1, -1)


    def utility_get(self, board, player_flag, opp_flag):
        gain = 0
        utility_values_block = []
        for i in range(16):
            utility_values_block.append(0)

        for i in range(16):
            utility_values_block[i] = self.calc_utility(board, i, player_flag, opp_flag)/1000.0

        #DIAMOND1
        p, pos, neg = 0, 0, 0
        p += utility_values_block[4]
        if board.block_status[1][0] == player_flag:
            pos = pos + 1
        elif board.block_status[1][0] == opp_flag:
            neg = neg + 1

        p += utility_values_block[1]
        if board.block_status[0][1] == player_flag:
            pos = pos + 1
        elif board.block_status[0][1] == opp_flag:
            neg = neg + 1

        p += utility_values_block[9]
        if board.block_status[2][1] == player_flag:
            pos = pos + 1
        elif board.block_status[2][1] == opp_flag:
            neg = neg + 1

        p += utility_values_block[6]
        if board.block_status[1][2] == player_flag:
            pos = pos + 1
        elif board.block_status[1][2] == opp_flag:
            neg = neg + 1

        gain = gain + (10 * self.utility_matrix[5*pos+neg]) + self.calc_imp(p)

        #DIAMOND2
        p, pos, neg = 0, 0, 0

        p += utility_values_block[5]
        if board.block_status[1][1] == player_flag:
            pos = pos + 1
        elif board.block_status[1][1] == opp_flag:
            neg = neg + 1

        p += utility_values_block[2]
        if board.block_status[0][2] == player_flag:
            pos = pos + 1
        elif board.block_status[0][2] == opp_flag:
            neg = neg + 1

        p += utility_values_block[10]
        if board.block_status[2][2] == player_flag:
            pos = pos + 1
        elif board.block_status[2][2] == opp_flag:
            neg = neg + 1

        p += utility_values_block[7]
        if board.block_status[1][3] == player_flag:
            pos = pos + 1
        elif board.block_status[1][3] == opp_flag:
            neg = neg + 1

        gain = gain + (10 * self.utility_matrix[5*pos+neg]) + self.calc_imp(p)

        #DIAMOND3
        p, pos, neg = 0, 0, 0

        p += utility_values_block[8]
        if board.block_status[2][0] == player_flag:
            pos = pos + 1
        elif board.block_status[2][0] == opp_flag:
            neg = neg + 1

        p += utility_values_block[5]
        if board.block_status[1][1] == player_flag:
            pos = pos + 1
        elif board.block_status[1][1] == opp_flag:
            neg = neg + 1

        p += utility_values_block[13]
        if board.block_status[3][1] == player_flag:
            pos = pos + 1
        elif board.block_status[3][1] == opp_flag:
            neg = neg + 1

        p += utility_values_block[10]
        if board.block_status[2][2] == player_flag:
            pos = pos + 1
        elif board.block_status[2][2] == opp_flag:
            neg = neg + 1

        gain = gain + (10 * self.utility_matrix[5*pos+neg]) + self.calc_imp(p)

        #DIAMOND4
        p, pos, neg = 0, 0, 0

        p += utility_values_block[9]
        if board.block_status[2][1] == player_flag:
            pos = pos + 1
        elif board.block_status[2][1] == opp_flag:
            neg = neg + 1

        p += utility_values_block[6]
        if board.block_status[1][2] == player_flag:
            pos = pos + 1
        elif board.block_status[1][2] == opp_flag:
            neg = neg + 1

        p += utility_values_block[14]
        if board.block_status[3][2] == player_flag:
            pos = pos + 1
        elif board.block_status[3][2] == opp_flag:
            neg = neg + 1

        p += utility_values_block[11]
        if board.block_status[2][3] == player_flag:
            pos = pos + 1
        elif board.block_status[2][3] == opp_flag:
            neg = neg + 1

        gain = gain + (10 * self.utility_matrix[5*pos+neg]) + self.calc_imp(p)

        for i in range(4):
            p, pos, neg = 0, 0, 0
            for j in range(4):
                p += utility_values_block[j*4+i]
                if board.block_status[j][i] == player_flag:
                    pos = pos + 1
                elif board.block_status[j][i] == opp_flag:
                    neg = neg + 1
            gain = gain + (10 * self.utility_matrix[5*pos+neg]) + self.calc_imp(p)

        for i in range(4):
            p, pos, neg = 0, 0, 0
            for j in range(4):
                p += utility_values_block[i*4+j]
                if board.block_status[i][j] == player_flag:
                    pos = pos + 1
                elif board.block_status[i][j] == opp_flag:
                    neg = neg + 1
            gain = gain + (10 * self.utility_matrix[5*pos+neg]) + self.calc_imp(p)

        count_plyr_block = count_opp_block = 0
        val1, val2 = 50 , 20

        for i in range(4):
            for j in range(4):
                if board.block_status[i][j] == player_flag:
                    count_plyr_block += 1
                elif board.block_status[i][j] == opp_flag:
                    count_opp_block += 1

        if count_opp_block > self.count_opp and count_plyr_block < self.count_plyr:
            gain-=val1

        elif (count_plyr_block - self.count_plyr) < (count_opp_block - self.count_opp) and count_plyr_block > self.count_plyr:
            gain-=val2

        elif count_opp_block == self.count_opp and self.count_plyr < count_plyr_block:
            gain+=val1

        return gain


    def calc_utility(self, board, board_num, player_flag, opp_flag):
        gain , board_x, board_y = 0, (board_num/4)*4, (board_num%4)*4

        for i in range(board_x, board_x + 4):
            pos, neg = 0, 0
            for j in range(board_y, board_y + 4):
                if board.board_status[i][j] == opp_flag:
                    neg = neg + 1
                elif board.board_status[i][j] == player_flag:
                    pos = pos + 1
            gain += self.utility_matrix[5*pos+neg]

        for j in range(board_y, board_y + 4):
            pos, neg = 0, 0
            for i in range(board_x, board_x + 4):
                if board.board_status[i][j] == opp_flag:
                    neg = neg + 1
                elif board.board_status[i][j] == player_flag:
                    pos = pos + 1
            gain += self.utility_matrix[5*pos+neg]

        #DIAMOND1
        pos, neg = 0, 0

        if board.board_status[board_x + 1][board_y + 0] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 1][board_y + 0] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 0][board_y + 1] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 0][board_y + 1] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 2][board_y + 1] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 2][board_y + 1] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 1][board_y + 2] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 1][board_y + 2] == opp_flag:
            neg = neg + 1

        gain += self.utility_matrix[5*pos+neg]


        #DIAMOND2
        pos, neg = 0, 0

        if board.board_status[board_x + 1][board_y + 1] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 1][board_y + 1] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 0][board_y + 2] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 0][board_y + 2] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 2][board_y + 2] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 2][board_y + 2] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 1][board_y + 3] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 1][board_y + 3] == opp_flag:
            neg = neg + 1

        gain += self.utility_matrix[5*pos+neg]


        #DIAMOND3
        pos, neg = 0, 0

        if board.board_status[board_x + 2][board_y + 0] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 2][board_y + 0] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 1][board_y + 1] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 1][board_y + 1] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 3][board_y + 1] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 3][board_y + 1] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 2][board_y + 2] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 2][board_y + 2] == opp_flag:
            neg = neg + 1

        gain += self.utility_matrix[5*pos+neg]

        #DIAMOND4
        pos, neg = 0, 0

        if board.board_status[board_x + 2][board_y + 1] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 2][board_y + 1] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 1][board_y + 2] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 1][board_y + 2] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 3][board_y + 2] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 3][board_y + 2] == opp_flag:
            neg = neg + 1

        if board.board_status[board_x + 2][board_y + 3] == player_flag:
            pos = pos + 1
        elif board.board_status[board_x + 2][board_y + 3] == opp_flag:
            neg = neg + 1

        gain += self.utility_matrix[5*pos+neg]

        plyr_flag = player_flag
        op_flag = 'o' if player_flag == 'x' else 'x'
        i, j, tempx, tempy = 0, 0, 0, 0

        hor, ver = [], []
        for p in range(4):
            temp_hor = []
            for q in range(4):
                temp_hor.append([p,q])
            hor.append(temp_hor)

        for q in range(4):
            temp_ver = []
            for p in range(4):
                temp_ver.append([p,q])
            ver.append(temp_ver)
        lim = 10

        for hor_line in hor:
            count_plyr_hor, count_opp_hor, count_plyr_ver, count_opp_ver = 0, 0, 0, 0
            for ver_line in ver:
                count_plyr_hor, count_opp_hor, count_plyr_ver, count_opp_ver = 0, 0, 0, 0

                for var in ver_line:
                    if plyr_flag == board.board_status[board_x+var[0]][board_y+var[1]]:
                        count_plyr_ver+=1
                    elif op_flag == board.board_status[board_x+var[0]][board_y+var[1]]:
                        count_opp_ver+=1
                    y_cord = var[1]

                for var in hor_line:
                    if plyr_flag == board.board_status[board_x+var[0]][board_y+var[1]]:
                        count_plyr_hor+=1
                    elif op_flag == board.board_status[board_x+var[0]][board_y+var[1]]:
                        count_opp_hor+=1
                    x_cord = var[0]

                a, b = board_x+x_cord, board_y+y_cord

                if board.board_status[a][b] == plyr_flag and count_plyr_hor == 3 and count_opp_ver == 2 and count_plyr_ver == 0 and count_opp_hor == 0:
                    gain += lim

                if board.board_status[a][b] == plyr_flag and count_opp_hor == 2 and count_plyr_ver == 3 and count_opp_ver == 0 and count_plyr_hor == 0:
                    gain += lim

        return gain

    def calc_imp(self, util):
        limit1, limit2 = 4, -4
        for i in range(-4,-1):
            if (util >= i and util < i+1):
                factr = pow(10, abs(i)-2)
                ret = (util-i-1)*9*factr - factr

        for i in range(1,4):
            if (util >= i and util < i+1):
                factr = pow(10, abs(i)-1)
                ret = (util-i)*9*factr + factr

        if abs(util) < 1 or util == -1:
            ret = util

        if util < limit2:
            factr = pow(10,3)
            ret = (util-limit2)*9*factr - factr

        if util >= limit1:
            factr = pow(10,3)
            ret = (util-limit1)*9*factr + factr

        return ret
