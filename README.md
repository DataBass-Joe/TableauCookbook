# TableauCookbook
This is the source code for the python project that adds a DEFINITIONS datasource via drag and drop

It uses [PyInstaller](https://www.pyinstaller.org/index.html) to create the TableauModifier.EXE file.

The underlying code works by

  1. Taking in a Workbook (twb or twbx) using sys.argv[1]
  2. Using the [tableaudocumentapi library](https://github.com/tableau/document-api-python) to scan the workbook and create an array with all fields in use
  3. Writing a query that uses the newly created array as part of it's WHERE statement
  4. Using the [tableau_tools libarary](https://github.com/bryantbhowell/tableau_tools) to create a datasource called "DEFINITIONS" using the query
  5. Create a copy of the original workbook called "Modified Workbook" and add the "DEFINITIONS" datasource to it.
  
Known Bugs:

  * Occasionally it will fail to read the initial workbook, I believe this is a bug with the [tableaudocumentapi library](https://github.com/tableau/document-api-python).
