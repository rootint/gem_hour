score = 25
with open('scores.txt') as file:
    data = file.read().split()
if int(data[-1]) < score:
    clear = open('scores.txt', 'w').close()    
    output = open('scores.txt', 'w')
    output.write(f"Your best score: {score}" + '\n')
    output.close()