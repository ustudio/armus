
[![Circle CI](https://circleci.com/gh/ustudio/armus.svg?style=svg&circle-token=9f77bab2ae75ccdbefe30a7b0551a8fc52e53cac)](https://circleci.com/gh/ustudio/armus)

Standalone Migration Tool a.k.a. "Armus"
=================

<img src="http://vignette1.wikia.nocookie.net/memoryalpha/images/5/58/Armus.jpg/revision/latest?cb=20120728222622&path-prefix=en" width="150"
 alt="armus logo" title="armus" align="right" />

### What is Armus?

armus is an open source tool for running migration scripts.  It was developed in an effort to simplify database migrations at [uStudio](http://www.ustudio.com).




## Usage

armus/run_migrations.py accepts a path to a package as well as a list of modules that have already been applied.  It will compare the provided list to the migrations in the directory provided and run the ```up()``` function on the unapplied modules.

## TO DO

1. Refactor and add features to the bin/create_migration.py script
2. Add a "revert" feature that will run the "down()" function on the specufied module
3. Rename the repo to something more descriptive

