#include <stdio.h>
#include <stdlib.h>
#include <SDL.h>

#define WIDTH_CONTROL 100

#ifndef min
	#define min(a, b) ((a < b) ? a : b)
#endif

void setPixel(SDL_Surface *affichage, int x, int y, Uint16 coul)
{
	*((Uint16**)(affichage->pixels) + x + y * affichage->w) = coul;
}

void echangerEntiers(int* x, int* y)
{
	int t = *x;
	*x = *y;
	*y = t;
}
 
void DrawLine(SDL_Surface *affichage, int x1, int y1, int x2, int y2, Uint32 coul) //Draw line using Bresenham algorithm
{
	int d, dx, dy, aincr, bincr, xincr, yincr, x, y;
	
	if(x1 == x2 || y1 == y2) //If horizontal or vertical, use the SDL library optimized function
	{
		SDL_Rect r;
		
		r.x = min(x1, x2);
		r.y = min(y1, y2);
		r.w = (x1 == x2) ? 1 : abs(x1 - x2);
		r.h = (y1 == y2) ? 1 : abs(y1 - y2);
		
		SDL_FillRect(affichage, &r, coul);
	}
	else if (abs(x2 - x1) < abs(y2 - y1)) //Go through vertical axis
	{
		if (y1 > y2)
		{
			echangerEntiers(&x1, &x2);
			echangerEntiers(&y1, &y2);
		}
		
		xincr = x2 > x1 ? 1 : -1;
		dy = y2 - y1;
		dx = abs(x2 - x1);
		d = 2 * dx - dy;
		aincr = 2 * (dx - dy);
		bincr = 2 * dx;
		x = x1;
		y = y1;

		setPixel(affichage, x, y, coul);

		for (y = y1+1; y <= y2; ++y) 
		{
			if (d >= 0) 
			{
				x += xincr;
				d += aincr;
			}
			else
				d += bincr;

			setPixel(affichage, x, y, coul);
		}
	} 
	else //Go through horizontal axis
	{

		if (x1 > x2) 
		{
			echangerEntiers(&x1, &x2);
			echangerEntiers(&y1, &y2);
		}

		yincr = y2 > y1 ? 1 : -1;
		dx = x2 - x1;
		dy = abs(y2 - y1);
		d = 2 * dy - dx;
		aincr = 2 * (dy - dx);
		bincr = 2 * dy;
		x = x1;
		y = y1;

		setPixel(affichage, x, y, coul);

		for (x = x1+1; x <= x2; ++x) 
		{
			if (d >= 0) 
			{
				y+= yincr;
				d += aincr;
			} 
			else
				d += bincr;
				setPixel(affichage, x, y, coul);
		}
	}
}


int main(int argc, char *argv[])
{
	int continuer = 1;
	int x_old = -1, y_old = -1;
	int left = 0;
	SDL_Event event;
	SDL_Surface *ecran = NULL, *controles = NULL;
	
	if(-1 == SDL_Init(SDL_INIT_VIDEO))
	{
		fprintf(stderr, "Erreur de chargement de la SDL : %s\n", SDL_GetError());
		exit(EXIT_FAILURE);
	}
	
	const SDL_VideoInfo* video_info = SDL_GetVideoInfo();
	int width = video_info->current_w;
	int height = video_info->current_h;
	int bpp = 16; //video_info ->vfmt->BitsPerPixel;

	SDL_Rect position_controles = {width - WIDTH_CONTROL, 0};

	ecran = SDL_SetVideoMode(width, height, bpp, SDL_HWSURFACE | SDL_FULLSCREEN); //Raspi has only a 16 bpp framebuffer
	controles = SDL_CreateRGBSurface(SDL_HWSURFACE, WIDTH_CONTROL, height, bpp, 0, 0, 0, 0);

	if(NULL == ecran || NULL == controles || NULL == ecran)
	{
		fprintf(stderr, "Erreur d'ouverture de la SDL : %s\n", SDL_GetError());
		exit(EXIT_FAILURE);
	}

	SDL_FillRect(ecran, NULL, SDL_MapRGB(ecran->format, 255, 255, 255));
	SDL_FillRect(controles, NULL, SDL_MapRGB(controles->format, 100, 100, 100));
	SDL_BlitSurface(controles, NULL, ecran, &position_controles);

	SDL_Flip(ecran);

	while(continuer)
	{
		SDL_WaitEvent(&event);

		switch(event.type)
		{
			case SDL_MOUSEBUTTONDOWN:
				if(event.button.x < width - WIDTH_CONTROL)
				{
					if(SDL_BUTTON_LEFT == event.button.button)
					{
						left = 1;
						x_old = event.button.x;
						y_old = event.button.y;
					}
					else if(SDL_BUTTON_RIGHT == event.button.button)
					{
						left = 0;
						x_old = event.button.x;
						y_old = event.button.y;
					}
				}
				break;

			case SDL_MOUSEMOTION:
				if(event.motion.x < width - WIDTH_CONTROL)
				{
					if(x_old > 0 && y_old > 0)
					{
						if(left)
							DrawLine(ecran, x_old, y_old, event.motion.x, event.motion.y, SDL_MapRGB(ecran->format, 0, 0, 0));
						else
							DrawLine(ecran, x_old, y_old, event.motion.x, event.motion.y, SDL_MapRGB(ecran->format, 255, 255, 255));

						SDL_Flip(ecran);
						x_old = event.motion.x;
						y_old = event.motion.y;
					}
				}
				else if(x_old > 0 && y_old > 0)
				{
					x_old = width - WIDTH_CONTROL;
					y_old = event.motion.y;;
				}
				break;

			case SDL_MOUSEBUTTONUP:
				if(SDL_BUTTON_LEFT == event.button.button || SDL_BUTTON_RIGHT == event.button.button)
				{
					x_old = -1;
					y_old = -1;
				}
				break;

			case SDL_KEYDOWN:
				continuer = 0;
				break;

			case SDL_QUIT:
				continuer = 0;
				break;
		}
	}
	
	SDL_FreeSurface(controles);
	SDL_Quit();
	return EXIT_SUCCESS;
}
