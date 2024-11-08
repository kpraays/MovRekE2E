### how to run the tests?

**if you want to run only the data processing unit tests**
from team-4/app/tests, run the following command
`pytest ./data_processing --html-report=./report/report.html`

The report creator is added to pytest as a plugin. If the requirements.txt is correctly installed on your system then the html report should be created automatically when you run tests with pytest.

Also, note that pytests can run the tests created using unittests unless there is a specific setup and tear down function on class objects.

**if you want to run unit tests using pytest**
Pytest will automatically pick all tests in a directory if they adhere to the conventions. You just need to give the directory location and recursive look up will do the remaining job. Giving a top level directory with modules which we have not created may not be a good idea because it will also start running their tests which we dont want.

**how to run tests then?**
execute this command: (inside the test directory)
`pytest . --html-report=./report/report.html`


