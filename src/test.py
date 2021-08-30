import math
def solution(n, k):
    answer = []
    arr = [i for i in range(1, n + 1)]
    while len(arr) > 0:
        for i in range(1, n + 1):
            if k <= i * math.factorial(n - 1):
                k -= (i - 1) * math.factorial(n - 1)
                n -= 1
                answer.append(arr[i - 1])
                arr.pop(i-1)
                break

    return answer

print(solution(3,4))