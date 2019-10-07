# -*- coding: utf-8 -*-

from tableau_tools.tableau_rest_api import *
from tableau_tools import *
from tableau_tools.tableau_documents import *

t_file = TableauFile('/Users/bhowell/PycharmProjects/Test for Captioning.twb')
dses = t_file.tableau_document.datasources  # type: list[TableauDatasource]
english_dict = {'{token1}': 'category', '{token2}': 'sub-category'}
german_dict = {'{token1}': 'Kategorie', '{token2}': 'Unterkategorie'}
for ds in dses:
    ds.columns.translate_captions(english_dict)
new_eng_filename = t_file.save_new_file('English Version')