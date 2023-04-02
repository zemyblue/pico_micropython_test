
def tohexstring(v):
    s="["
    for i, value in enumerate(v):
        if i != 0:
            s = s+ ", "
        s=s+ "0x{:02X}".format(value)
    s= s+ "]"
    return s

# parse TLV blocks from NFC datas
def parseTLVBlocks(datas):
    print("datas len:%d" % len(datas))
    blocks = []
    idx = 0
    while idx < len(datas):
        if datas[idx] in [0x01, 0x02, 0x03, 0xFD]:
            blockType = datas[idx]
            bLen = int(datas[idx + 1])
            blockValue = datas[idx + 2 : idx + 2 + bLen]
            print("blockType:0x%02X, bLen:%d, blockValue:%s" % (blockType, bLen, tohexstring(blockValue)))
            blocks.append((blockType, blockValue))
            idx += bLen + 2
            continue
        elif datas[idx] == 0xFE:
            print("file end.")
            break
        else:
            print("wrong TLV block type")
            return None
    return blocks


if __name__ == '__main__':
    hexstr = '0103A00C34030FD1010B5402656E7A656D79626C7565FE'
    octets = bytearray.fromhex(hexstr)
    octets = [0x01, 0x03, 0xA0, 0x0C, 0x34, 0x03, 0x0F, 0xD1, 0x01, 0x0B, 0x54, 0x02, 0x65, 0x6E, 0x7A, 0x65, 0x6D, 0x79, 0x62, 0x6C, 0x75, 0x65, 0xFE]
    print(octets)
    for block in parseTLVBlocks(octets):
        print(block)
