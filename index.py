import os
import argparse

#read input params, parse and return it
def readCMDParams():
    parser = argparse.ArgumentParser(description='A simple tools for find & replace text in files')
    # parser.add_argument('inputDir')
    # parser.add_argument('fileExtensions',help = 'e.g "java txt"')
    args = parser.parse_args()
    return args

#remove comments from helper translation files
def removeComments(ArrayString):
    for index, line in enumerate(ArrayString):
        if(line.startswith('#')):
            del ArrayString[index]

def findReplaceWithDic(data, translationsDic):
    for keyVal in translationsDic:
        t = keyVal.split(',')
        key = t[0].strip()
        key = key[1:-1] #remove start and end '
        value = t[1].strip()
        value = value[1:-1] #remove start and end '

        data = data.replace(key, value)
    return data
    
def findAndReplaceWithLine(linesContent, linesToReplace, translationsDic):
    if linesToReplace == 'ALL':
        for index, line in enumerate(linesContent):
            linesContent[index] = findReplaceWithDic(line,translationsDic)
    else:
        for lineNumber in linesToReplace:
            linesContent[lineNumber - 1] = findReplaceWithDic(linesContent[lineNumber - 1], translationsDic)
    return linesContent


def parseNumbers(numbersStr):
    result = []
    if numbersStr.isdigit():
        result = [int(numbersStr)]
    elif numbersStr.find(',') != -1: #selective mode, line 2,3,6 for example
        result = numbersStr.replace(' ','').split(',')
        result = map(lambda x: int(x), result)
    elif numbersStr.find('-') != -1: #range mode, from line 2 to 6 for example
        r = numbersStr.replace('[','').replace(']','').split('-')
        result = range(int(r[0]), int(r[1]) + 1)
    elif numbersStr.strip() == '*':
        result = 'ALL'
    return result

cmdArgs = readCMDParams()

translationsFile = open('translations.csv','r')
translationLocFile = open('translations-location.csv','r')

translationStrings = translationsFile.readlines()
translationLocStrings = translationLocFile.readlines()

# removeComments(translationStrings)
# removeComments(translationLocStrings)

for loc in translationLocStrings:
    if(loc.startswith('#')):
        continue
    splited = loc.split(' ')
    fileToTranslateLoc = splited[0]
    lines = splited[1]
    whatUseForTranslate = splited[2]

    whatUseForTranslate = whatUseForTranslate.replace('\n','')

    if(os.path.isfile(fileToTranslateLoc)):
        fileToTranslate = open(fileToTranslateLoc)
        linesToReplace = parseNumbers(lines)
        dicSelectedWordsIndex = parseNumbers(whatUseForTranslate)
        dicSelectedWords = translationStrings
        if dicSelectedWordsIndex != 'ALL':
            dicSelectedWords = []
            for index in dicSelectedWordsIndex:
                dicSelectedWords.append(translationStrings[index - 1])
        
        result = findAndReplaceWithLine(fileToTranslate.readlines(),linesToReplace,dicSelectedWords)

        filename = os.path.splitext(fileToTranslateLoc)
        outputFileName = filename[0] + '-translate' + filename[1]
        outputFile = file(outputFileName,'w')
        outputFile.write(''.join(result))
        outputFile.close()
    else:
        print('Warning: fileNotFound ' + fileToTranslateLoc)


    

# inputFile = open(cmdArgs.inputfile,'r')
# inputLines = inputFile.readlines

# outputFile = open(cmdArgs.outputfile,'w')


# outputTxt = [line.replace('find me','ok') for line in inputFile]
# outputFile.write(''.join(outputTxt))
# outputFile.close()