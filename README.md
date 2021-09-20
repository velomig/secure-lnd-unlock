# Building

This is still super new. Copy the code to your node via ssh. The rest of the instructions are to be run on your node directly.

You should just be able to run:

```bash
$ python3 build_unlocker.py --wallet-password <my_wallet_password>
```

If all went well, you'll have a: `secure_unlocker` in the same directory. You can test it out with:

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

After running `build_unlocker.py` you'll notice a `./secure_unlock.cpp` in the root of the repo. The first 'encryption' phase is to convert the script to base64. The second phase is to break it up into `10` character long lines.

```c++
DEFINE_HIDDEN_STRING(EncryptionKey0, 0x7f, ('a')('W')('1')('w')('b')('3')('J')('0')('I')('G'))
DEFINE_HIDDEN_STRING(EncryptionKey1, 0x7f, ('N')('v')('Z')('G')('V')('j')('c')('y')('w')('g'))
DEFINE_HIDDEN_STRING(EncryptionKey2, 0x7f, ('Z')('3')('J')('w')('Y')('y')('w')('g')('b')('3'))
...
```

The `DEFINE_HIDDEN_STRING` macro is implemented in [src/HideString.h](src/HideString.h) which is pretty much a copy and paste from this [stackoverflow](https://stackoverflow.com/questions/1356896/how-to-hide-a-string-in-binary-code) thread.

