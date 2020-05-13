# BEM Nesting Utility

A program to automate the creation of a fully nested BEM file structure from a flatter initial working copy.  This includes writing all of the declarations to the correct files in that structures, as well as the import statements. Still unfinished, but
initial tests suggest it already works pretty well.

### Usage

Well, it isn't very user friendly yet.  Just clone the repo locally, and then move the `BEM-nester` subfolder into your project root folder.
The `cd` into `BEM-nester` and run `build.py`.

### Assumptions / Requirements

The program assumes a file structure like so:

```
\root
  \blocks
    \block1\block-1.css
    \block2\block-2.css
    ...
```

Each `block-n.css` must contain all selectors of the following forms:

* `block-n`
* `block-n__elem`
* `block-n__elem_mod`
* `block-n__elem_mod_val`
* `block-n_mod`
* `block-m_mod_val`
* pseudo-elements and pseudo-classes involving any of the above
* `@media` queries involving any of the above

Currently, those are the only types of declarations supported.  A few other assumptions:

- If a modifier takes a value sometimes, it takes a value all of the time.

- Only one type of selector per media query (where _type_ simply implies that each selector should be directed to the same file).

### Output

This program does the following:

  1. Creates a file `pages/index.css` in which it writes all block level import statements.   

  2. Creates a file structure with component paths of the form
  ```
    ./../blocks
      /block
        block.css
        /__elem
          block__elem.css
          /_mod
            block__elem_mod.css
  ```

  or 

  ```
  ./../blocks
      /block
        block.css
        /__elem
          block__elem.css
          /_mod
            block__elem_mod_val.css
  ```

  or similar forms the omit the __elem part. 

  3. Writes all declarations from the original block.css files to the
  appropriate places in this file structure.  The new blocks/block.css
  files will have already had the element and modifier level import 
  statements written to them.


### TODO

- refactor build_mod_file_structure into multiple functions
- translate file string file paths to os.path.join
- better test cases