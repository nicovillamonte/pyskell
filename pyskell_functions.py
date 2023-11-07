from pyskell_types import PyskellFunction, number

# Función print (String -> String)
def log_pyskell(s):
    s = str(s)
    return s
log = PyskellFunction('log', log_pyskell, type=(str, str))

# Función factorial (Number -> Number)
def factorial_pyskell(n: number) -> number:
    n = number(n)
    return n * factorial_pyskell(n-1) if n > 1 else 1
factorial = PyskellFunction('factorial', factorial_pyskell, type=(number, number))

# Función double (Number -> Number)
def double_pyskell(n):
    n = number(n)
    return number(n * 2)
double = PyskellFunction('double', double_pyskell, type=(number, number))

# Función sum (Number -> Number -> Number)
def sum_pyskell(n: number) -> PyskellFunction:
    def inner_sum_pyskell (m: number) -> number:
        return number(n) + number(m)
    return PyskellFunction(func=inner_sum_pyskell, type=(number,number))
sum = PyskellFunction('sum', sum_pyskell, type=(number, PyskellFunction(type=(number,number))))

# Función upperCase (String -> String)
def upperCase_pyskell(s):
    s = str(s)
    return s.upper()
upperCase = PyskellFunction('upperCase', upperCase_pyskell, type=(str, str))

# Función lowerCase (String -> String)
def lowerCase_pyskell(s):
    s = str(s)
    return s.lower()
lowerCase = PyskellFunction('lowerCase', lowerCase_pyskell, type=(str, str))

# Función length (String -> Number)
def length_pyskell(s):
    s = str(s)
    return number(len(s))
length = PyskellFunction('length', length_pyskell, type=(str, number))

# Función sumOf (List -> Number)
def sumOf_pyskell(arr):
    if len(arr) == 0:
        return 0
    else:
        return number(number(arr[0]) + number(sumOf_pyskell(arr[1:])))
sumOf = PyskellFunction('sumOf', sumOf_pyskell, type=(list, number))

# Función isStrEq (String -> String -> Bool)
def isStrEq_pyskell(s):
    def inner_isStrEq_pyskell(x):
        return s == x
    return PyskellFunction(func=inner_isStrEq_pyskell, type=(str, bool))
isStrEq = PyskellFunction('isStrEq', isStrEq_pyskell, type=(str, PyskellFunction(type=(str, bool))))

# Función isStrEq (String)
def helloWorld_pyskell():
    return "Hello World!"
helloWorld = PyskellFunction('helloWorld', helloWorld_pyskell, type=(None,str))

# Función fibonacci (Number -> Number)
def fibonacci_pyskell(n):
    n = number(n)
    return number(fibonacci_pyskell(n-1) + fibonacci_pyskell(n-2) if n > 1 else n)
fibonacci = PyskellFunction('fibonacci', fibonacci_pyskell, type=(number, number))

# Función sleep (Number -> Number) (Make action)
def sleep_pyskell(n):
    import time
    time.sleep(int(n))
    return n
sleep = PyskellFunction('sleep', sleep_pyskell, type=(int, int))

def abs_pyskell(n):
    n = number(n)
    if n < 0:
        return n * (-1)
    else:
        return n
_abs = PyskellFunction('abs', abs_pyskell, type=(number,number))



# Función even (Number -> Bool)
def even_pyskell(n):
    n = number(n)
    return n % 2 == 0
even = PyskellFunction('even', even_pyskell, type=(number, bool))

# Funcion odd (Number -> Bool)
def odd_pyskell(n):
    n = number(n)
    return n % 2 != 0
odd = PyskellFunction('odd', odd_pyskell, type=(number, bool))

# Función negate (Bool -> Bool)
def negate_pyskell(n):
    n = number(n)
    if n > 0:
        return n * -1
    else:
        return n
negate = PyskellFunction('negate', negate_pyskell, type=(number, number))



# Función all (Func -> List -> Bool)
def all_pyskellf(n):
    func = globals().get(n)
    def inner_all_pyskell(arr):
                if len(arr) == 0:
                    return True
                else:
                    return func(arr[0]) and inner_all_pyskell(arr[1:])
    return PyskellFunction(func=inner_all_pyskell, type=(list, bool))
_all = PyskellFunction('all', all_pyskellf, type=(str, PyskellFunction(type=(list, bool))))


lean_functions = []
nicor_functions = [even, odd, negate, _all]
nicov_functions = [sleep, log, factorial, double, sum, upperCase, lowerCase, length, sumOf, 
                   isStrEq, helloWorld, fibonacci, _abs]

functions = nicov_functions + lean_functions + nicor_functions
# Exported functions
pyskell_exported_functions = functions