
# decode NDEF 
# warning: This function can parse only Text.
def decode_ndef(datas):
    print("----- start decode_ndef -----")
    print("datas len:%d" % len(datas))
    records = [] # [{record type: record value}]
    idx = 0
    while idx < len(datas):
        m = datas[idx]
        # check SR (payload length bytes if 1 => 1byte, 0 => 4byte)
        # if payload length is short(1byte), True
        isSR, SRLen = (True, 1) if (m & 0x10) > 0 else (False, 4)
        isID, ILLen = (False, 0) if (m & 0x08) == 0 else (True, 1)  # if id exist, True
        print("m:[0x%02X] SRLen:%d, ILLen:%d  - idx:%d" % (m, SRLen, ILLen, idx))
        idx += 1

        # load length
        print("idx+1:%x" % datas[idx])
        typeLen = int(datas[idx])
        idx += 1
        payloadLen = int(datas[idx]) if isSR else int.from_bytes(datas[idx: idx + SRLen], "big")
        idx += SRLen
        idLen = 0 if not isID else int(datas[idx])
        idx += ILLen
        print("typeLen:%d, payloadLen:%d, idLen:%d" % (typeLen, payloadLen, idLen))

        payloadType = str(bytearray(datas[idx : idx + typeLen]), 'utf-8')
        idx += typeLen
        print("payloadType:%s" % payloadType)
        if payloadType == 'T':
            th = datas[idx]
            utfType = 'utf-8' if (th & 0x80) == 0 else 'utf-16'
            langLen = int(th & 0x3f)
            print("th:0x%02x, langLen:%d" % (th, langLen))

            lang = str(bytearray(datas[idx + 1 : idx + 1 + langLen]), utfType)
            payload = str(bytearray(datas[idx + 1 + langLen : idx + payloadLen]), utfType)
            print("utfType:%s, lang:%s, payload:%s" % (utfType, lang, payload))
            records.append({payloadType: payload})
        else:
            print("don't support type(%s)" % payloadType)

        idx += payloadLen

        print("---- end parse (idx:%d) --- " % idx)

    return records


if __name__ == '__main__':
    # datas = [0xD1, 0x01, 0x0B, 0x54, 0x02, 0x65, 0x6E, 0x7A, 0x65, 0x6D, 0x79, 0x62, 0x6C, 0x75, 0x65]
    datas = [0x91, 0x01, 0x0B, 0x54, 0x02, 0x65, 0x6E, 0x7A, 0x65, 0x6D, 0x79, 0x62, 0x6C, 0x75, 0x65, 0x51, 0x01, 0x15, 0x54, 0x02, 0x65, 0x6E, 0xEB, 0x91, 0x90, 0xEB, 0xB2, 0x88, 0xEC, 0xA7, 0xB8, 0xEC, 0x9E, 0x85, 0xEB, 0x8B, 0x88, 0xEB, 0x8B, 0xA4]
    for i, d in enumerate(datas):
        print("%d:0x%02x, " % (i, d), end="")
    print()

    for record in decode_ndef(datas):
        print(record)
