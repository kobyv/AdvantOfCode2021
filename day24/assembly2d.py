v = [[] for _ in range(18)]
with open('assembly.txt') as f:
    i = 0
    for line in f:
        v[i%18].append(line.strip())
        i += 1

for q in v:
    print('\t'.join(q))
    
