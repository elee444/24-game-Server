<<<<<<< HEAD
##Test 4 integers (1-10) and 
##Determine if target/24 can be an outcome after applying +,-,*,+ on these
##4 numbers (each is used one and only one time).
##Use post-order representation to avoid parentheses
=======
# Test 4 integers (1-10) and
# Determine if target/24 can be an outcome after applying +,-,*,+ on these
# 4 numbers (each is used one and only one time).
# Use post-order representation to avoid parentheses
>>>>>>> f2718d7865ebe578f935fec0fe47b4a3a475d2cd
##
#!/usr/bin/python3


import itertools
#from fractions import Fraction
<<<<<<< HEAD
allAnswers=[]
#Evaluate the post-order representation
def postfixEval(postfixExpr,show):
    operandStack = [] 
=======
allAnswers = []
# Evaluate the post-order representation


def postfixEval(postfixExpr, show):
    operandStack = []
>>>>>>> f2718d7865ebe578f935fec0fe47b4a3a475d2cd
    for token in postfixExpr:
        if token in "1023456789":
            operandStack.append(int(token))
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            # if token =="/" and operand2=='0':
            #     return str(Fraction(0))
<<<<<<< HEAD
            result = doMath(token,operand1,operand2, exact=False)
            if (show is True):
                print(operand1,operand2, token, result)
            operandStack.append(result)   
    return operandStack.pop()

#Make it human readable
#op=operator, op1=left operand, op2=right operand.
#'exact' has not been implemened. Do so if fractions are allowed 
def doMath(op, op1, op2, exact=False): #return op1 op op2
    if (op1==None or op2==None):
        return None
    if op == "*":
        return op1 *op2
    elif op == "/":
        if (op2==0 or (op1 % op2!=0) ):  #watch out exceptions
            return None
        return op1 // op2      
=======
            result = doMath(token, operand1, operand2, exact=False)
            if (show is True):
                print(operand1, operand2, token, result)
            operandStack.append(result)
    return operandStack.pop()

# Make it human readable
# op=operator, op1=left operand, op2=right operand.
# 'exact' has not been implemened. Do so if fractions are allowed


def doMath(op, op1, op2, exact=False):  # return op1 op op2
    if (op1 == None or op2 == None):
        return None
    if op == "*":
        return op1 * op2
    elif op == "/":
        if (op2 == 0 or (op1 % op2 != 0)):  # watch out exceptions
            return None
        return op1 // op2
>>>>>>> f2718d7865ebe578f935fec0fe47b4a3a475d2cd
    elif op == "+":
        return op1 + op2
    else:
        return op1 - op2


<<<<<<< HEAD

def checkTarget(x,target): #x=a list of 4 numbers
    #target=24
    #answers=[]
    answers=set()
    #Each 4-tuple of number needs only 3 opeartions
    #Let's run through all possible collections of 3-operation, i.e. chooses 3 out of 4 operations with replacement.
    for y in itertools.permutations(x):
        for op in itertools.product("+-*/",repeat=3):
            #for each 4-tuple of numbers and 3-tuple of operations, there are only 4 possible valid formats (in post-order)
            st1=(y[0],y[1],op[0],y[2],op[1],y[3],op[2])
            st2=(y[0],y[1],op[0],y[2],y[3],op[1],op[2])
            st3=(y[0],y[1],y[2],op[0],op[1],y[3],op[2])
            st4=(y[0],y[1],y[2],op[0],y[3],op[1],op[2])
            st5=(y[0],y[1],y[2],y[3],op[0],op[1],op[2])
            st=[st1,st2,st3,st4,st5]
            res=[postfixEval(pl,False) for pl in st]
            for idx, val in enumerate(res):
                if (val==target):                  
                    answers.add(st[idx])
                    #break if one is enough
    return [list(a) for a in answers]

        
def main():
    #testing
    #print(check24(['6','6','6','6']))
    
    print(check24(['7','2','10','9']))
    #print(check24(['1','4','5','6']))
    print(allAnswers)
          
if __name__=='__main__':
=======
def checkTarget(x, target):  # x=a list of 4 numbers
    # target=24
    # answers=[]
    answers = set()
    # Each 4-tuple of number needs only 3 opeartions
    # Let's run through all possible collections of 3-operation, i.e. chooses 3 out of 4 operations with replacement.
    for y in itertools.permutations(x):
        for op in itertools.product("+-*/", repeat=3):
            # for each 4-tuple of numbers and 3-tuple of operations, there are only 4 possible valid formats (in post-order)
            st1 = (y[0], y[1], op[0], y[2], op[1], y[3], op[2])
            st2 = (y[0], y[1], op[0], y[2], y[3], op[1], op[2])
            st3 = (y[0], y[1], y[2], op[0], op[1], y[3], op[2])
            st4 = (y[0], y[1], y[2], op[0], y[3], op[1], op[2])
            st5 = (y[0], y[1], y[2], y[3], op[0], op[1], op[2])
            st = [st1, st2, st3, st4, st5]
            res = [postfixEval(pl, False) for pl in st]
            for idx, val in enumerate(res):
                if (val == target):
                    answers.add(st[idx])
                    # break if one is enough
    return [list(a) for a in answers]


def main():
    # testing
    # print(check24(['6','6','6','6']))

    print(check24(['7', '2', '10', '9']))
    # print(check24(['1','4','5','6']))
    print(allAnswers)


if __name__ == '__main__':
>>>>>>> f2718d7865ebe578f935fec0fe47b4a3a475d2cd
    main()
