import csv
from .models import Data
data = Data.objects.all()
A,B = [],[]
str1 = " "
with open('D:\\CHEM PROJECT\\EquationBalancer\\home\\CP1.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            row[0].strip()
            row[1].strip()
            A.append(row[0])
            B.append(row[1])
        except:
            pass
print(A, B)
def inp(eq):
    eq = eq.split()
    print(eq)
    for i in eq:
        if i in A:
            print(i)
            #print(B[A.index(i)])
            #print(eq[A.index(i)], B[A.index(i)])
            eq[eq.index(i)] = B[A.index(i)]
    print("send = ", str1.join(eq))
    print(str(eq))
    return (str1.join(eq))