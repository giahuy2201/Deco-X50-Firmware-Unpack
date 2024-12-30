# Deco X50 Firmware Unpack
## About
TODO
## Hardware Specifications
TODO
### NAND Layout and ECC
TODO
## Useful Commands
Install dependencies
```
poetry install
```
### Correct ECC errors
```
poetry run python correct-errors.py flashdump.bin
```
### Strip out non-data (Out-of-Band) parts
```
poetry run python remove-oob.py flashdump.bin.corrected
```
### Split the binary file
```
poetry run python carve-mtds.py flashdump.bin.corrected.main
```
### Unpack UBI partitions