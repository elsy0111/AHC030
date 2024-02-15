from random import randint
# GOMI FUNCTION
def ceil(a:float, b:float) -> int:
    return (a + b - 1) // b

# INPUT
N, M, eps = input().split()
N = int(N)
M = int(M)
eps = float(eps)
fields = []

is_opened = [[0 for _ in range(N)] for _ in range(N)]
is_oil    = [[0 for _ in range(N)] for _ in range(N)]

ALL_OIL = 0
for _ in range(M):
    li = list(map(int,input().split()))
    d = li[0]
    li = li[1:]
    Line = []
    ps = []
    ALL_OIL += d
    for i in range(2 * d):
        ps.append(li[i])
        if i % 2:
            Line.append(ps)
            ps = []
    fields.append(Line)

for i in fields:
    print("#",i)

# DEFINE SEND DIG
def query_dig(points:list) -> int:
    d = len(points)
    print("q", d, end = " ")
    for point in points:
        print(point[0], point[1], end = " ")
    print()
    return int(input())

# DEFINE SEND ANS
def ans_exit(points:list) -> int:
    d = len(points)
    print("a", d, end = " ")
    for point in points:
        print(point[0], point[1], end = " ")
    print()
    if int(input()):
        exit(0)
    else:
        exit(1)

d4 = [
    (-1, 0),
    ( 0,-1),
    ( 0, 1),
    ( 1, 0),
    ]

ans = []
found_all_cnt = 0
# ALGO
window = 4
for i in range(ceil(N, window)):
    for j in range(ceil(N, window)):
        #window x window
        search_area = []
        Ibegin = window * i
        Iend   = min(N, window * (i + 1))
        Jbegin = window * j
        Jend   = min(N, window * (j + 1))
        for p in range(Ibegin, Iend):
            for q in range(Jbegin, Jend):
                search_area.append([p, q])
        window_res = query_dig(points=search_area)
        
        #! TODO : window2みるとき、そこの合計がis_oil >= 2 なら見ない
        #found window x window
        if window_res > 1:
            # window2 x window2 in window x window
            found_window_cnt = 0
            window2 = window // 2
            for ii in range(ceil(Iend - Ibegin, window2)):
                for jj in range(ceil(Jend - Jbegin, window2)):
                    if found_window_cnt >= window_res: break
                    search_area2 = []
                    IIbegin = window2 * ii + Ibegin
                    IIend   = min(Iend - Ibegin, window2 * (ii + 1)) + Ibegin
                    JJbegin = window2 * jj + Jbegin
                    JJend   = min(Jend - Jbegin, window2 * (jj + 1)) + Jbegin
                    sum_ = 0
                    for pp in range(IIbegin, IIend):
                        for qq in range(JJbegin, JJend):
                            sum_ += is_oil[pp][qq]
                            search_area2.append([pp, qq])
                    if sum_ >= 2:
                        print("# SUM >= 2")
                        break
                    window_res2 = query_dig(points=search_area2)
                    # window2 x window2 actual
                    if window_res2 > 1:
                        found_window2_cnt = 0
                        for pp in range(IIbegin, IIend):
                            for qq in range(JJbegin, JJend):
                                if found_window_cnt >= window_res: break
                                if found_window2_cnt >= window_res: break
                                if is_opened[pp][qq] == 0:
                                    dig_res = query_dig(points=[[pp, qq]])
                                    is_opened[pp][qq] = 1
                                    # found
                                    if dig_res > 0:
                                        print("#c", pp, qq, "green")
                                        is_oil[pp][qq] = 1
                                        found_all_cnt += dig_res
                                        found_window_cnt += dig_res
                                        found_window2_cnt += dig_res
                                        ans.append([pp, qq])
                                        if found_all_cnt >= ALL_OIL: ans_exit(ans)
                                        print("# searchh")
                                        queue = [[pp,qq]]
                                        while queue:
                                            ci,cj = queue.pop(0)
                                            for d in d4:
                                                ni = ci + d[0]
                                                nj = cj + d[1]
                                                if 0 <= ni < N and 0 <= nj < N:
                                                    # havent opend yet
                                                    if is_opened[ni][nj] != 1: 
                                                        res = query_dig(points=[[ni, nj]])
                                                        is_opened[ni][nj] = 1
                                                        if res > 0:
                                                            queue.append([ni,nj])
                                                            print("#c", ni, nj, "green")
                                                            found_all_cnt += res
                                                            print("# found/all",found_all_cnt,ALL_OIL)
                                                            is_oil[ni][nj] = 1
                                                            ans.append([ni, nj])
                                                            if found_all_cnt >= ALL_OIL: ans_exit(ans)

print("# ==================================")
print("# found/all",found_all_cnt,ALL_OIL)
print("# ==================================")

# ALGO (window2 ががばい)
window = 4
for i in range(ceil(N, window)):
    for j in range(ceil(N, window)):
        #window x window
        search_area = []
        Ibegin = window * i # Ibegin = max(0, window * i - 1)
        Iend   = min(N, window * (i + 1))
        Jbegin = window * j
        Jend   = min(N, window * (j + 1))
        for p in range(Ibegin, Iend):
            for q in range(Jbegin, Jend):
                search_area.append([p, q])
        window_res = query_dig(points=search_area)
        
        #found window x window
        if window_res > 1:
            sum_ = 0
            # window2 x window2 in window x window
            found_window_cnt = 0
            window2 = window // 2
            for ii in range(ceil(Iend - Ibegin, window2)):
                for jj in range(ceil(Jend - Jbegin, window2)):
                    if found_window_cnt >= window_res: break
                    search_area2 = []
                    IIbegin = window2 * ii + Ibegin
                    IIend   = min(Iend - Ibegin, window2 * (ii + 1)) + Ibegin
                    JJbegin = window2 * jj + Jbegin
                    JJend   = min(Jend - Jbegin, window2 * (jj + 1)) + Jbegin
                    sum_ = 0
                    for pp in range(IIbegin, IIend):
                        for qq in range(JJbegin, JJend):
                            sum_ += is_oil[pp][qq]
                            search_area2.append([pp, qq])
                    if sum_ >= 2:
                        print("# SUM >= 2")
                        break
                    window_res2 = query_dig(points=search_area2)
                    # window2 x window2 actual
                    if window_res2 > 0:
                        found_window2_cnt = 0
                        for pp in range(IIbegin, IIend):
                            for qq in range(JJbegin, JJend):
                                if found_window_cnt >= window_res: break
                                if found_window2_cnt >= window_res: break
                                if is_opened[pp][qq] == 0:
                                    dig_res = query_dig(points=[[pp, qq]])
                                    is_opened[pp][qq] = 1
                                    # found
                                    if dig_res > 0:
                                        print("#c", pp, qq, "green")
                                        is_oil[pp][qq] = 1
                                        found_all_cnt += dig_res
                                        found_window_cnt += dig_res
                                        found_window2_cnt += dig_res
                                        ans.append([pp, qq])
                                        if found_all_cnt >= ALL_OIL: ans_exit(ans)
                                        print("# searchh")
                                        queue = [[pp,qq]]
                                        while queue:
                                            ci,cj = queue.pop(0)
                                            for d in d4:
                                                ni = ci + d[0]
                                                nj = cj + d[1]
                                                if 0 <= ni < N and 0 <= nj < N:
                                                    # havent opend yet
                                                    if is_opened[ni][nj] != 1: 
                                                        res = query_dig(points=[[ni, nj]])
                                                        is_opened[ni][nj] = 1
                                                        if res > 0:
                                                            queue.append([ni,nj])
                                                            print("#c", ni, nj, "green")
                                                            found_all_cnt += res
                                                            print("# found/all",found_all_cnt,ALL_OIL)
                                                            is_oil[ni][nj] = 1
                                                            ans.append([ni, nj])
                                                            if found_all_cnt >= ALL_OIL: ans_exit(ans)

# around_oli = [[0 for _ in range(N)] for _ in range(N)]
# for _ in range(4):
#     for i in range(N):
#         for j in range(N):
#             if is_oil[i][j]:
#                 for d in d4:
#                     ni = i + d[0]
#                     nj = j + d[1]
#                     if 0 <= ni < N and 0 <= nj < N:
#                         # havent opend yet
#                         if is_opened[ni][nj] == 0: 
#                             around_oli[ni][nj] = 1
#                             print("#c", ni, nj, "#ff0000")
#     # query_dig([[0, 0]])

#     for i in range(N):
#         for j in range(N):
#             if around_oli[i][j]:
#                 if is_opened[i][j] == 0:
#                     res = query_dig(points=[[i, j]])
#                     is_opened[i][j] = 1
#                     print("#c", i, j, "#ffff00")
#                     if res > 0:
#                         print("#c", i, j, "green")
#                         found_all_cnt += res
#                         is_oil[i][j] = 1
#                         around_oli[i][j] = 0
#                         ans.append([i, j])
#                         if found_all_cnt >= ALL_OIL: 
#                             ans_exit(ans)
