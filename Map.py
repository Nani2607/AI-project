import matplotlib.pyplot as plt
import numpy as np
import io
from collections import deque

# --- Step 1: Explicit Matrix Definition ---
maze_15x15 = np.array([
    [0,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
    [0,1,0,1,1,0,1,0,1,1,1,1,1,1,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,0,1,0],
    [1,1,0,1,0,1,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,1,0,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,0,1,0,1,1,1,1,1,1],
    [0,0,0,0,0,1,0,1,0,1,0,0,0,0,0],
    [0,1,1,1,0,1,0,0,0,1,0,1,1,1,0],
    [0,0,0,1,0,1,1,1,1,1,0,1,0,0,0],
    [1,1,0,1,0,0,0,0,0,0,0,1,0,1,1],
    [0,0,0,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,0,0,0]
])

# --- Step 2: BFS Logic with 8 Directions ---
def bfs_pathfinder(maze, start, goals):
    """Finds shortest path to the closest goal using 8 directions"""
    rows, cols = maze.shape
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()
        
        if (r, c) in goals:
            return path

        # Orthogonal + Diagonal movements (8 directions total)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),   # Basic
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonals
        ]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return None

def draw_fancy_maze(maze, path, start, goals, figsize=(8, 8)):
    """Generates the plot showing the path to the closest goal and marking both goals"""
    rows, cols = maze.shape
    data = np.array(maze, dtype=float)
    
    # 1. Draw the found path (Pink)
    if path:
        for (r, c) in path:
            data[r, c] = 2.0 
            
    # 2. Draw the Start position (Green)
    data[start[0], start[1]] = 3.0  

    # 3. Draw ALL goals (Yellow), even the one not reached
    for (r, c) in goals:
        data[r, c] = 4.0  

    # Palette: [Free, Wall, Path, Start, Goal]
    cmap = plt.cm.colors.ListedColormap(['#FFF0F5', '#D02A77', '#FF69B4', '#32CD32', '#FFD700'])
    bounds = [0, 1, 2, 3, 4, 5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(data, cmap=cmap, norm=norm)

    # Grid Styling
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which='minor', color='#FFC1CC', linestyle='-', linewidth=1)
    ax.tick_params(which='both', length=0, labelbottom=False, labelleft=False)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#FFF0F5')
    plt.close(fig)
    return buf

def get_available_coords(maze):
    """Returns available path coordinates for the selectbox"""
    coords = []
    for r in range(maze.shape[0]):
        for c in range(maze.shape[1]):
            if maze[r, c] == 0:
                coords.append(f"({r}, {c})")
    return coords