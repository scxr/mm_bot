def sol(n):
    mylist = input('Enter your numbers : ').split()
    return set(([tuple(sorted((i,j))) for i in mylist for j in mylist if int(i) + int(j) == n]))

'''
```py
def sol(n):
    mylist = input('Enter your numbers : ').split()
    return set(([(i, j) for i in mylist for j in mylist if int(i) + int(j) == n]))
```
but its a simple fix either way to fit the right question
'''
print(sol(9))