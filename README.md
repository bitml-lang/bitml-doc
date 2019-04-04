[![Build Status](https://travis-ci.org/balzac-lang/balzac-doc.svg?branch=master)](https://travis-ci.org/balzac-lang/balzac-doc)

# Requirements

The documentation is generated in Python (both 2 and 3 version are tested by Travis CI).


Use `pip` to install the following Python packages:

```
pip install sphinx pygments sphinxcontrib-inlinesyntaxhighlight
```

# Available commands

```
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
