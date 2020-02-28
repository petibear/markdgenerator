# simple example
from mdgenerator import MdDocGenerator
generator = MdDocGenerator()

# create h1 heading, include in a "intro" text block
generator.h1('intro',  'About')
# create a paragraph, include in the same block
generator.paragraph('intro',  'This document lists famous actors.')
# render the created text block
print(generator.render_textblock("intro"))

# create an "actors" table - add a header and three rows
generator.add_header('actors', ['name', 'surname'])
generator.add_row('actors', ['john', 'travolta'])
generator.add_row('actors', ['will', 'smith'])
generator.add_row('actors', ['tom', 'hanks'])
# render the table separately
print(generator.render_table("actors"))

# to print code
generator.h2("code", "Code example")
generator.codeblock("code", "from mdgenerator import MdDocGenerator")
print(generator.render_textblock("code"))
