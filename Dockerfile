FROM ubuntu:focal
COPY . /app

# Install dependencies
RUN apt-get update -qq && \
        apt-get install -yq --no-install-suggests --no-install-recommends \
        apt-transport-https ca-certificates \
        build-essential \
        file \
        gcc \
        make \
        git \
        autotools-dev automake autoconf libtool libtext-diff-perl pkg-config
RUN update-ca-certificates

# Install implementations of Annex K functions used by the MS C/C++ compiler
# that are not available in GCC
RUN git clone https://github.com/rurban/safeclib.git
WORKDIR safeclib
RUN git reset --hard 0234bec46da4863f849f100c2f5336412ab2f69b

RUN ./build-aux/autogen.sh && \
        ./configure && \
        make install
ENV LD_LIBRARY_PATH=/usr/local/lib

# Copy needed header files
RUN cp /usr/local/include/libsafec/* /usr/include/
RUN cp /usr/include/x86_64-linux-gnu/sys/io.h /usr/include

# Compile
WORKDIR /app/SatLightPollution
RUN g++ -std=c++17 -o /usr/bin/slp -I . *.cpp -L /usr/local/lib -lsafec-3.6.0 -lstdc++fs

CMD ["/bin/bash"]

