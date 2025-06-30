//
// Created by Chord on 25-6-13.
//

#ifndef OLED096_H
#define OLED096_H
#include <cstdint>


class Oled096 {
public:
	Oled096();
	void init();

private:
	void displaypoint();
	void testDisplay();
	void displayChar(uint8_t x, uint8_t y, char c);
	// void

};



#endif //OLED096_H
