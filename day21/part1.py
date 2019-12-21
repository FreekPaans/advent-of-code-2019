import random
from time import time
import os
import itertools as it
from collections import defaultdict

# Windows only :P
clear = lambda: os.system('cls')

def runComputer(data, input):
  program = defaultdict(int, { k: v for k, v in enumerate(data) })
  output = None
  i = 0
  relbase = 0

  while True:
    opcode = program[i] % 100

    if opcode == 99:
      break

    mode1 = (program[i] - opcode) // 100 % 10
    mode2 = (program[i] - opcode) // 1000 % 10
    mode3 = (program[i] - opcode) // 10000 % 10

    p1, p2, p3 = None, None, None

    if mode1 == 0: p1 = program[i + 1]
    elif mode1 == 1: p1 = i + 1
    elif mode1 == 2: p1 = program[i + 1] + relbase

    if mode2 == 0: p2 = program[i + 2]
    elif mode2 == 1: p2 = i + 2
    elif mode2 == 2: p2 = program[i + 2] + relbase
  
    if mode3 == 0: p3 = program[i + 3]
    elif mode3 == 1: raise ValueError('Immediate mode invalid for param 3')
    elif mode3 == 2: p3 = program[i + 3] + relbase

    # print('i =', i, '--- operation', opcode, '--- modes', mode1, mode2, mode3, '--- positions', str(p1).rjust(4, ' '), str(p2).rjust(4, ' '), str(p3).rjust(4, ' '))

    if opcode == 1: # addition
      program[p3] = program[p1] + program[p2]
      i += 4
    elif opcode == 2: # multiplication
      program[p3] = program[p1] * program[p2]
      i += 4
    elif opcode == 3: # input
      program[p1] = input.pop()
      i += 2
    elif opcode == 4: # output
      yield program[p1]
      i += 2
    elif opcode == 5: # jump-if-true
      i = program[p2] if program[p1] != 0 else i + 3
    elif opcode == 6: # jump-if-false
      i = program[p2] if program[p1] == 0 else i + 3
    elif opcode == 7: # less-than
      program[p3] = 1 if program[p1] < program[p2] else 0
      i += 4
    elif opcode == 8: # equals
      program[p3] = 1 if program[p1] == program[p2] else 0
      i += 4
    elif opcode == 9: # relative base adjust
      relbase += program[p1]
      i += 2
    else:
      raise ValueError(f'opcode {opcode} from {program[i]}')

def addMovesToInputStack(moves, inputsStack):
  # Reverse order since we need a stack for IntCode
  for i in reversed([ord(c) for line in moves for c in (line + "\n")]):
    inputsStack.append(i)

def solve(data, moves):
  inputs = []
  runner = runComputer(data, inputs)
  level = ""
  result = None
  addMovesToInputStack(moves, inputs)

  while True:
    status = next(runner, 'halt')
    if status == 'halt': break

    if status > 512:
      print("Large ascii value", status)
      result = status
      break
    else:
      level += chr(status)

  # print("RENDERING OUTPUT")
  # print(level)

  return result

with open('input.txt', 'r') as file:
  raw = list(map(int, file.read().splitlines()[0].split(",")))

registers = ["A", "B", "C", "D"]
outputs = ["T", "J"]
possibilities = []

for op in ["NOT", "AND", "OR"]:
  for left in registers:
    for right in outputs:
      possibilities.append(f"{op} {left} {right}")

def generateMoves(length):
  while True:
    yield [random.choice(possibilities) for _ in range(length)]

def solveOuter(raw):
  step = 0
  start = time()

  for combi in generateMoves(12):
    step += 1
    moves = list(combi) + ["WALK"]
    if step % 100 == 0:
      print('Step', str(step).ljust(2, ' '), 'time', str(round(time() - start, 4)).ljust(7, "0"), "trying moves", moves)
    result = solve(raw, moves)
    if result:
      print("Found solution with:", moves)
      return result

print("SOLUTION:", solveOuter(raw))