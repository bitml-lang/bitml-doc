[![Build Status](https://travis-ci.com/bitml-lang/bitml-doc.svg?branch=master)](https://travis-ci.com/bitml-lang/bitml-doc)

# Requirements

The documentation is generated in Python (both 2 and 3 version are tested by Travis CI).

Before start, install the needed packages *as it follows:*

* 1 - Use [pip](https://pip.pypa.io/en/stable/installing/) to install the following Python packages:

```shell
$ pip install sphinx pygments sphinxcontrib-inlinesyntaxhighlight
```

 * 2 - Install Lexer:

 ```shell
$ make install-lexer
 ```

 * 3 - Now you can build your own documentation, with the command:
 
 ```shell
 $ make build-doc
 ```

 * 4 - Then serve on your browser with the command:

 ```shell
$ make server
 ```

 Navigate to **localhost:8000** and check the built documentation from the step 3.

# Available commands

```console
make build-doc              # build the documentation
make build-doc-warning      # build the documentation and fail if there are warnings
make clean-doc              # clean the documentation
make install-lexer          # install the lexer for pygments
make remove-lexer           # remove the lexer from pygments
make full-clean             # clean the documentation and remove the lexers
make full-build             # build the documentation and install the lexers
make server                 # start a local server at port 8000 to view the docs
make server2                # start a local server at port 8000 to view the docs
make loop                   # compile the docs every time a file changes
```