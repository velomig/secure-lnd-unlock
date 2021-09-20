/* 
Obfuscated & secure unlocker for lnd
Author: Just an open-source dev.
Date: Year 12 Anno Satoshi
*/


#include <string>
#include <Python.h>
#include "src/HideString.h"
#include <iostream>

{MACROS}

int main(int argc, char *argv[]){
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        std::cerr << "Fatal error: cannot decode argv[0]\n" << std::endl;
        exit(1);
    }
    Py_Initialize();
    PyRun_SimpleString(std::string("import base64\neval(compile(base64.b64decode(b'" + {PROG} + "'), '<string>', 'exec'))").c_str());
    Py_Finalize();
    PyMem_RawFree(program);
    return 0;
}