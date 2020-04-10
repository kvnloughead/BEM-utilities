# BEM Nested File Structure Generator

An attempt to automate the creation of nested BEM file structures, along with the necessary css files.  Still quite untested.  

### Implemented Features

 1. Creates the basic directory structure (including root) along with all necessary css files with ".selector {}" declarations already in place.

 2. Writes all necessary import statements into created css files, including pages/index.css.

### Usage

You can clone the repo locally and us it in its own directory to see how it works.  It contains a directory called `blocks/` and another named `pages/` that contains an `index.css` file, and these are prerequisites.

Currently, you tell the program your desired file structure by modifying the `blocks` dictionary inside of `main.py`.   It is filled with sample data, and looks like this:

```Python
blocks = {  'root'   : [],
            'header' : ['logo', 'title', 'subtitle', '_theme_dark'],
            'footer' : ['logo', 'copyright', 'links'],
            'content': ['main-text', 'sidebar', 'sidebar_place_left', 'sidebar_place_right'],   
         }
```

The keys are the blocks that you wish to use, and items in the lists are in the following formats: `elements`, `_modifier_value` or `element_modifier_value` combinations.  Try modifying them to your desired file structure and let me know if it works!

### Limitations

Currently the only BEM formats supported are `block`, `block__elem`, `block_mod_val`, `block__elem_mod_val`.

### TODO list

2. command line functionality
3. bash script to make navigation to css files simpler
4. support more BEM formats? 
