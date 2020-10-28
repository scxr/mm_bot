def sol(n):
    mylist = input('Enter your numbers : ').split()
    return set(([tuple(sorted((i,j))) for i in mylist for j in mylist if int(i) + int(j) == n]))

def my_split(s, sep=",  '"):
    return [s[:s.index(sep)]] + my_split(s[s.index(sep)+1:]) if sep in s else [s]
'''
```py
def sol(n):
    mylist = input('Enter your numbers : ').split()
    return set(([(i, j) for i in mylist for j in mylist if int(i) + int(j) == n]))
```
but its a simple fix either way to fit the right question
'''
print(sol(9))