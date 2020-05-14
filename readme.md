# BEM Nesting Utility

A program to automate the creation of a fully nested BEM file structure from a flatter initial working copy.  This includes writing all of the declarations to the correct files in that structures, as well as the import statements. Still unfinished, but
initial tests suggest it already works pretty well.

### Usage

The driver file `nest.py` is executable, so if you clone the repo locally and place its directory somewhere in your path, you should be able to run it from by invoking its name at the command line.  Do so from the root directory of the project you wish to nest. 

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


### What it does

This program does the following:

  1. If pages/index.css does not exist, creates it and writes block import statements
     in it.

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

    - Corrects file paths listed under `url(...)` or `src(...)` in all
    files other than block.css.   The paths in block.css should be, since
    I assume those files are already correctly nested.


### TODO

- refactor build_mod_file_structure into multiple functions
- rewrite the regex in read_css.fix_file_paths to suck less
- translate file string file paths to os.path.join
- better test cases

- fix: last declaration in block_mod_val not being handled by fix_file_paths