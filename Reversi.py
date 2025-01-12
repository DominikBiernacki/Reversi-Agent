import sys
import datetime
import random

board = []  # -1-puste, 0-gracz1 1-gracz2
for i in range(8):
    line = []
    for j in range(8):
        line.append(-1)
    board.append(line)

empty = 60

MAX, MIN = 10000000, -10000000

visited_states = {}

cell_weights = [[20, -3, 11, 8, 8, 11, -3, 20],
                [-3, -7, -4, 1, 1, -4, -7, -3],
                [11, -4, 2, 2, 2, 2, -4, 11],
                [8, 1, 2, -3, -3, 2, 1, 8],
                [8, 1, 2, -3, -3, 2, 1, 8],
                [11, -4, 2, 2, 2, 2, -4, 11],
                [-3, -7, -4, 1, 1, -4, -7, -3],
                [20, -3, 11, 8, 8, 11, -3, 20]]


def show_board():
    for i in range(8):
        line = ""
        for j in range(8):
            if board[i][j] == -1:
                line += '.'
            elif board[i][j] == 0:
                line += 'o'
            else:
                line += '#'
        print(line, file=sys.stderr)


def update_board(i, j, state):
    brd = state[0]
    player = state[1]
    curr_board = []
    for x in range(8):
        line = []
        for y in range(8):
            line.append(brd[x][y])
        curr_board.append(line)

    curr_board[i][j] = player

    # w prawo
    k = min(j + 1, 7)
    while k < 7 and curr_board[i][k] == 1 - player:
        k += 1
    if curr_board[i][k] == player:
        k -= 1
        while (k > j):
            curr_board[i][k] = player
            k -= 1

    # w lewo
    k = max(j - 1, 0)
    while k > 0 and curr_board[i][k] == 1 - player:
        k -= 1
    if curr_board[i][k] == player:
        k += 1
        while (k < j):
            curr_board[i][k] = player
            k += 1

    # w dół
    k = min(i + 1, 7)
    while k < 7 and curr_board[k][j] == 1 - player:
        k += 1
    if curr_board[k][j] == player:
        k -= 1
        while (k > i):
            curr_board[k][j] = player
            k -= 1

    # w górę
    k = max(i - 1, 0)
    while k > 0 and curr_board[k][j] == 1 - player:
        k -= 1
    if curr_board[k][j] == player:
        k += 1
        while (k < i):
            curr_board[k][j] = player
            k += 1

    # prawo-dół
    k = min(i + 1, 7)
    p = min(j + 1, 7)
    while k < 7 and p < 7 and curr_board[k][p] == 1 - player:
        k += 1
        p += 1
    if curr_board[k][p] == player:
        k -= 1
        p -= 1
        while (k > i):
            curr_board[k][p] = player
            k -= 1
            p -= 1

    # prawo-góra
    k = max(i - 1, 0)
    p = min(j + 1, 7)
    while k > 0 and p < 7 and curr_board[k][p] == 1 - player:
        k -= 1
        p += 1
    if curr_board[k][p] == player:
        k += 1
        p -= 1
        while (k < i):
            curr_board[k][p] = player
            k += 1
            p -= 1

    # lewo-dół
    k = min(i + 1, 7)
    p = max(j - 1, 0)
    while k < 7 and p > 0 and curr_board[k][p] == 1 - player:
        k += 1
        p -= 1
    if curr_board[k][p] == player:
        k -= 1
        p += 1
        while (k > i):
            curr_board[k][p] = player
            k -= 1
            p += 1

    # lewo-góra
    k = max(i - 1, 0)
    p = max(j - 1, 0)
    while k > 0 and p > 0 and curr_board[k][p] == 1 - player:
        k -= 1
        p -= 1
    if curr_board[k][p] == player:
        k += 1
        p += 1
        while (k < i):
            curr_board[k][p] = player
            k += 1
            p += 1

    return curr_board


def is_legal(i, j, state):
    curr_board = state[0]
    player = state[1]
    if curr_board[i][j] != -1:
        return False

    # w prawo
    k = min(j + 1, 7)
    while k < 7 and curr_board[i][k] == 1 - player:
        k += 1
    if k != min(j + 1, 7) and curr_board[i][k] == player:
        return True

    # w lewo
    k = max(j - 1, 0)
    while k > 0 and curr_board[i][k] == 1 - player:
        k -= 1
    if k != max(j - 1, 0) and curr_board[i][k] == player:
        return True

    # w dół
    k = min(i + 1, 7)
    while k < 7 and curr_board[k][j] == 1 - player:
        k += 1
    if k != min(i + 1, 7) and curr_board[k][j] == player:
        return True

    # w górę
    k = max(i - 1, 0)
    while k > 0 and curr_board[k][j] == 1 - player:
        k -= 1
    if k != max(i - 1, 0) and curr_board[k][j] == player:
        return True

    # prawo-dół
    k = min(i + 1, 7)
    p = min(j + 1, 7)
    while k < 7 and p < 7 and curr_board[k][p] == 1 - player:
        k += 1
        p += 1
    if k != min(i + 1, 7) and curr_board[k][p] == player:
        return True

    # prawo-góra
    k = max(i - 1, 0)
    p = min(j + 1, 7)
    while k > 0 and p < 7 and curr_board[k][p] == 1 - player:
        k -= 1
        p += 1
    if k != max(i - 1, 0) and curr_board[k][p] == player:
        return True

    # lewo-dół
    k = min(i + 1, 7)
    p = max(j - 1, 0)
    while k < 7 and p > 0 and curr_board[k][p] == 1 - player:
        k += 1
        p -= 1
    if k != min(i + 1, 7) and curr_board[k][p] == player:
        return True

    # lewo-góra
    k = max(i - 1, 0)
    p = max(j - 1, 0)
    while k > 0 and p > 0 and curr_board[k][p] == 1 - player:
        k -= 1
        p -= 1
    if k != max(i - 1, 0) and curr_board[k][p] == player:
        return True

    return False


def actions(state):
    acts = []
    for i in range(8):
        for j in range(8):
            if is_legal(i, j, state):
                acts.append((i, j))

    if len(acts) == 0:
        return [(-1, -1)]
    return acts


def hash(state):
    hsh = str(state[1])
    for i in range(8):
        for j in range(8):
            hsh += str(state[0][i][j] + 1)
    return hsh


def is_finished(state):
    val = actions(state) == [(-1, -1)] and actions([state[0], 1 - state[1]]) == [(-1, -1)]
    if val:
        player_cnt = 0
        opp_cnt = 0
        for i in range(8):
            for j in range(8):
                if state[0][i][j] == state[1]:
                    player_cnt += 1
                elif state[0][i][j] == 1 - state[1]:
                    opp_cnt += 1
        if opp_cnt > player_cnt:
            visited_states[hash(state)] = MIN
        elif player_cnt > opp_cnt:
            visited_states[hash(state)] = MAX
        else:
            visited_states[hash(state)] = 0
    return val


def heura(state):
    hsh = hash(state)
    if hsh in visited_states:
        return visited_states[hsh]

    plr_cnt = 0
    opp_cnt = 0
    weight = 0

    for i in range(8):
        for j in range(8):
            if state[0][i][j] == state[1]:
                plr_cnt += 1
                weight += cell_weights[i][j]
            elif state[0][i][j] == 1 - state[1]:
                opp_cnt += 1
                weight -= cell_weights[i][j]

    cell_ratio = 100 * (plr_cnt - opp_cnt) / (plr_cnt + opp_cnt)

    plr_corners = 0
    opp_corners = 0

    for i in range(0, 8, 7):
        for j in range(0, 8, 7):
            if state[0][i][j] == state[1]:
                plr_corners += 1
            elif state[0][i][j] == 1 - state[1]:
                opp_corners += 1

    corner_ratio = 0
    if (plr_corners + opp_corners != 0):
        corner_ratio = 100 * (plr_corners - opp_corners) / (plr_corners + opp_corners)

    mobility = len(actions(state))
    # mobility = 0

    val = (10 * cell_ratio) + (100 * weight) + (800 * corner_ratio) + (270 * mobility)
    # val = (10 * cell_ratio) + (80 * weight) + (1000 * corner_ratio) + (200 * mobility)

    visited_states[hsh] = val

    return val


def max_value(state, alpha, beta, depth):
    if depth == 0 or is_finished(state):
        return heura(state)
    value = MIN - 1

    for a in actions(state):
        next_state = update_board(a[0], a[1], state)
        mv = min_value((next_state, 1 - state[1]), alpha, beta, depth - 1)
        if mv > value:
            value = mv
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


def min_value(state, alpha, beta, depth):
    if depth == 0 or is_finished(state):
        return -heura(state)
    value = MAX + 1

    for a in actions(state):
        next_state = update_board(a[0], a[1], state)
        mv = max_value((next_state, 1 - state[1]), alpha, beta, depth - 1)
        if mv < value:
            value = mv

        if value <= alpha:
            return value
        beta = min(beta, value)
    return value


def decision(state, depth):
    alpha = MIN - 1
    beta = MAX + 1
    val = MIN - 1
    act = (-1, -1)
    acts = actions(state)
    acts.sort(key=lambda a: -heura((update_board(a[0], a[1], state), state[1])))
    for a in acts:
        next_state = update_board(a[0], a[1], state)
        mv = min_value((next_state, 1 - state[1]), alpha, beta, depth - 1)
        if mv > val:
            val = mv
            act = a
        alpha = max(alpha, val)
    return act


def decision_random(state):
    return random.choice(actions(state))


def play_game():
    global board
    for i in range(8):
        for j in range(8):
            board[i][j] = -1

    board[3][3] = 1
    board[3][4] = 0
    board[4][3] = 0
    board[4][4] = 1

    empty = 60

    print("RDY")

    inp = input().split(" ")
    move = inp[0]
    if move == "BYE":
        exit()
    move_time = float(inp[1])
    game_time = float(inp[2])

    player = 1
    if move == "UGO":
        player = 0
    else:
        board = update_board(int(inp[3]), int(inp[4]), (board, 0))
        empty -= 1

    while True:
        if empty > 12:
            act = decision((board, player), 5)
        else:
            act = decision((board, player), 8)
        print("IDO " + str(act[0]) + " " + str(act[1]))
        board = update_board(act[0], act[1], (board, player))
        empty -= 1

        inp = input().split(" ")
        move = inp[0]
        if move == "HEDID":
            move_time = float(inp[1])
            game_time = float(inp[2])
            board = update_board(int(inp[3]), int(inp[4]), (board, 1 - player))
            empty -= 1
        elif move == "ONEMORE":
            play_game()
        elif move == "BYE":
            exit()


#play_game()


def simulate_game(starts):
    global board
    for i in range(8):
        for j in range(8):
            board[i][j] = -1

    board[3][3] = 1
    board[3][4] = 0
    board[4][3] = 0
    board[4][4] = 1

    empty = 60
    pl = starts
    passes = 0
    while (passes < 2):
        if pl == 0:
            act = decision((board, 0), 4)
            if (act != (-1, -1)):
                board = update_board(act[0], act[1], (board, 0))
                passes = 0
                empty -= 1
            else:
                passes += 1
        else:
            act = decision_random((board, 1))
            if (act != (-1, -1)):
                board = update_board(act[0], act[1], (board, 1))
                passes = 0
                empty -= 1
            else:
                passes += 1
        pl = 1 - pl

    cnt = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                cnt += 1
            elif board[i][j] == 1:
                cnt -= 1
    if cnt > 0:
        return 1
    if cnt < 0:
        return -1
    return 0


t0 = datetime.datetime.now()
wins = 0
draws = 0
losses = 0
for i in range(1000):
    res = simulate_game(i % 2)
    if res == 1:
        wins += 1
        print("win")
    elif res == -1:
        losses += 1
        print("loss")
    else:
        draws += 1
        print("draw")
    print(wins, draws, losses)

t1 = datetime.datetime.now()

print("time taken: " + str(t1 - t0))