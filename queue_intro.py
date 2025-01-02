from collections import deque

q = deque()

l = ["a","b", "c", "d"]

for i in range(len(l)):
    q.append(l[i])

print(q)

for i in range(len(q)):
    q.popleft()
    if len(q) == 0:
        q.append("Empty Queue")
        break

print(q)