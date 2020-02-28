from abc import ABC, abstractmethod
import pandas as pd


class CommonDocGenerator(ABC):
    """
    Common (abstract) parent class to generate text in markdown languages
    """

    def __init__(self):
        """
        Init function
        """
        self._blocks = {}
        self._tables = {}
        self._sections = {}
        self._DEFAULT_SECTION_NAME = "_DEFAULT_SECTION_"
        self._flush_section(self._DEFAULT_SECTION_NAME)

    def _flush_block(self, block_name):
        """
        Initializes and/or flushes a block

        Args:
            block_name(str): block to flush
        """

        self._blocks[block_name] = []

    def _flush_table(self, table_name):
        """
        Initializes and/or flushes a table

        Args:
            table_name(str): table to flush

        """

        self._tables[table_name] = {'header': [], 'rows': [], 'cols_count': 0, 'cols_widths':  [], 'rows_count': 0, 'has_header': False}

    def _flush_section(self, section_name):
        """
        Initializes and/or flushes a section
        Section is a sequence of paragraphs and/or tables

        Args:
            section_name(str): section to flush

        """
        self._sections[section_name] = []

    def _add_to_block(self, block_name, text):
        """
        Add the formatted text to a given block

        Args:
            block_name(str): block to write to
            text(str): formatted string to write
        """

        # if not yet existing, create a block
        if block_name not in self._blocks:
            self._flush_block(block_name)

        # append to the block the formatted text
        self._blocks[block_name].append(text)

    def add_to_section(self, section_name = None, block_name = None, table_name = None):
        """
        Adds either a block or a table (only one of the two) to a section
        that can be rendered together.

        Args:
            section_name(str): name of the section,
                if not given, the default section will be used
            block_name(str): name of the block to add to the section;
                needs to be None if table_name is given
            table_name(str): name of the table to add to the section;
                needs to be None if block_name is given
        """
        if ((block_name is None) and (table_name is None)) or \
            ((block_name is not None) and (table_name is not None)):
            raise ValueError('Either a table or block (and only one of the two) needs to be given')

        # if adding a block, it must exist
        if (block_name is not None) and (block_name not in self._blocks):
            raise ValueError('Block of text is not known to the generator')

        # if adding a table, it must exist
        if (table_name is not None) and (table_name not in self._tables):
            raise ValueError('Table is not known to the generator')

        # determine section
        # default
        if section_name is None:
            section_name = self._DEFAULT_SECTION_NAME

        # user given
        if section_name not in self._sections:
            self._flush_section(section_name)

        # add block if provided
        if block_name is not None:
            self._sections[section_name].append(
                {"type": "block", "name": block_name})

        # add table if provided
        if table_name is not None:
            self._sections[section_name].append(
                {"type": "table", "name": table_name})

    @abstractmethod
    def h1(self, block_name, text):
        pass

    @abstractmethod
    def h2(self, block_name, text):
        pass

    @abstractmethod
    def h3(self, block_name, text):
        pass

    @abstractmethod
    def paragraph(self, block_name, text):
        pass

    @abstractmethod
    def codeblock(self, block_name, text):
        pass

    @abstractmethod
    def render_textblock(self,block_name):
        pass

    @abstractmethod
    def render_section(self,section_name):
        pass

    def add_header(self, table_name, header):
        """
        Adds a header to a table
        Args:
            table_name(str): table to add header to
            header(str[]): list of strings
        """
        # new lines not yet supported
        if any(['\n' in c for c in header]):
            raise ValueError('Multi-lines cells not yet supported')

        # if table not yet existing, create it
        if table_name not in self._tables:
            self._flush_table(table_name)

        # check whether the additon is consistent with the table
        if self._tables[table_name]['has_header']:
            raise ValueError('Header already added')

        if self._tables[table_name]['cols_count'] != 0 and self._tables[table_name]['cols_count'] != len(header):
            raise ValueError('Number of cells in the header inconsistent with the number of columns of the table')

        # update the column widths
        if self._tables[table_name]['rows_count']>0:
            # some rows are already in the table, update the widths
            self._tables[table_name]['cols_widths'] = [max(a, b) for a, b in \
                zip(self._tables[table_name]['cols_widths'], [len(h) for h in header])]
        else:
            # no rows yet, define the widths from the header
            self._tables[table_name]['cols_widths'] = [len(h) for h in header]

        # all OK, add the header
        self._tables[table_name]['header'] = header
        self._tables[table_name]['has_header'] = True
        self._tables[table_name]['cols_count'] = len(header)

    def add_row(self, table_name, row):
        """
        Adds a row to a table
        Args:
            table_name(str): table to add row to
            row(str[]): list of strings
        """

        # new lines not yet supported
        if any(['\n' in c for c in row]):
            raise ValueError('Multi-lines cells not yet supported')

        # if table not yet existing, create it
        if table_name not in self._tables:
            self._flush_table(table_name)

        # check whether the additon is consistent with the table
        if self._tables[table_name]['cols_count'] != 0 and self._tables[table_name]['cols_count'] != len(row):
            raise ValueError('Number of cells in the row inconsistent with the number of columns of the table')

        # update the column widths
        if  self._tables[table_name]['has_header'] or self._tables[table_name]['rows_count']>0:
            # header or some rows are already in the table, update the widths
            self._tables[table_name]['cols_widths'] = [max(a,b) for a,b in \
                zip(self._tables[table_name]['cols_widths'], [len(c) for c in row])]
        else:
            # no rows/header yet, define the widths from this row
            self._tables[table_name]['cols_widths'] = [len(c) for c in row]

        # all OK, add the row
        self._tables[table_name]['rows'].append(row)
        self._tables[table_name]['cols_count'] = len(row)
        self._tables[table_name]['rows_count'] += 1

    def df_to_table(self, table_name, df,
                    replace_newlines=False, replace_with='; '):
        """
        Generate a full table for a given pandas' dataframe
        Args:
            table_name(str): name of the table to generate
            df(pandas.core.frame.DataFrame): dataframe
            replace_newlines(boolean): True if \n should be replaced
            replace_with(str): what to replace \n with
        """
        if table_name in self._tables:
            raise ValueError('Table under {} already existing'.format(table_name))
        if not isinstance(df, pd.core.frame.DataFrame):
            raise TypeError('Not a pandas dataframe')
        if isinstance(df.columns, pd.core.indexes.multi.MultiIndex):
            raise ValueError('Multi-index columns not supported')

        # convert cells to stirngs
        df_s = df.applymap(str)

        # replace function
        rep = lambda x : x if not replace_newlines else x.replace('\r\n','\n').replace('\n',replace_with)

        # add header
        header = [rep(c).strip() for c in list(df_s.columns)]
        self.add_header(table_name, header)

        # iterate over rows and add them
        for i in df.index:
            row = [rep(c).strip() for c in list(df_s.loc[i,:])]
            self.add_row(table_name, row)


class MdDocGenerator(CommonDocGenerator):
    """
    Class to generate Pandoc Markdown text with
    """

    def render_textblock(self, block_name):
        """
        Get the markdown string of a block
        Args:
            block_name(str): block to return the contents of
        """
        return '\n'.join(self._blocks[block_name])+'\n'

    def render_table(self, table_name):
        """
        Get the markdown string of a table
        Args:
            table_name(str): table to render
        """
        table = self._tables[table_name]
        cols_widths = table['cols_widths']
        table_list = []

        # add first grid line
        table_list.append('+'+'+'.join(['-'*w for w in cols_widths])+'+')

        # add header
        if table['has_header']:
            table_list.append('|'+'|'.join([format(c, '{}'.format(w)) for (c,w) in zip(table['header'],cols_widths)])+'|')
            table_list.append('+'+'+'.join(['='*w for w in cols_widths])+'+')

        # add rows
        for r in table['rows']:
            table_list.append('|'+'|'.join([format(c, '{}'.format(w)) for (c,w) in zip(r,cols_widths)])+'|')
            table_list.append('+'+'+'.join(['-'*w for w in cols_widths])+'+')

        return '\n'.join(table_list)+'\n'

    def render_section(self, section_name=None):
        """
        Renders a section
        Args:
            section_name(str): name of the section, if not given, the default section will be used
        """
        if section_name is None:
            section_name = self._DEFAULT_SECTION_NAME

        full_sect_str = ''

        if section_name in self._sections:
            # section exists, glue its elements
            rendfunc = lambda x: self.render_table(x['name']) if x['type'] == "table" else self.render_textblock(x['name'])
            full_sect_str =  '\n'.join([rendfunc(el) for el in self._sections[section_name]])

        # if we were rendering the default section, flush it
        if section_name == self._DEFAULT_SECTION_NAME:
            self._flush_section(section_name)

        return full_sect_str

    def h1(self, block_name, text):
        """
        Generate markdown h1 title and add it to a block
        Args:
            block_name(str): block to write to
            text(str): string to write
        """
        self._add_to_block(block_name, '')
        self._add_to_block(block_name, '# {}'.format(text))

    def h2(self, block_name, text):
        """
        Generate markdown h2 title and add it to a block
        Args:
            block_name(str): block to write to
            text(str): string to write
        """
        self._add_to_block(block_name, '')
        self._add_to_block(block_name, '## {}'.format(text))

    def h3(self, block_name, text):
        """
        Generate markdown h3 title and add it to a block
        Args:
            block_name(str): block to write to
            text(str): string to write
        """
        self._add_to_block(block_name, '')
        self._add_to_block(block_name, '### {}'.format(text))

    def paragraph(self, block_name, text):
        """
        Generate markdown paragraph text and add it to a block
        Args:
            block_name(str): block to write to
            text(str): string to write
        """
        self._add_to_block(block_name, '')
        self._add_to_block(block_name, '{}'.format(text))

    def codeblock(self, block_name, text):
        """
        Generate markdown paragraph text and add it to a block
        Args:
            block_name(str): block to write to
            text(str): string to write
        """
        self._add_to_block(block_name, '')
        self._add_to_block(block_name, '~~~~~~')
        self._add_to_block(block_name, '{}'.format(text))
        self._add_to_block(block_name, '~~~~~~')





if __name__ == '__main__':
    # just some example
    generator = MdDocGenerator()

    generator.h1('intro',  'About')
    generator.paragraph('intro',  'This document lists famous actors.')
    print(generator.render_textblock('intro'))

    generator.add_header('actors', ['name', 'surname'])
    generator.add_row('actors', ['john', 'travolta'])
    generator.add_row('actors', ['will', 'smith'])
    generator.add_row('actors', ['tom', 'hanks'])
    print(generator.render_table('actors'))



