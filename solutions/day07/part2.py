import itertools
import collections

with open('input.txt', 'r') as file:
  data = list(map(int, file.read().splitlines()[0].split(",")))

class Computer:
  def __init__(self, program, phase):
    self.i = 0
    self.lastOutput = None
    self.halted = False
    self.phase = phase
    self.hasUsedPhase = False
    self.program = program.copy()

  def run(self, input):
    if self.halted:
      raise RuntimeError("Computer was halted already")
    i, output, hasUsedPhase = runComputer(self.program, self.i, input, self.phase, self.hasUsedPhase)
    self.i = i
    self.halted = self.halted or output is None
    self.lastOutput = output
    self.hasUsedPhase = hasUsedPhase
    return output

def runComputer(program, i, input, phase, hasUsedPhase):
  while True:
    opcode = program[i] % 100

    if opcode == 99:
      return (i, None, True)

    mode1 = (program[i] - opcode) // 100 % 10
    mode2 = (program[i] - opcode) // 1000 % 10

    param1 = program[i+1] if mode1 == 1 or opcode == 3 else program[program[i+1]]
    param2 = (program[i+2] if mode2 == 1 else program[program[i+2]]) if opcode in [1, 2, 5, 6, 7, 8] else None
    param3 = program[i+3] if opcode in [1, 2, 7, 8] else None
    
    if opcode == 1: # add
      program[param3] = param1 + param2
      i += 4

    elif opcode == 2: # mul
      program[param3] = param1 * param2
      i += 4
    
    elif opcode == 3: # mov
      program[param1] = input if hasUsedPhase else phase
      hasUsedPhase = True
      i += 2

    elif opcode == 4: # out
      output = param1
      i += 2
      return (i, output, hasUsedPhase)

    elif opcode == 5: # jump-if-true
      i = param2 if param1 != 0 else i+3

    elif opcode == 6: # jump-if-false
      i = param2 if param1 == 0 else i+3

    elif opcode == 7: # less-than
      program[param3] = 1 if param1 < param2 else 0
      i += 4

    elif opcode == 8: # equals
      program[param3] = 1 if param1 == param2 else 0
      i += 4

    else:
      raise ValueError(f'opcode {opcode} from {program[i]}')
  
  raise ValueError(f'input {input} escaped the loop!')

def solve(input):
  results = collections.OrderedDict()

  for seq in itertools.permutations(range(5, 10), 5):
    computers = list()

    for phase in seq:
      computer = Computer(data, phase)
      computers.append(computer)

    computers[4].lastOutput = 0 # simulate that E gives A 0 the first time
    running = True

    while running:
      running = False
      for n in range(0, 5):
        if computers[n].halted: continue
        x = n - 1 if n > 0 else 4
        input = computers[x].lastOutput
        computers[n].run(input)
        running = True
      if not computers[4].halted:
        results[seq] = computers[4].lastOutput

  return max(results.values())

print(solve(data))