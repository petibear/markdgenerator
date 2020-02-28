markdgenerator
==============
This is a small library to help generate text in [pandoc markdown](https://pandoc.org/MANUAL.html#pandocs-markdown) language with.

So far, it supports:
* h1, h2, h3 headings
* paragraphs
* code blocks
* tables in [grid_table](https://pandoc.org/MANUAL.html#tables) format
    * also generated from a pandas DataFrame

It's extendable to support more markdown languages.

Output of the tool can be converted into multiple document formats using [pandoc](https://pandoc.org/) and its `--from=markdown` option


Installation
------------
`pip install markdgenerator`

Example usage
-------------
```python
from markdgenerator import PandocMdGenerator
import pandas as pd

generator = PandocMdGenerator()
generator.h1("Example")
generator.paragraph("Pandas dataframe example")
generator.add_block_to_section()
df = pd.DataFrame(
    columns=["car", "price"],
    data=[["vw", 10000], ["bmw", 20000], ["mercedes", 30000]])
generator.df_to_table(df)
generator.add_table_to_section()
print(generator)
```

which leads to:

```
# Cars

This document lists prices of german cars.

+--------+-----+
|car     |price|
+========+=====+
|vw      |10000|
+--------+-----+
|bmw     |20000|
+--------+-----+
|mercedes|30000|
+--------+-----+
```
