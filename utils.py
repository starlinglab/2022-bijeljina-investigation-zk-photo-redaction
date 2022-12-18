import hashlib
import os
import ast

p = 21888242871839275222246405745257275088548364400416034343698204186575808495617
h = 128

width = 430
height = 608

def getACoord(i, j):
	ij = str(i) + ',' + str(j)
	return int(hashlib.sha256(ij.encode('utf-8')).hexdigest(), 16) % p

def writeA():
	f = open('A.txt', 'w')
	for i in range(h):
		A = []
		for j in range(width * height):
			A.append(str(getACoord(i, j)))
		f.write(",".join(A))
		f.write("\n")
	f.close()

def getA(coord_vec):
	if not os.path.exists('A.txt'):
		writeA()

	A_orig = []
	with open('A.txt') as file:
		i = 0
		for line in file:
			A_orig.append(line.split(","))

	A = []
	for i in range(h):
		A.append([])
		for j in range(len(coord_vec)):
			# assert(int(A_orig[i][coord_vec[j]]) == getACoord(i, coord_vec[j]))
			A[i].append(int(A_orig[i][coord_vec[j]]))
	return A

def getRBGNValue(r, g, b):
	return r * 256 * 256 + g * 256 + b

def createNList(orig, pix):
	vec = []

	for i in range(orig.size[0]):
		for j in range(orig.size[1]):
			r, g, b = pix[i, j]
			vec.append(getRBGNValue(r, g, b))
	return vec

def calculateHash(vec, coord_vec):
	hash = []
	A = getA(coord_vec)
	for i in range(h):
		s = 0
		for j in range(len(vec)):
			s += A[i][j] * vec[j]
		hash.append(s % p)
	return (hash, A)


def getRedactedAndUnredactedNLists(orig, pix, red_coords):
	redactedVec = []
	unredactedVec = []
	A_redacted = []
	A_unredacted = []

	for i in range(orig.size[0]):
		for j in range(orig.size[1]):
			r, g, b = pix[i, j]
			val = getRBGNValue(r, g, b)
			coord = (i, j)
			coord_index = i * orig.size[1] + j

			if coord in red_coords:
				redactedVec.append(val)
				A_redacted.append(coord_index)
			else:
				unredactedVec.append(val)
				A_unredacted.append(coord_index)
	
	return (redactedVec, unredactedVec, A_redacted, A_unredacted)

def writeGoFile(input_filename, output_filename, A_redacted, hashRedacted, redactedVec):
	parts = open(input_filename).read().split("INSERT_VARIABLE")
	f = open(output_filename,'w')
	f.write(parts[0])
	f.write(str(h))
	f.write(parts[1])
	f.write(str(len(redactedVec)))
	f.write(parts[2])

	A_redacted_str = [[str(y) for y in x] for x in A_redacted]
	f.write(str(A_redacted_str).replace('[','{').replace(']','}').replace('\'', '\"'))

	f.write(parts[3])

	hashRedactedStr = [str(x) for x in hashRedacted]
	f.write(str(hashRedactedStr).replace('[','{').replace(']','}').replace('\'', '\"'))
	f.write(parts[4])
	redactedVecStr = [str(x) for x in redactedVec]
	f.write(str(redactedVec).replace('[','{').replace(']','}').replace('\'', '\"'))
	f.write(parts[5])
	f.close()