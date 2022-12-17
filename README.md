# ZK Photo Redaction

This Example uses the filename `ZKPHOTO.png`. Take note that many of the parameters do not include an extension

`ZKPHOTO.png` Photo to be redacted.  
`ZKPHOTO_coords.txt` Location of the redaction area on the photo. Each redaction area is a square and listed on a new line in the format of `x` `y` `width` `height`. For example, a box starting at coordinates x `10px` and y `15px` with a width of `5px` and height of `20px` will be represented as `10 15 5 20`  
`ZKPHOTO_hash.txt` Contains public hash 
`ZKPHOTO_proof.txt` ZK Proof of redaction  
`ZKPHOTO_red.png` Redacted photo  
`ZKPHOTO_main.go` Gnark go code to produce proof  
`verify/ZKPHOTO_main.go` Gnark go code to verify proof  


## Create ZK Redaction and generate proving files

Two files required in the same folder
- `ZKPHOTO.png`
- `ZKPHOTO_coords.txt` 

The code generates the following files
- `ZKPHOTO_hash.txt`
- `ZKPHOTO_red.png`
- `ZKPHOTO_proof.txt`

Following files are generated but can be purged 
- `ZKPHOTO_main.go` (used to run go)
- `srs.txt` (Used to speed up subsequent runs)
- `A.txt` (Used to speed up subsequent runs)

```
# Generate proving go code
python3 redact.py ZKPHOTO.png

# Run proving code to generate proof in 
go mod tidy
go run ZKPHOTO_main.go ZKPHOTO
```

## Verifying ZK Redaction using proving files

Three files required in the same folder
- `ZKPHOTO_hash.txt`
- `ZKPHOTO_red.png`
- `ZKPHOTO_proof.txt`

```
# Generate verifying go code 
python3 verify.py ZKPHOTO

# Run verification code
cd verify
go mod tidy
go run ZKPHOTO_main.go ZKPHOTO
```
