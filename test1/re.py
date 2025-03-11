# 4 11
# 1 1 2
# 1 2 3
# 1 3 4
# 1 1 4
# 3 4 2
# 2 1 2
# 3 2 4
# 2 3 4
# 3 4 2
# 1 2 4
# 3 4 2

# 1
# 1
# 0
# 1

# 1. 1과 2를 연결한다.
# 2. 2와 3을 연결한다.
# 3. 3과 4를 연결한다.
# 4. 1과 4를 연결한다.
# 5. 4와 2 사이에 경로가 있다.
# 6. 1과 2를 제거한다.
# 7. 2와 4 사이에 경로가 있다.
# 8. 3과 4를 제거한다.
# 9. 4와 2 사이에 경로가 없다.
# 10. 2와 4를 연결한다.
# 11. 4와 2 사이에 경로가 있다.

import sys

input = sys.stdin.readline

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, rank, a, b):
    a = find(parent, a)
    b = find(parent, b)
    if a < b:
        parent[b] = a
    elif rank[a] < rank[b]:
        parent[a] = b
    else:
        parent[b] = a
        rank[a] += 1

def rebuild_graph(n, edges):
    parent = [i for i in range(n + 1)]
    rank = [0] * (n + 1)
    
    for a, b in edges:
        union(parent, rank, a, b)
    
    return parent, rank

n, m = map(int, input().split())
edges = set()

parent = [i for i in range(n + 1)]
rank = [0] * (n + 1)

result = []

for _ in range(m):
    opt, a, b = map(int, input().split())

    if opt == 1:
        if (a, b) not in edges and (b, a) not in edges:
            edges.add((a, b))
            union(parent, rank, a, b)
    elif opt == 2:
        if (a, b) in edges:
            edges.remove((a, b))
        elif (b, a) in edges:
            edges.remove((b, a))
        parent, rank = rebuild_graph(n, edges)
    elif opt == 3:
        if find(parent, a) == find(parent, b):
            result.append(1)
        else:
            result.append(0)

for r in result:
    print(r)