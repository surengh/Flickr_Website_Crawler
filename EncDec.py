"""
File: EncDec.py
Version: 1.0
Author: Surender Kumar
Copyright @ *****
Contact: emailsurenderkumar@gmail.com

This script ensures the password protection with 'cryptography' package. The
following APIs are used to accomplish this.

genCipherPasswd() :
This will generate the cipher code corresponding to the given
password, and will write it into internal PASSWD_FILE for future use.

decPasswd() :
Read the cipher password from the saved PASSWD_FILE, decrypt and return.
"""

# coding: utf-8
import os.path
import Logger
from cryptography.fernet import Fernet

PASSWD_FILE = ".passwd.bin"
DB_PASSWD = "suren"

class Security:
    def __init__(self):
        self.logH = Logger.getLogger()
        self.passwdFile = PASSWD_FILE

    def getLogH(self):
        return self.lohH

    def getPasswdFile(self):
        return self.passwdFile

    """
    This routine will encrypt the password and write its cipher to the PASSWD_FILE
    file.
    """
    def genCipherPasswd(self):
        """ Lets generate a sKey to encript MYSQL DB password. """
        sKey = Fernet.generate_key();
        self.logH.debug("MYSQL DB password is protected with sKey: " + sKey)
        cipherBox = Fernet(sKey)
        cipherPasswd = cipherBox.encrypt(DB_PASSWD) # Password: suren
        self.logH.debug("MYSQL DB password cipher code: " + cipherPasswd)

        """ Lets save the cipher passcode into a file for later use. """
        with open(self.passwdFile, 'w') as fileObj:
            try:
                fileObj.write(sKey + "\n")
                fileObj.write(cipherPasswd + "\n")
                fileObj.close()
            except:
                self.logH.error("File I/O error! Please check write permission.")

    """
    This routine will read the cipher password from the PASSWD_FILE file, will
    decrypt and return it.
    """
    def decPasswd(self):
        if os.path.exists(self.passwdFile):
            with open(self.passwdFile, 'r') as fileObj:
                try:
                    sKey = ""
                    count = 1

                    for line in fileObj:
                        if (count == 1):
                            sKey = line
                        else:
                            encryPasswd = line

                        count += 1;

                    fileObj.close()

                    if ((sKey == "") or (encryPasswd == "")):
                        self.logH.critical("Password file is corrupted.");
                        return None

                    cipherBox = Fernet(sKey)
                    decPasswd = (cipherBox.decrypt(encryPasswd))
                    """ Lets convert it back to string. """
                    sDecPasswd = bytes(decPasswd).decode("utf-8")
                    self.logH.debug("MYSQL DB Password is: " + sDecPasswd)
                    return sDecPasswd
                except:
                    self.logH.error("Passwd file not found!")
                    return None

"""
if __name__ == '__main__':
    sec = Security()
    sec.genCipherPasswd()
    print(sec.decPasswd())
"""
