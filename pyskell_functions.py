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



# Función compare (Number -> Number -> String)
def compare(n):
    def inner_compare(m):
        if n > m:
            return "GT"
        elif n < m:
            return "LT"
        else:
            return "EQ"
    return PyskellFunction(func=inner_compare, type=(number, str))
compare_ = PyskellFunction('compare', compare, type= (number, PyskellFunction(type =(number, str))))


# Función cos (Number -> Number)
def cos_pyskell(n):
    n = number(n)
    import math
    return math.cos(n)
cos = PyskellFunction('cos', cos_pyskell, type=(number, number))

# Función sin (Number -> Number)
def sin_pyskell(n):
    n = number(n)
    import math
    return math.sin(n)
sin = PyskellFunction('sin', sin_pyskell, type=(number, number))

# Función div ( Number -> Number)
def div_pyskell(n):
    n = number(n)
    def inner_div(m):
        m = number(m)
        return number(n/m)
    return PyskellFunction(func=inner_div, type=(number, number))
div = PyskellFunction('div', div_pyskell, type=(number, PyskellFunction(type=(number, number))))


# Función elem (Number -> List -> Bool)
def elem_pyskell(n):
    n = number(n)
    def inner_elem(arr):
        if len(arr) == 0:
            return False
        else:
            return arr[0] == n or inner_elem(arr[1:])
    return PyskellFunction(func=inner_elem, type=(number, bool))
elem = PyskellFunction('elem', elem_pyskell, type=(number, PyskellFunction(type=(list, bool))))    

# Función exp (Number -> Number)
def exp_pyskell(n):
    n = number(n)
    import math
    return math.exp(n)
exp = PyskellFunction('exp', exp_pyskell, type=(number, number))

# Función head (List -> Number)
def head_pyskell(arr):
    return arr[0]
head = PyskellFunction('head', head_pyskell, type=(list,str))

# Función tail (List -> List)
def tail_pyskell(arr):
    return arr[1:]
tail = PyskellFunction('tail', tail_pyskell, type=(list,list))

# Función signum (Number -> Number)
def signum_pyskell(n):
    n= number(n)
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0
signum = PyskellFunction('signum', signum_pyskell, type=(number,number))


# Función maximun(List -> Number)
def maximum_pyskell(arr):
    if len(arr) == 1:
        return arr[0]
    else:
        return arr[0] if arr[0] > maximum_pyskell(arr[1:]) else maximum_pyskell(arr[1:])
maximum = PyskellFunction('maximum', maximum_pyskell, type=(list,number))

# Función minimun(List -> Number)
def minimum_pyskell(arr):
    if len(arr) == 1:
        return arr[0]
    else:
        return arr[0] if arr[0] < minimum_pyskell(arr[1:]) else minimum_pyskell(arr[1:])
minimum = PyskellFunction('minimum', minimum_pyskell, type=(list,number))

# Función not (Bool -> Bool)
def not_pyskell(b):
    b= bool(eval(b))
    return not b
not_ = PyskellFunction('not', not_pyskell, type=(bool,bool))

# Función or (List -> Bool)
def or_pyskell(arr):
    if len(arr) == 0:
        return False
    else:
        return arr[0] or or_pyskell(arr[1:])
or_ = PyskellFunction('or', or_pyskell, type=(list,bool))

# Función and (List -> Bool)
def and_pyskell(arr):
    if len(arr) == 0:
        return True
    else:
        return arr[0] and and_pyskell(arr[1:])
and_ = PyskellFunction('and', and_pyskell, type=(list,bool))

# Función sqtr (Number -> Number)
def sqtr_pyskell(n):
    n = number(n)
    import math
    return math.sqrt(n)
sqtr = PyskellFunction('sqtr', sqtr_pyskell, type=(number,number))

# Función subtract (Number -> Number -> Number)
def subtract_pyskell(n):
    def inner_subtract_pyskell(m):
        return number(n) - number(m)
    return PyskellFunction(func=inner_subtract_pyskell, type=(number,number))
subtract = PyskellFunction('subtract', subtract_pyskell, type=(number,PyskellFunction(type=(number,number))))


#NO FUNCIONA PARA CADENAS
# Función  succ (Number -> Number)
def succ_pyskell(x):
    #if isinstance(x, (int, float)):
    #    return x + 1
    #elif isinstance(x, str):
    #    return chr(ord(x[0]) + 1)
    #else:
        # Incrementa el código ASCII del primer carácter en la cadena
    #    raise TypeError("Tipo no compatible para la función succ_pyskell")
    x = number(x)
    return x + 1
succ = PyskellFunction('succ', succ_pyskell, type=(number, number))

#NO ESTARIA FUNCIONANDO
# Función take (Number -> List -> List)
def take_pyskell(n):
    n = number(n)
    def inner_take_pyskell(arr):
        if n == 0 or not arr:
            return []
        n=n-1
        return [arr[0]] + inner_take_pyskell(arr[1:])
    return PyskellFunction(func=inner_take_pyskell, type=(list,list))
take = PyskellFunction('take', take_pyskell, type=(number,PyskellFunction(type=(number,PyskellFunction(type=(list,list))))))

# Función tan (Number -> Number)
def tan_pyskell(n):
    n=number(n)
    import math
    return math.tan(n)
tan = PyskellFunction('tan', tan_pyskell, type=(number,number))




lean_functions = [compare_, cos, sin, div, elem, exp, head, 
                  tail, signum, maximum, minimum, not_, or_, and_, 
                  sqtr, subtract, succ, take, tan
                  ]
nicor_functions = []
nicov_functions = [sleep, log, factorial, double, sum, upperCase, lowerCase, length, sumOf, 
                   isStrEq, helloWorld, fibonacci, _abs]

functions = nicov_functions + lean_functions + nicor_functions
# Exported functions
pyskell_exported_functions = functions