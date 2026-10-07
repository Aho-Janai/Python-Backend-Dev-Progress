#factorial calculator but this time its a recursive function

def fact(n):
    if n ==1:
        return 1
    else:
        return n*fact(n-1)
