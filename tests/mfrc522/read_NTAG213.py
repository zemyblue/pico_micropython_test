from decode_TLV import parseTLVBlocks
from decode_ndef import decode_ndef
from mfrc522 import MFRC522
import utime

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring

def byteToString(block):
    for value in block:
        if (value > 0x20) and (value < 0x7f):
            print(chr(value),end="")
        else:
            print('.',end="")


reader = MFRC522(spi_id=0, sck=6, miso=4, mosi=7, cs=5, rst=22)

print("")
print("Please card before reader to write address 0x08")
print("")

PreviousCard = [0]

try:
    while True:
        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if uid == PreviousCard:
                continue

            if stat == reader.OK:
                print("Tag Type: %d" % tag_type)
                print("Card detected {}  uid={}".format(hex(int.from_bytes(bytes(uid),"little",False)).upper(),reader.tohexstring(uid)))

                # check If Mifare1K or Mifare ultralight
                stat, staticBlock = reader.read(0)
                if stat == reader.OK:
                    ccs = staticBlock[-4:]
                    # get NFC data memory size
                    numBlock = ccs[2] / 2
                    print("ccs: %s, numBlock:%d" % (reader.tohexstring(ccs), numBlock))

                    # load data blocks
                    datas = []
                    for i in range(1, numBlock):
                        stat, dataBlock = reader.read(i * 4)
                        if stat == reader.OK:
                            datas += dataBlock
                        else:
                            print("Failed to read data block[%d]" % i)
                            break
                    if len(datas) < (numBlock - 1) * 8:
                        print("Failed to read all datas.")
                        break

                    # parse TLV block
                    nfcBlocks = parseTLVBlocks(datas)
                    if nfcBlocks != None:
                        for type, value in nfcBlocks:
                            if type == 0x03:    # if NDEF
                                ndefValue = decode_ndef(value)
                                if ndefValue != None:
                                    print("NDEF value: %s" % ndefValue)
                                else:
                                    print(ndefValue)
                PreviousCard = uid
            else:
                PreviousCard = [0]
            reader.stop_crypto1()
        else:
            PreviousCard  = [0]
        utime.sleep_ms(50)
except KeyboardInterrupt:
    print("Bye")
