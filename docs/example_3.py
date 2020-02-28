from markdgenerator import PandocMdGenerator

generator = PandocMdGenerator()

# you can be also specific as what blocks to put various text to
generator.h1("Example", block_name="block_1")
generator.paragraph("Pandas dataframe example", block_name="block_1")
generator.h2("Sub-part", block_name="block_2")
generator.paragraph("This belongs elsewhere", block_name="block_2")

# add the default block to the default section
generator.add_block_to_section(block_name="block_1", section_name="section_1")
generator.add_block_to_section(block_name="block_2", section_name="section_2")

# table too can be named
generator.add_header(['name', 'surname'], table_name='actors')
generator.add_row(['john', 'travolta'], table_name='actors')
generator.add_row(['will', 'smith'], table_name='actors')
generator.add_row(['tom', 'hanks'], table_name='actors')
# and added to a specific section
generator.add_table_to_section(table_name="actors", section_name="section_1")

# if we have multiple sections we can render a specific one only
print(generator.render_section(section_name="section_2"))
# or all of them
print(generator)
