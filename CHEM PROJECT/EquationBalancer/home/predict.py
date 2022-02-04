import csv
def cal(eq):
    with open("D:\CHEM PROJECT\EquationBalancer\home\pre.csv", 'r') as file:
        reader = csv.reader(file)
        eq = eq.split()
        eq.remove('+')
        print(eq)
        for row in reader:
            for i in eq:
                a = True
                b = False
                if i in row[0]:
                    b = True
                    print(i)
                else:
                    a = False
                    break
            if a == True or b == True:
                return(row[0])
                break
