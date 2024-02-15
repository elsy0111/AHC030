from datetime import datetime
ss = 500

# f = open("./input.csv", "w")
# f.write("file,seed,N,M,e\n")
# for i in range(ss):
#     g = open("tools/in/" + str(i).zfill(4) + '.txt', 'r')
#     in_ = g.readline().replace("\n","").split()
#     g.close()
#     N = in_[0]
#     M = in_[1]
#     e = in_[2]
#     f.write(str(i) + "," + str(i) + "," + N + "," + M + "," + e + "\n")
# f.close()


f = open("./result.csv", "a")
# f.write("rank_min,1000000000,https://img.atcoder.jp/ahc030/awGA15Om.html\n")
f.write("Arcsecond" + str(datetime.now()))
for i in range(ss):
    g = open("tools/score/" + str(i).zfill(4) + '.txt', 'r')
    in_ = g.readline().replace("Score = ","").replace("\n","")
    print(in_)
    g.close()
    f.write("," + in_)
f.write("\n")
f.close()