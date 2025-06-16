from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Board initialization: 0=empty, 1=black, 2=white
board = [[0 for _ in range(8)] for _ in range(8)]
board[3][3] = board[4][4] = 2
board[3][4] = board[4][3] = 1
current_player = 1

DIRECTIONS = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (1, -1), (-1, 1), (-1, -1)
]

def valid_move(player, x, y):
    if board[y][x] != 0:
        return False
    opponent = 3 - player
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        has_opponent = False
        while 0 <= nx < 8 and 0 <= ny < 8 and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            has_opponent = True
        if has_opponent and 0 <= nx < 8 and 0 <= ny < 8 and board[ny][nx] == player:
            return True
    return False

def apply_move(player, x, y):
    opponent = 3 - player
    flips = []
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        path = []
        while 0 <= nx < 8 and 0 <= ny < 8 and board[ny][nx] == opponent:
            path.append((nx, ny))
            nx += dx
            ny += dy
        if path and 0 <= nx < 8 and 0 <= ny < 8 and board[ny][nx] == player:
            flips.extend(path)
    if not flips:
        return False
    board[y][x] = player
    for fx, fy in flips:
        board[fy][fx] = player
    return True

def available_moves(player):
    moves = []
    for y in range(8):
        for x in range(8):
            if valid_move(player, x, y):
                moves.append((x, y))
    return moves

@app.route('/')
def index():
    return render_template('index.html', board=board, player=current_player)

@app.route('/move', methods=['POST'])
def move():
    global current_player
    data = request.get_json()
    x = int(data.get('x'))
    y = int(data.get('y'))
    if valid_move(current_player, x, y):
        apply_move(current_player, x, y)
        current_player = 3 - current_player
    return jsonify({'board': board, 'player': current_player})

@app.route('/state')
def state():
    return jsonify({'board': board, 'player': current_player, 'valid_moves': available_moves(current_player)})

if __name__ == '__main__':
    app.run(debug=True)
