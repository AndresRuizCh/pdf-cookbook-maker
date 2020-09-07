# Cookbook Maker

Generates a .pdf file given a .csv or .xlsx source to create a Cookbook by automatically ordering all the recipes in the database.

# Usage

To use it, just write the new recipes at the end of the .csv or .xlsx file separating the ingredients and the steps using ````;```` and run the file ```recipe.py``` using the following options:

```
python recipe.py -l <language> -t <title> -i <ingredients> -a <author> -s <steps> '-x <tex> -d <database> -f <file>
```

# Requirements 

Paddington requires the following to run:

  * [Pandas][Pandas]
  * [NumPy][NumPy] 
  * [LaTeX][LaTeX]

[Pandas]: https://pandas.pydata.org/
[NumPy]: https://numpy.org/
[LaTeX]: https://www.latex-project.org/