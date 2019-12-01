with open('input.txt', 'r') as file:
  data = file.read().splitlines()

def fuelFor(input):
  output = (input // 3) - 2
  if output <= 0: 
    return 0
  return output + fuelFor(output)

sum = 0

for line in data: 
  sum += fuelFor(int(line))

# Not: 5058439
print(sum)
print(fuelFor(1969))