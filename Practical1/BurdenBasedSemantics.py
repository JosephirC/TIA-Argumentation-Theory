burden = set()

def bur(arg, i):
    b = 0
    if i == 0:
        b = 1
    if i > 0:
        b = 1 + int(1/bur(arg, i-1))
    return b 

def addset(bf, rebuts, n):
    cpt = 0
    dejaVu = []
    while n != 0:
        for arg in bf:
            if arg not in dejaVu:
                cpt = 0
                dejaVu.append(arg)
            else: 
                cpt += 1
            if cpt == 0:
                burden.add(bur(arg, 0))
            else:
                for arg2 in bf:
                    i = 0
                    # print(arg.name, arg2.name)
                    if (arg, arg2) or (arg2, arg) in rebuts:
                        i+=1
                burden.add(bur(arg, i))
        n -= 1
    return burden