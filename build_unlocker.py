"""
Build a secure unlocker for lnd.
Author: Just an open-source dev.
"""

import base64, os, sys
from textwrap import dedent


def parse_args():
    """
    Parse command-line arguments.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Build a secure unlocker for lnd")
    parser.add_argument(
        "-l",
        "--lnd-dir",
        help="LND directory location",
        default="~/.lnd",
    )
    parser.add_argument(
        "-w", "--wallet-password", help="Your wallet password", required=True
    )
    return parser.parse_args()


def main(pw, lndir):
    """
    Build the unlocker. This mostly involves building the obfuscated
    C++ source file.
    """
    args = parse_args()
    code = open("src/unlock.py").read().format(**dict(pw=pw, lndir=lndir)).encode()
    concats, macros, secret = [], [], base64.b64encode(code)
    for i, o in enumerate(range(0, int(len(secret)), 10)):
        blobs = "".join(f"('{x}')" for x in secret[o : o + 10 :].decode())
        macros.append(
            f"DEFINE_HIDDEN_STRING(EncryptionKey{i}, {hex(ord(os.urandom(1))%2**7)}, {blobs})"
        )
        concats.append(f"GetEncryptionKey{i}()")

    with open("secure_unlock.cpp", "w") as f:
        f.write(
            (
                open("src/secure_unlock.cpp")
                .read()
                .replace("{MACROS}", "\n".join(macros))
                .replace("{PROG}", " + ".join(concats))
            )
        )

    build()


def build():
    """
    Build the resuling C++ secure unlocker source file.
    """
    os.system(
        "g++ $(python3-config --cflags) -Wunused-function -fpermissive -fPIE -c secure_unlock.cpp -o secure_unlock.o"
    )
    os.system(
        "g++ secure_unlock.o $(python3-config --embed --ldflags) -o secure_unlock"
    )


if __name__ == "__main__":
    args = parse_args()
    main(pw=args.wallet_password, lndir=args.lnd_dir)
