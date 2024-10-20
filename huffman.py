import heapq
import os
from heapq import heappop, heappush
import math

huffCodes  = {}
entropy  = 0 
entropy2 = 0
freqDictionary = {}
L = 0
class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
 
    # элемент с наивысшим приоритетом имеет наименьшую частоту
    def __lt__(self, other):
        return self.freq < other.freq

def getCode(root , binStr ):

    # обнаружил листовой узел
    if (root.left is None and root.right is None):
        return {root.char : binStr} 

    d=dict()
    d.update(getCode(root.left, binStr + '1'))
    d.update(getCode(root.right, binStr + '0'))
    return d


def buildTree(inputText):
    global freqDictionary 

    for char in inputText:
        if(char in freqDictionary):
            freqDictionary[char] +=1
        else: 
            freqDictionary[char] = 1

    queue = [Node(char , freq) for char, freq in freqDictionary.items()]
    heapq.heapify(queue)

    while (len(queue) != 1):
        first = heappop(queue)
        second = heappop(queue)
        heappush(queue,Node(None,first.freq + second.freq,first,second))
    
    return getCode(queue[0],'')

def bitstring_to_bytes(s):  
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def encode(data ,  outputFile):
    global huffCodes,entropy,freqDictionary , L , entropy2
    huffCodes = buildTree(data)

    entropy = math.log2(len(huffCodes))

    L = sum([freqDictionary[char]*len(huffCodes[char]) / len(data) for char in freqDictionary.keys()])
    entropy2 = - sum([freq/len(data) * math.log2(freq/len(data)) for key , freq in freqDictionary.items()])

    output_file = open(outputFile, 'wb')
    binString = ''.join([huffCodes.get(char) for char in data])

    output_file.write(bitstring_to_bytes(binString))
    output_file.close()

def encodeFile(inputFile ,  outputFile):
    file = open(inputFile , 'rt' )
    data = file.read()
    file.close()
    encode(data , outputFile)


def decode(name):
    global huffCodes
    file = open(name , 'rb' )
    data = file.read()
    file.close()
    byteString = bin(int.from_bytes(data, byteorder='big'))[2:]
    charsDict = dict((v,k) for k,v in huffCodes.items())
    resArray = []
    sequence = ''
    for char in byteString:
        if not char:
            break
        sequence = sequence+char
        if sequence in charsDict:
            value = charsDict[sequence]
            resArray.append(value)
            sequence = ''
    return resArray

def decodeFile(inputFile , outputFile):
    decodeFile = open(outputFile,'wt')
    data = decode(inputFile)
    for char in data:
        decodeFile.write(char)
    decodeFile.close()

