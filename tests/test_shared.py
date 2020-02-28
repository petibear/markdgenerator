"""Unit tests."""
from markdgenerator.common import CommonMdGenerator
from markdgenerator import PandocMdGenerator
from markdgenerator.config import NEWLINE
import pandas as pd
import pytest

@pytest.mark.parametrize("MdGenerator", [
        (PandocMdGenerator)
])
def test_init(MdGenerator):
    """Test object init."""
    _ = MdGenerator()


@pytest.mark.parametrize("MdGenerator, method_name, text, exp_result", [
        (PandocMdGenerator, 'h1', 'dummy', NEWLINE+'# dummy'+NEWLINE),
        (PandocMdGenerator, 'h2', 'dummy', NEWLINE+'## dummy'+NEWLINE),
        (PandocMdGenerator, 'h3', 'h3', NEWLINE+'### h3'+NEWLINE),
        (PandocMdGenerator, 'paragraph', 'dummy', NEWLINE+'dummy'+NEWLINE+NEWLINE),
        (PandocMdGenerator, 'codeparagraph', 'dummy', '~~~~~~'+NEWLINE+'dummy'+NEWLINE+'~~~~~~'+NEWLINE+NEWLINE),
])
def test_basic_elements(MdGenerator, method_name, text, exp_result):
    """Test correctness of simple methods returning string."""
    generator = MdGenerator()
    method = getattr(generator, method_name)
    method(text)
    assert exp_result == generator.render_block()

@pytest.mark.parametrize("MdGenerator, exp_result", [
        (PandocMdGenerator,
         '+-+-+' + NEWLINE +
         '|a|b|' + NEWLINE +
         '+=+=+' + NEWLINE +
         '|1|2|' + NEWLINE +
         '+-+-+' + NEWLINE +
         '|3|4|' + NEWLINE +
         '+-+-+' + NEWLINE
        )
])
def test_df_to_table(MdGenerator, exp_result):
    """Test processing of pandas dataframes."""
    df = pd.DataFrame(columns=['a', 'b'], data=[[1, 2], [3, 4]])
    generator = MdGenerator()
    generator.df_to_table(df)
    generator.add_table_to_section()
    assert exp_result == generator.render_section()

@pytest.mark.parametrize("MdGenerator, exp_result", [
        (PandocMdGenerator,
         '+-+-+' + NEWLINE +
         '|a|b|' + NEWLINE +
         '+=+=+' + NEWLINE +
         '|1|2|' + NEWLINE +
         '+-+-+' + NEWLINE +
         '|3|4|' + NEWLINE +
         '+-+-+' + NEWLINE
        )
])
def test_table_manual(MdGenerator, exp_result):
    """Test manual creation of tables."""
    generator = MdGenerator()
    generator.add_header(['a', 'b'])
    generator.add_row([1, 2])
    generator.add_row([3, 4])
    generator.add_table_to_section()
    assert exp_result == generator.render_section()


@pytest.mark.parametrize("MdGenerator", [
        (PandocMdGenerator)
])
def test_workflow_simpletable(MdGenerator):
    """Test a possible workflow."""
    generator = MdGenerator()

    # create h1 heading, include in a "intro" text block
    generator.h1('About', block_name='intro')
    # create a paragraph, include in the same block
    generator.paragraph('This document lists famous actors.', block_name='intro')
    # render the created text block
    print(generator.render_block(block_name="intro"))

    # create an "actors" table - add a header and three rows
    generator.add_header(['name', 'surname'], table_name='actors')
    generator.add_row(['john', 'travolta'], table_name='actors')
    generator.add_row(['will', 'smith'], table_name='actors')
    generator.add_row(['tom', 'hanks'], table_name='actors')
    # render the table separately
    md_text = generator.render_table(table_name="actors")
    assert len(md_text)>0

    # to print code
    generator.h2("Code example", block_name="code")
    generator.codeparagraph("from markdgenerator import PandocMdGenerator", block_name="code")
    md_text = generator.render_block(block_name="code")
    assert len(md_text)>0

@pytest.mark.parametrize("MdGenerator", [
        (PandocMdGenerator)
])
def test_workflow_pandas(MdGenerator):
    """Test a possible workflow."""
    generator = PandocMdGenerator()
    generator.h1("Cars", block_name="pandas")
    generator.paragraph("This document lists prices of german cars.", block_name="pandas")

    df = pd.DataFrame(
        columns=["car", "price"],
        data=[["vw", 10000], ["bmw", 20000], ["mercedes", 30000]])
    generator.df_to_table(df, table_name="cars")

    generator.add_block_to_section(block_name="pandas", section_name="example_section")
    generator.add_table_to_section(table_name="cars", section_name="example_section")
    md_text = generator.render_section(section_name="example_section")
    assert len(md_text)>0