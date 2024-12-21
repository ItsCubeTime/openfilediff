def bytesToInt(myBytes:bytes)->int:
    "Variable length, positive integers presented as bytes, terminated using b'-' (you have to append the terminator yourself however)"
    r=0
    for b in myBytes:
        r+=b
    return r
def intToBytes(myInt:int)->bytearray:
    "Variable length, positive integers presented as bytes, terminated using b'-' (you have to append the terminator yourself however)"
    r=bytearray()
    extras=myInt%255
    total255s=(myInt-extras)/255
    i=0
    while i < total255s:
        i+=1
        r.append(255)
    if extras==45:# 45 is b'-'
        return r+b',\x01' # ',' is 44 & \x01 is 1. So were replacing '-' with a 2 byte equivalent as we cant use the '-' (because were using '-' as null terminator)
    else:
        r.append(extras)
        return r
# def bytesToInt(myBytes:bytes)->int:
#     return int(myBytes.decode('ascii'))
# def intToBytes(myInt:int)->bytes:
#     return bytes(str(int(myInt)),'ascii')

def getDiff(bytes1:bytes|bytearray,bytes2:bytes|bytearray)->bytearray:
    """
    Example usage:
    ```py
    b1=b"1234567890abcde"
    b2=b"1234321890abcde"
    diff=getDiff(b1,b2)
    B2=applyDiff(b1,diff)
    print(b2==B2) # Will always print true, regardless of the original contents of b1 & b2
    ```

    Returns a 3rd bytearray that describes the differences between `bytes1` and `bytes2`. You can then feed this 3rd bytearray as arg1 in `def applyDDiff()` and `bytes1` as arg2."""
    def print(*args):pass
    r=bytearray()
    indexTable=bytearray()
    bytes1=bytearray(bytes1)
    bytes2=bytearray(bytes2)
    bytes1Len=len(bytes1)
    bytes2Len=len(bytes2)
    iendDiff =bytes1Len
    i2endDiff=bytes2Len
    i=-1
    i2=-1
    while True: # 
        i+=1
        i2+=1
        try:
            b2=bytes2[i2]
        except IndexError:
            charsToRemove=i2endDiff-bytes2Len-(iendDiff-bytes1Len)
            removeAfterIndex=bytes1Len-charsToRemove
            print(f"charsToRemove {charsToRemove}")
            if removeAfterIndex!=bytes1Len:
                indexTable+=intToBytes(removeAfterIndex)+b'-'+intToBytes(bytes1Len)+b'--'
            else:
                indexTable+=b'-'
            return indexTable+b'-'+r
        try:
            b1=bytes1[i]
        except IndexError:
            print(f"bytes1Len:! {intToBytes(bytes1Len-1)}")
            finalSection=bytes2[i2:]
            rLen=len(r)
            indexTable+=intToBytes(bytes1Len)+b'-'+intToBytes(bytes1Len)+b'-'+intToBytes(rLen)+b'-'+intToBytes(len(finalSection)+rLen)
            return indexTable+b'---'+r+finalSection
            # return r
            # i2endDiff-iendDiff
        if b1!=b2:
            istartDiff=i
            i2startDiff=i2
            # print("1")
            i-=1
            while i < bytes1Len-1:
                # print("2")
                i+=1
                b1=bytes1[i]
                b1s=bytes1[i:min(bytes1Len,i+5)]
                shouldBreak=False
                i2=i2startDiff
                i2-=1
                while i2 < bytes2Len-1:
                    i2+=1
                    b2=bytes2[i2]
                    b2s=bytes2[i2:min(bytes2Len,i2+5)]
                    if b1s==b2s:
                        iendDiff =i
                        i2endDiff=i2
                        shouldBreak=True
                        break
                if shouldBreak:
                    break
            if not shouldBreak:
                print("mhm")
                # iendDiff=bytes1Len+1
                # i2endDiff=bytes2Len+1
                finalSection=bytes2[i2startDiff:bytes2Len]
                rLen=len(r)
                indexTable+=intToBytes(istartDiff)+b'-'+intToBytes(bytes1Len)+b'-'+intToBytes(rLen)+b'-'+intToBytes(rLen+len(finalSection))+b'---'
                return indexTable+r+finalSection
                # return r+key+intToBytes(istartDiff)+b'-'+intToBytes(iendDiff-1)+b']'+bytes2[i2startDiff:i2endDiff-1]
            # if shouldBreak:
            addedBytes=bytes2[i2startDiff:i2endDiff]
            rLen=len(r)
            print(f"rLen: {rLen}")
            indexTable+=intToBytes(istartDiff)+b'-'+intToBytes(iendDiff)+b'-'+intToBytes(rLen)+b'-'+intToBytes(rLen+len(addedBytes))+b'-'
            r+=addedBytes
    print("defaultr")
    return r
class _DiffFileComponent():
    def __init__(self,replaceFrom:int,replaceTo:int,replaceWith:bytearray):
        self.replaceFrom:     int =replaceFrom
        self.replaceTo:       int =replaceTo
        self.replaceWith:bytearray=replaceWith

    def __repr__(self):
        return f"\n    replaceFrom: {self.replaceFrom} replaceTo: {self.replaceTo} replaceWith: {self.replaceWith}"
        
def applyDiff(bytes1:bytes|bytearray,diff:bytes|bytearray)->bytearray:
    def print(*args):pass

    bytes1=bytearray(bytes1)
    diff=bytearray(diff)
    indexTable,diff=diff.split(b'---')
    indexTableLen=len(indexTable)
    # indexTable+=b'---'
    indexTable=indexTable
    print(f"diff: {diff} indexTable: {indexTable}")
    r=bytes1.copy()
    # diffLen=len(diff)
    # keyLen=len(key)
    bytes1Len=len(bytes1)
    components:list[_DiffFileComponent]=[]
    shouldBreak=False
    i=0
    while i<indexTableLen-1:
        dashIndex0=indexTable.find(b'-',i+1)
        print(f"i: {i} dashIndex0: {dashIndex0}")
        replaceToStartIndex=bytesToInt(indexTable[i:dashIndex0])
        dashIndex1=indexTable.find(b'-',dashIndex0+1)
        if dashIndex1==-1:
            print(f"p1")
            newI=dashIndex3
            print(f"dashIndex1: {dashIndex1} dashIndex2: {dashIndex2}")
            replaceToEndIndex=bytesToInt(indexTable[dashIndex0+1:indexTableLen])
            # indexTable+=
            replaceWithStr=b''
            shouldBreak=True
        else:
            replaceToEndIndex=bytesToInt(indexTable[dashIndex0+1:dashIndex1])
            dashIndex2=indexTable.find(b'-',dashIndex1+1)
            dashIndex3=indexTable.find(b'-',dashIndex2+1)
            if dashIndex1+1==dashIndex2: # Replace with nothing
                print(f"p2")
                newI=dashIndex2
                # if dashIndex2+1==diff.find(b'-',dashIndex1):
                    # foundIndexTerminator=True
                replaceWithStr=b''
            else:
                # if :
                print(f"p3")
                newI=indexTableLen if dashIndex3==-1 else dashIndex3
                replaceFromStartIndex=bytesToInt(indexTable[dashIndex1+1:dashIndex2])
                replaceFromEndIndex=bytesToInt(indexTable[dashIndex2+1:newI])
                print(f"dashIndex1: {dashIndex1} dashIndex2: {dashIndex2} dashIndex3: {dashIndex3} replaceFromStartIndex: {replaceFromStartIndex} replaceFromEndIndex: {replaceFromEndIndex} newI {newI} indexTableLen {indexTableLen}")
                replaceWithStr=diff[replaceFromStartIndex:replaceFromEndIndex]


        components.append(_DiffFileComponent(replaceToStartIndex,replaceToEndIndex,replaceWithStr))
        i=newI+1
        if shouldBreak:
            break
        # print(f"appending comp: {components[-1]}")
    print(f"components: {components}")
    for component in reversed(components):
        print(f"bytes1Len: {bytes1Len}")
        r=r[:component.replaceFrom]+component.replaceWith+(r[component.replaceTo:] if  bytes1Len > component.replaceTo-1 else b'')
    return r

# b1=b"LERUMIPSUMVIRAKOLERA12345670890abcdefgAWEShijklmnopqABCDEdddddddddddddd"
# b2=b"LERUMIPSUMVIRAKOLERA1234321890abcdefgBAEhijklmnpqAfBCDEdddddddddddddda"
# diff=getDiff(b1,b2)
# print(f"b1: {b1} len: {len(b1)}\nb2: {b2} len: {len(b2)}\ndi: {bytes(diff)} len: {len(diff)}")
# print("applyDiff")
# B2=applyDiff(b1,diff)
# print(f"B2: {bytes(B2)}\n{bytes(B2)==b2}")


# b1=b"1234dwads567890abcddwasdaseadwodwadawdasddsdawdsadeadwdodwaddadasdswadas"
# b2=b"1234321890abcdeadwdodwaddadasdswadasddeaasdwadwdodwaddadasdswadas"
# diff=getDiff(b1,b2)
# print(f"b1: {b1} len: {len(b1)}\nb2: {b2} len: {len(b2)}\ndi: {bytes(diff)} len: {len(diff)}")
# B2=applyDiff(b1,diff)
# print(f"B2: {bytes(B2)}\n{bytes(B2)==b2}")
# print(b2==B2) # Will always print true, regardless of the original contents of b1 & b2

# b1=b"12d3sdsaaaassSSsawads"
# b2=b"a123ddsaaaasasdaadwwadaaa"
# # b1=b"123abcdDIFFGENERATIONISAWESOMEwoof"
# # b2=b"a1234abcdDIFFGENERATIONISAWESOMEfffs"
# diff=getDiff(b1,b2)
# print(f"b1: {b1} len: {len(b1)}\nb2: {b2} len: {len(b2)}\ndi: {bytes(diff)} len: {len(diff)}")
# B2=applyDiff(b1,diff)
# print(f"B2: {bytes(B2)}\n{bytes(B2)==b2}")
# print(b2==B2) # Will always print true, regardless of the original contents of b1 & b2