import numpy as np
import math
import time

def is_valid_move(board, x, y):
    # Kiểm tra xem nước đi (x, y) có hợp lệ không
    n = len(board)
    if x < 0 or x >= n or y < 0 or y >= n or board[x][y] != 0:
        return False
    return True

def is_terminal_node(board):
    # Kiểm tra xem bàn cờ đã đầy chưa
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True


def evaluate(board):
    # Hàm đánh giá cho Alpha-Beta pruning
    # Kiểm tra trạng thái chiến thắng cho các hàng, cột và đường chéo
    n = len(board)
    for i in range(n):
        for j in range(n):
            if j + 4 < n:
                if board[i][j] == 1 and board[i][j+1] == 1 and board[i][j+2] == 1 and board[i][j+3] == 1 and board[i][j+4] == 1:
                    return 1000
                if board[i][j] == -1 and board[i][j+1] == -1 and board[i][j+2] == -1 and board[i][j+3] == -1 and board[i][j+4] == -1:
                    return -1000
            if i + 4 < n:
                if board[i][j] == 1 and board[i+1][j] == 1 and board[i+2][j] == 1 and board[i+3][j] == 1 and board[i+4][j] == 1:
                    return 1000
                if board[i][j] == -1 and board[i+1][j] == -1 and board[i+2][j] == -1 and board[i+3][j] == -1 and board[i+4][j] == -1:
                    return -1000
            if i + 4 < n and j + 4 < n:
                if board[i][j] == 1 and board[i+1][j+1] == 1 and board[i+2][j+2] == 1 and board[i+3][j+3] == 1 and board[i+4][j+4] == 1:
                    return 1000
                if board[i][j] == -1 and board[i+1][j+1] == -1 and board[i+2][j+2] == -1 and board[i+3][j+3] == -1 and board[i+4][j+4] == -1:
                    return -1000
            if i - 4 >= 0 and j + 4 < n:
                if board[i][j] == 1 and board[i-1][j+1] == 1 and board[i-2][j+2] == 1 and board[i-3][j+3] == 1 and board[i-4][j+4] == 1:
                    return 1000
                if board[i][j] == -1 and board[i-1][j+1] == -1 and board[i-2][j+2] == -1 and board[i-3][j+3] == -1 and board[i-4][j+4] == -1:
                    return -1000
    return 0

def minimax(board, depth, alpha, beta, maximizing_player, start_time, time_limit):
    if depth == 0 or is_terminal_node(board):
        return evaluate(board)

    if maximizing_player:
        max_eval = -math.inf
        for x in range(len(board)):
            for y in range(len(board)):
                if is_valid_move(board, x, y):
                    board[x][y] = 1
                    eval = minimax(board, depth - 1, alpha, beta, False, start_time, time_limit)
                    board[x][y] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                    if time.time() - start_time >= time_limit:
                        return max_eval
        return max_eval
    else:
        min_eval = math.inf
        for x in range(len(board)):
            for y in range(len(board)):
                if is_valid_move(board, x, y):
                    board[x][y] = -1
                    eval = minimax(board, depth - 1, alpha, beta, True, start_time, time_limit)
                    board[x][y] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                    if time.time() - start_time >= time_limit:
                        return min_eval
        return min_eval

def find_best_move(board, m, time_limit):
    best_eval = -math.inf
    best_move = None
    start_time = time.time()
    for x in range(len(board)):
        for y in range(len(board)):
            if is_valid_move(board, x, y):
                board[x][y] = 1
                eval = minimax(board, m, -math.inf, math.inf, False, start_time, time_limit)
                board[x][y] = 0
                if eval > best_eval:
                    best_eval = eval
                    best_move = (x, y)
                if time.time() - start_time >= time_limit:
                    return best_move
    return best_move

def main():
    n = int(input("Nhập kích thước bàn cờ (10 < n < 20): "))
    m = int(input("Nhập số lượng nước đã đi: "))
    board = np.zeros((n, n), dtype=int)

    print("Nhập tọa độ của các nước đã đi:")
    for i in range(m):
        while True:
            try:
                x, y = map(int, input(f"Nhập tọa độ của nước đi thứ {i+1} (x y): ").split())
                if not is_valid_move(board, x, y):
                    print("Nước đi không hợp lệ! Vui lòng thử lại.")
                else:
                    board[x][y] = -1 if i % 2 == 0 else 1
                    break
            except ValueError:
                print("Vui lòng nhập hai số nguyên cách nhau bằng khoảng trắng.")

    time_limit = 15 # Giới hạn thời gian cho mỗi nước đi là 15 giây
    best_move = find_best_move(board, m, time_limit)
    print("Nước đi tốt nhất cho máy tính:", best_move)

if __name__ == "__main__":
    main()
