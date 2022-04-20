PR = 6
tokenHolder = 1
class Token:
    def __init__(self) -> None:
        self.id = 0
        self.LN = []
        self.tokenQ = []
        for i in range(PR):
            self.LN.append(0)

token = Token()

class Site:
    def __init__(self):
        self.RN = []
        self.exec = False
        self.isReq = False
        self.hasToken = False
        for i in range(PR):
            self.RN.append(0)
    def request(self,pid,seqn):
        self.RN[pid] = max(self.RN[pid],seqn)
        if self.hasToken == True:
            if self.exec == False and token.LN[pid] + 1 == self.RN[pid]:
                self.hasToken = False
                global tokenHolder
                tokenHolder = pid
            elif(token.LN[pid] + 1 == self.RN[pid]):
                token.tokenQ.append(pid)

site = [Site() for _ in range(PR)]


def request(pid):
    global tokenHolder
    site[pid].RN[pid] +=1
    seqno = site[pid].RN[pid]
    if site[pid].isReq == True or site[pid].exec == True:
        print("SITE {} is already requesting\n".format(pid))
        return
    site[pid].isReq = True
    if tokenHolder == pid:
        site[pid].isReq = False
        site[pid].exec = True
        print("Site {} already has the token and it enters CS".format(pid))
        return
    if tokenHolder != pid:
        for i in range(PR): # broadcast
            if i!=pid:
                site[i].request(pid,seqno)

    if tokenHolder == pid:
        site[pid].hasToken = True
        site[pid].exec = True
        site[pid].isReq = True
        print("SITE {} gets the token and it enters CS".format(pid))
    else:
        print("SITE {} is currently executing the CS\nSite {} has placed its request".format(tokenHolder,pid))

def release(pid):
    global tokenHolder
    if site[pid].exec != True:
        print("SITE {} is not currently executing the critical section".format(pid))
        return
    token.LN[pid] = site[pid].RN[pid]
    site[pid].exec = False
    print("SITE {} releases the CS".format(pid))
    if len(token.tokenQ) > 0:
        siteid = token.tokenQ.pop(0)
        token.id = siteid
        site[pid].hasToken = False
        tokenHolder = siteid
        site[siteid].hasToken = True
        site[siteid].exec = True
        site[siteid].isReq = False
        print('SITE {} gets the token and it enters the CS'.format(siteid))
        return
    print("SITE {} still has the token\n".format(pid))

def printData():
    global tokenHolder
    temp = []
    print("Token State\n")
    print("Token Holder: {}\n".format(tokenHolder))
    print("TOKEN QUEUE: {}\n".format(token.tokenQ))
    print("TOKEN SEQ NO ARRAY: {}\n".format(token.LN))
    print("SITES SEQ NO ARRAYS: \n")
    for i in range(PR):
        print('S {}: {}'.format(i,site[i].RN))

def main():
    global tokenHolder,site,PR
    tokenHolder = 0
    inpstr = None
    site[0].hasToken = True
    time = 0
    print("The number of sites are {}".format(PR))
    print("INITIAL STATE\n")
    printData()
    print('\n')
    while inpstr!="QUIT":
        inpstr = input()
        if inpstr == "REQ":
            pid = int(input())
            print("EVENT: {} {}".format(inpstr,pid))
            request(pid)
            printData()
            print("\n")
        elif inpstr == "REL":
            pid = int(input())
            print("EVENT: {} {}".format(inpstr,pid))
            release(pid)
            printData()
            print("\n")

main()