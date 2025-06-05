def is_perfect_square(n):
    if n < 0:
        return False
    if n == 0 or n == 1:
        return True
    low = 2
    high = n // 2
    while low <= high:
        mid = (low + high) // 2
        square = mid * mid
        if square == n:
            return True
        elif square < n:
            low = mid + 1
        else:
            high = mid - 1
    return False
