from classExam.FourCal import MoreFourCal, FourCal

result = 0

def add(num):
    global result
    result += num
    return result

print(add(3))
print(add(4))

class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, num):
        self.result += num
        return self.result

cal1 = Calculator()
cal2 = Calculator()

print(cal1.add(3))
print(cal1.add(4))
print(cal2.add(3))
print(cal2.add(7))

class safeFourCal(FourCal):
    def div(self):
        if self.second == 0:
            return 0
        else:
            return self.first / self.second

a = safeFourCal()
a.setdata(4,0)
print(a.div())





