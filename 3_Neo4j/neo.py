req = ""
for i in range(1, 16):
    req = req.join('Match ('+f'stop{i}'+': Stop {name: "'+f'stop{i}'+'"}), ('+f'stop{i+1}'+': Stop {name:"'+f'stop{i+1}'+'"})\n create ('+f'stop{i}'+')<-[:1]->('+f'stop{i+1}'+')\n')
print(req)


