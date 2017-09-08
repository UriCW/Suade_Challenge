import unittest
from models import *
from sqlalchemy.orm import sessionmaker

#A test class the check the model with
class TestModel(unittest.TestCase):
    Session = sessionmaker()

    #Populate the users table.
    def populate_users(self):
        session=self.Session()
        session.add_all([
                User(name='Adam Smith'),
                User(name='Karl Marx'),
                User(name='Emma Goldman'),
            ])
        session.commit()

    #Populate the loans table
    def populate_loans(self):
        session=self.Session()
        session.add_all([
                Loan(currency='JPY',balance=1000.50),
                Loan(currency='GBP',balance=87.79),
                Loan(currency='USD',balance=100000000000.99),
                Loan(currency='USD',balance=170000000.99)
            ])
        session.commit()

    #Query for related entries and populate the reports table
    def populate_reports(self):
        session=self.Session()
        
        #Get users
        adam,karl,emma=session.query(User)
        #Get loans
        loan1,loan2,loan3,loan4=session.query(Loan)
        
        #Some test files for report body
        WealthOfNations=open("test_files/AdamSmith_WealthOfNations.txt",'rb').read()
        Capital=open("test_files/KarlMarx_Capital.txt",'rb').read()
        MyDisillusionmentInRussia=open("test_files/EmmaGoldman_MyDisillusionmentInRussia.txt",'rb').read()

        
        report1 = Report(title='The Wealth Of Nations',body='WealthOfNations',author=adam.id,loans=[loan1,loan2])
        report2 = Report(title='Capital',body='Capital' ,author=karl.id,loans=[loan2,loan3])
        report3 = Report(title='My Disillusionment With Russia',body='MyDisillusionmentInRussia' ,author=emma.id,loans=[loan3,loan4])

        session.add_all([report1,report2,report3])
        session.commit()

    #Populate the currency conversion (to GBP) table
    def populate_conversion(self):
        session=self.Session()
        session.add_all([
            Conversion(currency="USD",value=0.76),
            Conversion(currency="JPY",value=0.007),
            Conversion(currency="GBP",value=1),
        ])
        session.commit()

    #Seed the database
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        self.Session.configure(bind=engine)
       
        User.metadata.create_all(engine)
        self.populate_users()
    
        Loan.metadata.create_all(engine)
        self.populate_loans()

        Report.metadata.create_all(engine)
        self.populate_reports()
        
        Conversion.metadata.create_all(engine)
        self.populate_conversion()

    #Test table relationships work as expected
    def test_relationships(self):
        session=self.Session()
        report1,report2,report3=session.query(Report)
        user1,user2,user3 = session.query(User)
        loan1,loan2,loan3,loan4=session.query(Loan)
        assert report1.author==user1.id and user1.name=='Adam Smith'
        assert report2.author==user2.id and user2.name=='Karl Marx'
        assert report3.author==user3.id and user3.name=='Emma Goldman'
        assert loan1 and loan2 in report1.loans
        assert loan2 and loan3 in report2.loans
        assert loan3 and loan4 in report3.loans

    #Show a reports containing a given loan
    def test_show_loan_in_report(self):
        session=self.Session()
        loan=session.query(Loan)[2] #the desired loan to check
        for report in loan.reports:
            print "loan:%s,%s %s , report: %s"%(loan.id,loan.currency,loan.balance, report.title)
        
    #Show total of all loans in a given report, in GBP
    def test_show_report_sum(self):
        session=self.Session()
        report=session.query(Report)[1] #the desired report to check
        total=0
        for loan in report.loans:
            total+=Conversion.convert(session,loan.currency,loan.balance)
        print "Report: {0}, total: {1:.2f} GBP".format(report.title,total)
        
if __name__=="__main__":
    unittest.main()
