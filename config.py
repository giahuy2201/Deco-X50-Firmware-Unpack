# F50D1G41LB: 2048B main + 64B oob page
PAGE_SIZE = 2048
OOB_SIZE = 64
CW_NUM = 4  # numbers of codewords per page
MAIN1_SIZE = 464  # main data first segment
BBM_SIZE = 1  # bad block marker
MAIN2_SIZE = 52  # main data second segment
ECC_SIZE = 7  # ecc code
PADDING_SIZE = 4

ECC_MODE = 4  # 4-bit ECC, BCH4
BCH_POLY = 8219

# calculated values
CW_SIZE = (PAGE_SIZE + OOB_SIZE) / CW_NUM # = MAIN1_SIZE + BBM_SIZE + MAIN2_SIZE + ECC_SIZE + PADDING_SIZE
LAST_CW_SIZE = PAGE_SIZE - (CW_NUM - 1) * (MAIN1_SIZE + MAIN2_SIZE) # last codeword of each page only has size of 500 to compensate for all before it being oversized