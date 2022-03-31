# AE3KR-tasks-RSAandDSA

## task description (DSA)

* Loading the file for signing (fileDialog)
* Showing the file info in the application -> like file name, path to the file, type (extension), file 
size, etc.
* Signing the file -> hashing and encryption with private key using your previously made RSA 
cipher.
* Verifying the signed file (digital sign verifying) -> here to use public key
* Generating the key pair for RSA with possibility to save public/private key in the files -> files 
with extension .pub and .priv
* GUI with only using fileDialogs and buttons and outputs -> no inputs are necessary … For 
loading keys should be used files .priv and .pub
More details:
* Digital sign should be file with extension .sign (output of hash function encrypted by private 
key and using RSA). File .sign should contains following data:
RSA_SHA3-512 DIGITAL_SIGN_IN_BASE64. (for example "RSA_SHA3-512
QWhvaiBQZXBvLCBqYWsgc2UgbcOhxaEgPw==")
* For verifying the user need to load .sing file + public key file .pub + original file
* Key pair file .pub and .priv should contain data as following: 
RSA PRIVATE_KEY_IN_BASE64.
RSA PUBLIC_KEY_IN_BASE64


## how this application works (DSA)

1. the user chooses a text file
2. then the user presses the button to generate the public and private keys
3. next the user presses a button to generate a hash of the text then create the signiture
4. Then in a hypothetical situation, the user can share the text file with the sign file and the public key
5. the user on the other side can load the files and check with their key if the files match or they have been tempered with

## picture of the application (DSA)

![DSA app](https://github.com/ap-Camel/AE3KR-tasks-RSAandDSA/blob/master/Screenshot%202022-03-31%20094649.png)


## task description (RSA)

RSA is the asymmettric cipher from asymmetric cryptology
Be careful, the principle is so easy, but for implementation there some „traps“
The basic descirption you can of course find on Wikipedia. Base on it you should implemented 
following 5:
1. Generating the public and private key pair
2. Transformation the open text to numeric form
3. Encryption using public key
4. Decryption using private key
5. Transofrmation back from numeric form to text form of open-text
For this cipher is not necessary to ommit any special characters on trasnfer letter to capitalized -> it 
can také anything as input.
Key generating:
1. Two big prime numbers are chosen -> p and q (randomly generated and different)
2. The number n is counted as n = p*q
3. The number phi(n) is counted as from Euler function -> phi(n) = (p-1)*(q-1)
4. The random number e is chosen on the interval (1; phi(n)) -> 1 < e < phi(n), when the 
GCD(e, phi(n) should be equal to 1.
5. Number d is chosen as inverse modulo number to the number e when i sis moduled by 
phi(n) -> similar function to PowerMod from wolfram mathematica should be used.
Public key will be numbers (n, e)
Private key will be numbers (n, d)
Encryption is simple function c = me mod n
Where m - message, c - ciphertext
Decryption is analogious m = cd mod n
kde m - message, c – ciphertex

## picture of the application (RSA)

![RSA app](https://github.com/ap-Camel/AE3KR-tasks-RSAandDSA/blob/master/Screenshot%202022-03-31%20094349.png)
