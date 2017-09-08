A basic loans reporting system to demonstrate my coding abilities.
The code uses SQLAlchemy and unittest.

The model.py contains the 3 required ORM models: User,Loan,Report.
It also contains a relationship reference table to map between reports and loans.
In addition, it contains a currency conversion helper table to convert the loan's currency into GBP.

The tests.py contains a test class TestModel.
This seeds the database with some data (In function setUp() ), and preforms the required tests.
All database tables in tests are stored as an sqlite database in memory.

to run all the tests execute:
$python tests.py

or to run a specific test, execute any of:
$python tests.py TestModel.test_relationships
$python tests.py TestModel.test_show_loan_in_report
$python tests.py TestModel.test_show_report_sum
