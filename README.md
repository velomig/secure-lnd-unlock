# Building

This is still super new. Copy the code to your node via ssh. The rest of the instructions are to be run on your node directly.

You should just be able to run:

```bash
$ python3 build_unlocker.py --wallet-password <my_wallet_password>
```

If all went well, you'll have a: `secure_unlock` in the same directory. You can test it out with:

```bash
$ ./secure_unlock
```

If that worked (you should get a message telling you the wallet is already unlocked), then you can add this to your crontab:

```
$ crontab -e

*/5 * * * * cd /home/ubuntu/dev/unlock && ./secure_unlock
```

Make sure your wallet password is safe & secure using whatever security or backup mechanism you have put in place. Once this is done, you can safely delete your wallet password from your node.

Enjoy.

# How does the wallet password key encryption work?

The only 'encryption' taking place here is making it very unfeasible to read the strings from the binary.

The first 'encryption' phase is to convert the unlock script to base64, in 10 character chunks with a random seed for each line. The seed for each line is generated using `os.urandom()` (random bytes suitable for cryptographic use). After running `build_unlocker.py` you'll notice a `./secure_unlock.cpp` in the root of the repo:

```c++
DEFINE_HIDDEN_STRING(EncryptionKey0, 0x4c, ('a')('W')('1')('w')('b')('3')('J')('0')('I')('G'))
DEFINE_HIDDEN_STRING(EncryptionKey1, 0x12, ('N')('v')('Z')('G')('V')('j')('c')('y')('w')('g'))
DEFINE_HIDDEN_STRING(EncryptionKey2, 0x5d, ('Z')('3')('J')('w')('Y')('y')('w')('g')('b')('3'))
DEFINE_HIDDEN_STRING(EncryptionKey3, 0x3d, ('M')('s')('I')('H')('N')('5')('c')('w')('o')('K'))
DEFINE_HIDDEN_STRING(EncryptionKey4, 0x1, ('c')('3')('l')('z')('L')('n')('B')('h')('d')('G'))
DEFINE_HIDDEN_STRING(EncryptionKey5, 0x53, ('g')('u')('Y')('X')('B')('w')('Z')('W')('5')('k'))
DEFINE_HIDDEN_STRING(EncryptionKey6, 0x7e, ('K')('C')('I')('u')('I')('i')('k')('K')('c')('3'))
...
```

Each line generates a decryption function that takes the seed and chunk. The `DEFINE_HIDDEN_STRING` macro is implemented in [src/HideString.h](src/HideString.h) which is pretty much a copy and paste from this [stackoverflow](https://stackoverflow.com/questions/1356896/how-to-hide-a-string-in-binary-code) thread.

The character ordinal values are xored them by seed-i, where i is their 0-based index of the character. 

```
('a'^0x4c-0)('W'^0x4c-1)('1'^0x4c-2)('w'^0x4c-3)('b'^0x4c-4)('3'^0x4c-5)('J'^0x4c-6)('0'^0x4c-7)('I'^0x4c-8)('G'^0x4c-9)
```

# Side-channel attacks

Embedding the GRPC python libraries into the binary would resolve the most obvious side-channel attack currently available.