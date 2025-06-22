# Useful docker images

## luadec

To decode lua byte-code files or at least disassemble `config.lua` and `crypto.lua`.

```sh
# https://github.com/RE-Solver/luadec-openwrt-tplink
docker build -f docker/luadec.Dockerfile -t luadec .
# https://github.com/zhangjiequan/luadec
docker build -f docker/luadec2.Dockerfile -t luadec2 .
# 
docker run -it --rm -v $PWD:/data luadec
```