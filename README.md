# 2022 Bijeljina Investigation: ZK Photo Redaction

This repository contains the code used to generate and to verify zero knowledge proofs in our _2022 Bijeljina Investigation_. The process is used to provably redact regions in authenticated images before they are published.

The following example uses the filename `ZKPHOTO`, and the following files are involved in the process:
- `ZKPHOTO.png`: photo to be redacted.
- `ZKPHOTO_coords.txt`: location of the redaction area on the photo. Each redaction area is a square and listed on a new line in the format of `x` `y` `width` `height`. For example, a box starting at coordinates `x=10px` and `y=15px` with a width of `5px` and height of `20px` will be represented as `10 15 5 20`.
- `ZKPHOTO_hash.txt`: public hash.
- `ZKPHOTO_proof.txt`: ZK proof of redaction.
- `ZKPHOTO_red.png`: redacted photo.
- `ZKPHOTO_main.go`: gnark Go code to produce the proof.
- `verify/ZKPHOTO_main.go`: gnark Go code to verify proof.

## Creating ZK redaction and generating proof files

Two source files are required in the same folder:
- `ZKPHOTO.png`
- `ZKPHOTO_coords.txt`

The code generates the following files:
- `ZKPHOTO_hash.txt`
- `ZKPHOTO_red.png`
- `ZKPHOTO_proof.txt`

The following files are generated but can be purged:
- `ZKPHOTO_main.go` (used to run Go)
- `srs.txt` (used to speed up subsequent runs)
- `A.txt` (used to speed up subsequent runs)

Run:
```
# Generate proving Go code
python3 redact.py ZKPHOTO

# Run proving Go code to generate proof
go mod tidy
go run ZKPHOTO_main.go ZKPHOTO
```

## Verifying ZK redaction using proof files

Three files are required in the same folder:
- `ZKPHOTO_hash.txt`
- `ZKPHOTO_proof.txt`
- `ZKPHOTO_red.png`

Run:
```
# Generate verifying Go code 
python3 verify.py ZKPHOTO

# Run verifying Go code to verify proofs
cd verify
go mod tidy
go run ZKPHOTO_main.go ZKPHOTO
```
