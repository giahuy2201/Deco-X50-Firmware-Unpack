FROM rockylinux:9.3

RUN dnf install -y --nogpgcheck git gcc gcc-c++ make automake autoconf kernel-devel ncurses-devel readline-devel
RUN git clone https://github.com/RE-Solver/luadec-openwrt-tplink

WORKDIR /luadec-openwrt-tplink
RUN cd lua-5.1 && make linux && make install
RUN cd luadec && LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/ make LUAVER=5.1 && cp ./luadec /usr/bin
RUN dnf remove -y git gcc gcc-c++ make automake autoconf kernel-devel ncurses-devel readline-devel lua lua-devel

WORKDIR /luadec-openwrt-tplink/luadec

CMD ["bash"]