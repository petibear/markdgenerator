# example with pandas
from mdgenerator import MdDocGenerator
import pandas as pd

generator = MdDocGenerator()
generator.h1("pandas", "Cars")
generator.paragraph("pandas", "This document lists prices of german cars.")

df = pd.DataFrame(
    columns=["car", "price"],
    data=[["vw", 10000], ["bmw", 20000], ["mercedes", 30000]])
generator.df_to_table("cars", df)

generator.add_to_section(section_name="example_section", block_name="pandas")
generator.add_to_section(section_name="example_section", table_name="cars")
print(generator.render_section(section_name="example_section"))
