import pymysql
import Backend
from datetime import datetime
connection = pymysql.connect(host="localhost",
                                user="root",
                                password="24242424",
                                charset='utf8',
                                db = 'beltline',
                                cursorclass=pymysql.cursors.DictCursor)
cur = connection.cursor()

'''
####### THINGS TO STILL FIX #############
- GUI 15 high range filter acts weird with 2 vs 2.00



#########################################
'''

### Initializing All Views ###
#PLACE ANY CREATE VIEW STATEMENTS HERE#
## 4/16 Grant changed Init Views to work on GUI 15 ##
def InitViews(username):
    viewList = []
    takeTransitViewQ = "CREATE VIEW TakeTransitTable AS SELECT A.TransitRoute, A.TransitType, A.TransitPrice, C.sitename from beltline.TRANSIT AS A NATURAL JOIN beltline.CONNECT AS C"
    viewList.append(takeTransitViewQ)
    transitHistoryQ = "CREATE VIEW TransitHistory AS SELECT * FROM beltline.taketransit INNER JOIN transit using (TransitType, TransitRoute)"
    viewList.append(transitHistoryQ)
    manageStaffQ1 = "create view StaffCount as select count(StaffUsername) as EventShifts, StaffUsername from beltline.event natural join beltline.assign_to  group by StaffUsername"
    viewList.append(manageStaffQ1)
    manageStaffQ2 = "create or replace view StaffCountNames as select StaffUsername, Firstname, Lastname, EventShifts from beltline.staffcount, beltline.user where StaffUsername = Username"
    viewList.append(manageStaffQ2)
    manageStaffQ3 = "create or replace view ManageStaff as select EventName, SiteName, StartDate, EndDate, StaffUsername, Firstname, Lastname, EventShifts from beltline.Assign_To natural join beltline.event natural join StaffCountNames"
    viewList.append(manageStaffQ3)
    manageUserQ = "CREATE VIEW ManageUser AS (SELECT username, userType, count(*) AS emails, status  status FROM user Natural Join USEREMAIL where  UserType = 'User' OR UserType = 'Visitor' GROUP BY Username) UNION (SELECT username, employeeType, count(*) AS emails, status FROM user INNER JOIN  employee USING (Username) Natural Join useremail GROUP BY Username)";
    viewList.append(manageUserQ)
    staffScheduleQ = "CREATE OR REPLACE VIEW StaffViewSchedule AS (SELECT EventName, StartDate, EndDate, SiteName, Description, count(*) as 'StaffCount', EventPrice FROM beltline.ASSIGN_TO Natural join beltline.event group by EventName, StartDate, EndDate, SiteName)"
    viewList.append(staffScheduleQ)
    AdminManageSiteViewQ = "CREATE VIEW SiteTable AS SELECT SiteName, Concat(Firstname, ' ',Lastname) as Manager, OpenEveryday FROM site INNER JOIN user on Site.managerusername = user.username"
    viewList.append(AdminManageSiteViewQ)
    AdminManageSiteManagerList = "CREATE view ManagerNameMS as select Concat(Firstname, ' ', Lastname) as ManagerName, Username from beltline.user natural join beltline.employee where EmployeeType = 'Manager'"
    viewList.append(AdminManageSiteManagerList)
    VisitHistoryQ = "CREATE OR REPLACE VIEW VisitHistory as (select VisitSiteDate as DateVisited, NULL as EventName, SiteName, 0 as Price from Visit_Site where VisitorUsername = '{}')  UNION ALL  (select VisitEventDate as DateVisited, EventName, SiteName, EventPrice from beltline.Visit_Event natural join beltline.event where VisitorUsername = '{}') order by DateVisited".format(username, username)
    viewList.append(VisitHistoryQ)
    AdminManageTransitView1 = "CREATE or replace view ConnectedSitesTable as select TransitType, TransitRoute, count(*) as ConnectedSites from beltline.connect group by TransitType, TransitRoute"
    viewList.append(AdminManageTransitView1)
    AdminManageTransitView2 ="CREATE or replace view TransitANDTakeTransit2 as select transit.TransitRoute, transit.TransitType, transit.TransitPrice, count(*) as TransitsLogged from beltline.TAKETRANSIT, beltline.transit where taketransit.TransitRoute = transit.TransitRoute and taketransit.TransitType= Transit.TransitType group by TransitType, TransitRoute"
    viewList.append(AdminManageTransitView2)
    AdminManageTransitViewInt = "CREATE OR REPLACE VIEW transitandtaketransit AS (SELECT * FROM transitandtaketransit2) UNION (SELECT TransitRoute, TransitType, TransitPrice, 0 as TransitCount FROM transit WHERE (TransitType, TransitRoute) NOT IN (SELECT TransitType, TransitRoute FROM transitandtaketransit2));"
    viewList.append(AdminManageTransitViewInt)
    AdminManageTransitView3 = "CREATE or replace view AdminManageTransit as select TransitANDTakeTransit.TransitRoute, TransitANDTakeTransit.TransitType, TransitPrice, ConnectedSites, TransitsLogged from beltline.TransitANDTakeTransit, ConnectedSitesTable where TransitANDTakeTransit.TransitRoute = ConnectedSitesTable.TransitRoute and TransitANDTakeTransit.TransitType = ConnectedSitesTable.TransitType"
    viewList.append(AdminManageTransitView3)
    AdminManageTransitView4 = "CREATE or replace View AMTwithSite as select SiteName, A.TransitRoute, A.TransitType, TransitPrice, ConnectedSites, TransitsLogged from beltline.AdminManageTransit as A NATURAL JOIN beltline.connect as B where A.TransitRoute = B.TransitRoute and A.TransitType = B.TransitType"
    viewList.append(AdminManageTransitView4)
    SiteReport11Q = 'CREATE or REPLACE view EventVisitCount as  (select b.EventName, b.SiteName, b.StartDate, EventPrice, VisitEventDate, count(VisitorUsername) as VisitorCount, count(VisitorUsername)* EventPrice as Revenue  from Visit_Event as a right join Event as b on a.SiteName = b.SiteName and a.EventName = b.EventName and a.StartDate = b.StartDate group by b.StartDate, b.SiteName, b.EventName, VisitEventDate)'
    viewList.append(SiteReport11Q)
    SiteReport2q = "CREATE or Replace view allSites_EventvisitCount as select Site.SiteName, EventName, StartDate, IfNull(EventPrice,0) as EventPrice, VisitEventDate, ifNuLL(VisitorCount,0) as VisitorCount, ifNULL(Revenue,0) as Revenue from EventVisitCount right join beltline.site on EventVisitCount.SiteName = Site.SiteName"
    viewList.append(SiteReport2q)
    SiteReport1Q = "CREATE or replace view Event_Staffcounts as select a.EventName, a.SiteName, a.StartDate, EventPrice, VisitEventDate, VisitorCount, Revenue, count(a.StartDate) as StaffCount from allSites_EventVisitCount as a left join Assign_to as b on a.EventName = b.EventName and  a.SiteName= b.SiteName and a.StartDate=b.StartDate group by a.StartDate, a.SiteName, a.EventName, VisitEventDate, VisitorCount, Revenue"
    viewList.append(SiteReport1Q)
    SiteReport3q = "CREATE or replace view SiteVisitCount as  select SiteName, VisitSiteDate, count(VisitorUsername) as VisitorSiteCount from beltline.visit_site group by SiteName, VisitSiteDate"
    viewList.append(SiteReport3q)
    ManageEventQ11 = 'CREATE OR REPLACE VIEW StaffViewSchedule3 AS SELECT EventName, StartDate, EndDate, SiteName, Description, count(*) as "StaffCount", EventPrice FROM beltline.ASSIGN_TO Natural join beltline.event group by EventName, StartDate, EndDate, SiteName '
    viewList.append(ManageEventQ11)
    ManageEventQ1 = 'CREATE OR REPLACE view TotalEventVisits as Select event.EventName, event.SiteName, event.StartDate, VisitEventDate, EventPrice, count(VisitorUsername) as EventVisits, count(VisitorUsername) *EventPrice as Profit  from beltline.event left join beltline.VISIT_EVENT on event.SiteName = Visit_event.SiteName and event.StartDate = Visit_event.StartDate and event.EventName = Visit_event.EventName group by EventName, SiteName, VisitEventDate, EventPrice, StartDate'
    viewList.append(ManageEventQ1)
    ManageEventQ2 = 'CREATE OR REPLACE view ManageEvent as  select TotalEventVisits.SiteName, TotalEventVisits.EventName, TotalEventVisits.StartDate,  VisitEventDate, TotalEventVisits.EventPrice, (Staffviewschedule3.EndDate-Staffviewschedule3.StartDate) as Duration, StaffCount, EventVisits, Profit, Description from beltline.TotalEventVisits inner join beltline.staffviewschedule3 on TotalEventVisits.EventName = staffviewschedule3.EventName and TotalEventVisits.SiteName = staffviewschedule3.SiteName and TotalEventVisits.StartDate = staffviewschedule3.StartDate '
    viewList.append(ManageEventQ2)
    ManageEventQ3 = 'CREATE OR REPLACE view ManageEvent as  select TotalEventVisits.SiteName, TotalEventVisits.EventName, TotalEventVisits.StartDate,  VisitEventDate, TotalEventVisits.EventPrice, (Staffviewschedule3.EndDate-Staffviewschedule3.StartDate) as Duration, StaffCount, EventVisits, Profit, Description from beltline.TotalEventVisits inner join beltline.staffviewschedule3 on TotalEventVisits.EventName = staffviewschedule3.EventName and TotalEventVisits.SiteName = staffviewschedule3.SiteName and TotalEventVisits.StartDate = staffviewschedule3.StartDate'
    viewList.append(ManageEventQ3)
    Q123 = 'CREATE OR REPLACE VIEW DailyEvents as SELECT EventName, Event.EventPrice,Visit_Event.VisitEventDate, Event.startDate FROM beltline.Event NATURAL JOIN beltline.Visit_Event '
    viewList.append(Q123)
    MaggieWHY1 = "CREATE OR REPLACE VIEW VISITORUSERNAMES AS SELECT Username FROM beltline.USER where UserType like '%Visitor%'"
    viewList.append(MaggieWHY1)
    MaggieWHY2 = "CREATE OR REPLACE VIEW HASNOTVISITED AS SELECT * FROM VISITORUSERNAMES WHERE Username NOT IN (SELECT DISTINCT VisitorUsername FROM beltline.VISIT_EVENT)"
    viewList.append(MaggieWHY2)
    MaggieWHY3 = "CREATE OR REPLACE VIEW NOTVISITORS33 AS SELECT Username, EventName, SiteName, StartDate, 0 as MyVisits FROM HASNOTVISITED JOIN beltline.EVENT"
    viewList.append(MaggieWHY3)
    MaggieWHY4 = "CREATE OR REPLACE VIEW ALLVISITORS AS select  * from VISITORUSERNAMES AS A LEFT OUTER JOIN beltline.VISIT_EVENT AS B ON A.Username=B.VisitorUsername"
    viewList.append(MaggieWHY4)
    MaggieWHY5 = "CREATE OR REPLACE VIEW Screen33A AS select VisitorUsername, EventName, SiteName, StartDate, count(*) as MyVisits from beltline.VISIT_EVENT group by EventName, SiteName, StartDate, VisitorUsername"
    viewList.append(MaggieWHY5)
    MaggieWHY6 = "CREATE OR REPLACE VIEW TotalScreen33A AS (SELECT VisitorUsername, EventName, SiteName, StartDate, MyVisits FROM Screen33A) UNION ALL (SELECT Username, EventName, SiteName, StartDate, MyVisits FROM NOTVISITORS33)"
    viewList.append(MaggieWHY6)
    MaggieWHY7 = "CREATE VIEW B AS SELECT EventName, StartDate, SiteName, count(*) AS TotalVisits2 FROM beltline.VISIT_EVENT GROUP BY EventName, StartDate, SiteName"
    viewList.append(MaggieWHY7)
    MaggieWhy8 = "CREATE OR REPLACE VIEW ANOTHERVIEW AS SELECT A.EventName, A.StartDate, A.SiteName, A.EndDate, A.Capacity,A.Description, A.EventPrice, IFNULL(bee.TotalVisits2,0) AS TotalVisits, IFNULL(Capacity-bee.TotalVisits2,0) as TicketsRemaining FROM beltline.EVENT AS A LEFT OUTER JOIN B AS bee ON A.EventName=bee.EventName and A.StartDate=bee.StartDate and A.SiteName = bee.SiteName"
    viewList.append(MaggieWhy8)
    MaggieWHY9 = "CREATE OR REPLACE VIEW IDK AS SELECT A.EventName, A.StartDate, A.SiteName, A.EndDate, A.Capacity,A.Description, A.EventPrice, B.VisitorUsername FROM beltline.EVENT AS A CROSS JOIN  TotalScreen33A AS B"
    viewList.append(MaggieWHY9)
    MaggieWhy10 ="CREATE OR REPLACE VIEW STILLATSCHELLER AS SELECT A.EventName, A.StartDate, A.SiteName, A.EndDate, A.Capacity, A. Description, A.EventPrice, A.VisitorUsername, IFNULL(B.MyVisits,0) AS MyVisits FROM IDK as A LEFT OUTER JOIN TotalScreen33A as B ON A.VisitorUsername =B.VisitorUsername and A.EventName=B.EventName and A.StartDate=B.StartDate and A.SiteName=B.SiteName"
    viewList.append(MaggieWhy10)
    Finally = "CREATE OR REPLACE VIEW FINALSCREEN33 AS SELECT VisitorUsername, EventName, SiteName, StartDate, EventPrice, TicketsRemaining, TotalVisits, MyVisits, Description FROM STILLATSCHELLER NATURAL JOIN ANOTHERVIEW"
    viewList.append(Finally)
    Finally2 = "CREATE or replace view THISISTHEFINALSCREEN33 as SELECT DISTINCT * FROM FINALSCREEN33 WHERE VisitorUsername=\"{}\"".format(username)
    viewList.append(Finally2)
    Screen27Q = "CREATE or replace  view AssignedStaff as select StaffUsername, concat(c.Firstname, " ", c.Lastname) as StaffName, a.EventName, b.StartDate, EndDate, a.SiteName from beltline.assign_to as a inner join beltline.event as b inner join beltline.User as c where a.EventName = b.EventName and a.StartDate = b.StartDate and a.StaffUsername = c.Username"
    aaa = "CREATE OR REPLACE VIEW SCREEN35B AS select SiteName, count(*) as TotalVisits  from beltline.VISIT_EVENT NATURAL JOIN beltline.VISIT_SITE  group by SiteName "
    viewList.append(aaa)
    bbb = "CREATE OR REPLACE VIEW SCREEN35A AS select SiteName, OpenEveryday, count(*) as EventCount from beltline.EVENT NATURAL JOIN beltline.SITE  group by SiteName "
    viewList.append(bbb)
    viewList.append(Screen27Q)
    for view in viewList:
        try:
            print("attempting to" + view[0:30])
            cur.execute(view)
            print("view created")
        except:
            print("this view already exists or failed to create")
### END INITIALIZING VIEWS
#
#
#
#
#
#
#
#### Screen 1 ####
def login(email, password):
    loginQ = "SELECT EXISTS (SELECT Email, Password FROM user INNER JOIN useremail USING (username) WHERE Email = '{}' AND Password = '{}')".format(email, password)
    loginQKey = "EXISTS (SELECT Email, Password FROM user INNER JOIN useremail USING (username) WHERE Email = '{}' AND Password = '{}')".format(email, password)
    cur.execute(loginQ)
    exists = cur.fetchone()
    if exists[loginQKey]:
        userTypeQ = "SELECT Usertype FROM user inner join useremail using (username) WHERE Email = '{}' AND Password = '{}'".format(email, password)
        userTypeQKey = "Usertype FROM user  WHERE Email = '{}' AND Password = '{}')".format(email, password)
        cur.execute(userTypeQ)
        userType = cur.fetchone()
        userType = userType['Usertype']
        if userType == 'User' or userType == 'Visitor' or userType == 'Master':
            return (exists, userType)
        else:
            usernameQ = "SELECT username FROM useremail where email = '{}'".format(email)
            cur.execute(usernameQ)
            username = cur.fetchone()
            username = username['username']
            employeeTypeQ = "SELECT EmployeeType FROM employee where username = '{}'".format(username)
            cur.execute(employeeTypeQ)
            employeeType = cur.fetchone()
            employeeType = employeeType['EmployeeType']
            return(exists, userType, employeeType)
    else:
        return exists[loginQKey]

def getUsername(email):
    usernameQ = "SELECT username FROM useremail where email = '{}'".format(email)
    cur.execute(usernameQ)
    username = cur.fetchone()
    return username['username']

### Added in by Chandler 4/15#######
def checkemail(email):
        emailQ = "SELECT EXISTS (SELECT Email from beltline.USEREMAIL where Email = '{}')".format(email)
        cur.execute(emailQ)
        emailexists = cur.fetchone()
        return emailexists["EXISTS (SELECT Email from beltline.USEREMAIL where Email = '{}')".format(email)]
### End GUI 1 ###
#
#
#
#
#
#
#
#
#
#### Added in by Chandler 4/15######
#### Register User & Visitor Screen ####
def registerusercheck(firstname, lastname, username, password, confpassword, emaillist):
    usernameQ = "SELECT EXISTS (SELECT username from beltline.USER where username = '{}')".format(username)
    cur.execute(usernameQ)
    exists = cur.fetchone()
    if exists["EXISTS (SELECT username from beltline.USER where username = '{}')".format(username)]:
        return "This username is taken. Please select a different one."
    if Backend.checkfirstname(firstname):
        return Backend.checkfirstname(firstname)
    if Backend.checklastname(lastname):
        return Backend.checklastname(lastname)
    if Backend.checkusername(username):
        return Backend.checkusername(username)
    if Backend.checkpassword(password):
        return Backend.checkpassword(password)
    if Backend.checkconfirm(password, confpassword):
        return Backend.checkconfirm(password, confpassword)

def registeruser(firstname, lastname, username, password, emaillist):
    usertype = "User"
    adduserQ = "INSERT INTO beltline.USER (Username, Password, Status, Firstname, Lastname, UserType) VALUES (\"{}\", \"{}\", \"Pending\", \"{}\", \"{}\", \"{}\")".format(username, password, firstname, lastname, usertype)
    cur.execute(adduserQ)
    connection.commit()
    for email in emaillist:
        adduseremailQ = "INSERT INTO beltline.USEREMAIL (Username, Email) VALUES (\"{}\", \"{}\")".format(username, email)
        cur.execute(adduseremailQ)
        connection.commit()
def registervisitor(firstname, lastname, username, password, emaillist):
    usertype = "Visitor"
    adduserQ = "INSERT INTO beltline.USER (Username, Password, Status, Firstname, Lastname, UserType) VALUES (\"{}\", \"{}\", \"Pending\", \"{}\", \"{}\", \"{}\")".format(username, password, firstname, lastname, usertype)
    cur.execute(adduserQ)
    connection.commit()
    for email in emaillist:
        adduseremailQ = "INSERT INTO beltline.USEREMAIL (Username, Email) VALUES (\"{}\", \"{}\")".format(username, email)
        cur.execute(adduseremailQ)
        connection.commit()
    addvisitorQ = "INSERT INTO beltline.VISITOR (Username) VALUES (\"{}\")".format(username)
    cur.execute(addvisitorQ)
    connection.commit()
#### End User & Visitor Screen #####
#
#
#
def ToughScene():
    Q = "SELECT * FROM Site"
    cur.execute(Q)
    return cur.fetchall()
#
#
#
#
#
#### Register Employee & Employee Visitor Screen  ####
def registeremployeecheck(fname, lname, username, usertype, password, confirmPass, phone, address, city, state, zipcode, emailList):
    if registerusercheck(fname, lname, username, password, confirmPass, emailList):
        return registerusercheck(fname, lname, username, password, confirmPass, emailList)
    if Backend.checkphone(phone):
        return Backend.checkphone(phone)
    if Backend.checkcity(city):
        return Backend.checkcity(city)
    if Backend.checkzip(zipcode):
        return Backend.checkzip(zipcode)
    if Backend.checkaddress(address):
        return Backend.checkaddress(address)
    phoneQ = "SELECT EXISTS (SELECT Phone from beltline.EMPLOYEE where Phone = '{}')".format(phone)
    cur.execute(phoneQ)
    exists = cur.fetchone()
    if exists["EXISTS (SELECT Phone from beltline.EMPLOYEE where Phone = '{}')".format(phone)]:
        return "This phone number is already in our database. Please enter a different number."

def registeremployee(fname, lname, username, emptype, password, confirmPass, phone, address, city, state, zipcode, emailList):
    usertype = "Employee"
    adduserQ = "INSERT INTO beltline.USER (Username, Password, Status, Firstname, Lastname, UserType) VALUES (\"{}\", \"{}\", \"Pending\", \"{}\", \"{}\", \"{}\")".format(username, password, fname, lname, usertype)
    cur.execute(adduserQ)
    connection.commit()
    getemployeesQ = "SELECT MAX(EmployeeID) FROM beltline.EMPLOYEE"
    cur.execute(getemployeesQ)
    employeeIDS = cur.fetchone()
    empID = employeeIDS["MAX(EmployeeID)"]
    if empID < 100000000:
        empID = 100000000
    else:
        empID += 1
    for email in emailList:
        adduseremailQ = "INSERT INTO beltline.USEREMAIL (Username, Email) VALUES (\"{}\", \"{}\")".format(username, email)
        cur.execute(adduseremailQ)
        connection.commit()
    addemployeeQ = "INSERT INTO beltline.EMPLOYEE (Username, EmployeeID, Phone, EmployeeAddress, EmployeeCity, EmployeeState, EmployeeZipCode, EmployeeType) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(username, empID, phone, address, city, state, zipcode, emptype)
    cur.execute(addemployeeQ)
    connection.commit()
    if emptype == "Manager":
        addmanagerQ = "INSERT INTO beltline.MANAGER (Username) VALUES (\"{}\")".format(username)
        cur.execute(addmanagerQ)
        connection.commit()
    if emptype == "Staff":
        addstaffQ = "INSERT INTO beltline.STAFF (Username) VALUES (\"{}\")".format(username)

def registeremployeevisitor(fname, lname, username, emptype, password, confirmPass, phone, address, city, state, zipcode, emailList):
    usertype = "Employee"
    adduserQ = "INSERT INTO beltline.USER (Username, Password, Status, Firstname, Lastname, UserType) VALUES (\"{}\", \"{}\", \"Pending\", \"{}\", \"{}\", \"{}\")".format(username, password, fname, lname, usertype)
    cur.execute(adduserQ)
    connection.commit()
    getemployeesQ = "SELECT MAX(EmployeeID) FROM beltline.EMPLOYEE"
    cur.execute(getemployeesQ)
    employeeIDS = cur.fetchone()
    empID = employeeIDS["MAX(EmployeeID)"]
    if empID < 100000000:
        empID = 100000000
    else:
        empID += 1
    for email in emailList:
        adduseremailQ = "INSERT INTO beltline.USEREMAIL (Username, Email) VALUES (\"{}\", \"{}\")".format(username, email)
        cur.execute(adduseremailQ)
        connection.commit()
    addemployeeQ = "INSERT INTO beltline.EMPLOYEE (Username, EmployeeID, Phone, EmployeeAddress, EmployeeCity, EmployeeState, EmployeeZipCode, EmployeeType) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(username, empID, phone, address, city, state, zipcode, emptype)
    cur.execute(addemployeeQ)
    connection.commit()
    if emptype == "Manager":
        addmanagerQ = "INSERT INTO beltline.MANAGER (Username) VALUES (\"{}\")".format(username)
        cur.execute(addmanagerQ)
        connection.commit()
    if emptype == "Staff":
        addstaffQ = "INSERT INTO beltline.STAFF (Username) VALUES (\"{}\")".format(username)
    addvisitorQ = "INSERT INTO beltline.VISITOR (Username) VALUES (\"{}\")".format(username)
    cur.execute(addvisitorQ)
    connection.commit()

##### End Register Employee & Employee Visitor Screen #########
#
#
#
#
#
#
#
##### Screen 15 #####
# edited by grant 4/16 ##
def TakeTransitTable(table, site, transType, lowRange, highRange, orderTuple):
    if Backend.checkpriceFilter(lowRange):
        return Backend.checkpriceFilter(lowRange)
    if Backend.checkpriceFilter(highRange):
        return Backend.checkpriceFilter(highRange)
    filterCount = 0
    filterTable = []
    if site !='-ALL-':
        filterCount += 1
        filterTable.append('sitename = "{}"'.format(site))
    if transType != '-ALL-':
        filterCount += 1
        filterTable.append("TransitType = '{}'".format(transType))
    if lowRange != '':
        filterCount += 1
        filterTable.append('TransitPrice >= "{}"'.format(lowRange))
    if highRange != '':
        filterCount += 1
        filterTable.append('TransitPrice <= "{}"'.format(highRange))
    if filterCount == 0:
        takeTransitQ = "SELECT TransitRoute, TransitType, TransitPrice, count(sitename) AS siteCount FROM TakeTransitTable"
        if orderTuple == 'no order':
            takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType"
        else:
            if orderTuple[0] == 4:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY siteCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitType {}".format(orderTuple[1])
    elif filterCount == 1:
        takeTransitQ = "SELECT TransitRoute, TransitType, TransitPrice, count(sitename) AS siteCount FROM TakeTransitTable WHERE {}".format(filterTable[0])
        if orderTuple == 'no order':
            takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType"
        else:
            if orderTuple[0] == 4:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY siteCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitType {}".format(orderTuple[1])
    elif filterCount == 2:
        takeTransitQ = "SELECT TransitRoute, TransitType, TransitPrice, count(sitename) AS siteCount FROM TakeTransitTable WHERE {} AND {}".format(filterTable[0], filterTable[1])
        if orderTuple == 'no order':
            takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType"
        else:
            if orderTuple[0] == 4:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY siteCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitType {}".format(orderTuple[1])
    elif filterCount == 3:
        takeTransitQ = "SELECT TransitRoute, TransitType, TransitPrice, count(sitename) AS siteCount FROM TakeTransitTable WHERE {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType"
        else:
            if orderTuple[0] == 4:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY siteCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitType {}".format(orderTuple[1])
    elif filterCount == 4:
        takeTransitQ = "SELECT TransitRoute, TransitType, TransitPrice, count(sitename) AS siteCount FROM TakeTransitTable WHERE {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3])
        if orderTuple == 'no order':
            takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType"
        else:
            if orderTuple[0] == 4:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY siteCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                takeTransitQ = takeTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitType {}".format(orderTuple[1])
    cur.execute(takeTransitQ)
    return cur.fetchall()

def logTransit(username, transType, route, date):
    if Backend.checkdateInsert(date):
        return Backend.checkdateInsert(date)
    logTransitQ = "INSERT INTO taketransit VALUES ('{}','{}','{}','{}')".format(username, transType, route, date)
    cur.execute(logTransitQ)
    connection.commit()


def SiteComboBox():
    allSitesQ = "SELECT sitename from site"
    cur.execute(allSitesQ)
    return cur.fetchall()

####### END 15 ###############
#
#
#
#
#
#
#
#
#
##### Screen 16 #####
# edited by grant 4/19 ##
def TransitHistoryTable(table, username, route, site, transType, startDate, endDate, orderTuple):
    if Backend.checkdateFilter(startDate):
        return Backend.checkpriceFilter(startDate)
    if Backend.checkdateFilter(endDate):
        return Backend.checkpriceFilter(endDate)
    if route != '':
        if Backend.checkroute(route):
            return Backend.checkroute(route)
    filterCount = 0
    filterTable = []
    if site !='-ALL-':
        filterCount += 1
        filterTable.append('(transittype, transitroute) IN (SELECT transittype, transitroute FROM connect WHERE sitename = "{}")'.format(site))
    if route != '':
        filterCount += 1
        filterTable.append('TransitRoute = "{}"'.format(route))
    if transType != '-ALL-':
        filterCount += 1
        filterTable.append("TransitType = '{}'".format(transType))
    if startDate != '':
        filterCount += 1
        filterTable.append('TransitDate >= "{}"'.format(startDate))
    if endDate != '':
        filterCount += 1
        filterTable.append('TransitDate <= "{}"'.format(endDate))
    if filterCount == 0:
        takeTransitQ = "SELECT TransitDate, TransitRoute, TransitType, TransitPrice FROM TransitHistory WHERE Username = '{}'".format(username)
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                takeTransitQ = takeTransitQ + " ORDER BY TransitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                takeTransitQ = takeTransitQ + " ORDER BY TransitRoute {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                takeTransitQ = takeTransitQ + " ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                takeTransitQ = takeTransitQ + " ORDER BY TransitPrice {}".format(orderTuple[1])
    if filterCount == 1:
        takeTransitQ = "SELECT TransitDate, TransitRoute, TransitType, TransitPrice FROM TransitHistory WHERE Username = '{}' AND {}".format(username, filterTable[0])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                takeTransitQ = takeTransitQ + " ORDER BY TransitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                takeTransitQ = takeTransitQ + " ORDER BY TransitRoute {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                takeTransitQ = takeTransitQ + " ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                takeTransitQ = takeTransitQ + " ORDER BY TransitPrice {}".format(orderTuple[1])
    if filterCount == 2:
        takeTransitQ = "SELECT TransitDate, TransitRoute, TransitType, TransitPrice FROM TransitHistory WHERE Username = '{}' AND {} AND {}".format(username, filterTable[0], filterTable[1])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                takeTransitQ = takeTransitQ + " ORDER BY TransitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                takeTransitQ = takeTransitQ + " ORDER BY TransitRoute {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                takeTransitQ = takeTransitQ + " ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                takeTransitQ = takeTransitQ + " ORDER BY TransitPrice {}".format(orderTuple[1])
    if filterCount == 3:
        takeTransitQ = "SELECT TransitDate, TransitRoute, TransitType, TransitPrice FROM TransitHistory WHERE Username = '{}' AND {} AND {} AND {}".format(username, filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                takeTransitQ = takeTransitQ + " ORDER BY TransitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                takeTransitQ = takeTransitQ + " ORDER BY TransitRoute {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                takeTransitQ = takeTransitQ + " ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                takeTransitQ = takeTransitQ + " ORDER BY TransitPrice {}".format(orderTuple[1])
    if filterCount == 4:
        takeTransitQ = "SELECT TransitDate, TransitRoute, TransitType, TransitPrice FROM TransitHistory WHERE Username = '{}' AND {} AND {} AND {} AND {}".format(username, filterTable[0], filterTable[1], filterTable[2], filterTable[3])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                takeTransitQ = takeTransitQ + " ORDER BY TransitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                takeTransitQ = takeTransitQ + " ORDER BY TransitRoute {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                takeTransitQ = takeTransitQ + " ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                takeTransitQ = takeTransitQ + " ORDER BY TransitPrice {}".format(orderTuple[1])
    if filterCount == 5:
        takeTransitQ = "SELECT TransitDate, TransitRoute, TransitType, TransitPrice FROM TransitHistory WHERE Username = '{}' AND {} AND {} AND {} AND {} AND {}".format(username, filterTable[0], filterTable[1], filterTable[2], filterTable[3])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                takeTransitQ = takeTransitQ + " ORDER BY TransitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                takeTransitQ = takeTransitQ + " ORDER BY TransitRoute {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                takeTransitQ = takeTransitQ + " ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                takeTransitQ = takeTransitQ + " ORDER BY TransitPrice {}".format(orderTuple[1])
    cur.execute(takeTransitQ)
    return cur.fetchall()

### END GUI 16 ###
#
#
#
#
#
#
#
#
#
### Added by Chandler 4/17#############
##### Screen 17 - Manage Profile #####

def updatecheck(firstname, lastname, username, phone):
    if firstname != None and lastname != None:
        if Backend.checkfirstname(firstname):
            return Backend.checkfirstname(firstname)
        if Backend.checklastname(lastname):
            return Backend.checklastname(lastname)
    if phone != None:
        if Backend.checkphone(phone):
            return Backend.checkphone(phone)

def update(firstname, lastname, username, phone):
    updatefirstnameQ = "UPDATE beltline.USER SET Firstname = \"{}\", Lastname = \"{}\", Phone = \"{}\" WHERE Username = \"{}\"".format(firstname, lastname, phone, username)
    cur.execute(updatefirstnameQ)
    connection.commit()

def removeemail(email):
    if checkemail(email):
        deleteeemailQ = "DELETE FROM beltline.USEREMAIL WHERE Email = \"{}\"".format(email)
        cur.execute(deleteemailQ)
        cur.commit()
    else:
        pass

def showsite(username, emptype):
    if emptype == "Manager-Only" or emptype == "Manager-Visitor":
        getsiteQ = "SELECT SiteName FROM beltline.SITE WHERE ManagerUsername = \"{}\"".format(username)
        cur.execute(getsiteQ)
        exists = cur.fetchall()
        try:
            return exists[0]["SiteName"]
        except:
            return ''

def showempID(username):
    getempIDQ = "SELECT EmployeeID from beltline.EMPLOYEE WHERE Username = \"{}\"".format(username)
    cur.execute(getempIDQ)
    empID = cur.fetchone()
    return str(empID["EmployeeID"])

def showaddress(username):
    getaddressQ = "SELECT EmployeeAddress from beltline.EMPLOYEE WHERE Username = \"{}\"".format(username)
    cur.execute(getaddressQ)
    address = cur.fetchone()
    print(address)
    return address["EmployeeAddress"]


def getemails(username):
    getemailsQ = "SELECT Email from beltline.USEREMAIL WHERE Username = \"{}\"".format(username)
    cur.execute(getemailsQ)
    emails = cur.fetchall()
    emaillist = []
    for item in emails:
        emaillist.append(item["Email"])
    return emaillist


def visitorcheck(username):
    getUserTypeQ = "SELECT UserType FROM beltline.USER WHERE Username = \"{}\"".format(username)
    cur.execute(getUserTypeQ)
    vis = cur.fetchall()
    isvis = vis[0]["UserType"]
    if isvis == "Employee-Visitor":
        return 1

def updatevisitor(username):
    addvisitorQ = "INSERT INTO beltline.VISITOR (Username) VALUES (\"{}\")".format(username)
    cur.execute(addvisitorQ)
    connection.commit()
    updateUserTypeQ = "UPDATE beltline.USER UserType = \"{}\" WHERE Username = \"{}\"".format("Employee-Visitor", username)
    cur.execute(updateUserTypeQ)
    connection.commit()

#### End GUI 17 ###########
#
#
#
#
#
#
#
#
####### Screen 18 ###############

def ManageUser(table, username, usertype, status, orderTuple):
    if Backend.checkusername(username):
        return Backend.checkusername(username)
    filterCount = 0
    filterTable = []
    if username != "":
        if Backend.checkusername(username):
                return Backend.checkusername(username)
        filterCount += 1
        filterTable.append('username = "{}"'.format(username))
    if usertype != '-ALL-':
        filterCount += 1
        filterTable.append("UserType = '{}'".format(usertype, usertype))
    if status != "-ALL-":
        filterCount += 1
        filterTable.append('Status = "{}"'.format(status))
    if filterCount == 0:
        editUserQ = "SELECT username, emails, UserType, Status from ManageUser"
        if orderTuple == 'no order':
            editUserQ = editUserQ + " GROUP BY username"
        else:
            if orderTuple[0] == 4:
                editUserQ = editUserQ + " GROUP BY username ORDER BY Status \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " GROUP BY username ORDER BY UserType \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " GROUP BY username ORDER BY emails \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " GROUP BY username ORDER BY username \"{}\"".format(orderTuple[1])
    elif filterCount == 1:
        editUserQ = "SELECT username, emails, UserType, Status from ManageUser WHERE {}".format(filterTable[0])
        if orderTuple == 'no order':
            editUserQ = editUserQ + " GROUP BY username"
        else:
            if orderTuple[0] == 4:
                editUserQ = editUserQ + " GROUP BY username ORDER BY Status \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " GROUP BY username ORDER BY UserType \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " GROUP BY username ORDER BY count(*) \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " GROUP BY username ORDER BY username \"{}\"".format(orderTuple[1])
    elif filterCount == 2:
        editUserQ = "SELECT username, emails, UserType, Status from ManageUser WHERE {} AND {}".format(filterTable[0], filterTable[1])
        if orderTuple == 'no order':
            editUserQ = editUserQ + " GROUP BY username"
        else:
            if orderTuple[0] == 4:
                editUserQ = editUserQ + " GROUP BY username ORDER BY Status \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " GROUP BY username ORDER BY UserType \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " GROUP BY username ORDER BY count(*) \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " GROUP BY username ORDER BY username \"{}\"".format(orderTuple[1])
    elif filterCount == 3:
        editUserQ = "SELECT username, emails, UserType, Status from ManageUser WHERE {} AND {}".format(filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            editUserQ = editUserQ + " GROUP BY username"
        else:
            if orderTuple[0] == 4:
                editUserQ = editUserQ + " GROUP BY username ORDER BY Status \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " GROUP BY username ORDER BY UserType \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " GROUP BY username ORDER BY count(*) \"{}\"".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " GROUP BY username ORDER BY username \"{}\"".format(orderTuple[1])
    cur.execute(editUserQ)
    return cur.fetchall()

def approve(username):
    approveUserQ = "UPDATE beltline.USER SET Status = \"{}\" WHERE username = \"{}\"".format("Approved", username)
    cur.execute(approveUserQ)
    connection.commit()

def decline(username):
    thecheckQ = "SELECT Status FROM beltline.USER WHERE username = \"{}\"".format(username)
    cur.execute(thecheckQ)
    approved= cur.fetchall()[0]["Status"]
    if approved == "Approved":
        return "You cannot decline an approved account"
    else:
        declineUserQ = "UPDATE beltline.USER SET Status = \"Declined\" WHERE username = \"{}\"".format(username)
        cur.execute(declineUserQ)
        connection.commit()

#### End GUI 18 ######
#
#
#
#
#
#
#
#
#
#
######## Screen 19 ###########
def getManagers():
    allManagersQ = "SELECT ManagerName FROM ManagerNameMS"
    cur.execute(allManagersQ)
    return cur.fetchall()

def AdminManageSite(table, site, manager, openeveryday, orderTuple):
    filterCount = 0
    filterTable = []
    if site !='-ALL-':
        filterCount += 1
        filterTable.append("SiteName = \"{}\"".format(site))
    if  manager != '-ALL-':
        filterCount += 1
        filterTable.append('Manager = "{}"'.format(manager))
    if openeveryday != '-ALL-':
        filterCount += 1
        filterTable.append("OpenEveryday = '{}'".format(openeveryday))
    if filterCount == 0:
        AdminManageSiteQ = "SELECT SiteName, Manager, OpenEveryday from SiteTable"
        if orderTuple == 'no order':
            AdminManageSiteQ = AdminManageSiteQ + " GROUP BY SiteName"
        else:
            if orderTuple[0] == 0:
                AdminManageSiteQ = AdminManageSiteQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                AdminManageSiteQ = AdminManageSiteQ + " ORDER BY Manager {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                AdminManageSiteQ = AdminManageSiteQ + " ORDER BY OpenEveryday {}".format(orderTuple[1])
    if filterCount == 1:
        AdminManageSiteQ = "SELECT SiteName, Manager, OpenEveryday from SiteTable WHERE {}".format(filterTable[0])
        if orderTuple == 'no order':
            AdminManageSiteQ = AdminManageSiteQ + " GROUP BY SiteName"
        else:
            if orderTuple[0] == 0:
                AdminManageSiteQ = AdminManageSiteQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                AdminManageSiteQ = AdminManageSiteQ + " ORDER BY Manager {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                AdminManageSiteQ = AdminManageSiteQ + " ORDER BY OpenEveryday {}".format(orderTuple[1])
    if filterCount == 2:
        AdminManageSiteQ = "SELECT SiteName, Manager, OpenEveryday from SiteTable WHERE {} and {}".format(filterTable[0], filterTable[1])
        if orderTuple == 'no order':
            AdminManageSiteQ = AdminManageSiteQ + " GROUP BY SiteName"
        else:
            if orderTuple[0] == 0:
                AdminManageSiteQ = AdminManageSiteQ  + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                AdminManageSiteQ = AdminManageSiteQ  + " ORDER BY Manager {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                AdminManageSiteQ = AdminManageSiteQ + " ORDER BY OpenEveryday {}".format(orderTuple[1])
    if filterCount == 3:
        AdminManageSiteQ = "SELECT SiteName, Manager, OpenEveryday from SiteTable WHERE {} and {} and {}".format(filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            AdminManageSiteQ = AdminManageSiteQ + " GROUP BY SiteName"
        else:
            if orderTuple[0] == 0:
                AdminManageSiteQ = AdminManageSiteQ  + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                AdminManageSiteQ = AdminManageSiteQ + " ORDER BY Manager {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                AdminManageSiteQ = AdminManageSiteQ  + " ORDER BY OpenEveryday {}".format(orderTuple[1])
    cur.execute(AdminManageSiteQ)
    return cur.fetchall()

def deleteSite(sitename, manager):
    deleteQ = "DELETE from beltline.SITE where SiteName=\"{}\" and ManagerUsername in (select Username from ManagerNameMS where ManagerName = \"{}\")".format(sitename, manager)
    cur.execute(deleteQ)
    connection.commit()

def getEditInfo(sitename):
    SiteInfoQ = "SELECT * FROM beltline.SITE WHERE SiteName = \"{}\"".format(sitename)
    cur.execute(SiteInfoQ)
    infodict = cur.fetchall()[0]
    thelist = []
    name = infodict["SiteName"]
    thelist.append(name)
    address = infodict["SiteAddress"]
    thelist.append(address)
    zipcode = infodict["SiteZipcode"]
    thelist.append(zipcode)
    isopen = infodict["OpenEveryday"]
    thelist.append(isopen)
    username = infodict["ManagerUsername"]
    thelist.append(username)
    return thelist
#
#
#
#
#
##
#
#
########### Screen 20 ###########
def ManagerList():
    managerList = []
    ManagerListQ = "SELECT concat(FirstName,\" \",Lastname) as ManagerName FROM beltline.USER where Username in (select Username from beltline.EMPLOYEE where employeetype=\"Manager\") and Username not in (select ManagerUsername from beltline.SITE)"
    cur.execute(ManagerListQ)
    ManagerDict = cur.fetchall()
    for item in ManagerDict:
        managerList.append(item["ManagerName"])
    return managerList

def AdminEditCheck(zipcode, address):
    if Backend.checkzip(zipcode):
        return Backend.checkzip(zipcode)
    if Backend.checksiteaddress(address):
        return Backend.checksiteaddress(address)

def AdminEditSite(originalsitename, newsitename, zipcode, address, manager, isopen):
    openvalue = ""
    if isopen:
        openvalue = "Yes"
    else:
        openvalue = "No"
    if manager == "No":
        manager = None
    else:
        getManagerUsernameQ = "SELECT Username FROM ManagerNameMS Where ManagerName = \"{}\"".format(manager)
        cur.execute(getManagerUsernameQ)
        manager = cur.fetchall()[0]["Username"]
    updatesiteQ = "UPDATE beltline.SITE set SiteName = \"{}\", SiteZipcode = \"{}\", SiteAddress = \"{}\", ManagerUsername =\"{}\", OpenEveryday = \"{}\" where Sitename= \"{}\"".format(newsitename, zipcode, address, manager, openvalue, originalsitename)
    cur.execute(updatesiteQ)
    connection.commit()

#### End Screen 20 #####
#
#
#
#
#
#
#
#
#### Screen 21 #####

def checkSite(zipcode, address):
    if Backend.checkzip(zipcode):
        return Backend.checkzip(zipcode)
    if Backend.checksiteaddress(address):
        return Backend.checksiteaddress(address)

def createdSite(sitename, zipcode, address, manager, openeveryday):
    isopen = ""
    if openeveryday:
        isopen = "Yes"
    else:
        isopen = "No"
    if manager == "No":
        manager = None
    else:
        getManagerUsernameQ = "SELECT Username FROM ManagerNameMS Where ManagerName = \"{}\"".format(manager)
        cur.execute(getManagerUsernameQ)
        manager = cur.fetchall()[0]["Username"]
    insertSiteQ = "INSERT INTO beltline.SITE values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(sitename, address, zipcode, isopen, manager)
    cur.execute(insertSiteQ)
    connection.commit()
#### End Screen 21 #####
#
#
#
#
#
####### Screen 22 ###########
def editManageTransit(table, site, transType, lowRange, highRange, route, orderTuple):
    if Backend.checkpriceFilter(lowRange):
        return Backend.checkpriceFilter(lowRange)
    if Backend.checkpriceFilter(highRange):
        return Backend.checkpriceFilter(highRange)
    filterCount = 0
    filterTable = []
    if site !='-ALL-':
        filterCount += 1
        filterTable.append('SiteName = "{}"'.format(site))
    if transType != '-ALL-':
        filterCount += 1
        filterTable.append("TransitType = '{}'".format(transType))
    if lowRange != '':
        filterCount += 1
        filterTable.append('TransitPrice >= "{}"'.format(lowRange))
    if highRange != '':
        filterCount += 1
        filterTable.append('TransitPrice <= "{}"'.format(highRange))
    if route != '':
        filterCount += 1
        filterTable.append('TransitRoute = "{}"'.format(route))
    if filterCount == 0:
        ManageTransitQ = "SELECT TransitRoute, TransitType, TransitPrice, ConnectedSites, TransitsLogged FROM AMTwithSite"
        if orderTuple == 'no order':
            ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType"
        else:
            if orderTuple[0] == 1:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitPrice {}".format(orderTuple[1])
    elif filterCount == 1:
        ManageTransitQ = "SELECT TransitRoute, TransitType, TransitPrice, ConnectedSites, TransitsLogged FROM AMTwithSite WHERE {}".format(filterTable[0])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitPrice {}".format(orderTuple[1])
    elif filterCount == 2:
        ManageTransitQ = "SELECT TransitRoute, TransitType, TransitPrice, ConnectedSites, TransitsLogged FROM AMTwithSite WHERE {} and {}".format(filterTable[0], filterTable[1])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitPrice {}".format(orderTuple[1])
    elif filterCount == 3:
        ManageTransitQ = "SELECT TransitRoute, TransitType, TransitPrice, ConnectedSites, TransitsLogged FROM AMTwithSite WHERE {} and {} and {}".format(filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitPrice {}".format(orderTuple[1])
    elif filterCount == 4:
        ManageTransitQ = "SELECT TransitRoute, TransitType, TransitPrice, ConnectedSites, TransitsLogged FROM AMTwithSite WHERE {} and {} and {} and {} ".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitPrice {}".format(orderTuple[1])
    elif filterCount == 5:
        ManageTransitQ = "SELECT TransitRoute, TransitType, TransitPrice, ConnectedSites, TransitsLogged FROM AMTwithSite WHERE {} and {} and {} and {} and {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitType {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                ManageTransitQ = ManageTransitQ + " GROUP BY TransitRoute, TransitType ORDER BY TransitPrice {}".format(orderTuple[1])
    cur.execute(ManageTransitQ)
    return cur.fetchall()

def deletetransit(route, transittype):
    deleteQ = "DELETE FROM beltline.TRANSIT WHERE TransitType = \"{}\" AND TransitRoute = \"{}\"".format(transittype, route)
    cur.execute(deleteQ)
    connection.commit()

############ Screen 23 #########
def EditTransit(transporttype, originalroute, newroute, price, sites):
    EditTransitQ = "UPDATE beltline.Transit set TransitRoute = \"{}\", TransitPrice = \"{}\" where TransitType = \"{}\" and TransitRoute = \"{}\"".format(newroute, price, transporttype, originalroute)
    cur.execute(EditTransitQ)
    connection.commit()
    dropSiteQ = "DELETE FROM beltline.connect WHERE transitType = '{}' AND TransitRoute = '{}'".format(transporttype, newroute)
    cur.execute(dropSiteQ)
    connection.commit()
    for site in sites:
        insertSiteQ = "INSERT INTO beltline.Connect VALUES ('{}', '{}', '{}')".format(site, transporttype, newroute)
        cur.execute(insertSiteQ)
        connection.commit()

def ListOfSites(transporttype, originalroute):
    getSitesQ = "SELECT SiteName from beltline.CONNECT WHERE TransitType = \"{}\" AND TransitRoute = \"{}\"".format(transporttype, originalroute)
    cur.execute(getSitesQ)
    thesites = cur.fetchall()
    sitelist = []
    for item in thesites:
        sitelist.append(item["SiteName"])
    return sitelist

###### Screen 24 ##########
def CreateTransit(transporttype, route, price, sites):
    insertTransitQ = "INSERT INTO beltline.Transit VALUES ('{}', '{}', '{}')".format(transporttype, route, price)
    cur.execute(insertTransitQ)
    connection.commit()
    for site in sites:
        insertSiteQ = "INSERT INTO beltline.Connect VALUES ('{}', '{}', '{}')".format(site, transporttype, route)
        cur.execute(insertSiteQ)
        connection.commit()
##### End Screen 24 ##############
#
#
#
#
#
#
#
#
#
#
### GUI 25 ###
def getManSite(username):
    getManSiteQ = "SELECT SiteName FROM site WHERE ManagerUsername = '{}'".format(username)
    cur.execute(getManSiteQ)
    a = cur.fetchone()
    print(a)
    return a['SiteName']

def GetManageEvent(site, name, startDate, keyword, lowDur, highDur, lowVis, highVis, lowRev, highRev, orderTuple):
    ManageEventTableQ = 'CREATE OR REPLACE VIEW ManageEventTable AS select EventName, StartDate, Sum(StaffCount) as StaffCount, Sum(Duration) as Duration, Sum(TotalVisits) as TotalVisits, sum(TotalRevenue) as Revenue, Description from AllManageSite  where SiteName = "{}" group by EventName, StartDate, Description'.format(site)
    cur.execute(ManageEventTableQ)
    connection.commit()
    if startDate != '' and Backend.checkdateFilter(startDate):
        return Backend.checkdateFilter(startDate)
    if lowDur != '' and Backend.checkduration(lowDur):
        return Backend.checkstaffcount(lowDur)
    if highDur != '' and Backend.checkduration(highDur):
        return Backend.checkstaffcount(highDur)
    if lowVis != '' and Backend.checkvisit(lowVis):
        return Backend.checkvisit(lowVis)
    if highVis != '' and Backend.checkvisit(highVis):
        return Backend.checkvisit(highVis)
    if lowRev != '' and Backend.checkrevenue(lowRev):
        return Backend.checkrevenue(lowRev)
    if highRev != '' and Backend.checkrevenue(highRev):
        return Backend.checkrevenue(highRev)
    filterCount = 0
    filterTable = []
    for item in [lowDur, highDur, lowVis, highVis, lowRev, highRev]:
        if item != '':
            filterCount += 1
            if item == lowDur:
                a = 'Duration  >= "{}"'.format(lowDur)
            elif item == highDur:
                a = 'Duration  <= "{}"'.format(highDur)
            elif item == lowVis:
                a = 'TotalVisits >= "{}"'.format(lowVis)
            elif item == highVis:
                a = 'TotalVisits <= "{}"'.format(highVis)
            elif item == lowRev:
                a = 'Revenue >= "{}"'.format(lowRev)
            elif item == highRev:
                a = 'Revenue <= "{}"'.format(highRev)
            filterTable.append(a)
    if startDate != '':
        filterTable.append('StartDate >= "{}"'.format(startDate))
        filterCount += 1
    if name != "":
        filterCount += 1
        filterTable.append('EventName LIKE "%{}%"'.format(name))
    if keyword != '':
        filterCount += 1
        filterTable.append('Description LIKE "%{}%"'.format(keyword))
    if filterCount == 0:
        editUserQ = "SELECT * FROM ManageEventTable"
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY Duration {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 1:
        editUserQ = "SELECT * FROM ManageEventTable WHERE {}".format(filterTable[0])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY Duration {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 2:
        editUserQ = "SELECT * FROM ManageEventTable WHERE {} AND {}".format(filterTable[0], filterTable[1])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY Duration {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 3:
        editUserQ = "SELECT * FROM ManageEventTable WHERE {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY Duration {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 4:
        editUserQ = "SELECT * FROM ManageEventTable WHERE {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY Duration {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 5:
        editUserQ = "SELECT * FROM ManageEventTable WHERE {} AND {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY Duration {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 6:
        editUserQ = "SELECT * FROM ManageEventTable WHERE {} AND {} AND {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY Duration {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 7:
        editUserQ = "SELECT * FROM ManageEventTable WHERE {} AND {} AND {} AND {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5], filterTable[6])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY Duration {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 8:
        editUserQ = "SELECT * FROM ManageEventTable WHERE {} AND {} AND {} AND {} AND {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5], filterTable[6], filterTable[7])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY Duration {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 9:
        editUserQ = "SELECT * FROM ManageEventTable WHERE {} AND {} AND {} AND {} AND {} AND {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5], filterTable[6], filterTable[7], filterTable[8])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY Duration {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    cur.execute(editUserQ)
    cur.execute(editUserQ)
    return cur.fetchall()

def deleteEvent(name, startDate, site):
    print(name, startDate, site)
    deleteQ = "DELETE FROM beltline.EVENT WHERE EventName = '{}' AND StartDate = '{}' AND SiteName = '{}'".format(name, startDate, site)
    cur.execute(deleteQ)
    connection.commit()


### END GUI 25 ###
#
#
#
#
#
#
#
#
#
#
### GUI 26 ###
def getEventInfo2(site, name, startDate):
    infoQ1 = 'SELECT * FROM event WHERE SiteName = "{}" AND EventName = "{}" AND startDate = "{}"'.format(site,name,startDate)
    cur.execute(infoQ1)
    return cur.fetchall()

def getAssignedStaff(site, name, startDate):
    infoQ1 = 'SELECT concat(firstname," ",lastname) as name FROM assign_to INNER JOIN user on assign_to.staffusername = user.username WHERE SiteName = "{}" AND EventName = "{}" AND startDate = "{}"'.format(site,name,startDate)
    cur.execute(infoQ1)
    a = cur.fetchall()
    nameList = []
    for item in a:
        nameList.append(item['name'])
    return nameList


def getAllStaff():
    infoQ1 = 'SELECT concat(firstname," ",lastname) as name FROM beltline.employee inner join user using(username) where employeeType ="Staff"'
    cur.execute(infoQ1)
    a = cur.fetchall()
    nameList = []
    for item in a:
        nameList.append(item['name'])
    return nameList

def updateDescription(site, eventName, startDate, description, names):
    Q1 = 'UPDATE event SET Description = "{}" WHERE SiteName = "{}" AND EventName = "{}" AND startDate = "{}"'.format(description, site, eventName, startDate)
    cur.execute(Q1)
    connection.commit()
    dropSiteQ = 'DELETE FROM beltline.assign_to WHERE SiteName = "{}" AND EventName = "{}" AND startDate = "{}"'.format(site, eventName, startDate)
    cur.execute(dropSiteQ)
    connection.commit()
    for name in names:
        fname = name.split(' ')[0]
        lname = name.split(' ')[1]
        Q2 = 'SELECT username FROM user Where FirstName = "{}" AND LastName = "{}"'.format(fname,lname)
        cur.execute(Q2)
        username = cur.fetchone()['username']
        insertSiteQ = "INSERT INTO beltline.assign_to VALUES ('{}', '{}', '{}', '{}')".format(username, eventName, startDate, site)
        cur.execute(insertSiteQ)
        connection.commit()
def SpecificEventTable(eventName, startDate, orderTuple):
    Q1 = 'SELECT VisitEventDate , count(*) as TotalVisits, count(*)*EventPrice as Revenue FROM DailyEvents WHERE EventName = "{}" and StartDate = "{}"'.format(eventName, startDate)
    if orderTuple == 'no order':
        Q1 = Q1 + " GROUP BY VisitEventDate"
    else:
        if orderTuple[0] == 0:
            Q1 = Q1 + " ORDER BY VisitEventDate '{}'".format(orderTuple[1]) +  " GROUP BY VisitEventDate"
        elif orderTuple[0] == 1:
            Q1 = Q1 + " ORDER BY TotalVisits '{}'".format(orderTuple[1]) +  " GROUP BY VisitEventDate"
        elif orderTuple[0] == 2:
            Q1 = Q1 + " ORDER BY Revenue '{}'".format(orderTuple[1]) +  " GROUP BY VisitEventDate"
    print(Q1)
    cur.execute(Q1)
    return cur.fetchall()


### END GUI 26 ###
#
#
#
#
#
#
### 28 ###
def ManageStaff(table, site, fname, lname, startDate, endDate, orderTuple):
    if Backend.checkfirstname(fname) and fname != '':
        return Backend.checkfirstname(fname)
    if Backend.checklastname(lname) and lname != '':
        return Backend.checklastname(lname)
    if Backend.checkdateFilter(startDate) and startDate != '':
        return Backend.checkdateFilter(startDate)
    if Backend.checkdateFilter(endDate) and endDate != '':
        return Backend.checkdateFilter(endDate)
    filterCount = 0
    filterTable = []
    if fname != "":
        filterCount += 1
        filterTable.append('Firstname = "{}"'.format(fname))
    if site != '-ALL-':
        filterCount += 1
        filterTable.append("SiteName = '{}'".format(site))
    if lname != '':
        filterCount += 1
        filterTable.append('Lastname = "{}"'.format(lname))
    if startDate != '':
        filterCount += 1
        filterTable.append('StartDate >= "{}"'.format(startDate))
    if endDate != '':
        filterCount += 1
        filterTable.append('EndDate <= "{}"'.format(endDate))
    if filterCount == 0:
        editUserQ = "SELECT concat(Firstname, ' ', Lastname) AS staffName, EventShifts FROM ManageStaff"
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                editUserQ = editUserQ + " ORDER BY staffName {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventShifts {}".format(orderTuple[1])
    elif filterCount == 1:
        editUserQ = "SELECT concat(Firstname, ' ', Lastname) AS staffName, EventShifts FROM ManageStaff WHERE {}".format(filterTable[0])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                editUserQ = editUserQ + " ORDER BY staffName {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventShifts {}".format(orderTuple[1])
    elif filterCount == 2:
        editUserQ = "SELECT concat(Firstname, ' ', Lastname) AS staffName, EventShifts FROM ManageStaff WHERE {} AND {}".format(filterTable[0], filterTable[1])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                editUserQ = editUserQ + " ORDER BY staffName {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventShifts {}".format(orderTuple[1])
    elif filterCount == 3:
        editUserQ = "SELECT concat(Firstname, ' ', Lastname) AS staffName, EventShifts FROM ManageStaff WHERE {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                editUserQ = editUserQ + " ORDER BY staffName {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventShifts {}".format(orderTuple[1])
    elif filterCount == 4:
        editUserQ = "SELECT concat(Firstname, ' ', Lastname) AS staffName, EventShifts FROM ManageStaff WHERE {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                editUserQ = editUserQ + " ORDER BY staffName {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventShifts {}".format(orderTuple[1])
    elif filterCount == 5:
        editUserQ = "SELECT concat(Firstname, ' ', Lastname) AS staffName, EventShifts FROM ManageStaff WHERE {} AND {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                editUserQ = editUserQ + " ORDER BY staffName {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventShifts {}".format(orderTuple[1])
    cur.execute(editUserQ)
    return cur.fetchall()
### END GUI 28 ###
#
#
#
#
#
#
#
#
#
#
#
#
##### GUI 29 ####
def GetSiteReport(site, startDate, endDate, lowEvent, highEvent, lowStaff, highStaff, lowVis, highVis, lowRev, highRev, orderTuple):
    if Backend.checkdateInsert(startDate):
        return Backend.checkdateInsert(startDate)
    if Backend.checkdateInsert(endDate):
        return Backend.checkdateInsert(endDate)
    if lowEvent != '' and Backend.checkeventcount(lowEvent):
        return Backend.checkeventcount(lowEvent)
    if highEvent != '' and Backend.checkeventcount(highEvent):
        return Backend.checkeventcount(highEvent)
    if lowStaff != '' and Backend.checkstaffcount(lowStaff):
        return Backend.checkstaffcount(lowStaff)
    if highStaff != '' and Backend.checkstaffcount(highStaff):
        return Backend.checkstaffcount(highStaff)
    if lowVis != '' and Backend.checkvisit(lowVis):
        return Backend.checkvisit(lowVis)
    if highVis != '' and Backend.checkvisit(highVis):
        return Backend.checkvisit(highVis)
    if lowRev != '' and Backend.checkrevenue(lowRev):
        return Backend.checkrevenue(lowRev)
    if highRev != '' and Backend.checkrevenue(highRev):
        return Backend.checkrevenue(highRev)
    SiteReportViewQ = 'CREATE OR REPLACE VIEW SiteReport as select VisitDate, Count(EventName) as EventCount, Sum(StaffCount) as StaffCount, sum(VisitorCount) as TotalVisits, sum(Revenue) as Revenue from  ((select EventName, SiteName, StartDate, EventPrice, VisitEventDate as VisitDate, VisitorCount, Revenue, StaffCount from Event_StaffCounts) UNION ALL (select Null as EventName, SiteName, Null as StartDate, 0 as EventPrice, VisitSiteDate as VisitDate, VisitorSiteCount as VisitorCount, 0 as Revenue, 0 as StaffCount from SiteVisitCount)) as nums where SiteName = "{}" and VisitDate between "{}" and "{}" group by VisitDate'.format(site, startDate, endDate)
    cur.execute(SiteReportViewQ)
    connection.commit()
    filterCount = 0
    filterTable = []
    for item in [lowEvent, highEvent, lowStaff, highStaff, lowVis, highVis, lowRev, highRev]:
        if item != '':
            filterCount += 1
            if item == lowEvent:
                a = 'EventCount  >= "{}"'.format(lowEvent)
            elif item == highEvent:
                a = 'EventCount  <= "{}"'.format(highEvent)
            elif item == lowStaff:
                a = 'StaffCount >= "{}"'.format(lowStaff)
            elif item == highStaff:
                a = 'StaffCount <= "{}"'.format(highStaff)
            elif item == lowVis:
                a = 'TotalVisits >= "{}"'.format(lowVis)
            elif item == highVis:
                a = 'TotalVisits <= "{}"'.format(highVis)
            elif item == lowRev:
                a = 'Revenue >= "{}"'.format(lowRev)
            elif item == highRev:
                a = 'Revenue <= "{}"'.format(highRev)
            filterTable.append(a)
    if filterCount == 0:
        editUserQ = "SELECT * FROM SiteReport"
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY VisitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY EventCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 1:
        editUserQ = "SELECT * FROM SiteReport WHERE {}".format(filterTable[0])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY VisitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY EventCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 2:
        editUserQ = "SELECT * FROM SiteReport WHERE {} AND {}".format(filterTable[0], filterTable[1])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY VisitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY EventCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 3:
        editUserQ = "SELECT * FROM SiteReport WHERE {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY VisitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY EventCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 4:
        editUserQ = "SELECT * FROM SiteReport WHERE {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY VisitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY EventCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 5:
        editUserQ = "SELECT * FROM SiteReport WHERE {} AND {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY VisitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY EventCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 6:
        editUserQ = "SELECT * FROM SiteReport WHERE {} AND {} AND {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY VisitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY EventCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 7:
        editUserQ = "SELECT * FROM SiteReport WHERE {} AND {} AND {} AND {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5], filterTable[6])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY VisitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY EventCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    elif filterCount == 8:
        editUserQ = "SELECT * FROM SiteReport WHERE {} AND {} AND {} AND {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5], filterTable[6], filterTable[7])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY VisitDate {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY EventCount {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])
    cur.execute(editUserQ)
    return cur.fetchall()



#### END GUI 29 ####
#
#
#
#
#
#
#
#
#
#
#
#
#### GUI 30 ####
def GetDailyDetail(date, site, orderTuple):
    Q1 = 'CREATE OR REPLACE VIEW  UsernameDailyReport as  (select n.EventName, n.StartDate, StaffUsername, VisitorCount as TotalVisits, Revenue from allSites_EventvisitCount as n left join beltline.Assign_to as m on n.EventName = m.EventName and n.StartDate = m.StartDate  where n.SiteName = "{}" and VisitEventDate = "{}")'.format(site, date)
    cur.execute(Q1)
    connection.commit()
    Q2 = 'CREATE OR REPLACE VIEW EmployeeNames as select Firstname, Lastname, Username  from beltline.User  where Username in (select StaffUsername from beltline.assign_to)'
    cur.execute(Q2)
    connection.commit()
    Q3 = 'CREATE OR REPLACE VIEW DailyReport as select EventName, concat(Firstname, ",", Lastname) as StaffName, TotalVisits, Revenue from EmployeeNames inner join UsernameDailyReport on Username = StaffUsername'
    cur.execute(Q3)
    connection.commit()
    editUserQ = "SELECT EventName, GROUP_CONCAT(StaffName SEPARATOR ' '), TotalVisits, Revenue FROM DailyReport"
    if orderTuple == 'no order':
        editUserQ = editUserQ + " GROUP BY EventName"
    else:
        if orderTuple[0] == 1:
            editUserQ = editUserQ + " ORDER BY StaffNames {}".format(orderTuple[1])+ " GROUP BY EventName"
        elif orderTuple[0] == 2:
            editUserQ = editUserQ + " ORDER BY TotalVisits {}".format(orderTuple[1])+ " GROUP BY EventName"
        elif orderTuple[0] == 3:
            editUserQ = editUserQ + " ORDER BY Revenue {}".format(orderTuple[1])+ " GROUP BY EventName"
        elif orderTuple[0] == 0:
            editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])+ " GROUP BY EventName"
    cur.execute(editUserQ)
    return cur.fetchall()
###### END GUI 30 ####
#
#
#
#
#
#
#
#
#
#
### GUI 31 ###
def StaffSchedule(table, username, event, keyword, startDate, endDate, orderTuple):
    if Backend.checkdateFilter(startDate) and startDate != '':
        return Backend.checkdateFilter(startDate)
    if Backend.checkdateFilter(endDate) and endDate != '':
        return Backend.checkdateFilter(endDate)
    filterCount = 0
    filterTable = []
    if event != "":
        filterCount += 1
        filterTable.append('EventName LIKE "%{}%"'.format(event))
    if keyword != '':
        filterCount += 1
        filterTable.append('Description LIKE "%{}%"'.format(keyword))
    if startDate != '':
        filterCount += 1
        filterTable.append('StartDate >= "{}"'.format(startDate))
    if endDate != '':
        filterCount += 1
        filterTable.append('EndDate <= "{}"'.format(endDate))
    if filterCount == 0:
        editUserQ = "SELECT EventName, SiteName, StartDate, EndDate, StaffCount FROM StaffViewSchedule WHERE (EventName,Sitename, StartDate) IN (SELECT EventName, SiteName, StartDate FROM assign_to WHERE staffusername = '{}')".format(username)
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY EndDate {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
    elif filterCount == 1:
        editUserQ = "SELECT EventName, SiteName, StartDate, EndDate, StaffCount FROM StaffViewSchedule WHERE (EventName,Sitename, StartDate) IN (SELECT EventName, SiteName, StartDate FROM assign_to WHERE staffusername = '{}') AND {}".format(username, filterTable[0])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY EndDate {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
    elif filterCount == 2:
        editUserQ = "SELECT EventName, SiteName, StartDate, EndDate, StaffCount FROM StaffViewSchedule WHERE (EventName,Sitename, StartDate) IN (SELECT EventName, SiteName, StartDate FROM assign_to WHERE staffusername = '{}') AND {} AND {}".format(username, filterTable[0], filterTable[1])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY EndDate {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
    elif filterCount == 3:
        editUserQ = "SELECT EventName, SiteName, StartDate, EndDate, StaffCount FROM StaffViewSchedule WHERE (EventName,Sitename, StartDate) IN (SELECT EventName, SiteName, StartDate FROM assign_to WHERE staffusername = '{}') AND {} AND {} AND {}".format(username, filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY EndDate {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
    elif filterCount == 4:
        editUserQ = "SELECT EventName, SiteName, StartDate, EndDate, StaffCount FROM StaffViewSchedule WHERE (EventName,Sitename, StartDate) IN (SELECT EventName, SiteName, StartDate FROM assign_to WHERE staffusername = '{}') AND {} AND {} AND {} AND {}".format(username, filterTable[0], filterTable[1], filterTable[2], filterTable[3])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY StartDate {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                editUserQ = editUserQ + " ORDER BY EndDate {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                editUserQ = editUserQ + " ORDER BY StaffCount {}".format(orderTuple[1])
    cur.execute(editUserQ)
    return cur.fetchall()
### END GUI 31 ###
#
#
#
#
#
#
#
#
### GUI 32 and 34 ###
def getEventStaff(event, site, startDate):
    getStaffQ = "SELECT concat(firstname,' ', lastname) FROM assign_to INNER JOIN user ON username = staffusername WHERE eventName = '{}' AND StartDate = '{}' AND Sitename = '{}'".format(event, startDate, site)
    cur.execute(getStaffQ)
    nameList = cur.fetchall()
    staffList = []
    for name in nameList:
        staffList.append(name["concat(firstname,' ', lastname)"])
    return ', '.join(staffList)

def getEventInfo(event, site, startDate):
    getEventInfoQ = "SELECT EndDate, EventPrice, Capacity, Description FROM event WHERE eventName = '{}' AND StartDate = '{}' AND Sitename = '{}'".format(event, startDate, site)
    cur.execute(getEventInfoQ)
    infoList = cur.fetchall()
    cleanList = []
    for info in infoList:
        for item in info:
            cleanList.append(info[item])
    return cleanList

def logVisitEvent(username, event, startDate, site, date, startObject, endObject):
    if Backend.checkdateInsert(date):
        return Backend.checkdateInsert(date)
    date_dateTime = datetime.strptime(date, '%Y-%m-%d')
    if date_dateTime >= startObject and date_dateTime <= endObject:
        logVisitEventQ = "INSERT INTO beltline.VISIT_EVENT values('{}','{}','{}','{}','{}')".format(username, event, startDate, site, date)
        cur.execute(logVisitEventQ)
        connection.commit()
    else:
        return 'Please enter a date within the duration of the event'
#### END 32 AND 34 ###
#
#
#
#
#
#
#
#
### GUI 37 ###
def getSiteInfo(site):
    Q1 = "SELECT Sitename, OpenEveryday, SiteAddress as Address FROM site where SiteName = '{}'".format(site)
    cur.execute(Q1)
    return cur.fetchall()[0]


def logSiteVisit1(username, sitename, visitDate):
    if Backend.checkdateInsert(visitDate):
        return Backend.checkdateInsert(visitDate)
    Q1 = "INSERT INTO visit_site VALUES ('{}','{}','{}')".format(username, sitename, visitDate)
    cur.execute(Q1)
    connection.commit()

#### END GUI 37 ####
#
#
#
#
### GUI 38 ###
def GetVisitHistory(event, site, startDate, endDate, orderTuple):
    if Backend.checkdateFilter(startDate):
        return Backend.checkdateFilter(startDate)
    if Backend.checkdateFilter(endDate):
        return Backend.checkdateFilter(endDate)
    filterCount = 0
    filterTable = []
    if event != "":
        filterCount += 1
        filterTable.append('EventName LIKE "%{}%"'.format(event))
    if site != '-ALL-':
        filterCount += 1
        filterTable.append('SiteName = "{}"'.format(site))
    if startDate != '':
        filterCount += 1
        filterTable.append('DateVisited >= "{}"'.format(startDate))
    if endDate != '':
        filterCount += 1
        filterTable.append('DateVisited <= "{}"'.format(endDate))
    if filterCount == 0:
        editUserQ = "SELECT * FROM VisitHistory"
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                editUserQ = editUserQ + " ORDER BY  DateVisited {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY Price {}".format(orderTuple[1])
    elif filterCount == 1:
        editUserQ = "SELECT * FROM VisitHistory WHERE {}".format(filterTable[0])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                editUserQ = editUserQ + " ORDER BY  DateVisited {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY Price {}".format(orderTuple[1])
    elif filterCount == 2:
        editUserQ = "SELECT * FROM VisitHistory WHERE {} AND {}".format(filterTable[0], filterTable[1])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                editUserQ = editUserQ + " ORDER BY  DateVisited {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY Price {}".format(orderTuple[1])
    elif filterCount == 3:
        editUserQ = "SELECT * FROM VisitHistory WHERE {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                editUserQ = editUserQ + " ORDER BY  DateVisited {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY Price {}".format(orderTuple[1])
    elif filterCount == 4:
        editUserQ = "SELECT * FROM VisitHistory WHERE {} AND {} AND {} AND {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3])
        if orderTuple == 'no order':
            pass
        else:
            if orderTuple[0] == 0:
                editUserQ = editUserQ + " ORDER BY  DateVisited {}".format(orderTuple[1])
            elif orderTuple[0] == 1:
                editUserQ = editUserQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                editUserQ = editUserQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                editUserQ = editUserQ + " ORDER BY Price {}".format(orderTuple[1])
    cur.execute(editUserQ)
    dictList = cur.fetchall()
    finalDictList = []
    for i in range(len(dictList)):
        if dictList[i]['EventName'] == None:
            dictList[i]['EventName'] = ' '
        finalDictList.append(dictList[i])
    return finalDictList

#### Screen 27 ########
#getManSite(username)
def getAssignedStaff(startdate, enddate):
    AssignedStaffQ = "SELECT StaffName from AssignedStaff WHERE '{}' between StartDate and EndDate or '{}' between StartDate and EndDate".format(startdate, enddate)
    cur.execute(AssignedStaffQ)
    exists = cur.fetchall()
    AssignedStaff = []
    for item in exists:
        AssignedStaff.append(item['StaffName'])
def getAllStaff():
    getStaffQ = "SELECT Username, concat(Firstname, \" \", Lastname) as StaffName from beltline.user where Username in (select Username from Employee where employeetype = \"Staff\")"
    cur.execute(getStaffQ)
    exists = cur.fetchall()
    stafflist = []
    for item in exists:
        stafflist.append(item['StaffName'])
    return stafflist

def createEventCheck(username, eventname, startdate, sitename, enddate, price, capacity, minstaff, descprition):
    if Backend.checkeventname(eventname):
        print(eventname)
        return Backend.checkeventname(eventname)
    if Backend.checkdateInsert(startdate):
        return Backend.checkInsertdate(startdate)
    if Backend.checkdateInsert(enddate):
        return Backend.checkdateInsert(enddate)
    if Backend.checkpriceInsert(price):
        return Backend.checkpriceInsert(price)
    if Backend.checkcapacity(capacity):
        return Backend.checkcapacity(capacity)
    if Backend.checkcapacity(minstaff):
        return Backend.checkcapacity(minstaff)
    if int(minstaff) < 1:
        return "Minimum staff required is 1."
    overlapQ = "SELECT EXISTS ( select EventName, SiteName, StartDate, EndDate from beltline.event where \"{}\" between StartDate and EndDate or \"{}\" between StartDate and EndDate and SiteName = \"{}\")".format(startdate, enddate, sitename)
    cur.execute(overlapQ)
    exists = cur.fetchall()[0]["EXISTS ( select EventName, SiteName, StartDate, EndDate from beltline.event where \"{}\" between StartDate and EndDate or \"{}\" between StartDate and EndDate and SiteName = \"{}\")".format(startdate, enddate, sitename)]
    print(type(exists))
    print(exists)
    print('aaaaaaaa')
    if exists != '0':
        return "There is already an event going on at this site at this time."


def createEvent(username, eventname, startdate, sitename, enddate, price, capacity, minstaff, descprition, stafflist):
    price = int(price)
    capacity = int(capacity)
    minstaff = int(minstaff)
    try:
        insertEventQ = "INSERT INTO beltline.Event values ({}, {}, {}, {}, {}, {}, {}, {})".format(eventname, startdate, sitename, enddate, price, capacity, minstaff, description)
        print(insertEventQ)
        cur.execute(insertEventQ)
        connection.commit()
        try:
            insertAssignToQ = "INSERT INTO beltline.Assign_to values ({}, {}, {}, {})".format(username, eventname, startdate, sitename)
            cur.execute(insertAssignToQ)
            connection.commt()
        except:
            return "This staff is already working an event at this time."
    except:
        return "An Event with this name and startdate already exists at this site."

#### Screen 33 #####
def VisitorExploreEvent(table, name, keyword, sitename, startdate, enddate, visitrangetop, visitrangebottom, ticketrangetop, ticketrangebottom, includevisited, includesoldout, orderTuple):
    if Backend.checkdateFilter(startdate):
        return Backend.checkdateFilter(startdate)
    if Backend.checkdateFilter(enddate):
        return Backend.checkdateFilter(enddate)
    if Backend.checkpriceFilter(ticketrangetop):
        return Backend.checkpriceFilter(ticketrangetop)
    if Backend.checkpriceFilter(ticketrangebottom):
        return Backend.checkpriceFilter(ticketrangebottom)
    filterCount = 0
    filterTable = []
    if name != "":
        filterCount +=1
        filterTable.append("EventName = \"{}\"".format(name))
    if keyword != "":
        filterCount +=1
        filterTable.append("Description like \"%{}%\"".format(keyword))
    if sitename != "-ALL-":
        filterCount +=1
        filterTable.append("SiteName = \"{}\"".format(sitename))
    if startdate != "":
        filterCount += 1
        filterTable.append("StartDate = \"{}\"".format(startdate))
    if enddate != "":
        filterCount +=1
        filterTable.append("EndDate = \"{}\"".format(enddate))
    if visitrangebottom != "":
        filterCount += 1
        filterTable.append("TotalVisits >= \"{}\"".format(visitrangebottom))
    if visitrangetop != "":
        filterCount += 1
        filterTable.append("TotalVisits <= \"{}\"".format(visitrangetop))
    if ticketrangebottom != "":
        filterCount += 1
        filterTable.append("EventPrice >= \"{}\"".format(ticketrangebottom))
    if ticketrangetop != "":
        filterCount += 1
        filterTable.append("EventPrice <= \"{}\"".format(ticketrangetop))
    if includevisited:
        filterCount += 1
        filterTable.append("MyVisits = 0")
    if includesoldout:
        filterCount += 1
        filterTable.append("TicketsRemaining >0")
    if filterCount == 0:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33"
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    elif filterCount == 1:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33 WHERE {} AND WHERE {}".format(filterTable[0], filterTable[1])
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    elif filterCount == 2:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33 WHERE {} AND WHERE {} AND WHERE {}".format(filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    elif filterCount == 3:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33 WHERE {} AND WHERE {} AND WHERE {}".format(filterTable[0], filterTable[1], filterTable[2])
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    elif filterCount == 4:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33 WHERE {} AND WHERE {} AND WHERE {} AND WHERE {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3])
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    elif filterCount == 5:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33 WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4])
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    elif filterCount == 6:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33 WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5])
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    elif filterCount == 7:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33 WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5], filterTable[6])
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    elif filterCount == 8:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33 WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5], filterTable[6], filterTable[7])
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    elif filterCount == 9:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33 WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5], filterTable[6], filterTable[7], filterTable[8])
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    elif filterCOunt == 10:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33 WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5], filterTable[6], filterTable[7], filterTable[8], filterTable[9])
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    elif filterCount == 11:
        VisitorExploreEventQ = "SELECT EventName, SiteName, EventPrice, TicketsRemaining, TotalVisits, MyVisits from THISISTHEFINALSCREEN33 WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {} AND WHERE {}".format(filterTable[0], filterTable[1], filterTable[2], filterTable[3], filterTable[4], filterTable[5], filterTable[6], filterTable[7], filterTable[8], filterTable[9], filterTable[10])
        if orderTuple == 'no order':
            VisitorExploreEventQ = VisitorExploreEventQ + " GROUP BY EventName, SiteName"
        else:
            if orderTuple[0] == 1:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventName {}".format(orderTuple[1])
            elif orderTuple[0] == 2:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY SiteName {}".format(orderTuple[1])
            elif orderTuple[0] == 3:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY EventPrice {}".format(orderTuple[1])
            elif orderTuple[0] == 4:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TicketsRemaining {}".format(orderTuple[1])
            elif orderTuple[0] == 5:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY TotalVisits {}".format(orderTuple[1])
            elif orderTuple[0] == 6:
                VisitorExploreEventQ = VisitorExploreEventQ + " ORDER BY MyVisits {}".format(orderTuple[1])
    cur.execute(VisitorExploreEventQ)
    return cur.fetchall()

