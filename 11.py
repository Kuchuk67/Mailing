import json

with open('2.csv', 'r') as f:
    i = 1
    d = {}
    for line in f:
        st = line.split(';')
        if st[3].find('@') > 0:
            print(st[0]+' '+st[1]+' '+st[2], st[3])
            d[i] = {'name': st[0]+' '+st[1]+' '+st[2], 'email': st[3] }
            i += 1
print(d)
with open('client.json', 'w', encoding="utf-8") as f:
    json.dump(d, f, indent=4, ensure_ascii=False)
