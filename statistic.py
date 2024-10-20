import huffman
import lz77
import os

def start():
    print('Сжатие методом Хаффмана:')
    runEncoding('test1.txt' , 'Huffman.stepan',huffman.encodeFile)  
    runDecoding('Huffman.stepan' , 'HuffmanDecode.txt',huffman.decodeFile)

    print('\nСжатие методом lz77:')
    runEncoding('EO.txt' , 'lz77.stepan',lz77.lz77encode)
    runDecoding('lz77.stepan' , 'lz77Decode.txt',lz77.lz77decode)
    return

def runEncoding(inputFileName , outputFileName , method):
    inSize = os.stat(inputFileName).st_size
    print('Начальный размер файла:' , inSize,' байт')
    method(inputFileName,outputFileName)
    outSize = os.stat(outputFileName).st_size
    print('Размер после сжатия:' , outSize,' байт')
    getStatistic(inSize , outSize)

def runDecoding(inputFileName , outputFileName , method):
    method(inputFileName,outputFileName)
    print('Размер после восстановления:' , os.stat(outputFileName).st_size,' байт')

def getStatistic(inSize , outSize):
    print("Коэффициент ститистического сжатия: " , huffman.entropy / huffman.L)
    print('Процент сжатия: ' , ((inSize-outSize)/inSize)*100 , '%')
    print("Коэффициент относительной эффективности: " , huffman.entropy2 / huffman.L)

start()