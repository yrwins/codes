#Physical Class

def f_to_c(f_temp = 10):
  c_temp = ((f_temp - 32) * 5/9) 
  return c_temp
f100_in_celsius = f_to_c(100) # this is not working question 2. 

print(f_to_c(), "Converts Fahrenheit to Celsius" )

#f100_in_celsius = f_to_c(100)
  
def c_to_f(c_temp = 10):
  f_temp = c_temp * (9/5) + 32
  return f_temp

print(c_to_f(), "Converts Celsius to Fahrenheit")