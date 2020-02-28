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