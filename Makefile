CC = g++
CFLAGS = -Wall -g

init:
	@mkdir -p bin input
	@for name in {A..E}; do cp ../default $$name.cpp; touch input/$$name.in; done;

wipe:
	@rm *.cpp
	@rm -r bin input

%: %.cpp
	@$(CC) $(CFLAGS) -o bin/$@.o $<
	@cat input/$@.in | ./bin/$@.o