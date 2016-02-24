# yubicrypto

A simple web application for performing basic cryptographic operations with a Yubikey.

## Development

Check out the source code to a directory on your local machine.

    $ git clone https://github.com/jmckind/yubicrypto.git
    $ cd yubicrypto

Next, set up and activate a virtual environment.

    $ pip install virtualenv
    $ mkdir .venv
    $ virtualenv --prompt="(yubicrypto) " .venv
    $ source .venv/bin/activate

Download and install the application dependencies.

    $ pip install -r requirements.txt

Once the dependencies have been installed, start the development server.

    $ gunicorn server:app

This will start the development server on the local machine, listening on port 8000. You should be able to access the application at [http://localhost:8000/](http://localhost:8000).

## Usage

Once the application is running, encrypt some text.

##### httpie

    $ http -v POST localhost:8000/encrypt plaintext=foo

    HTTP/1.1 200 OK
    Connection: close
    Date: Wed, 24 Feb 2016 19:17:29 GMT
    Server: gunicorn/19.4.5
    content-length: 21
    content-type: application/json; charset=utf-8

    {
        "ciphertext": "oof"
    }

You can also decrypt some text...

    $ http -v POST localhost:8000/decrypt ciphertext=oof

    HTTP/1.1 200 OK
    Connection: close
    Date: Wed, 24 Feb 2016 19:17:29 GMT
    Server: gunicorn/19.4.5
    content-length: 21
    content-type: application/json; charset=utf-8

    {
        "plaintext": "foo"
    }
