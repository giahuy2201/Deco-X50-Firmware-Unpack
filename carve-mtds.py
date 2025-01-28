import sys, os, re, subprocess
import config

if len(sys.argv) < 3:
    print(f'Usage: python {sys.argv[0]} <corrected dump> <address map>')
    sys.exit(-1)
mapfname = sys.argv[2]  # mtd partition mapping obtained from boot log via UART
binfname = sys.argv[1]  # flashdump.bin.corrected.main

# ex.0x000000000000-0x000000080000 : "SBL1"
ADDRESSES_RE = r"0x[0-9a-fA-F]*"  # extract start and end address
NAME_RE = r':\s*"([^"]+)"'  # mtd name

# echo mtd partition is stored under parts/mtd<number>.<name>.bin
folder_name = "parts"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

ps = []  # dd process list
i = 0
with open(mapfname) as mapf:
    for line in mapf:
        region = re.findall(ADDRESSES_RE, line)
        name = re.findall(NAME_RE, line)
        if len(region) == 2 and len(name) == 1:  # only relevant lines
            start = int(region[0][2:], 16)
            count = int(region[1][2:], 16) - start
            mtd = name[0]

            cmd = [
                "dd",
                "if=%s" % binfname,
                "of=parts/mtd%d.%s.bin" % (i, mtd),
                "bs=1",
                "skip=%d" % start,
                "count=%d" % count,
            ]
            process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
            ps.append((mtd, process))
            print(cmd)
            i += 1

for i, process in ps:
    stdout, stderr = process.communicate()  # Wait for the process to finish
    if process.returncode == 0:
        print(f"Process {i} succeeded")
    else:
        print(
            f"Process {i} failed with return code {process.returncode}: {stderr.decode().strip()}"
        )
