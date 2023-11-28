import csv

def WriteToCSV(simObj):
    fName = 'Fitness.csv'
    with open(fName,'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["x-axis", "Min","Avg", "Max"])
        for i in range(simObj.lGen):
            writer.writerow([i, round(simObj.avgFitnesses[0][i],5), round(simObj.avgFitnesses[1][i],5), round(simObj.avgFitnesses[2][i],5)])
    fName = 'RTP.csv'
    with open(fName,'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["x-axis", "Min","Avg", "Max"])
        for i in range(simObj.lGen):
            writer.writerow([i, round(simObj.avgRTPs[0][i],5), round(simObj.avgRTPs[1][i],5), round(simObj.avgRTPs[2][i],5)])
    fName = 'symDiversities.csv'
    with open(fName,'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["x-axis", "Min","Avg", "Max"])
        for i in range(simObj.lGen):
            writer.writerow([i, round(simObj.avgSymDiversities[0][i],5), round(simObj.avgSymDiversities[1][i],5), round(simObj.avgSymDiversities[2][i],5)])

def BestToCSV(simObj):
    fName = 'Best.csv'
    with open(fName,'w',newline='') as file:
        writer = csv.writer(file)
        row = ['Seed IDX', 'Generation', 'Fitness', 'RTP', 'Symbol Diversity']
        for i in range(len(simObj.best[0][4])):
            for j in range(len(simObj.best[0][4][i])):
                row.append('R'+str(i+1)+' Seg' + str(j) + ' Symbol')
                row.append('R'+str(i+1)+' Seg' + str(j) + ' Length')
        writer.writerow(row)
        for i in range(simObj.lSeeds):
            row = [i,simObj.best[i][0],round(simObj.best[i][1],5), round(simObj.best[i][2],5), round(simObj.best[i][3],5)]
            for j in range(len(simObj.best[i][4])):
                for k in range(len(simObj.best[i][4][j])):
                    row.append(simObj.best[i][4][j][k][0])
                    row.append(simObj.best[i][4][j][k][1])
            writer.writerow(row)

def ReadInPaytable(slotModel):
    fileName = "paytable.csv"
    sectionIter = 0
    with open(fileName,"r") as f:
        for line in f:
            sLine = line.strip().split(',')
            if len(sLine):
                if sLine[0] == "Pays":
                    sectionIter = 1
                elif sLine[0] == "Includes":
                    slotModel.symbolList.append(100) #any symbol
                    sectionIter = 2
                elif sLine[0] == "Bonus":
                    sectionIter = 3
                elif sLine[0] == "Stack":
                    sectionIter = 4
                    slotModel.symbolsToStack.extend(list([int(x) for x in sLine[1:]]))
                elif sLine[0] == "Reels":
                    sectionIter = 5
                    slotModel.numReels = int(sLine[1])
                elif sLine[0] == "Rows":
                    sectionIter = 6
                    slotModel.numRows = int(sLine[1])
                elif sLine[0] == "Targets":
                    sectionIter = 7
                    slotModel.targets.extend(list([float(x) for x in sLine[1:]]))
                elif sectionIter == 1:
                    slotModel.symbolList.append(int(sLine[0]))
                    slotModel.actualSymbolList.append(int(sLine[0]))
                    slotModel.symbolList.append(int(sLine[0])+slotModel.exclDiff) #exclude
                    slotModel.excludes.append(int(sLine[0])+slotModel.exclDiff)
                    for i in range(5,0,-1):
                        slotModel.payCombinations.append([int(sLine[i]),list([int(sLine[0]) for x in range(i)])])
                        if len(slotModel.payCombinations[len(slotModel.payCombinations)-1][1]) < 5:
                            slotModel.payCombinations[len(slotModel.payCombinations)-1][1].append(int(sLine[0])+slotModel.exclDiff)
                        tLen = len(slotModel.payCombinations[len(slotModel.payCombinations)-1][1])
                        while tLen < 5:
                            slotModel.payCombinations[len(slotModel.payCombinations)-1][1].append(100)
                            tLen = len(slotModel.payCombinations[len(slotModel.payCombinations)-1][1])
                elif sectionIter == 2:
                    slotModel.includes.append([int(sLine[0]),list([int(x) for x in sLine[1:]])])
                elif sectionIter == 3:
                    slotModel.bonusSymbols.append(int(sLine[0]))
            