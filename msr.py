import sys
import usb.core
import usb.util


# USB characteristics
VENDOR_ID = 0x0801
PRODUCT_ID = 0x0003

# Order format
oRESET = '\x1b\x61'
oSELECT_BPI = '\x1b\x62'
oERASE_CARD = '\x1b\x63'
oGET_HICO_LOCO_STATUS = '\x1b\x64'
oCOM_TEST = '\x1b\x65'
oLEADING_ZERO_CHECK = '\x1b\x6c'
oREAD_RAW = '\x1b\x6d'
oWRITE_RAW = '\x1b\x6e'
oSET_BPC = '\x1b\x6f'
oREAD_ISO = '\x1b\x72'
oGET_DEVICE_MODEL = '\x1b\x74'
oGET_FIRMWARE_VERSION = '\x1b\x76'
oWRITE_ISO = '\x1b\x77'
oSET_HICO = '\x1b\x78'
oSET_LOCO = '\x1b\x79'
oLEADING_ZERO_SET = '\x1b\x7a'
oALL_LED_OFF = '\x1b\x81'
oALL_LED_ON = '\x1b\x82'
oGREEN_LED = '\x1b\x83'
oORANGE_LED = '\x1b\x84'
oRED_LED = '\x1b\x85'
oSENSOR_TEST = '\x1b\x86'
oRAM_TEST = '\x1b\x87'


dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    sys.exit("Could not find MagTek USB HID Swipe Reader.")

if dev.is_kernel_driver_active(0):
    try:
        dev.detach_kernel_driver(0)
        print "kernel driver detached"
    except usb.core.USBError as e:
        sys.exit("Could not detach kernel driver: %s" % str(e))
else:
    print "no kernel driver attached"

try:
    usb.util.claim_interface(dev, 0)
    print "claimed device"
except Exception as e:
    print(e)


msg = '\xc2%s' % oREAD_RAW
assert dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)


resp = dev.read(0x81, 1024, 5000)
print(''.join([hex(x)for x in resp]))