def is_valid(row, col, board):
    # Check the number in the row
    for x in range(9):
        if x != col and board[row][x] == board[row][col]:
            return False

    # Check the number in the column
    for y in range(9):
        if y != row and board[y][col] == board[row][col]:
            return False

    # Check the number in the 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if (start_row + i != row or start_col + j != col) and board[start_row + i][start_col + j] == board[row][col]:
                return False

    return True

def solve(row, col, board):
    # base case
    if col == len(board[row]):
        if row == len(board) - 1:
            return True
        else:
            col = 0
            row += 1

    if board[row][col] != ".":
        return solve(row, col + 1, board)

    for value in range(1, 10):
        board[row][col] = str(value)
        if is_valid(row, col, board):
            if solve(row, col + 1, board):
                return True
        board[row][col] = "."

    return False
def solveSudoku(board):
    row=0
    col=0
    solve(row,col,board)
    return board
    
board=[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
print(solveSudoku(board))