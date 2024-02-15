from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
import pyperclip
import subprocess
import datetime
from time import sleep
import streamlit as st

# driver_path = 'chromedriver.exe'
driver_path = r'C:\Users\kpp01\Downloads\chromedriver-win64\chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_service = fs.Service(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service, options=options)
url = "https://img.atcoder.jp/ahc030/awGA15Om.html?lang=ja"

def clear_txt(file_path):
    f = open(file_path, 'w')
    f.close()

def score_write(current):
    o = False
    f = open("score_tmp.txt", "r")
    g = open("delta_score.txt", "a")
    d = open("DEBUG.txt", "w")
    for i in f:
        line = i
        if line[0] == "#":
            d.write(line)
        else:
            # print(line.split(" = "))
            if not o:
                try:
                    score = list(line.split(" = "))[1]
                    pyperclip.copy(score)
                    clear_txt("score_tmp.txt")
                    if current:
                        g.write("+" + score)
                    else:
                        g.write("-" + score)
                except:
                    o = True
                    print(i)
            else:
                print(i)
    f.close()
    g.close()
    d.close()
    if o:
        exit()


# READ in.txt, out.txt => vis(html)
def read_send(k : int):
    # 1. OPEN NEW WINDOW
    # driver.switch_to.new_window('tab')

    # 2. OPEN url
    driver.get(url)

    sleep(.2)

    in_texts = driver.find_element(By.ID, "input")
    out_texts = driver.find_element(By.ID, "output")

    # 4. Clead Form
    in_texts.clear()
    out_texts.clear()

    # 5.1 READ
    f = open("in/" + str(k).zfill(4) + '.txt', 'r')
    in_ = f.read()
    pyperclip.copy(in_)
    f.close()

    # 5.2 WRITE
    in_texts.send_keys(Keys.CONTROL, "v")

    # 6.1 READ
    f = open("out/" + str(k).zfill(4) + '.txt', 'r')
    out_ = f.read()
    pyperclip.copy(out_)
    f.close()

    # 6.2 WRITE
    out_texts.send_keys(Keys.CONTROL, "v")

def write_date(file_path : str):
    f = open(file_path, "w")
    f.write(str(datetime.datetime.now()) + "\n")
    f.close()

# write_date("delta_score.txt")
# write_date("DEBUG.txt")

def main(k:int, past = False):
    if not past:
        cmd = "tester.exe py ../main.py <" + \
            " in/" + str(k).zfill(4) + ".txt"  + \
         " > out/"+ str(k).zfill(4) + ".txt"
    else:
        cmd = "tester.exe py ../past.py <" + \
            " in/" + str(k).zfill(4) + ".txt"  + \
         " > out/"+ str(k).zfill(4) + ".txt"
    print("===========================")
    print(datetime.datetime.now())
    print("seeds =", k)
    print(*cmd.split())
    runcmd = subprocess.call(cmd.split(),shell = True)
    if runcmd == 1:
        raise(1)
    print("read & send")
    read_send(k)
        
    # score_write(current = 0)

seeds = st.text_input('Seeds', 0)

st.title("RUN")
if st.button("RUN"):
    main(seeds)
st.title("PAST")
if st.button("PAST"):
    main(seeds, past = True)
