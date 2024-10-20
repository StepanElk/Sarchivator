from huffman import encode , decode
import os

def longest_prefix_from(Left, Right):
    LongestPrefixLength = 0
    LongestPrefixPos = -1

    while True:
        PrefixLength = LongestPrefixLength+1
        if PrefixLength >= len(Right):
            break

        Prefix = Right[0: PrefixLength]
        PrefixPos = Left.find(Prefix)

        if PrefixPos == -1:
            break

        LongestPrefixLength = PrefixLength
        LongestPrefixPos = PrefixPos
    return (LongestPrefixLength, LongestPrefixPos)

def codeBufferLZ77(Buffer):
    Result = []
    CodePos = 0

    while CodePos < len(Buffer):
        Left = Buffer[0:CodePos]
        Right = Buffer[CodePos:]

        (PrefixLength, PrefixPos) = longest_prefix_from(Left, Right)

        if (PrefixLength == 0):
            Result.append(Buffer[CodePos])
            CodePos = CodePos+1
        else:
            Result.append((PrefixLength,CodePos-PrefixPos))
            CodePos = CodePos + PrefixLength
    return Result


def lz77encode(input_filename, output_filename):
    input_file = open(input_filename, 'r')
    CodedText = []
    while True:
        #Размер буфера = 60 символов
        Window = 60
        Buffer = input_file.read(Window)
        if Buffer == '':
            break
        Code = codeBufferLZ77(Buffer)
        CodedText += Code

    input_file.close()

    data = []
    for c in CodedText:
        if type(c) == tuple : 
            data.append(f'({c[0]},{c[1]})')
        else:
            data.append(c)
    encode(data ,output_filename)
    

def lz77decode(filename, output_filename):
    decData = decode(filename)  
    DecodedText = ''
    print('Пример кодирования lz77: ' , decData[:20])
    Pos = 0
    for Value in decData:
        if Value[0]=='(' and Value[-1]==')':
            (PrefixLength, Shift) = eval(Value)
            PrefixPos = Pos-Shift
            DecodedText += DecodedText[PrefixPos:PrefixPos+PrefixLength]
            Pos = Pos + PrefixLength
        else:
            DecodedText = DecodedText+Value
            Pos = Pos + 1

    output_file = open(output_filename, 'w')
    output_file.write(DecodedText)
    output_file.close()
