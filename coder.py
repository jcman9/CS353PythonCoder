from PIL import Image
from bitstring import BitArray
from math import ceil
import sys, string

'''
Name:decoder()
Function: Handles the decoding section without any arguments. Will check to see if there are too many arguments before continuing on with decoding the image. It will print out the size of the image passed in, the length of the message and the message before exiting the program. 
#code are debug statements left in for future understanding
'''
def decoder():
	
	#Error check
	if len(sys.argv) >  3 and sys.argv[1] == "-d":
		print ("Error. Too many arguments in decoder call.")
		print ("Example: coder.py -d testImage.png")
		sys.exit()

	#Assigns the image file name to a string
	img = sys.argv[2]


	#Open the image file or print an error and stop if it cannot open
	try:
		myimage = Image.open(img)
	except:
		print ("Error. Unable to load image. Double check image exists or is typed correctly.")
		sys.exit()
	
	#reads in the width and height of the image and prints it out
	width = myimage.size[0]
	height = myimage.size[1]
	print (myimage.size)

	#rotates the image so that the bottom right pixel is now the top left and translates image into RGB format
	out = myimage.rotate(180)
	rgb_out = out.convert('RGB')
	
	#creates a list of all RGB values and calculates the length of that list
	image_array = list(rgb_out.getdata())
	arraylength = len(image_array)
	#print (arraylength)

	#declarations
	i = 0
	j = 0
	binstring = ""

	#Parses through the image by coordinates for the first 11 pixels. Will return the concatenated binary string.
	for count in range(11):
		r,g,b = rgb_out.getpixel((i,j))
		#print(i,j, r,g,b)
		rbin = bin(r)
		rstring = str(rbin)
		rstring = rstring[2:]
		gbin = bin(g)
		gstring = str(gbin)
		gstring = gstring[2:]
		bbin = bin(b)
		bstring = str(bbin)
		bstring = bstring[2:]
		#print(rbin, gbin, bbin) 	
		binstring += rstring[-1] + gstring[-1] + bstring[-1]
		#print(binstring)
		i = i + 1

	#Removes the blue value of the 11th pixel from the string and calculates the length of the message
	binstring = binstring[:-1]
	length = int(binstring,2)
	#print("binstring:")
	#print (binstring)
	#print ("length:", length)

	#This half will now decode the message located after the length
	#Declarations
	textstring = ""
	message = ""
	upper_bound = ceil(length/3)

	#for loop to run through the image starting from 12th pixel to the bound. Will return the textstring that contains the message.
	x = 11
	y = 0
	for i in range(0, upper_bound):
		textstring += str(bin(image_array[x][0])[-1]) + str(bin	(image_array[x][1])[-1]) + str(bin(image_array[x][2])[-1])
		x += 1
	#print(textstring)
	#print("textstring length:", len(textstring))
	

	#For loop to run through the textstring and translate each 8 bits into a character and returns the message
	for i in range(0, len(textstring), 8):
		message += chr(int(textstring[i:i+8],2))
	print(message)

	out = myimage.rotate(180)
	sys.exit()

'''
Name: encoder()
Function: Handles the encoding process of the program. It takes 5 arguments and will take an existing image and a file to be encoded and outputs the new image that has the file encoded into it.
#code are debug statements left in for future understanding
'''

def encoder():	
	#Error checking for the right amount of arguments	
	if len(sys.argv) < 5 or len(sys.argv) > 5:
		print("Error. Misuse of encoding arguments.")
		print("Example: coder.py -e [textfile] [imagesource] [output]")
		sys.exit()
	
	#try to open the image, otherwise exit
	img = sys.argv[3]
	try:
		myimage = Image.open(img)
	except:
		print ("Error. Unable to load image. Double check image exists or is typed correctly.")
		sys.exit()

	#try to read the file, otherwise exit
	filename = sys.argv[2]
	try:
		open(filename, "r")
	except:
		print("Error. Unable to open file to encode. Double check file exists or is typed correctly.")

	#stores the desired output name from the argument
	outputfile = sys.argv[4]
	
	#opens the file and reads each line
	filebinstring = ""
	filebinstring = filebinstring.encode()
	with open(filename) as f:
		lines = 0
		words = 0
		characters = 0
		wordslist = []
		for line in f:
			filebinstring += line.encode()
	#print("filebinstring:")
	#print(filebinstring)		
	
	#turns the incoming file into ASCII bytes, and then turns those bytes into bits
	filebinstring = BitArray(filebinstring)
	filebinstring = filebinstring.bin	
	#print("binary filebinstring:")
	#print(filebinstring)
	#print("binaryfilebinstring length:", len(filebinstring))

	#converts the length of characters into bytes needed for the message and converts it into a bitstring
	binlenstring = bin(len(filebinstring))
	binlenstring = "0" + binlenstring[2:]
	strlength = len(binlenstring)
	fillin = 32 - strlength
	for i in range(fillin):
		binlenstring = "0" + binlenstring
	#print("binlenstring:")	
	#print (binlenstring)
	#print("binlenstring:", int(binlenstring,2))

	#reads in the width and height of the image and prints it out
	width = myimage.size[0]
	height = myimage.size[1]
	print (myimage.size)

	#rotates the image so that the bottom right pixel is now the top left and translates image into RGB format
	out = myimage.rotate(180)
	rgb_out = out.convert('RGB')
	
	#creates a list of all RGB values and calculates the length of that list
	image_array = list(rgb_out.getdata())
	arraylength = len(image_array)
	#print (arraylength)

	#pulls the first 11 pixels and their RGB values
	x = 0
	y = 0
	binstring = ""
	for i in range(11):
		r,g,b = rgb_out.getpixel((x,y))
		rbin = bin(r)
		rstring = str(rbin)
		rstring = rstring[2:]
		gbin = bin(g)
		gstring = str(gbin)
		gstring = gstring[2:]
		bbin = bin(b)
		bstring = str(bbin)
		bstring = bstring[2:]	
		binstring += rstring[-1] + gstring[-1] + bstring[-1]
		x += 1
	#print("binstring:")
	#print (binstring)

	#converts the binary into a mutable list
	messagelength = list(binlenstring)
	newbin = list(binstring)

	#joins the list after replacing the values of the first 32 bits
	for i in range(32):
		newbin[i] = messagelength[i]
	newbin = ''.join(newbin)	
	#print("newbin:")
	#print(newbin)
	
	#Will traverse 32 bits again and change the least significant bit so in the binary so that the rgb values are changed.
	x = 0
	y = 0
	foo = ""
	for i in range(0,32,3):
		#grab the pixels		
		r,g,b = rgb_out.getpixel((x,y))
		
		#handles red values
		rbin = bin(r)
		rstring = str(rbin)
		rstring = rstring[2:]
		rlist = list(rstring)
		#print("newbin[i]:", newbin[i])
		#print("old rstring")
		#print(rlist)
		rlist[-1] = newbin[i]
		#print("new rstring:")
		#print(rlist)
		rstring = ''.join(rlist)
		r = int(rstring,2)
		#print("r:", r)

		#handles green values
		gbin = bin(g)
		gstring = str(gbin)
		gstring = gstring[2:]
		glist = list(gstring)
		#print("newbin[i+1]:", newbin[i+1])
		#print("old gstring")
		#print(glist)
		glist[-1] = newbin[i+1]
		#print("new gstring:")
		#print(glist)
		gstring = ''.join(glist)
		g = int(gstring,2)		
		#print("g:", g)
	
		#handles blue values
		bbin = bin(b)
		bstring = str(bbin)
		bstring = bstring[2:]
		blist = list(bstring)		
		#print("newbin[i+2]:", newbin[i+2])
		#print("old bstring")
		#print(blist)
		blist[-1] = newbin[i+2]
		#print("new bstring:")
		#print(blist)
		bstring = ''.join(blist)
		b = int(bstring,2)
		#print("b:", b)

		#save the pixels to the image object
		rgb_out.putpixel((x,y),(r,g,b))
		#pixels = rgb_out.getpixel((x,y))
		#print(pixels)
		x += 1
	
	#for loop to run through the image starting from 12th pixel to the bound. Will return the textstring that is originally in the pixels.
	#[0] = red. [1] = green. [2] = blue
	textstring = ""	
	x = 12
	y = 0
	for i in range(0, len(filebinstring)):
		textstring += str(bin(image_array[i][0])[-1]) + str(bin	(image_array[i][1])[-1]) + str(bin(image_array[i][2])[-1])
		#print(i)
		x += 1
	#print("textstring:")	
	#print(textstring)

	#turns the output, "textstring," into an mutable list for easier replacement of bits
	newmessage = list(textstring)
	#print("Length of filebinstring:", len(filebinstring))
	#print ("Length of textstring:", len(textstring))			

	#replaces the least significant bit with the message
	for i in range(0, len(filebinstring)):		
		newmessage[i] = filebinstring[i]

	#rejoins the list as one string
	newmessage = ''.join(newmessage)
	#print("New Message:")	
	#print(newmessage)
	#print("new message length:", len(newmessage))
	
	#for loop to traverse the image and replace the least significant bit to have the message
	x = 11
	y = 0
	j = 0
	for i in range(0, ceil(len(filebinstring)/3)):	
		#handles red values		
		r = str(bin(image_array[x][0]))[2:]
		rlist = list(r)
		rlist[-1] = newmessage[j]
		rstring = ''.join(rlist)
		rbin = int(rstring,2)
		r = rbin
		
		#handles green values
		g =str(bin(image_array[x][1]))[2:]
		glist = list(g)
		glist[-1] = newmessage[j+1]
		gstring = ''.join(glist)
		gbin = int(gstring,2)
		g = gbin

		#handles blue values
		b =str(bin(image_array[x][2]))[2:]
		blist = list(b)
		blist[-1] = newmessage[j+2]
		bstring = ''.join(blist)
		bbin = int(bstring,2)
		b = bbin

		#assigns the new pixels to the image object
		rgb_out.putpixel((x,y),(r,g,b))
		#pixels = rgb_out.getpixel((x,y))
		#print(pixels)
		x += 1
		j += 3
		if x == width:
			x = 0
			y += 1


	#re-rotate the image so that it is upright and creates a new image object that will contain all of the changed pixels
	rgb_out = rgb_out.rotate(180)
	rgb_out.save(outputfile + ".png", "PNG")
	sys.exit()
	


'''
Main part of the code. Will run here before going into the other functions. Error checks for flags before going into functions.
'''
#checks the input and sends it to the appropriate function of the program
if sys.argv[1] == "-d":
	print("Beginning decoding portion.")
	decoder()
elif sys.argv[1] == "-e":
	print("Beginning encoding portion.")
	encoder()
else:
	print("Error. Misuse of arguments.")
	sys.exit()
