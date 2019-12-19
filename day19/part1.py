from collections import defaultdict

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

def draw(level):
  # clear()
  
  minx = min([x for x, _ in level.keys()])
  miny = min([y for _, y in level.keys()])
  maxx = max([x for x, _ in level.keys()])
  maxy = max([y for _, y in level.keys()])

  for y in range(miny, maxy+1):
    line = ""
    for x in range(minx, maxx+1):
      line += level[(x,y)]
    print(line)

def solve(data):
  x, y = 0, 0
  level = defaultdict(lambda:".")
  result = 0

  while True:
    # print("Checking", x, y)
    inputs = [y, x] # IntCode requires a stack of commands, not a queue!
    runner = runComputer(data, inputs)

    status = next(runner, 'halt')
    if status == 'halt': break

    if status == 0:
      level[(x,y)] = "."
    elif status == 1:
      level[(x,y)] = "#"
      result += 1
    
    if x < 50:
      x += 1
    else:
      x = 0
      y += 1

    if y > 50:
      break
  
  draw(level)

  return result

with open('input.txt', 'r') as file:
  raw = list(map(int, file.read().splitlines()[0].split(",")))

# Not 125!?
print("Part 2:", solve(raw))