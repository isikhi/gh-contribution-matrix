import os
import random
from datetime import datetime, timedelta

# --- SETTINGS ---
MESSAGE = "SPOOFED"
NOISE_RATE = 0.03  # 3% chance of random dot (Slightly noisy appearance)

# Commit Counts
DARK_GREEN_MIN = 12  # For Text and Brackets
DARK_GREEN_MAX = 20
LIGHT_GREEN_MIN = 1   # For Background Noise
LIGHT_GREEN_MAX = 4

# --- DESIGNS (1 = Filled, 0 = Empty) ---
# Left Square Bracket [
ICON_LEFT = [
    [0,1,1,1,0],
    [0,1,0,0,0],
    [0,1,0,0,0],
    [0,1,0,0,0],
    [0,1,0,0,0],
    [0,1,0,0,0],
    [0,1,1,1,0]
]

# Sağ Köşeli Parantez ]
ICON_RIGHT = [
    [0,1,1,1,0],
    [0,0,0,1,0],
    [0,0,0,1,0],
    [0,0,0,1,0],
    [0,0,0,1,0],
    [0,0,0,1,0],
    [0,1,1,1,0]
]

ALFABE = {
    'S': [[0,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[0,1,1,1,0],[0,0,0,0,1],[0,0,0,0,1],[1,1,1,1,0]],
    'P': [[1,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0]],
    'O': [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
    'F': [[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0]],
    'E': [[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
    'D': [[1,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,0]]
}

def get_start_date():
    today = datetime.now()
    one_year_ago = today - timedelta(weeks=52)
    days_until_sunday = (6 - one_year_ago.weekday()) % 7
    return one_year_ago + timedelta(days=days_until_sunday)

def commit_date(date_obj, count):
    date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    os.environ['GIT_AUTHOR_DATE'] = date_str
    os.environ['GIT_COMMITTER_DATE'] = date_str
    
    for _ in range(count):
        with open('history.txt', 'a') as f:
            f.write(f'{date_str}\n')
        os.system(f'git add history.txt > /dev/null 2>&1')
        os.system(f'git commit -m "update data packet" > /dev/null 2>&1')

def draw_shape(grid, shape, start_col):
    h = len(shape)
    w = len(shape[0])
    for r in range(h):
        for c in range(w):
            if shape[r][c] == 1:
                if start_col + c < 52:
                    grid[r][start_col + c] = 2 # 2 = Dark Color
    return w

def main():
    print("🚀 [ SPOOFED ] mode is starting...")
    
    grid = [[0 for _ in range(52)] for _ in range(7)]
    
    # --- Layout Calculation ---
    # Total width of letters
    text_width = 0
    for letter in MESSAGE:
        text_width += len(ALFABE[letter][0]) + 1 # +1 letter spacing
    text_width -= 1 # Remove last space
    
    icon_w = len(ICON_LEFT[0])
    
    # Total width: Left Icon + Space + Text + Space + Right Icon
    total_filled_area = icon_w + 2 + text_width + 2 + icon_w
    
    # Starting point for centering
    start_col = (52 - total_filled_area) // 2
    
    # --- Drawing ---
    current_col = start_col
    
    # 1. Left Bracket
    draw_shape(grid, ICON_LEFT, current_col)
    current_col += icon_w + 2 # Icon + space
    
    # 2. Text
    for letter in MESSAGE:
        w = draw_shape(grid, ALFABE[letter], current_col)
        current_col += w + 1
    
    current_col += 1 # Extra 1 space after text (total 2)
    
    # 3. Right Bracket
    draw_shape(grid, ICON_RIGHT, current_col)
    
    # --- Commit Process ---
    start_date = get_start_date()
    total_commits = 0
    
    print("Processing commits in the past (This may take 1-2 minutes)...")
    
    for col in range(52):
        for row in range(7):
            current_date = start_date + timedelta(weeks=col, days=row)
            
            if current_date > datetime.now():
                continue
            
            cell_val = grid[row][col]
            commit_count = 0
            
            if cell_val == 2:
                # Text and Icons (Dark Green)
                commit_count = random.randint(DARK_GREEN_MIN, DARK_GREEN_MAX)
            else:
                # Spaces (Glitch / Noise)
                if random.random() < NOISE_RATE:
                    commit_count = random.randint(LIGHT_GREEN_MIN, LIGHT_GREEN_MAX)
            
            if commit_count > 0:
                commit_date(current_date, commit_count)
                total_commits += commit_count
                
        if col % 10 == 0:
            print(f"Week {col}/52 completed...")

    print(f"\n✅ PROCESS COMPLETED! A total of {total_commits} commits were created.")

if __name__ == "__main__":
    main()
