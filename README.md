[![Build Status](https://travis-ci.com/bitml-lang/bitml-doc.svg?branch=master)](https://travis-ci.com/bitml-lang/bitml-doc)

# Requirements

The documentation is generated in Python (both 2 and 3 version are tested by Travis CI).

Before starting, execute the following commands in this order:

* 1 - Use [pip](https://pip.pypa.io/en/stable/installing/) to install the following Python packages:

```shell
$ pip install sphinx pygments sphinxcontrib-inlinesyntaxhighlight sphinx-intl
```

 * 2 - Install Lexer:

 ```shell
$ make install-lexer
 ```
 
# Building

 * 1 - Build your own documentation:
 
 ```shell
 $ make build-doc
 ```

 * 2 - Start a local web server:(NOTE: You'll need to build the documentation before serving)

 ```shell
$ make server
 ```

 Browse to **localhost:8000** to check your documentation.


# Creating the documentation in another languange

To generate these .po locale files needed for localization,  you'll need to run this command from the **source** directory:
```console
$ sphinx-build -b gettext . _build/gettext
```
NOTE: You can skip this step, if there is already a  _build/gettext directory inside the **/source directory**

Inside the source folder, generate the localization folder with this command:
```console
$ sphinx-intl update -p _build/gettext -l languange_COUNTRY
````

Use the following syntax for when generating a new localization: Languange + Country
Example using Spanish from Argentina: es_ AR
Example using Portuguese from Portugal: pt_PT

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
