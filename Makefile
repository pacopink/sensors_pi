
dht11_reader:dht11_reader.c
	gcc -Wall -O9 -o $@ $^ -lwiringPi

all:dht11_reader

clean:
	rm -f dht11_reader
