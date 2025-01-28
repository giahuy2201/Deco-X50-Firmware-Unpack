import sys, os
import config

if len(sys.argv) < 2:
    print(f'Usage: python {sys.argv[0]} <corrected dump>')
    sys.exit(-1)
infname = sys.argv[1]
inf = open(infname, "rb")

outf_main = open("{}.main".format(infname), "wb")
outf_oob = open("{}.oob".format(infname), "wb")


def write(data, oob):
    outf_main.write(data)
    outf_oob.write(oob)


num_codewords = int(os.stat(infname).st_size / config.CW_SIZE)
i = 0
while i < num_codewords:
    main1: bytes = inf.read(config.MAIN1_SIZE)
    bbm: bytes = inf.read(config.BBM_SIZE)
    main2: bytes = inf.read(config.MAIN2_SIZE)
    ecc: bytes = inf.read(config.ECC_SIZE)
    padding: bytes = inf.read(config.PADDING_SIZE)

    data: bytes = main1 + main2
    oob: bytes = bbm + ecc + padding

    if (i + 1) % 4 == 0:
        data = data[: config.LAST_CW_SIZE]

    write(data, oob)
    i += 1

inf.close()
outf_main.close()
outf_oob.close()
