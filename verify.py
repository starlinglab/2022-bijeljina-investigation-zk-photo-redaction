from PIL import Image
import ast
import sys
from utils import p, h, createNList, writeGoFile, getRedactedAndUnredactedNLists, calculateHash
import os

def main():
	filename = sys.argv[1]

	base = os.path.basename(filename)
	hash = ast.literal_eval(open(filename + '_hash.txt').read())
	
	x_coords= []
	y_coords = []
	widths = []
	heights=  []

	with open(f"{filename}_coords.txt", "r") as f:
		y=f.read()
		yy=y.split("\n")
		for l in yy:
			if l != "":
				item = l.split()
				x_coords.append(int(item[0]))
				y_coords.append(int(item[1]))
				widths.append(int(item[2]))
				heights.append(int(item[3]))


	red = Image.open(filename + '_red.png') 
	pix = red.load()

	# Seems to be an unsed variable
	# vec = createNList(red, pix)

	red_coords = set()
	for i in range(len(x_coords)):
		for j in range(widths[i]):
			for k in range(heights[i]):
				red_coords.add((x_coords[i] + j, y_coords[i] + k))

	redactedVec, unredactedVec, redacted_coord_vec, unredacted_coord_vec = getRedactedAndUnredactedNLists(red, pix, red_coords)
	_, A_redacted  = calculateHash(redactedVec, redacted_coord_vec)
	hashUnredacted, A_unredacted = calculateHash(unredactedVec, unredacted_coord_vec)

	hashRedacted = []
	for i in range(len(hash)):
		hashRedacted.append((hash[i] - hashUnredacted[i]) % p)

	writeGoFile('verify.txt', f"verify/{base}_main.go", A_redacted, hashRedacted, [0 for i in range(len(redactedVec))])

main()



