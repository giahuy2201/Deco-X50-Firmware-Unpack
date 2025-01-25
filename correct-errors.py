import sys, os, bchlib
import config

if len(sys.argv) < 2:
    print(f'Usage: python {sys.argv[0]} <uncorrected dump>')
    sys.exit(-1)
infname = sys.argv[1]
inf = open(infname, "rb")

outf = open("{}.corrected".format(infname), "wb")

bch = bchlib.BCH(config.ECC_MODE, prim_poly=config.BCH_POLY)


def write(data, bbm, ecc):
    outf.write(data[: config.MAIN1_SIZE])
    outf.write(bbm)
    outf.write(data[config.MAIN1_SIZE :])
    outf.write(ecc)
    outf.write(b"\xFF" * config.PADDING_SIZE)


num_codewords = int(os.stat(infname).st_size / config.CW_SIZE)
total_errors = 0
i = 0
while i < num_codewords:
    main1: bytes = inf.read(config.MAIN1_SIZE)
    bbm: bytes = inf.read(config.BBM_SIZE)
    main2: bytes = inf.read(config.MAIN2_SIZE)
    ecc: bytes = inf.read(config.ECC_SIZE)
    padding: bytes = inf.read(config.PADDING_SIZE)

    data: bytes = main1 + main2

    if ecc != b"\xFF" * config.ECC_SIZE:  # no ecc code means no data
        nerrs = bch.decode(data, ecc)
        if nerrs > 0:
            # print("%d: %d" % (i, nerrs))

            corrected_data = bytearray(data)
            corrected_ecc = bytearray(ecc)
            bch.correct(corrected_data, corrected_ecc)

            data = bytes(corrected_data)
            total_errors += 1

    write(data, bbm, ecc)
    i += 1

inf.close()
outf.close()

print("Corrected %d errors over %d codewords" % (total_errors, num_codewords))
