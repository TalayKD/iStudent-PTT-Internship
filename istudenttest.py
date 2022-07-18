import service
import unittest

### Testing Client Services ###

class TestClientMethods(unittest.TestCase):

    @classmethod
    def setUpClass(TestClientMethods):
        # create table if it does not exist
        service.createClientTable()

        # clear tables first for testing
        service.deleteClient() 

    @classmethod
    def tearDownClass(TestClientMethods):
        # delete all test cases from table
        service.deleteClient()

        # initialize table with one client
        service.initClientTable()

    def test_insert_one(self):
        service.insertClientRow(["name", "email", "password"], ["test", "test2435@gmail.com", "testpassword"])
        data = service.getClientRow("email", "test2435@gmail.com")

        self.assertEqual(data[0][1], "test")
        self.assertEqual(data[0][2], "test2435@gmail.com")
        self.assertEqual(data[0][3], "testpassword")

    def test_insert_two(self):
        service.insertClientRow(["name", "email"], ["nopassword", "nopassword@gmail.com"])
        data = service.getClientRow("name", "nopassword")

        self.assertEqual(data[0][1], "nopassword")
        self.assertEqual(data[0][2], "nopassword@gmail.com")

    def test_update(self):
        service.insertClientRow(["name", "email", "password"], ["update", "update@gmail.com", "updateme"])
        data = service.getClientRow("email", "update@gmail.com")

        self.assertEqual(data[0][1], "update")
        self.assertEqual(data[0][2], "update@gmail.com")
        self.assertEqual(data[0][3], "updateme")


        updatedData = {"name" : "updatedName", "password" : "updatedPassword"}
        service.updateClient(updatedData, "email", "update@gmail.com")
        data = service.getClientRow("email", "update@gmail.com")

        self.assertEqual(data[0][1], "updatedName")
        self.assertEqual(data[0][2], "update@gmail.com")
        self.assertEqual(data[0][3], "updatedPassword")


    def test_delete(self):
        service.insertClientRow(["name", "email", "password"], ["deleteme", "deleteme@gmail.com", "popsicle"])

        initialTotal = service.getClientAll()
        initialCount = len(initialTotal)

        # we will also check count with the get column function
        initTotal = service.getClientCol("email")
        initCount = len(initTotal)

        self.assertEqual(initialCount, initCount)

        data = service.getClientRow("email", "deleteme@gmail.com")
        self.assertEqual(data[0][1], "deleteme")
        self.assertEqual(data[0][2], "deleteme@gmail.com")
        self.assertEqual(data[0][3], "popsicle")

        service.deleteClient("email", "deleteme@gmail.com")
        finalTotal = service.getClientAll()
        finalCount = len(finalTotal)
        self.assertEqual(finalCount, initialCount - 1)

        # check count with get column function
        finTotal = service.getClientCol("email")
        finCount = len(finTotal)

        self.assertEqual(finCount, finalCount)


### Testing Education Services ###

class TestEducationMethods(unittest.TestCase):

    @classmethod
    def setUpClass(TestEducationMethods):

        # create and clear student table first in case it references education
        service.createStudentTable()
        service.deleteStudent()

        # create table if it does not exist
        service.createEducationTable()

        # clear tables first for testing
        service.deleteEducation() 

    @classmethod
    def tearDownClass(TestEducationMethods):
        # delete all test cases from table
        service.deleteEducation()

        # initialize table with 4 educational degrees
        service.initEducationTable()

    def test_insert(self):
        service.insertEducationRow(["degree", "credits", "duration", "earnings"], ["elementary", 30, 6, 20000])
        data = service.getEducationRow("degree", "elementary")

        self.assertEqual(data[0][1], "elementary")
        self.assertEqual(data[0][2], 30)
        self.assertEqual(data[0][3], 6)
        self.assertEqual(data[0][4], 20000)

    def test_update(self):
        service.insertEducationRow(["degree", "credits", "duration", "earnings"], ["primary", 50, 4, 35000])
        data = service.getEducationRow("degree", "primary")

        self.assertEqual(data[0][1], "primary")
        self.assertEqual(data[0][2], 50)
        self.assertEqual(data[0][3], 4)
        self.assertEqual(data[0][4], 35000)

        updatedData = {"degree" : "secondary", "credits" : 100, "earnings" : 37000}
        service.updateEducation(updatedData, "degree", "primary")
        data = service.getEducationRow("degree", "secondary")

        self.assertEqual(data[0][1], "secondary")
        self.assertEqual(data[0][2], 100)
        self.assertEqual(data[0][3], 4)
        self.assertEqual(data[0][4], 37000)


    def test_delete(self):
        service.insertEducationRow(["degree", "credits", "duration", "earnings"], ["associate", 80, 6, 102034])

        initialTotal = service.getEducationAll()
        initialCount = len(initialTotal)

        # we will also check count with the get column function
        initTotal = service.getEducationCol("degree")
        initCount = len(initTotal)

        self.assertEqual(initialCount, initCount)

        data = service.getEducationRow("degree", "associate")
        self.assertEqual(data[0][1], "associate")
        self.assertEqual(data[0][2], 80)
        self.assertEqual(data[0][3], 6)
        self.assertEqual(data[0][4], 102034)

        service.deleteEducation("degree", "associate")
        finalTotal = service.getEducationAll()
        finalCount = len(finalTotal)
        self.assertEqual(finalCount, initialCount - 1)

        # check count with get column function
        finTotal = service.getEducationCol("degree")
        finCount = len(finTotal)

        self.assertEqual(finCount, finalCount)


### Testing Student Services ###

class TestStudentMethods(unittest.TestCase):

    @classmethod
    def setUpClass(TestStudentMethods):

        # create table if it does not exist
        service.createStudentTable()
        # clear tables first for testing
        service.deleteStudent() 

        # set up Education table because we must pull data from it
        service.createEducationTable()
        service.deleteEducation()
        service.initEducationTable()

        data = service.getEducationCol("education_id")
        TestStudentMethods.edID = []
        for d in data:
            TestStudentMethods.edID.append(d[0])

    @classmethod
    def tearDownClass(TestStudentMethods):
        # delete all test cases from table
        service.deleteStudent()


    def test_insert(self):
        service.insertStudentRow(["name", "nationality", "age", "gender", "grade", "education_id"], ["Bob", "American", 67, "Male", 80, self.edID[3]])
        data = service.getStudentRow("name", "Bob")

        self.assertEqual(data[0][1], "Bob")
        self.assertEqual(data[0][2], "American")
        self.assertEqual(data[0][3], 67)
        self.assertEqual(data[0][4], "Male")
        self.assertEqual(data[0][5], 80)
        self.assertEqual(data[0][6], self.edID[3])


    def test_update(self):
        service.insertStudentRow(["name", "nationality", "age", "gender", "grade", "education_id"], ["Jessica", "Korean", 48, "Female", 39, self.edID[2]])
        data = service.getStudentRow("name", "Jessica")

        self.assertEqual(data[0][1], "Jessica")
        self.assertEqual(data[0][2], "Korean")
        self.assertEqual(data[0][3], 48)
        self.assertEqual(data[0][4], "Female")
        self.assertEqual(data[0][5], 39)
        self.assertEqual(data[0][6], self.edID[2])

        updatedData = {"name" : "Jessie", "nationality" : "Japanese", "age" : 37, "education_id" : self.edID[0] }
        service.updateStudent(updatedData, "name", "Jessica")
        data = service.getStudentRow("name", "Jessie")

        self.assertEqual(data[0][1], "Jessie")
        self.assertEqual(data[0][2], "Japanese")
        self.assertEqual(data[0][3], 37)
        self.assertEqual(data[0][4], "Female")
        self.assertEqual(data[0][5], 39)
        self.assertEqual(data[0][6], self.edID[0])


    def test_delete(self):
        service.insertStudentRow(["name", "nationality", "age", "gender", "grade", "education_id"], ["Sam", "Mexican", 19, "Female", 89, self.edID[1]])

        initialTotal = service.getStudentAll()
        initialCount = len(initialTotal)

        # we will also check count with the get column function
        initTotal = service.getStudentCol("name")
        initCount = len(initTotal)

        self.assertEqual(initialCount, initCount)

        data = service.getStudentRow("name", "Sam")
        self.assertEqual(data[0][1], "Sam")
        self.assertEqual(data[0][2], "Mexican")
        self.assertEqual(data[0][3], 19)
        self.assertEqual(data[0][4], "Female")
        self.assertEqual(data[0][5], 89)
        self.assertEqual(data[0][6], self.edID[1])

        service.deleteStudent("name", "Sam")
        finalTotal = service.getStudentAll()
        finalCount = len(finalTotal)
        self.assertEqual(finalCount, initialCount - 1)

        # check count with get column function
        finTotal = service.getStudentCol("name")
        finCount = len(finTotal)

        self.assertEqual(finCount, finalCount)

if __name__ == '__main__':
    unittest.main()