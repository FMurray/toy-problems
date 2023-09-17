# def find_min_path(a, r, c): 


def path_helper(i, j, r, c, A): 
    if i == r or j == c:
        return 0
    if A[i][j] == 1:
        return 0
    if i == r-1 and j == c-1:
        return 1
    
    return path_helper(i + 1, j, r, c, A) + path_helper(i, j + 1, r, c, A)

def robot_grid(A, r: int, c: int) -> int:
    r = len(A)
    c = len(A[0])

    return path_helper(0, 0, r, c, A)