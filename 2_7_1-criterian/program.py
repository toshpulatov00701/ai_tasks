def generate_combinations(start, end, k):
    def backtrack(start_index, path):
        if len(path) == k:
            if path[0] == 1:
                result.append(path[:])
            return
        for i in range(start_index, end + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    result = []
    backtrack(start, [])
    return result

# Misol uchun:
start = 1
end = 50
k = 4  # nechta son tanlash kerak
combinations = generate_combinations(start, end, k)

print('len:::', len(combinations))

# Natijani chiqarish
# for combo in combinations:
#     print(combo)
