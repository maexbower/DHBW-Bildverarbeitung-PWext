# DHBW-Bildverarbeitung-PWext
Analyse pictures of PostIt walls and generate a pdf file with all grouped same-color-PostIts.


## Dependencies
The following python packages are necasary for this project
 - reportlab
 - pillow
 - opencv

 ## Run
you need to add the output pdf path and at least one image as a param. * are allowed as placeholders in filenames.

```python ./main.py -o test.pdf ./Bilder/*```
