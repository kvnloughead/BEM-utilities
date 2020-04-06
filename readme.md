# BEM Nested File Structure Generator

An attempt to automate the creation of nested BEM file structures, along with the necessary css files.  Still quite untested.  

### Implemented Features

Creates the basic directory structure (including root) along with all necessary css files wiht ".selector {}" declarations already in place.

### Usage

Currently you must edit the `blocks` dictionary inside of `main.py`.  This contains all of the blocks, elements, modifiers and values that you will be working.   Currently supports the following styles:  `block`, `block__elem`, `block_mod_val`, `block__elem_mod_val`.  Then run this from within the root directory of your project.  There needs to be a `blocks` directory in the directory alongside `main.py`.

### TODO list

1. import statements, pages directory
2. command line functionality
3. bash script to make navigation to css files simpler
4. support more BEM styles? 
