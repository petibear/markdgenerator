Welcome to markdgenerator's documentation!
==========================================

Installation
------------
::

    pip install markdgenerator

Example 1
---------
::

    from markdgenerator import PandocMdGenerator

    generator = PandocMdGenerator()

    # text elements are by default added to the default block
    generator.h1("Example")
    generator.paragraph("This is an example:")
    generator.h2("Code")
    generator.codeparagraph("pip install markdgenerator")

    # since no section is defined, the default block will be printed
    print(generator)

leads to::


    # Example

    This is an example:


    ## Code
    ~~~~~~
    pip install markdgenerator
    ~~~~~~


Example 2
---------
::

    from markdgenerator import PandocMdGenerator
    import pandas as pd

    generator = PandocMdGenerator()
    # text elements are by default added to the default block
    generator.h1("Example")
    generator.paragraph("Pandas dataframe example")
    # add the default block to the default section
    generator.add_block_to_section()
    df = pd.DataFrame(
        columns=["car", "price"],
        data=[["vw", 10000], ["bmw", 20000], ["mercedes", 30000]])
    # table will be created as a default table
    generator.df_to_table(df)
    # add the default table to the default section
    generator.add_table_to_section()

    # the default section will be printed
    print(generator)


leads to::


    # Example

    Pandas dataframe example


    +--------+-----+
    |car     |price|
    +========+=====+
    |vw      |10000|
    +--------+-----+
    |bmw     |20000|
    +--------+-----+
    |mercedes|30000|
    +--------+-----+

Example 3
---------
::

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


leads to::


    ## Sub-part

    This belongs elsewhere

and::

    # Example

    Pandas dataframe example


    +----+--------+
    |name|surname |
    +====+========+
    |john|travolta|
    +----+--------+
    |will|smith   |
    +----+--------+
    |tom |hanks   |
    +----+--------+


    ## Sub-part

    This belongs elsewhere
