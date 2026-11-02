# INPUT ===================================================
N, M, eps = input().split()
N = int(N)
M = int(M)
eps = float(eps)

ALL_OIL = 0
fields = []
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
# INPUT ===================================================

# INIT ==============================
ans = []
found_all_cnt = 0
is_opened = [[0 for _ in range(N)] for _ in range(N)]
is_oil    = [[0 for _ in range(N)] for _ in range(N)]
# INIT ==============================

# GOMI FUNCTION =============================
def ceil(a:float, b:float) -> int:
    return (a + b - 1) // b

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

# DEFINE SEND ANS
def ans_dos(points:list) -> int:
    d = len(points)
    print("a", d, end = " ")
    for point in points:
        print(point[0], point[1], end = " ")
    print()
    if int(input()): #OK => EXIT
        exit(0)
    else:
        return  #NO => TRY AGAIN
        
def find_around1():
    Dos_Res = []
    visited = [[0 for _ in range(N)]for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if is_oil[i][j] and visited[i][j] == 0:
                queue = [[i,j]]
                visited[i][j] = 1
                while queue:
                    ci, cj = queue.pop(-1)
                    for d in d4:
                        ii = ci + d[0]
                        jj = cj + d[1]
                        if inside(ii,jj) and visited[ii][jj] == 0:
                            visited[ii][jj] = 1
                            if is_oil[ii][jj] == 1:
                                queue.append([ii, jj])
                            elif is_opened[ii][jj] == 0:
                                Dos_Res.append([ii, jj])
    return Dos_Res

def find_around2():
    return None
    
def find_around3():
    return None

#ramain <= 3 => LETS DoS
def rand_dos(dos, remain):
    if remain == 3:
        queue = find_around3()
    if remain == 2:
        queue = find_around2()
    if remain == 1:
        queue = find_around1()
    cnt = 0
    print("#",queue)
    while cnt < dos and cnt < len(queue):
        ans_dos(ans + [queue[cnt]])
        cnt += 1
        
        
d4 = [
    (-1, 0),
    ( 0,-1),
    ( 0, 1),
    ( 1, 0),
    ]

def inside(i, j):
    return (0 <= i < N and 0 <= j < N)

def update():
    global is_opened
    global visited
    visited = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if is_opened[i][j] == 0 and visited[i][j] == 0:
                dfs_update(i, j)

def dfs_update(i, j):
    global is_opened
    global visited
    cnt = 1
    queue = [[i, j]]
    visited[i][j] = 1
    road = [[i, j]]
    while queue:
        ci,cj = queue.pop(0)
        for d in d4:
            ni = ci + d[0]
            nj = cj + d[1]
            if inside(ni, nj):
                if is_opened[ni][nj] == 0 and visited[ni][nj] == 0:
                    cnt += 1
                    visited[ni][nj] = 1
                    road.append([ni, nj])
                    queue.append([ni,nj])
    if cnt < 4:
        for i,j in road:
            is_opened[i][j] = 1
            print("#c", i, j, "red")

def dfs(i, j):
    global ans
    global found_all_cnt
    global is_opened
    global is_oil
    global d4
    global ALL_OIL
    queue = [[i, j]]
    while queue:
        ci,cj = queue.pop(0)
        for d in d4:
            ni = ci + d[0]
            nj = cj + d[1]
            if inside(ni, nj):
                # havent opend yet
                if is_opened[ni][nj] == 0: 
                    res = query_dig(points=[[ni, nj]])
                    is_opened[ni][nj] = 1
                    if res > 0:
                        print("#c", ni, nj, "green")
                        queue.append([ni,nj])
                        ans.append([ni, nj])
                        is_oil[ni][nj] = 1
                        found_all_cnt += res
                        print("# SEARCHING...")
                        print("# found/all",found_all_cnt,ALL_OIL)
                        if found_all_cnt >= ALL_OIL: ans_exit(ans)
                        # if found_all_cnt >= ALL_OIL - 3: rand_dos(100000, ALL_OIL - found_all_cnt)
                        if found_all_cnt == ALL_OIL - 1: rand_dos(100000, ALL_OIL - found_all_cnt)
    update()

def finder(Ibegin, Iend, Jbegin, Jend):
    global found_all_cnt
    for pp in range(Ibegin, Iend):
        for qq in range(Jbegin, Jend):
            # havent opend yet
            if is_opened[pp][qq] == 0:
                res = query_dig(points=[[pp, qq]])
                is_opened[pp][qq] = 1
                # found
                if res > 0:
                    print("#c", pp, qq, "green")
                    ans.append([pp, qq])
                    is_oil[pp][qq] = 1
                    found_all_cnt += res
                    print("# SEARCH START")
                    print("# found/all",found_all_cnt,ALL_OIL)
                    if found_all_cnt >= ALL_OIL: ans_exit(ans)
                    dfs(pp, qq)

def check_win2(IIbegin, IIend, JJbegin, JJend, later_bool = True):
    search_area2 = []
    global is_opened
    global is_oil
    global later
    cell_cnt = 0
    oil_sum = 0
    open_sum = 0
    for pp in range(IIbegin, IIend):
        for qq in range(JJbegin, JJend):
            cell_cnt += 1
            open_sum += is_opened[pp][qq]
            oil_sum += is_oil[pp][qq]
            search_area2.append([pp, qq])
    if cell_cnt == 4:
        if oil_sum >= 2:
            print("# skiped cuz :",end = "")
            print("oil_sum  >= 2")
            return []
        elif open_sum == 4:
            print("# skiped cuz :",end = "")
            print("open_sum == 4",end = "")
            print()
            return []
        elif open_sum >= 2 and later_bool:
            print("# LATER")
            later.append(search_area2)
            return []
    elif cell_cnt == 2:
        if oil_sum >= 1 or open_sum == 2:
            print("# skiped cuz :",end = "")
            if oil_sum >= 1:  print("oil_sum  >= 1",end = "")
            if open_sum == 2: print("open_sum == 2",end = "")
            print()
            return []
    elif cell_cnt == 1:
        return []
    else:
        raise(1)
    return search_area2

# GOMI FUNCTION =============================

# window = 3
# for i in range(ceil(N, window)):
#     for j in range(ceil(N, window)):
#         #window x window
#         search_area = []
#         Ibegin = window * i
#         Iend   = min(N, window * (i + 1))
#         Jbegin = window * j
#         Jend   = min(N, window * (j + 1))
#         open_sum = 0
#         cell_cnt = 0
#         print("#c", Ibegin, Jbegin, "yellow")
#         for p in range(Ibegin, Iend):
#             for q in range(Jbegin, Jend):
#                 cell_cnt += 1
#                 search_area.append([p, q])
#         window_res = query_dig(points=search_area)
#         if window_res >= cell_cnt * 1 // 3 and window_res < cell_cnt * 4 // 9:
#             window_res = query_dig(points=search_area)
#         if window_res >= cell_cnt * 4 // 9:
#             CI = Ibegin + 1
#             CJ = Jbegin + 1
#             if inside(CI, CJ):
#                 finder(CI, CI + 1, CJ, CJ + 1)
#             for d in d4:
#                 ii = CI + d[0]
#                 jj = CJ + d[1]
#                 if inside(ii, jj):
#                     finder(ii, ii + 1, jj, jj + 1)

# ALGO
window = 4
# エラーが怖いので余分に取っておく
cache_window_res =  [[-1 for _ in range(N)]for _ in range(N)]
cache_window_res2 = [[-1 for _ in range(N)]for _ in range(N)]
later = []
for i in range(ceil(N, window)):
    for j in range(ceil(N, window)):
        #window x window
        search_area = []
        Ibegin = window * i
        Iend   = min(N, window * (i + 1))
        Jbegin = window * j
        Jend   = min(N, window * (j + 1))
        open_sum = 0
        for p in range(Ibegin, Iend):
            for q in range(Jbegin, Jend):
                search_area.append([p, q])
                open_sum += is_opened[p][q]
        if open_sum >= 6:
            print("# skiped cuz : opensum", open_sum, ">= 6")
            if open_sum == 16:
                window_res = 0 # actual NG
            else:
                window_res = -2 # SKIP
        else: window_res = query_dig(points=search_area)
        cache_window_res[Ibegin][Jbegin] = window_res
        
        #found window x window
        if window_res >= 2:
            window2 = window // 2
            for ii in range(ceil(Iend - Ibegin, window2)):
                for jj in range(ceil(Jend - Jbegin, window2)):
                    IIbegin = window2 * ii + Ibegin
                    IIend   = min(Iend - Ibegin, window2 * (ii + 1)) + Ibegin
                    JJbegin = window2 * jj + Jbegin
                    JJend   = min(Jend - Jbegin, window2 * (jj + 1)) + Jbegin

                    search_area2 = check_win2(IIbegin, IIend, JJbegin,JJend)
                    if search_area2 == []: window_res2 = 0 # actual NG
                    else: window_res2 = query_dig(points=search_area2)
                    cache_window_res2[IIbegin][JJbegin] = window_res2
                    
                    cell_cnt = (IIend - IIbegin) * (JJend - JJbegin)
                    if cell_cnt == 4:
                        if window_res2 >= 2:
                            finder(IIbegin, IIend, JJbegin, JJend)
                    elif cell_cnt == 2:
                        if window_res2 >= 1:
                            finder(IIbegin, IIend, JJbegin, JJend)
                    elif cell_cnt == 1:
                        None
                    else:
                        raise(1) # No

print("# ==================================")
print("# CANT FOUND ALL IN FIRST SEARCH")
print("# => LATER")
print("# ==================================")

while later:
    pop_later = later.pop(0)
    print("# popLATER", pop_later)
    for i, j in pop_later:
        if is_opened[i][j] == 0:
            finder(i, i + 1, j, j + 1)

print("# ==================================")
print("# found/all",found_all_cnt,ALL_OIL)
print("# ==================================")

# ALGO (window2 ががばい)
for i in range(ceil(N, window)):
    for j in range(ceil(N, window)):
        #window x window
        search_area = []
        Ibegin = window * i
        Iend   = min(N, window * (i + 1))
        Jbegin = window * j
        Jend   = min(N, window * (j + 1))
        open_sum = 0
        for p in range(Ibegin, Iend):
            for q in range(Jbegin, Jend):
                search_area.append([p, q])
                open_sum += is_opened[p][q]
        if open_sum == 16:
            print("# skiped cuz : opensum", open_sum, ">= 16")
            window_res = 0 # actual NG
        else:
            window_res = cache_window_res[Ibegin][Jbegin]
        if window_res == -2: # SKIPED
            window_res = query_dig(points=search_area) # RE DIG
        if window_res == -1: raise(1) # NO CACHE
        # print("#c",Ibegin, Jbegin)
        #found window x window
        if window_res >= 2:
            window2 = window // 2
            for ii in range(ceil(Iend - Ibegin, window2)):
                for jj in range(ceil(Jend - Jbegin, window2)):
                    IIbegin = window2 * ii + Ibegin
                    IIend   = min(Iend - Ibegin, window2 * (ii + 1)) + Ibegin
                    JJbegin = window2 * jj + Jbegin
                    JJend   = min(Jend - Jbegin, window2 * (jj + 1)) + Jbegin

                    search_area2 = check_win2(IIbegin, IIend, JJbegin,JJend,later_bool = False)
                    if search_area2 == []: window_res2 = 0 # actual NG
                    else: window_res2 = cache_window_res2[IIbegin][JJbegin]
                    if window_res2 == -1: # NO CACHE (閾値きつかったから)
                        window_res2 = query_dig(points=search_area2)

                    cell_cnt = (IIend - IIbegin) * (JJend - JJbegin)
                    if cell_cnt == 4:
                        if window_res2 >= 1:
                            finder(IIbegin, IIend, JJbegin, JJend)
                    elif cell_cnt == 2:
                        if window_res2 >= 1:
                            finder(IIbegin, IIend, JJbegin, JJend)
                    elif cell_cnt == 1:
                        None
                    else:
                        raise(1) # No


