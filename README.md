# DHBW-Bildverarbeitung-PWext
Analyse pictures of PostIt walls and generate a pdf file with all grouped same-color-PostIts.


## Dependencies
The following python packages are necasary for this project
 - reportlab for pdf creation
 - pillow for images processing in pdf creation
 - opencv for parsing images
 - numpy for math operations while image processing

 ## Run
you need to add the output pdf path and at least one image as a param. * are allowed as placeholders in filenames.

```python ./main.py -o test.pdf ./Bilder/*```

to get the possible parameters you can use the parameter -h

```python ./main.py -h```