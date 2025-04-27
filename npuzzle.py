from cmath import sqrt
import copy
import math

class State:
  def __init__(self, data = None, par = None, g= 0, h= 0, op= None):
    self.data = data
    self.par = par
    self.g = g
    self.h= h

  def clone(self):
    sn= copy.deepcopy(self)
    return sn

  def string(self):
    if self.data== None:
      return None
    res = ''
    for x in self.data:
      res += (str)(x)
    return res

  def __lt__(self, other):
    if other == None:
      return False
    return self.g + self.h < other.g + other.h

  def __eq__(self, other):
    if other == None:
      return False
    return self.string() == other.string()

class Operator:
  def __init__(self, i):
    self.i = i

  def checkStateNull(self, s):
    return s.data == None

  def findPosEmpty(self, s):
    size = int(math.sqrt(len(s.data)))
    for i in range(size):
      for j in range(size):
        if s.data[i* size + j] == 0:
          return i,j
    return None

  def swap(self,s, x, y, i):
    sz= int(math.sqrt(len(s.data)))
    nextState= s.clone()
    x_new= x
    y_new= y

    if i== 0:
      x_new= x+1
      y_new= y
    if i== 1:
      x_new= x-1
      y_new= y
    if i== 2:
      x_new = x
      y_new = y +1
    if i==3:
      x_new= x
      y_new = y-1

    nextState.data[x * sz + y] = nextState.data[x_new * sz + y_new]
    nextState.data[x_new * sz + y_new] = 0
    return nextState


  def Up(self, s):
    if self.checkStateNull(s) == True:
      return None
    x,y= self.findPosEmpty(s)
    if x==int(math.sqrt(len(s.data))) - 1:
      return None
    return self.swap(s, x, y, self.i)

  def Down(self, s):
    if self.checkStateNull(s) == True:
      return None
    x,y= self.findPosEmpty(s)
    if x==0:
      return None
    return self.swap(s, x, y, self.i)


  def Left(self, s):
    if self.checkStateNull(s) == True:
      return None
    x,y= self.findPosEmpty(s)
    if y== int(math.sqrt(len(s.data))) - 1:
      return None
    return self.swap(s, x, y, self.i)


  def Right(self, s):
    if self.checkStateNull(s) == True:
      return None
    x,y= self.findPosEmpty(s)
    if y==0:
      return None
    return self.swap(s, x, y, self.i)


  def Move(self, s):
    if self.i == 0:
      return self.Up(s)
    if self.i == 1:
      return self.Down(s)
    if self.i == 2:
      return self.Left(s)
    if self.i == 3:
      return self.Right(s)
    return None

def checkInPriority(Open, tmp):
  if tmp== None:
    return False
  return (tmp in Open.queue)

def equal(O, G):
  if O == None:
    return False
  return O == G

step= []

def Path(O):
  if O.par != None:
    Path(O.par)
    if O.op.i == 0 :
      step.append("down")
    if O.op.i == 1 :
      step.append("up")
    if O.op.i == 2 :
      step.append("right")
    if O.op.i == 3 :
      step.append("left")

def H(S, G):
  sz = int(math.sqrt(len(G.data)))
  res = 0
  for i in range(sz):
    for j in range(sz):
      if S.data[i * sz + j] != G.data[i * sz + j]:
        res += 1
  return res

# A-star
from queue import PriorityQueue

def Solve(S,G):
  Open= PriorityQueue()
  Closed = PriorityQueue()
  S.g = 0
  S.h = H(S,G)
  Open.put(S)

  while True:
    if Open.empty() == True:
      print("failure!")
      return

    O= Open.get()
    Closed.put(O)

    if equal(O,G) == True:
      print("Success!")
      Path(O)
      return

    for i in range(4):
      op= Operator(i)
      child= op.Move(O)

      if child == None:
        continue

      ok1 = checkInPriority(Open, child)
      ok2 = checkInPriority(Closed, child)

      if not ok1 and not ok2:
        child.par = O
        child.op = op
        child.g = O.g + 1
        child.h = H(child, G)
        Open.put(child)

def main():

  n = int(input())

  start = []

  for i in range(n):
    for j in range(n):
      x = int(input())
      start.append(x)
 
  
  S = State(start)

  if n == 3: 
    G= State([1,2,3,4,5,6,7,8,0])
  elif n == 4:
    G= State([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0])
  elif n == 5:
    G= State([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0])

  
   
  Solve(S, G)
  print(len(step))



main()

