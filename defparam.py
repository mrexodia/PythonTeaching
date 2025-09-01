import course

def foo(x: int, y: str = "hello"):
    print(x, y)

def bar(x: int, y = [1, 2, 3]): # error
    print(x, y)