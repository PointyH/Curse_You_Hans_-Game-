def sum_val(lis1,lis2): #these two are used to add/subtract lists together such that [a,b] + [c,d] = [a+c,b+d]. Yes i know i can do this in python but I cba to find out.
    return [a+b for a,b in zip(lis1,lis2)]

def minus_val(lis1,lis2):
    return [a-b for a,b in zip(lis1,lis2)]
