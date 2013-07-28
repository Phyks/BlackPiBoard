all : main

main : main.c
	gcc -o main main.c `sdl-config --cflags --libs`
