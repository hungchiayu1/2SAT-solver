import sys 
import random
import time

def read_clauses(path):
    clauses = []

    try:
        file = open(path,"r")
        n_var = 0
        n_clause = 0
        clauses_lines = False
        clause=[]
        temp = ''
        neg = 0
        for line in file:
            if line.startswith("p"):
                clauses_lines = True
                n_var = int(line.split()[-2])
                n_clause = int(line.split()[-1])
                continue
            if line.startswith('c'):
                continue
            if clauses_lines:
                num = ''
                char_prev=''
                for char in line:
                    if char=='\n':
                        continue
                    if char ==' ':
                        char_prev = char
                        clause.append(num)
                        num=''
                        continue
                    if char=='0' and char_prev==' ':
                        clauses.append(clause)
                        clause = []
                        continue
        
                    num+=char
                    char_prev = char
        file.close()       
    except IOError:
        print("Can not find input file or read data")
        exit()
    return clauses,n_var
def check_solution(result,clauses):  
    '''result is stored in 
    '''
    false_clause = [False] * len(clauses)
    for i in range(len(clauses)):
        first_literal = clauses[i][0]
        second_literal = clauses[i][1]
                                 
        num1 = int(first_literal)
        num2 = int(second_literal)
        if num1<0:  
            num1 = -1*num1
            if result[num1-1]==-1:
                valid1 = True
            else:
                valid1 = False
        else:
            valid1 = result[num1-1]
            if result[num1-1]==-1:
                valid1 = False
            else:
                valid1 = True
        if num2<0:
            num2 = -1*num2
            if result[num2-1] == -1:
                valid2 = True
            else:
                valid2 = False
            
        else:
            if result[num2-1] == -1:
                valid2 = False
            else:
                valid2 = True
        if valid1==False and valid2==False:
            false_clause[i] = False
        else:
            false_clause[i] = True
    return false_clause
       
        
def randomize(path):
    clauses,n_var = read_clauses(path)
    result = [-1]*n_var ## Assign all to false
    count = 0
    while True:
        count+=1
        correct_clause = check_solution(result,clauses)
        if count>100*n_var**2:
            print("No solution")
            return None,count
        if all(correct_clause):
            return result,count
        for i in range(len(correct_clause)):
            if correct_clause[i]== False: ## This clause is not satisfied
                first_literal = abs(int(clauses[i][0]))
                second_literal = abs(int(clauses[i][1]))
                ran = random.randint(0,1)
                if ran == 1:
                    if result[first_literal-1]==-1:
                        result[first_literal-1]=1
                    else:
                        result[first_literal-1] = -1
                    break
                else:
                    if result[second_literal-1]==-1:
                        result[second_literal-1]=1
                    else:
                        result[second_literal-1] = -1
                    break
    return result,count
               
if __name__ == '__main__':
    file = sys.argv[1]
    start_time = time.time()
    result,count = randomize(file)
    print("Number of steps = {} ".format(count))
    print("--- %s seconds ---" % (time.time() - start_time))
    print(result)
                   
