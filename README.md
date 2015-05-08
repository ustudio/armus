Standalone Migration Tool a.k.a. "Odo"
=================

<img src="http://ds9.trekcore.com/gallery/albums/publicityphotos/odo/9O_2pub.jpg" width="150"
 alt="Odo logo" title="Odo" align="right" />

### What is Odo?

Odo will be an open source tool for running migration scripts.  It was developed in an effort to simplify database migrations at [uStudio](http://www.ustudio.com).



## Usage

odo/run_migrations.py accepts a path to a package as well as a list of modules that have already been applied.  It will compare the provided list to the migrations in the directory provided and run the ```up()``` function on the unapplied modules.

## TO DO

1. Refactor and add features to the bin/create_migration.py script
2. Add a "revert" feature that will run the "down()" function on the specufied module
3. Rename the repo to something more descriptive

## Why "Odo"?
As this tool was primarily developed for making changes to a database, we thought an homage to the greatest shapeshifter in starfleet was appropriate.
