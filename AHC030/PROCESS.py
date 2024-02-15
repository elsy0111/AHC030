import subprocess
from concurrent.futures import ProcessPoolExecutor
# import threading

from termcolor import colored

# # ロックオブジェクトを作成
# output_lock = threading.Lock()

def ACp(s : str, cr = True):
    if cr:
        print(colored(s, "blue"))
    else:
        print(colored(s, "blue"), end = " ")

def AC(s : str, cr = True):
    if cr:
        print(colored(s, "green"))
    else:
        print(colored(s, "green"), end = " ")

def WA(s : str, cr = True):
    if cr:
        print(colored(s, "red"))
    else:
        print(colored(s, "red"), end = " ")

def run_test(seed):
    input_file = f"tools/in/{seed:04d}.txt"
    output_file = f"tools/out/{seed:04d}.txt"
    score_file = f"tools/score/{seed:04d}.txt"
    score__file = f"tools/score_/{seed:04d}.txt"
    
    process = subprocess.run(["tools/tester.exe", "py", "main.py"], 
                                 stdin=open(input_file, 'r'), 
                                 stdout=open(output_file, 'w'),
                                 stderr=open(score_file,"w"))

    process = subprocess.run(["tools/tester.exe", "py", "past.py"], 
                                 stdin=open(input_file, 'r'), 
                                 stdout=open(output_file, 'w'),
                                 stderr=open(score__file,"w"))
    ACp("#" + str(seed), cr = False)

def sum_score(start_seed : int, num : int):
    accept_cnt = 0
    score_cnt = 0
    score__cnt = 0
    AC("Passed :", cr = False)
    for seed in range(start_seed, start_seed + num):
        score_file = f"tools/score/{seed:04d}.txt"
        score__file = f"tools/score_/{seed:04d}.txt"
        g = open(score__file, 'r')
        line_ = g.read()
        g.close()

        f = open(score_file, 'r')
        line = f.read()
        f.close()
        if not("Score = " in line):
            WA("#" + str(seed), cr = False)
            # WA("Error Seed : " + str(seed) + " has no score")
        else:
            AC("#" + str(seed), cr = False)
            accept_cnt += 1
            score = int(line.replace("Score = ","").replace("\n",""))
            score_ = int(line_.replace("Score = ","").replace("\n",""))
            if score > score_:
                WA("#" + str(seed), cr = False)
            score_cnt += score
            score__cnt += score_
    print()
    return accept_cnt, score_cnt, score__cnt

def ceil(a:int, b:int) -> int:
    return (a + b - 1) // b

if __name__ == "__main__":
    #memo
    #515
    #756
    start = 0
    num = 500
    
    ACp("Processing...")
    with ProcessPoolExecutor() as executor:
        executor.map(run_test, range(start, start + num))
    print()
    
    accept, score, score_ = sum_score(start_seed=start, num = num)
    AC("accept  \t: "  + str(accept) + " / " + str(num))
    AC("score_ave\t: " + str(score / accept))
    WA("score_ave\t: " + str(score_ / accept))
