# Python functions can be defined with named arguments which may have 
# default values provided. When function arguments are passed using their names, 
# they are referred to as keyword arguments. The use of keyword arguments when calling a 
# function allows the arguments to be passed in any order — not just the order that they were defined 
# in the function. If the function is invoked without a value for a specific argument, the default value will be used.

def findvolume(length=1, width=1, depth=1):
  print("Length = " + str(length))
  print("Width = " + str(width))
  print("Depth = " + str(depth))
  return length * width * depth;

findvolume(1, 2, 3)
findvolume(length=5, depth=2, width=4)
findvolume(2, depth=3, width=4)