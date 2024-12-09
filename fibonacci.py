# def fib():
#     a,b=0,1
#     while True:
#         yield a
#         a,b=b,a+b
# fibb=fib()
# for _ in range(10):
#     print(next(fibb))


def fibonnaci_generator(n):
    a,b=0,1
    for _ in range(n):
        yield a
        a,b=b,a+b
def main():
    n = int(input('enter the number of fibonacci numbers to generate:'))
    fib_gen = fibonnaci_generator(n)
    for num in fib_gen:
        print(num)
if __name__ == '__main__':
    main()            