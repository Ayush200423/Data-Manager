# Data Manager

This Data Manager securely stores credentials and files in a SQLite 3 database for later retrieval.

Cybersecurity methods, including cryptography, are used to encrypt, decrypt, and hash passwords to secure sensitive information.

This project was developed as a personal project. 
SQLite 3 has been used as the database since this project is not intended for commercial use and is meant to run locally on your device.

Although this password managing system is quite secure and data may only be decrypted with the master password, it is highly recommended to use another professional data management system to store sensitive information.
## Features

- Multiple Account Creations
- Save Credentials & .jpg, .png, .jpeg, and .pdf Files
- Retrieve Credentials & Files
- Delete Credentials, Files, Account
## How It Works

Hashing a password with a salt is irreversible. 
Encrypting a password with a key, however, is reverrsible by decrypting it.

Two salts are generated for each user, and both are stored in the SQLite 3 database. The master password is hashed with the first salt, and the key is also stored in the database.

When logging in, the master password entered is again hashed with the same salt, & compared to the stored key.
If matched, you're authenticated.

Once verified, the master password is hashed with the second generated salt, and encoded into base64 for the cryptography library to use as the key. This key is used to encrypt and decrypt credentials and files.

Therefore, it is inconceivable to recover data without the master password (which is not stored in the database).
## Author

Ayush Patel