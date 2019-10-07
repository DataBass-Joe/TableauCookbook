from tableau_tools.tableau_documents import *
from tableaudocumentapi import *
import sys

droppedFile = sys.argv[1]
workbook_filename = droppedFile


print(workbook_filename)

# -------print(workbook_filename)-------------------------------------------------------- #
# Create a query dynamically based off of queries in the workbook #
# --------------------------------------------------------------- #

sourceWB = Workbook(filename=workbook_filename)

pivot_definition_array = []

definition_array = []

field_array = []

for datasource in sourceWB.datasources:
    for count, field in enumerate(datasource.fields.values()):
        if field.worksheets:
            for datasourceTDS in sourceWB.datasources:
                sourceTDS = Datasource.from_connections(caption=datasourceTDS.caption,
                                                        connections=datasourceTDS.connections)
                for datasource_field in sourceTDS.fields:
                    if datasource_field == field.id and datasource_field not in field_array:
                        field_array.append(datasource_field)
                        datasource_field_no_brackets = datasource_field[1:-1]
                        clean_datasource_field = datasource_field_no_brackets.split(' ')
                        pivot_definition_array.append("''" + clean_datasource_field[0] + "''")
                        definition_array.append("'" + clean_datasource_field[0] + "'")

pivot_definition_list = ', '.join(map(str, pivot_definition_array))
definition_list = ', '.join(map(str, definition_array))


pivot_query = u"SELECT * FROM TABLE(COOKBOOK.PIVOT('SELECT FIELD_DESCRIBED, PUBLIC_DEFINITION FROM " \
        u"DB_CONNECTION_DEFINITION_VW WHERE COLUMN_NAME IN (" + pivot_definition_list + ")')) "

normal_query = "SELECT DISTINCT FIELD_DESCRIBED, PUBLIC_DEFINITION FROM DB_CONNECTION_DEFINITION_VW WHERE COLUMN_NAME IN (" \
         + definition_list + ") "

print(pivot_query)


# --------------------------------------------------------------- #
# Create a Definition Datasource then add the query as Custom SQL #
# --------------------------------------------------------------- #

tab_file = TableauFile(workbook_filename)

new_tab_file = TableauFile("test.tds", create_new=True, ds_version=u'10.3')

new_tableau_document = new_tab_file.tableau_document

def_datasources = new_tableau_document.datasources
def_datasource = def_datasources[0]
def_datasource.add_new_connection(ds_type=u'oracle',
                                  server=u'prod01-scan.sys.utah.edu',
                                  db_or_schema_name="STUDENT_DM")

new_data_source = def_datasource.connections[0]
new_data_source.port = "1521"
new_data_source.service = "biprusr"


new_tableau_document.xml.attrib['name'] = "DEFINITIONS"

def_datasource.set_first_custom_sql(pivot_query,
                                    table_alias="pivot_def",
                                    connection=new_data_source.connection_name)

tab_file.tableau_document.datasources.append(new_tableau_document)
tab_file.save_new_file(r'Modified Workbook')