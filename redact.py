from PIL import Image
import sys
import os
from utils import p, h, createNList, writeGoFile, getRedactedAndUnredactedNLists, calculateHash

def main():
	filename = sys.argv[1]
	base = os.path.basename(filename)

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

	orig = Image.open(filename + '.png') 
	pix = orig.load()

	vec = createNList(orig, pix)
	hash, A = calculateHash(vec, [i for i in range(len(vec))])

	red_coords = set()
	for i in range(len(x_coords)):
		for j in range(widths[i]):
			for k in range(heights[i]):
				red_coords.add((x_coords[i] + j, y_coords[i] + k))

	redactedVec, unredactedVec, redacted_coord_vec, unredacted_coord_vec = getRedactedAndUnredactedNLists(orig, pix, red_coords)
	hashRedacted, A_redacted  = calculateHash(redactedVec, redacted_coord_vec)
	hashUnredacted, A_unredacted = calculateHash(unredactedVec, unredacted_coord_vec)

	print('redactedVec length', len(redactedVec))

	writeGoFile('redact.txt', f"{base}_main.go", A_redacted, hashRedacted, redactedVec)

	f = open(filename + '_hash.txt','w')
	f.write(str(hash))
	f.close()

	for i in range(len(hash)):
		assert((hashUnredacted[i] + hashRedacted[i] - hash[i]) % p == 0)

	for i in range(len(x_coords)):
		for j in range(widths[i]):
			for k in range(heights[i]):
				pix[x_coords[i] + j, y_coords[i] + k] = (0, 0, 0)

	orig.save(filename + '_red.png')

main()
