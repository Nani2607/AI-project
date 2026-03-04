import numpy as np
from sklearn.neighbors import NearestNeighbors

def find_best_case(action_val, exploration_val, difficulty_val):
    # Step 1: Case Base - Past Video Games
    case_base = [
        {"name": "Elden Ring", "action": 9, "exploration": 10, "difficulty": 10, "genre": "Soulslike"},
        {"name": "Stardew Valley", "action": 1, "exploration": 5, "difficulty": 2, "genre": "Simulation"},
        {"name": "DOOM Eternal", "action": 10, "exploration": 3, "difficulty": 8, "genre": "FPS"},
        {"name": "Minecraft", "action": 3, "exploration": 10, "difficulty": 4, "genre": "Sandbox"},
        {"name": "Tetris Effect", "action": 5, "exploration": 0, "difficulty": 7, "genre": "Puzzle"},
        {"name": "Uncharted 4", "action": 8, "exploration": 6, "difficulty": 5, "genre": "Adventure"}
    ]

    # Step 2: Convert to feature matrix (X)
    X = np.array([[c["action"], c["exploration"], c["difficulty"]] for c in case_base])

    # Step 3: New Case from function arguments
    x_new = np.array([[action_val, exploration_val, difficulty_val]])

    # Step 4: Retrieve the most similar case
    model = NearestNeighbors(n_neighbors=1)
    model.fit(X)
    distance, index = model.kneighbors(x_new)

    # Step 5: Reuse the solution
    matched_case = case_base[index[0][0]]
    
    # Return the dictionary for Streamlit to display
    return matched_case

if __name__ == "__main__":
    test_result = find_best_case(9, 2, 6)
    print(f"Standalone Test: {test_result['name']}")