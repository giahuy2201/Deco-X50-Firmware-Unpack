import sys, os, bchlib
import config

infname = sys.argv.pop()
inf = open(infname, "rb")

outf = open("{}.corrected".format(infname), "wb")

bch = bchlib.BCH(config.ECC_MODE, prim_poly=config.BCH_POLY)


def write(data, bbm, ecc):
    outf.write(data[: config.MAIN1_SIZE])
    outf.write(bbm)
    outf.write(data[config.MAIN1_SIZE :])
    if len(data) == config.LAST_CW_SIZE:
        outf.write(
            b"\xFF" * (config.MAIN1_SIZE + config.MAIN2_SIZE - config.LAST_CW_SIZE)
        )
    outf.write(ecc)
    outf.write(b"\xFF" * config.PADDING_SIZE)


num_codewords = int(os.stat(infname).st_size / config.CW_SIZE)
num_errors = 0
i = 0
while i < num_codewords:
    main1: bytes = inf.read(config.MAIN1_SIZE)
    bbm: bytes = inf.read(config.BBM_SIZE)
    main2: bytes = inf.read(config.MAIN2_SIZE)
    data: bytes = main1 + main2

    ecc: bytes = inf.read(config.ECC_SIZE)
    padding: bytes = inf.read(config.PADDING_SIZE)

    if ecc != b"\xFF" * config.ECC_SIZE:  # no ecc code means no data
        nerrs = bch.decode(data, ecc)
        if nerrs > 0:
            # print("%d: %d" % (i, nerrs))
            num_errors += 1

            corrected_data = bytearray(data)
            corrected_ecc = bytearray(ecc)
            bch.correct(corrected_data, corrected_ecc)

            if (
                i + 1
            ) % 4 == 0:  # cut the last 16 bytes at the end of each page to avoid misalignments
                data = bytes(corrected_data)[:config.LAST_CW_SIZE]
            else:
                data = bytes(corrected_data)
        else:
            if (i + 1) % 4 == 0:
                data = data[:config.LAST_CW_SIZE]
    else:
        if (i + 1) % 4 == 0:
            data = data[:config.LAST_CW_SIZE]

    write(data, bbm, ecc)
    i += 1

inf.close()
outf.close()

print("Corrected %d errors over %d codewords" % (num_errors, num_codewords))
