class Branch():
    def __init__(self,name, location):
        self.name=name
        self.location=location
    def returnLoc(self):
        return self.location
    def returnName(self):
        return self.name



def loadMachineFile(filename):
    registers = [""] * 100
    file = open(filename)
    i = 0
    for each in file:
        registers[i] = each.strip()
        if (registers[i] == ""):
            registers[i] = "000"
        i += 1
    if i < 100:
        for x in range(i, 100):
            registers[x] = "000"
    runCode(registers)

def loadAssemblyFile(filename):
    instructions=[]

    file = open(filename)
    errors=False
    for each in file:
        each=each.strip()
        instructions.append(instructions.append(each.strip()))
        instructions.pop()
    if errors==False:
        assembler(instructions)
    else:
        print('An unexpected error occured')
def baseInstructionCode(i,registers,each):
            if each=='HLT':
                #print("HLT")
                registers[i]="000"
            elif each[:3]=='ADD':
                #print("ADD",each[4:])
                registers[i]='1'+each[each.find(" ")+1:]

            elif each[:3]=='SUB':
                #print("SUB",each[4:])
                registers[i]='2'+each[each.find(" ")+1:]

            elif each[:3]=='STA':
                #print("STA",each[4:])
                registers[i]='3'+each[each.find(" ")+1:]

            elif each[:3]=='LDA':
                #print("LDA",each[4:])
                registers[i]="5"+each[each.find(" ")+1:]

            elif each[:3]=='BRA':
                #print("BRA",each[4:])
                registers[i]='6'+each[each.find(" ")+1:]
            elif each[:3]=='BRZ':
                #print("BRZ",each[4:])
                registers[i]='7'+each[each.find(" ")+1:]

            elif each[:3]=='BRP':
                #print("BRZ",each[4:])
                registers[i]='8'+each[each.find(" ")+1:]

            elif each[:3]=='INP':
                #print("INP",each[4:])
                registers[i]='901'

            elif each[:3]=='OUT':
                #print("OUT",each[4:])
                registers[i]='902'
            if len(registers[i])==2:
                registers[i]=registers[i][0]+"0"+registers[i][1]
            return registers[i]

def assembler(assembly):
    registers=[""]*100
    if len(assembly)>100:
        print('File too large: Must be less than 100 instructions')
    else:
        variables=[]        #Name, Location
        variableReferences=[]   #Name of variable, Line it's being referenced on
        i=0
        branchesTo=[]
        branchesFrom=[]
        for each in assembly:
            #print(each)
            if each==None:
                i-=1
                each="SKIP"
            else:
                each=each.strip()
            if each=="SKIP":
                x=0
            elif each.find('HLT')==0:
                baseInstructionCode(i, registers, each)
            elif each.find('ADD')==0:
                baseInstructionCode(i, registers, each)
            elif each.find('SUB')==0:
                baseInstructionCode(i, registers, each)
            elif each.find('STA')==0:
                baseInstructionCode(i, registers, each)
            elif each.find('LDA')==0:
                baseInstructionCode(i, registers, each)
            elif each.find('BRA')==0:
                tempStr=each[each.find(' ')+1:].strip()
                tempStr=each[each.find(' ')+1:].strip()
                branchesFrom.append([tempStr,'6',str(i)])          #Where to branch to, kind of branch, where from
                #print(branchesFrom[len(branchesFrom)-1])
            elif each.find('BRZ')==0:
                tempStr=each[each.find(' ')+1:].strip()
                tempStr=each[each.find(' ')+1:].strip()
                branchesFrom.append([tempStr,'7',str(i)])          #Where to branch to, kind of branch, where from
                #print(branchesFrom[len(branchesFrom)-1])
            elif each.find('BRP')==0:
                tempStr=each[each.find(' ')+1:].strip()
                tempStr=each[each.find(' ')+1:].strip()
                branchesFrom.append([tempStr,'8',str(i)])          #Where to branch to, kind of branch, where from
                #print(branchesFrom[len(branchesFrom)-1])
            elif each.find('INP')==0:
                baseInstructionCode(i, registers, each)
            elif each.find('OUT')==0:
                baseInstructionCode(i, registers, each)
            else:
                if(each.find('DAT')!=-1):
                    variables.append([each[:each.find(" ")],str(i)])
                    tempStr=each[each.find(' ')+1:].strip()
                    if tempStr.find(' ')==-1:
                        registers[i]="000"
                    else:
                        tempStr=tempStr[tempStr.find(' ')+1:].strip()
                        if len(tempStr)==1:
                            registers[i]="00"+tempStr[-1]
                        elif len(tempStr)==2:
                            registers[i]="0"+tempStr[-1]
                        elif len(tempStr)==3:
                            registers[i]=tempStr

                elif each.find('HLT')!=-1 or each.find('ADD')!=-1 or each.find('SUB')!=-1 or each.find('STA')!=-1 or each.find('LDA')!=-1 or each.find('BRA')!=-1 or each.find('BRZ')!=-1 or each.find('BRP')!=-1 or each.find('INP')!=-1 or each.find('OUT')!=-1:
                    branchesTo.append(Branch(each[:each.find(' ')],str(i)))
                    #print(branchesTo[0].returnName()+"."+branchesTo[0].returnLoc())
                    registers[i]=baseInstructionCode(i,registers,each[each.find(' ')+1:].strip())
                    #fprint(registers[i])
            i+=1
        for x in range(0,100):
            if registers[x]=="":
                registers[x]="000"
        i=0     #Routing variables to their memory locations
        for each in registers:
            if each[0]!=6 and each[0]!=7 and each[0]!=8:
                changeInst=False
                try:
                    int(each)
                except ValueError:
                    changeInst=True
                if changeInst:

                    varRef=each[1:]
                    if varRef[0]=="0":
                        varRef=varRef[1:]
                    #print(varRef)
                    for item in variables:
                        if varRef==item[0]:
                            if int(item[1])<10:
                                registers[i]=each[0]+"0"+item[1]
                            else:
                                registers[i]=each[0]+item[1]
            i+=1
        for x in branchesTo:
            for y in branchesFrom:
                if(x.returnName()==y[0]):
                    if(int(x.returnLoc())<10):
                        tempStr="0"+x.returnLoc()
                    else:
                        tempStr=x.returnLoc()
                    registers[int(y[2])]=y[1]+tempStr

        newFile=""
        newFile=str(input('Would you like to write the machine code to a File Y/N>>> '))
        if(newFile.lower()=="y"):
            name=str(input("Please enter the name of your file>>> "))
            f=open(name+".txt","w")
            f.write("")
            f=open(name+".txt","a")
            for each in registers: f.write(each+"\n")
        #print(registers)
        runCode(registers)


def runCode(code):
    interrupt = False
    Acc = 0
    PC = 0
    print('Starting Code')
    while interrupt == False:
        if (code[PC][0] == '0'):
            interrupt = True
            #print('HLT')
        elif (code[PC][0] == "1"):  # Add
            Acc += int(code[int(code[PC][1:])])
            while (Acc > 999):
                Acc = -1000 + (Acc - 999)
                print('WARNING: STACK OVERFLOW')
            #print('ADD' + str(int(code[PC][1:])))
            PC += 1
        elif (code[PC][0] == "2"):  # Sub
            Acc -= int(code[int(code[PC][1:])])

            while (Acc < -999):
                Acc = 1000 + (999 - Acc)
                print('WARNING: STACK OVERFLOW')
            #print('SUB' + str(int(code[PC][1:])))
            PC += 1
        elif (code[PC][0] == "3"):  # STA
            if Acc>=100:
                code[int(code[PC][1:])] = str(Acc)
            elif Acc>=10:
                code[int(code[PC][1:])] = "0"+str(Acc)
            elif Acc>=0:
                code[int(code[PC][1:])] = "00"+str(Acc)
            #print('STA at ' + code[PC][1:])
            PC += 1
        elif (code[PC][0] == "5"):  # LDA
            Acc = int(code[int(code[PC][1:])])
            #print('LDA from ' + code[PC][1:])
            PC += 1
        elif (code[PC][0] == "6"):  # BRA
            PC = int(code[PC][1:])
            #print('Branching')
        elif (code[PC][0] == "7"):  # BRZ
            if Acc == 0:
                PC = int(code[PC][1:])
            #    print('Branching')
            else:
            #    print('Failure to Branch')
                PC+=1
        elif (code[PC][0] == "8"):  # BRP
            if Acc >= 0:
                PC = int(code[PC][1:])
            #    print('Branch')
            else:
            #    print('Failure to Branch')
                PC+=1
        elif (code[PC] == "902"):  # OUT
            print('Output: '+str(Acc))
            PC += 1

        elif (code[PC] == "901"):  # INP
            Acc = int(input('Waiting For Interger Input: '))
            PC += 1
        else:
            interrupt = True
            print('Unexpected error')
        #print('PC:'+str(PC))
        #print('Acc:'+str(Acc))


loadAssemblyFile('LMC.txt')
