from random import randint
length = input("Enter length of answer: ")
answer = [str(randint(0,9)) for _ in range(int(length))]
guess_num = 1
while True:
  response = ["L" for _ in range(int(length))]
  guess = ["NA" for _ in range(int(length)+1)]
  while len(guess) > int(length):
    guess = list(input(f"Enter guess #{guess_num}: "))
  guess_num += 1
  place = 0
  answer_copy = list(answer)
  for n in guess:
    if n == answer[place]:
      response[place] = "X"
      answer_copy[answer_copy.index(n)] = "N"
    place += 1
  place = 0
  for n in guess:
    if n in answer_copy:
      response[place] = "O"
      answer_copy[answer_copy.index(n)] = "N"
    place += 1
  print("".join(response))
  if response == ["X" for _ in range(int(length))]:
    print("You win!")
    break
  elif guess_num > 10:
    print("You lose!")
    break