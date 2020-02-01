#this is a test for gifhub.
class Robot:
    def __init__(self, name, color, weight, age, state, level):
       self.name = name
       self.color = color
       self.weight = weight
       self.age = age
       self.state = state
       self.level = level

    def introduce_self(self):
        print("My name is " + self.name)
        print("My color is " + self.color)
        print("My Weight is " + self.weight)
        print("My age is " + self.age)
        print("My state is " + self.state)
        print("My level is " + self.level)

r1 = Robot("Tom", "red", "30", "39", "Texas","level9")
r2 = Robot("Jerry", "blue", "40","40", "California", "level5")
 
r1.introduce_self()
r2.introduce_self()
