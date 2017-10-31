README.md for PythonCoder

Name: Josh Manulat

Description: A program that will either decode an image with a message hiding init or encode a desired message into an existing image. Each mode is denoted "-d"for decoding or "-e" for encoding. Uses the bitstring module for the use of BitArray and pillow module for image manipulation.

Instructions:
	1) Make sure Python3 is equipped with the bitstring module
		1.a) If not, use "pip3 install bitstring"
	2) Make sure Python3 is equipped with the pillow module
		2.a) Make use of "pip3 install pillow"
	3) Navigate to the appropiate directory in terminal where program is contained
		3.a) use "cd"
	4) run with instructions "python3 coder.py [flag] [arg] [arg] [arg]"
		4.a) if decoding, replace [flag] with "-d"
			4.a.i) the next [arg] will be used as the image file you wish to decode
			4.a.ii) the next arguments will not be used in this mode
		4.b) if encoding, replace [flag] with "-e"
			4.b.i) the next [arg] will be used as the file you wish to encode
			4.b.ii) the next [arg] will be used as an existing image file that will be used to contain the encoded message
			4.c.iii) the next [arg] will be used as the name of the output file that will be automatically created as a .png file
				4.c.iii.1) Example, string "secret" will become "secret.png"
# CS353PythonCoder
