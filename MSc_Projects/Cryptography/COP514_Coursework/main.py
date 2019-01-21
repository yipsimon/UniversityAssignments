import timeit,copy,sys

sbox = {'0' : {'0':'63', '1':'7C', '2':'77', '3':'7B', '4':'F2', '5':'6B', '6':'6F', '7':'C5', '8':'30', '9':'01', 'A':'67', 'B':'2B', 'C':'FE', 'D':'D7', 'E':'AB', 'F':'76'},
        '1' : {'0':'CA', '1':'82', '2':'C9', '3':'7D', '4':'FA', '5':'59', '6':'47', '7':'F0', '8':'AD', '9':'D4', 'A':'A2', 'B':'AF', 'C':'9C', 'D':'A4', 'E':'72', 'F':'C0'},
        '2' : {'0':'B7', '1':'FD', '2':'93', '3':'26', '4':'36', '5':'3F', '6':'F7', '7':'CC', '8':'34', '9':'A5', 'A':'E5', 'B':'F1', 'C':'71', 'D':'D8', 'E':'31', 'F':'15'},
        '3' : {'0':'04', '1':'C7', '2':'23', '3':'C3', '4':'18', '5':'96', '6':'05', '7':'9A', '8':'07', '9':'12', 'A':'80', 'B':'E2', 'C':'EB', 'D':'27', 'E':'B2', 'F':'75'},
        '4' : {'0':'09', '1':'83', '2':'2C', '3':'1A', '4':'1B', '5':'6E', '6':'5A', '7':'A0', '8':'52', '9':'3B', 'A':'D6', 'B':'B3', 'C':'29', 'D':'E3', 'E':'2F', 'F':'84'},
        '5' : {'0':'53', '1':'D1', '2':'00', '3':'ED', '4':'20', '5':'FC', '6':'B1', '7':'5B', '8':'6A', '9':'CB', 'A':'BE', 'B':'39', 'C':'4A', 'D':'4C', 'E':'58', 'F':'CF'},
        '6' : {'0':'D0', '1':'EF', '2':'AA', '3':'FB', '4':'43', '5':'4D', '6':'33', '7':'85', '8':'45', '9':'F9', 'A':'02', 'B':'7F', 'C':'50', 'D':'3C', 'E':'9F', 'F':'A8'},
        '7' : {'0':'51', '1':'A3', '2':'40', '3':'8F', '4':'92', '5':'9D', '6':'38', '7':'F5', '8':'BC', '9':'B6', 'A':'DA', 'B':'21', 'C':'10', 'D':'FF', 'E':'F3', 'F':'D2'},
        '8' : {'0':'CD', '1':'0C', '2':'13', '3':'EC', '4':'5F', '5':'97', '6':'44', '7':'17', '8':'C4', '9':'A7', 'A':'7E', 'B':'3D', 'C':'64', 'D':'5D', 'E':'19', 'F':'73'},
        '9' : {'0':'60', '1':'81', '2':'4F', '3':'DC', '4':'22', '5':'2A', '6':'90', '7':'88', '8':'46', '9':'EE', 'A':'B8', 'B':'14', 'C':'DE', 'D':'5E', 'E':'0B', 'F':'DB'},
        'A' : {'0':'E0', '1':'32', '2':'3A', '3':'0A', '4':'49', '5':'06', '6':'24', '7':'5C', '8':'C2', '9':'D3', 'A':'AC', 'B':'62', 'C':'91', 'D':'95', 'E':'E4', 'F':'79'},
        'B' : {'0':'E7', '1':'C8', '2':'37', '3':'6D', '4':'8D', '5':'D5', '6':'4E', '7':'A9', '8':'6C', '9':'56', 'A':'F4', 'B':'EA', 'C':'65', 'D':'7A', 'E':'AE', 'F':'08'},
        'C' : {'0':'BA', '1':'78', '2':'25', '3':'2E', '4':'1C', '5':'A6', '6':'B4', '7':'C6', '8':'E8', '9':'DD', 'A':'74', 'B':'1F', 'C':'4B', 'D':'BD', 'E':'8B', 'F':'8A'},
        'D' : {'0':'70', '1':'3E', '2':'B5', '3':'66', '4':'48', '5':'03', '6':'F6', '7':'0E', '8':'61', '9':'35', 'A':'57', 'B':'B9', 'C':'86', 'D':'C1', 'E':'1D', 'F':'9E'},
        'E' : {'0':'E1', '1':'F8', '2':'98', '3':'11', '4':'69', '5':'D9', '6':'8E', '7':'94', '8':'9B', '9':'1E', 'A':'87', 'B':'E9', 'C':'CE', 'D':'55', 'E':'28', 'F':'DF'},
        'F' : {'0':'8C', '1':'A1', '2':'89', '3':'0D', '4':'BF', '5':'E6', '6':'42', '7':'68', '8':'41', '9':'99', 'A':'2D', 'B':'0F', 'C':'B0', 'D':'54', 'E':'BB', 'F':'16'}
        }


sboxinv = {'0' : {'0':'52', '1':'09', '2':'6A', '3':'D5', '4':'30', '5':'36', '6':'A5', '7':'38', '8':'BF', '9':'40', 'A':'A3', 'B':'9E', 'C':'81', 'D':'F3', 'E':'D7', 'F':'FB'},
        '1' : {'0':'7C', '1':'E3', '2':'39', '3':'82', '4':'9B', '5':'2F', '6':'FF', '7':'87', '8':'34', '9':'8E', 'A':'43', 'B':'44', 'C':'C4', 'D':'DE', 'E':'E9', 'F':'CB'},
        '2' : {'0':'54', '1':'7B', '2':'94', '3':'32', '4':'A6', '5':'C2', '6':'23', '7':'3D', '8':'EE', '9':'4C', 'A':'95', 'B':'0B', 'C':'42', 'D':'FA', 'E':'C3', 'F':'4E'},
        '3' : {'0':'08', '1':'2E', '2':'A1', '3':'66', '4':'28', '5':'D9', '6':'24', '7':'B2', '8':'76', '9':'5B', 'A':'A2', 'B':'49', 'C':'6D', 'D':'8B', 'E':'D1', 'F':'25'},
        '4' : {'0':'72', '1':'F8', '2':'F6', '3':'64', '4':'86', '5':'68', '6':'98', '7':'16', '8':'D4', '9':'A4', 'A':'5C', 'B':'CC', 'C':'5D', 'D':'65', 'E':'B6', 'F':'92'},
        '5' : {'0':'6C', '1':'70', '2':'48', '3':'50', '4':'FD', '5':'ED', '6':'B9', '7':'DA', '8':'5E', '9':'15', 'A':'46', 'B':'57', 'C':'A7', 'D':'8D', 'E':'9D', 'F':'84'},
        '6' : {'0':'90', '1':'D8', '2':'AB', '3':'00', '4':'8C', '5':'BC', '6':'D3', '7':'0A', '8':'F7', '9':'E4', 'A':'58', 'B':'05', 'C':'B8', 'D':'B3', 'E':'45', 'F':'06'},
        '7' : {'0':'D0', '1':'2C', '2':'1E', '3':'8F', '4':'CA', '5':'3F', '6':'0F', '7':'02', '8':'C1', '9':'AF', 'A':'BD', 'B':'03', 'C':'01', 'D':'13', 'E':'8A', 'F':'6B'},
        '8' : {'0':'3A', '1':'91', '2':'11', '3':'41', '4':'4F', '5':'67', '6':'DC', '7':'EA', '8':'97', '9':'F2', 'A':'CF', 'B':'CE', 'C':'F0', 'D':'B4', 'E':'E6', 'F':'73'},
        '9' : {'0':'96', '1':'AC', '2':'74', '3':'22', '4':'E7', '5':'AD', '6':'35', '7':'85', '8':'E2', '9':'F9', 'A':'37', 'B':'E8', 'C':'1C', 'D':'75', 'E':'DF', 'F':'6E'},
        'A' : {'0':'47', '1':'F1', '2':'1A', '3':'71', '4':'1D', '5':'29', '6':'C5', '7':'89', '8':'6F', '9':'B7', 'A':'62', 'B':'0E', 'C':'AA', 'D':'18', 'E':'BE', 'F':'1B'},
        'B' : {'0':'FC', '1':'56', '2':'3E', '3':'4B', '4':'C6', '5':'D2', '6':'79', '7':'20', '8':'9A', '9':'DB', 'A':'C0', 'B':'FE', 'C':'78', 'D':'CD', 'E':'5A', 'F':'F4'},
        'C' : {'0':'1F', '1':'DD', '2':'A8', '3':'33', '4':'88', '5':'07', '6':'C7', '7':'31', '8':'B1', '9':'12', 'A':'10', 'B':'59', 'C':'27', 'D':'80', 'E':'EC', 'F':'5F'},
        'D' : {'0':'60', '1':'51', '2':'7F', '3':'A9', '4':'19', '5':'B5', '6':'4A', '7':'0D', '8':'2D', '9':'E5', 'A':'7A', 'B':'9F', 'C':'93', 'D':'C9', 'E':'9C', 'F':'EF'},
        'E' : {'0':'A0', '1':'E0', '2':'3B', '3':'4D', '4':'AE', '5':'2A', '6':'F5', '7':'B0', '8':'C8', '9':'EB', 'A':'BB', 'B':'3C', 'C':'83', 'D':'53', 'E':'99', 'F':'61'},
        'F' : {'0':'17', '1':'2B', '2':'04', '3':'7E', '4':'BA', '5':'77', '6':'D6', '7':'26', '8':'E1', '9':'69', 'A':'14', 'B':'63', 'C':'55', 'D':'21', 'E':'0C', 'F':'7D'}
        }

def substitution(block,mode):
    if mode == 'inv':
        for i in range(len(block)):
            hx = hex(block[i]).lstrip('-0x').zfill(2).upper()
            sub = sboxinv[hx[0]][hx[1]]
            block[i] = int(sub,16)
    else:
        for i in range(len(block)):
            hx = hex(block[i]).lstrip('-0x').zfill(2).upper()
            sub = sbox[hx[0]][hx[1]]
            block[i] = int(sub,16)

def permutation(block,mode):
    bitelist = []
    length = len(block)
    for i in range(length):
        bite = bin(block[i]).lstrip('-0b').zfill(8)
        bitelist.append(str(bite))
    if mode == 'inv':
        for i in range(length):
            pbite = ''
            for j in range(length):
                num = (i+j) % length
                pbite = pbite + str(bitelist[num][j])
            block[i] = int(pbite,2)
    else:
        for i in range(length):
            pbite = ''
            for j in range(length):
                num = (i-j) % length
                pbite = pbite + str(bitelist[num][j])
            block[i] = int(pbite,2)

def bitxorstate(state,key):
    for i in range(len(state)):
        state[i] = state[i] ^ key[i]

def roundkey(key):
    for i in range(len(key)):
        if i%2 == 0:
            key[i] = key[i] ^ key[i+1]
        else:
            hx = hex(key[i]).lstrip('-0x').zfill(2).upper()
            sub = sbox[hx[0]][hx[1]]
            key[i] = int(sub,16)

def createkeys(keylist,origin):
    key = copy.deepcopy(origin)
    keylist.append(copy.deepcopy(key))
    for i in range(5):
        roundkey(key)
        keylist.append(copy.deepcopy(key))

def encryption(state,keys):
    bitxorstate(state,keys[0])
    for i in range(5):
        if i == 4:
            substitution(state,'reg')
            bitxorstate(state,keys[i+1])
        else:
            substitution(state,'reg')
            permutation(state,'reg')
            bitxorstate(state,keys[i+1])

def decryption(state,keys):
    for i in range(5, 0, -1):
        if i == 5:
            bitxorstate(state,keys[i])
            substitution(state,'inv')
        else:
            bitxorstate(state,keys[i])
            permutation(state,'inv')
            substitution(state,'inv')
    bitxorstate(state,keys[0])

def modeECB(tx,key,mode):
    if mode == 'deqt':
        for block in tx:
            decryption(block,key)
    else:
        for block in tx:
            encryption(block,key)

def modeCBC(tx,key,mode):
    iv = [1,2,3,4,5,6,7,8]
    if mode == 'deqt':
        for i in range(len(tx)-1,-1,-1):
            decryption(tx[i],key)
            if i == 0:
                bitxorstate(tx[i],iv)
            else:
                bitxorstate(tx[i],tx[i-1])
    else:
        for i in range(len(tx)):
            if i == 0:
                bitxorstate(tx[i],iv)
            else:
                bitxorstate(tx[i],tx[i-1])
            encryption(tx[i],key)

def modeOFB(tx,key,mode):
    iv = [1,2,3,4,5,6,7,8]
    for i in range(len(tx)):
        encryption(iv,key)
        bitxorstate(tx[i],iv)

def modeCFB(tx,key,mode):
    iv = [1,2,3,4,5,6,7,8]
    if mode == 'deqt':
        for i in range(len(tx)-1,-1,-1):
            if i == 0:
                encryption(iv,key)
                bitxorstate(tx[i],iv)
            else:
                tempc = copy.deepcopy(tx[i-1])
                encryption(tempc,key)
                bitxorstate(tx[i],tempc)
    else:
        for i in range(len(tx)):
            if i == 0:
                encryption(iv,key)
                bitxorstate(tx[i],iv)
            else:
                tempc = copy.deepcopy(tx[i-1])
                encryption(tempc,key)
                bitxorstate(tx[i],tempc)

def modeCTR(tx,key,mode):
    iv = [1,2,3,4,5,6,7,8]
    counter = 0
    for i in range(len(tx)):
        ivcp = copy.deepcopy(iv)
        for j in range(len(ivcp)):
            ivcp[j] = int(ivcp[j])+counter
        encryption(ivcp,key)
        bitxorstate(tx[i],ivcp)
        counter += 1

def asciitodec(string):
    letters = list(string)
    for i in range(len(letters)):
        letters[i] = ord(str(letters[i]))
    return letters

def createblocks(listletters):
    listblocks = []
    length = len(listletters)
    if length % 8 != 0:
        padding = 8 - (length % 8)
    else:
        padding = 0
    block = []
    for i in range(length):
        if (i != 0) and (i % 8 == 0):
            listblocks.append(copy.deepcopy(block))
            block = []
        if i == length-1:
            block.append(listletters[i])
            if padding > 0:
                for j in range(padding):
                    if j == padding-1:
                        block.append(padding)
                        listblocks.append(copy.deepcopy(block))
                    else:
                        block.append(0)
            else:
                listblocks.append(copy.deepcopy(block))
        else:
            block.append(listletters[i])
    return listblocks

def decryptascii(listblocks):
    last = len(listblocks)-1
    lastval = listblocks[last][7]
    string = ''
    if lastval < 8:
        for i in range(6,-1,-1):
            if listblocks[last][i] != 0:
                lastletter = i
                break
    else:
        lastletter = 7

    for i in range(len(listblocks)):
        if i == len(listblocks)-1:
            for j in range(lastletter+1):
                string = string+chr(listblocks[i][j])
        else:
            for j in range(8):
                string = string+chr(listblocks[i][j])
    return string

def newfile(mode,ptx):
    filename = raw_input('Please enter a file name: ')
    fname = filename+'.txt'
    f = open(fname, 'w')
    if mode == 'enqt':
        mode = raw_input('Choose your choice of output: dec, hex or bin \n')
    else:
        mode = 'text'

    if mode == 'hex':
        for i in range(len(ptx)):
            for j in range(8):
                f.write(hex(ptx[i][j]))
                f.write(';')
    elif mode == 'bin':
        for i in range(len(ptx)):
            for j in range(8):
                f.write(bin(ptx[i][j]))
                f.write(';')
    elif mode == 'dec':
        for i in range(len(ptx)):
            for j in range(8):
                f.write(str(ptx[i][j]))
                f.write(';')
    elif mode == 'text':
        output = decryptascii(ptx)
        f.write(output)

    f.close()

def readfile(mode):
    filename = raw_input('Please enter a file name: ')
    fname = filename+'.txt'
    f = open(fname, 'r')
    data = []
    formatting = f.read(2)
    f.seek(0,0)
    if formatting == '0x':
        for line in f:
            temp = line.split(';')
            del temp[-1]
            for i in range(len(temp)):
                temp[i] = int(temp[i],0)
            data.extend(temp)
    elif formatting == '0b':
        for line in f:
            temp = line.split(';')
            del temp[-1]
            for i in range(len(temp)):
                temp[i] = int(temp[i],0)
            data.extend(temp)
    elif mode == 'deqt':
        for line in f:
            temp = line.split(';')
            del temp[-1]
            for i in range(len(temp)):
                temp[i] = int(temp[i],0)
            data.extend(temp)
    else:
        for line in f:
            temp = asciitodec(line)
            data.extend(temp)

    f.close()
    return data

def printblocks(listblocks):
    for i in range(len(listblocks)):
        print listblocks[i]

def iotext(mode,listblock):
    if mode == 'enqt':
        text = 'cipher'
    else:
        text = 'plain'
    listblocks = copy.deepcopy(listblock)
    sel1 = input('Print '+text+'text to screen? Yes = 1, No = 0 \n')
    if sel1 == 1:
        if text == 'cipher':
            sel3 = raw_input('Choose your choice of output: dec, hex, bin\n')
            if sel3 == 'hex':
                for list in listblocks:
                    print ([hex(n) for n in list])
            elif sel3 == 'bin':
                for list in listblocks:
                    print ([bin(n) for n in list])
            elif sel3 == 'dec':
                printblocks(listblocks)
        else:
            output = decryptascii(listblocks)
            print output

    sel2 = input('Store '+text+'text in .txt file? Yes = 1, No = 0 \n')
    if sel2 == 1:
        newfile(mode,listblocks)
        print 'File created, please check directory\n'

def wrap(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def modeofop(crypt,listblocks,keyslist):
    print 'Choose mode of encryptions:'
    mode = input('1.ECB  2.CBC  3.OFB  4.CFB  5.CTR \n')
    if mode == 1:
        modeECB(listblocks,keyslist,crypt)
        iotext(crypt,listblocks)
    elif mode == 2:
        modeCBC(listblocks, keyslist, crypt)
        iotext(crypt,listblocks)
    elif mode == 3:
        modeOFB(listblocks, keyslist, crypt)
        iotext(crypt,listblocks)
    elif mode == 4:
        modeCFB(listblocks, keyslist, crypt)
        iotext(crypt,listblocks)
    elif mode == 5:
        modeCTR(listblocks, keyslist, crypt)
        iotext(crypt,listblocks)


print 'Welcome to the encrpytion/decryption program.'
print 'Please choose the following operations'
print '1. Enter a message to encrypt'
print '2. Read from a file to encrypt'
print '3. Read from a file to decrypt'
print '4. Test performance of encrypt and decrypt'
print '5. Test mode'
print '7. Termination'

binary = [0b110000,0b110001,0b110010,0b110011,0b110100,0b110101,0b110101,0b110110]
origin = [105,106,107,108,109,110,111,112]
keys = copy.deepcopy(origin)
keyslist = []
createkeys(keyslist,keys)

while 1:
    x = input("Select: ")
    if x == 1:
        message = raw_input('Please enter an message: ')
        listletter = asciitodec(message)
        listblocks = createblocks(listletter)
        sel0 = input('Save plaintext in .txt file? Yes = 1, No = 0 \n')
        if sel0 == 1:
            newfile('deqt',listblocks)
            print 'Plaintext file created\n'

        modeofop('enqt',listblocks,keyslist)
        sel3 = input('Do you want to run the decryption? Yes = 1, No = 0 \n')
        if sel3 == 1:
            modeofop('deqt',listblocks,keyslist)

        print 'Return to menu'
        listletter = []

    elif x == 2:
        filedata = readfile('enqt')
        listblocks = createblocks(filedata)
        modeofop('enqt',listblocks,keyslist)
        sel3 = input('Do you want to run the decryption? Yes = 1, No = 0 \n')
        if sel3 == 1:
            modeofop('deqt',listblocks,keyslist)
        print 'Return to menu'
        filedata = ''

    elif x == 3:
        filedata = readfile('deqt')
        listblocks = createblocks(filedata)
        modeofop('deqt',listblocks,keyslist)
        print 'Return to menu'

    elif x == 4:
        use = input('Use default block or insert a file/meesage for testing? \n 1. Insert file  2. Insert message  3. Default\n')
        if use == 1:
            filedata = readfile('enqt')
            listblocks = createblocks(filedata)
        elif use == 2:
            message = raw_input('Please enter an message: ')
            listletter = asciitodec(message)
            listblocks = createblocks(listletter)
        else:
            listblocks = []
            listblocks.append(binary)

        blocknum = len(listblocks)
        test = input('List of testing available: \n 1.ECB Encrypt+Decrypt  2.CBC Encrypt+Decrypt  3.OFB Encrypt+Decrypt  4.CFB Encrypt+Decrypt  5.CTR Encrypt+Decrypt \n')
        if test == 1:
            mode = modeECB
        elif test == 2:
            mode = modeCBC
        elif test == 3:
            mode = modeOFB
        elif test == 4:
            mode = modeCFB
        elif test == 5:
            mode = modeCTR
        wrapped1 = wrap(mode,listblocks,keyslist,'enqt')
        wrapped2 = wrap(mode,listblocks,keyslist,'deqt')
        a = timeit.timeit(wrapped1, number=1)
        b = timeit.timeit(wrapped2, number=1)

        print "Number of execution: {0:d}".format(1)
        print "Number of blocks: {0:d}".format(blocknum)
        print "Number of bytes: {0:d}".format(blocknum*8)
        print "Number of bits: {0:d}".format(blocknum*8*8)
        print "Encryption: {0:.6f} seconds".format(a)
        print "Decryption: {0:.6f} seconds".format(b)
        print "Encryption speed per block: {0:.6f} seconds".format(a/float(blocknum))
        print "Decryption speed per block: {0:.6f} seconds".format(b/float(blocknum))

        print "Return to menu"

    elif x == 5:
        use = input('Use default block or insert a file/message for testing? \n 1. Insert file  2. Insert message  3. Default\n')
        if use == 1:
            filedata = readfile('enqt')
            listblocks = createblocks(filedata)
        elif use == 2:
            message = raw_input('Please enter an message: ')
            listletter = asciitodec(message)
            listblocks = createblocks(listletter)
        else:
            listblocks = []
            listblocks.append(binary)

        print 'Choose mode of encryptions:'
        mode = input('1.ECB  2.CBC  3.OFB  4.CFB  5.CTR \n')
        if mode == 1:
            crypt = modeECB
        elif mode == 2:
            crypt = modeCBC
        elif mode == 3:
            crypt = modeOFB
        elif mode == 4:
            crypt = modeCFB
        elif mode == 5:
            crypt = modeCTR

        print 'original'
        printblocks(listblocks)
        wrapped1 = wrap(crypt,listblocks,keyslist,'enqt')
        wrapped1()
        print 'Encrypt:'
        printblocks(listblocks)
        wrapped2 = wrap(crypt,listblocks,keyslist,'deqt')
        wrapped2()
        print 'Decrypt: '
        printblocks(listblocks)
        print 'Plaintext: '
        output = decryptascii(listblocks)
        print output
        print 'Return to menu'

    elif x == 7:
        print 'Terminating Program'
        sys.exit()
    else:
        print 'Error selection, try again'

    listblocks = []
