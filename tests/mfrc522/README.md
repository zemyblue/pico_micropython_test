# MFRC522

This is NTAG213 test in raspberry pi pico with MicroyPython.
Many other sample code about MFRC522 are not suitable for NTAG213. Because NTAG213 doesn't need Authentication.
So I analyize the spec and I implement that can read only text message in NTAG213 NFC.

Specialy, NTAG213 NFC is composed of `NFC Forum Type 2` and data can be read or written according to the NDEF standard.

I use danjperron's [mfrc522.py](https://github.com/danjperron/micropython-mfrc522) library.

## NTAG213 Spec
* total memory: 180 bytes
* user Read/Write area: 144 bytes
* max url charactors: 136

### references
* [NXP NTAG213_215_216](https://www.nxp.com/products/rfid-nfc/nfc-hf/ntag-for-tags-labels/ntag-213-215-216-nfc-forum-type-2-tag-compliant-ic-with-144-504-888-bytes-user-memory:NTAG213_215_216)


## NFC Forum Type 2
First 16 bytes can't rewrite and manifactory area.
The data area is written TLV format and the message that I want to read is composed of NDEF format.

### reference: 
* https://www.amebaiot.com.cn/en/nfc-intro/
* https://developer.nordicsemi.com/nRF_Connect_SDK/doc/1.3.0/nrfxlib/nfc/doc/type_2_tag.html#static-lock-bytes

## NDEF

### references
* https://ndeflib.readthedocs.io/en/latest/ndef.html
* https://stackoverflow.com/questions/35363563/defining-a-ndef-message
* https://github.com/rafaelurben/circuitpy-nfc/blob/main/documentation/NDEF.pdf
* https://github.com/nfcpy/ndeflib
* https://sunflaur.tistory.com/301
* https://smartits.tistory.com/206
* https://velog.io/@hooray/NFC-NDEF-분석


## Other references
* https://github.com/miguelbalboa/rfid/blob/master/src/MFRC522Extended.cpp
* https://github.com/miguelbalboa/rfid
* https://github.com/vtt-info/MicroPython_MFRC522