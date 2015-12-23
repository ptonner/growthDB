# Microbial Growth Data

This is an app for managing microbial growth data in the Django web framework for python.
The app supports the storage and downloading of growth data, as well as a robust system for specifying experimental design and replicate information for all data.
Searching for and downloading of specific experimental parameters is also supported.

The app outlines structures for:
* **plates**: a collection of **wells** containing microbial population growth measurements sampled over time, also contains the raw data file
* **well**: contains microbial growth data for a single **experimental design**, as well as provides replicate information
* **experimental design**: a collection of **design elements** and a **strain**
* **design elements**: specific elements of an **experimental design**
* **strain**: different strains with growth data stored in the app
