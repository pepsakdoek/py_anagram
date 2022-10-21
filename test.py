import tools as t
from datetime import datetime

# tests and usage
a = t.readdict("Woorde.csv")
timestart = datetime.now()


t1 = t.runfilter(a,'.ra..','stegf')
print(t1)


#f = open("output.txt","w")
#f.write(repr(t)+"\n")
#f.close(


print(datetime.now() - timestart)





















