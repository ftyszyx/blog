it = iter([1, 2, 5, 4, 3])
while True:
    x = next(it)
    it.send
    print(x)
    if x == 'a':
        break
