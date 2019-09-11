#For deleting and uploading a fresh beltline database
import pymysql
import csv
connection = pymysql.connect(host="localhost",
                                user="root",
                                password="24242424",
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor)

#drops the existing database
cur = connection.cursor()
dropBeltlineQ = "DROP DATABASE beltline"
cur.execute(dropBeltlineQ)


#create fresh beltline database
createBeltlineQ = "CREATE DATABASE beltline"
cur.execute(createBeltlineQ)



connection = pymysql.connect(host="localhost",
                                user="root",
                                password="24242424",
                                db="beltline",
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor)
cur = connection.cursor()

userQ = "CREATE TABLE USER (Username               VARCHAR(15)     NOT NULL, Password                VARCHAR(30)     NOT NULL, Status                  VARCHAR(15)     NOT NULL, Firstname               VARCHAR(30)     NOT NULL, Lastname                VARCHAR(30)     NOT NULL, UserType                VARCHAR(30)     NOT NULL, PRIMARY KEY (Username))"
cur.execute(userQ)

useremailQ = "CREATE TABLE USEREMAIL (Username               VARCHAR(15)     NOT NULL, Email                   VARCHAR(30)     NOT NULL, PRIMARY KEY (Email), FOREIGN KEY (Username) REFERENCES USER(Username) ON UPDATE CASCADE   ON DELETE CASCADE )"
cur.execute(useremailQ)


employeeQ = "CREATE TABLE EMPLOYEE (Username               VARCHAR(15)     NOT NULL, EmployeeID              INT             NOT NULL, Phone                   CHAR(10)            NOT NULL, EmployeeAddress         VARCHAR(30), EmployeeCity                VARCHAR(30), EmployeeState           VARCHAR(5), EmployeeZipcode         CHAR(5), EmployeeType            VARCHAR(15)     NOT NULL, PRIMARY KEY (Username), UNIQUE (Phone), UNIQUE (Username), FOREIGN KEY (Username) REFERENCES USER(Username) ON UPDATE CASCADE   ON DELETE CASCADE )"
cur.execute(employeeQ)


visitorQ = "CREATE TABLE VISITOR (Username               VARCHAR(15)         NOT NULL, PRIMARY KEY (Username), FOREIGN KEY (Username) REFERENCES USER(Username) ON UPDATE CASCADE ON DELETE CASCADE );"
cur.execute(visitorQ)


adminQ = "CREATE TABLE ADMINISTRATOR (Username               VARCHAR(15)         NOT NULL, PRIMARY KEY (Username), FOREIGN KEY (Username) REFERENCES EMPLOYEE(Username) ON UPDATE CASCADE ON DELETE RESTRICT )"
cur.execute(adminQ)


managerQ = "CREATE TABLE MANAGER (Username               VARCHAR(15)         NOT NULL, PRIMARY KEY (Username), FOREIGN KEY (Username) REFERENCES EMPLOYEE(Username) ON UPDATE CASCADE ON DELETE RESTRICT )"
cur.execute(managerQ)


staffQ = "CREATE TABLE STAFF (Username               VARCHAR(15)         NOT NULL, PRIMARY KEY (Username), FOREIGN KEY (Username) REFERENCES EMPLOYEE(Username) ON UPDATE CASCADE ON DELETE RESTRICT )"
cur.execute(staffQ)

siteQ = "CREATE TABLE SITE (SiteName               VARCHAR(30)     NOT NULL, SiteAddress             VARCHAR(30), SiteZipcode             CHAR(5), OpenEveryday                VARCHAR(3), ManagerUsername         VARCHAR(15)     NOT NULL, PRIMARY KEY (SiteName), FOREIGN KEY (ManagerUsername) REFERENCES EMPLOYEE (Username) ON UPDATE CASCADE ON DELETE CASCADE )"
cur.execute(siteQ)

eventQ = "CREATE TABLE EVENT (EventName              VARCHAR(50)     NOT NULL, StartDate               DATE                NOT NULL, SiteName                VARCHAR(30)     NOT NULL, EndDate             DATE, EventPrice              VARCHAR(30), Capacity                INT, MinStaffRequired            INT, Description             VARCHAR(1000), CONSTRAINT CompKey_Event PRIMARY KEY (EventName, StartDate, SiteName), FOREIGN KEY (SiteName) REFERENCES SITE(SiteName) ON UPDATE CASCADE   ON DELETE RESTRICT)"
cur.execute(eventQ)


transitQ = "CREATE TABLE TRANSIT (TransitType                VARCHAR(30)     NOT NULL, TransitRoute                VARCHAR(30)     NOT NULL, TransitPrice                VARCHAR(10000), CONSTRAINT CompKey_Transit PRIMARY KEY (TransitType, TransitRoute) )"
cur.execute(transitQ)

connectQ = "CREATE TABLE CONNECT (SiteName               VARCHAR(30)     NOT NULL, TransitType             VARCHAR(30)     NOT NULL, TransitRoute                VARCHAR(30)     NOT NULL, CONSTRAINT CompKey_Connect PRIMARY KEY (SiteName, TransitRoute, TransitType), FOREIGN KEY (SiteName) REFERENCES SITE (SiteName) ON UPDATE CASCADE   ON DELETE CASCADE, FOREIGN KEY (TransitType, TransitRoute) REFERENCES TRANSIT (TransitType, TransitRoute) ON UPDATE CASCADE   ON DELETE CASCADE)"
cur.execute(connectQ)

taketransitQ = "CREATE TABLE TAKETRANSIT (Username               VARCHAR(15)     NOT NULL, TransitType             VARCHAR(30)     NOT NULL, TransitRoute                VARCHAR(30)     NOT NULL, TransitDate             DATE                NOT NULL, CONSTRAINT CompKey_TakeTransit PRIMARY KEY (Username, TransitRoute, TransitType, TransitDate), FOREIGN KEY (Username) REFERENCES USER (Username) ON UPDATE CASCADE   ON DELETE CASCADE, FOREIGN KEY (TransitType, TransitRoute) REFERENCES TRANSIT (TransitType, TransitRoute) ON UPDATE CASCADE   ON DELETE CASCADE )"
cur.execute(taketransitQ)


assignTOQ = "CREATE TABLE ASSIGN_TO (StaffUsername          VARCHAR(15)     NOT NULL, EventName               VARCHAR(50)     NOT NULL, StartDate               DATE                NOT NULL, SiteName                VARCHAR(30)     NOT NULL, CONSTRAINT CompKey_AssignTo PRIMARY KEY (StaffUsername, EventName, StartDate, SiteName), FOREIGN KEY (StaffUsername) REFERENCES EMPLOYEE (Username)  ON UPDATE CASCADE   ON DELETE CASCADE, FOREIGN KEY (EventName, StartDate, SiteName) REFERENCES EVENT (EventName, StartDate, SiteName)  ON UPDATE CASCADE   ON DELETE CASCADE, FOREIGN KEY (SiteName) REFERENCES  SITE(SiteName) ON UPDATE CASCADE   ON DELETE CASCADE )"
cur.execute(assignTOQ)

visitEventQ = "CREATE TABLE VISIT_EVENT (VisitorUsername            VARCHAR(15)     NOT NULL, EventName               VARCHAR(50)     NOT NULL, StartDate               DATE                NOT NULL, SiteName                VARCHAR(30)     NOT NULL, VisitEventDate          DATE                NOT NULL, CONSTRAINT CompKey_VisitEvent PRIMARY KEY (VisitorUsername, EventName, StartDate, VisitEventDate, SiteName), FOREIGN KEY (VisitorUsername) REFERENCES USER (Username) ON UPDATE CASCADE   ON DELETE CASCADE, FOREIGN KEY (EventName, StartDate, SiteName) REFERENCES EVENT (EventName, StartDate, SiteName) ON UPDATE CASCADE   ON DELETE CASCADE, FOREIGN KEY (SiteName) REFERENCES EVENT (SiteName) ON UPDATE CASCADE   ON DELETE CASCADE )"
cur.execute(visitEventQ)


visitSiteQ = "CREATE TABLE VISIT_SITE (VisitorUsername            VARCHAR(15)     NOT NULL, SiteName                VARCHAR(30)     NOT NULL, VisitSiteDate               DATE                NOT NULL, CONSTRAINT CompKey_VisitSite PRIMARY KEY (VisitorUsername, SiteName, VisitSiteDate), FOREIGN KEY (VisitorUsername) REFERENCES USER (Username) ON UPDATE CASCADE   ON DELETE CASCADE, FOREIGN KEY (SiteName) REFERENCES SITE (SiteName) ON UPDATE CASCADE   ON DELETE CASCADE )"
cur.execute(visitSiteQ)

fileList = ['user.csv','useremail.csv','employee.csv','visitor.csv','administrator.csv','manager.csv','staff.csv','site.csv','event.csv','transit.csv','connect.csv','taketransit.csv','assignto.csv','visitevent.csv','visitsite.csv']





#######################################################

userInsertQ = "INSERT INTO User (Username,Password,Status,Firstname,Lastname,UserType) VALUES ('james.smith','jsmith123','Approved','James','Smith','Employee'), ('michael.smith','msmith456','Approved','Michael','Smith','Employee-Visitor'),('robert.smith','rsmith789','Approved','Robert','Smith','Employee'),('maria.garcia','mgarcia123','Approved','Maria','Garcia','Employee-Visitor'),('david.smith','dsmith456','Approved','David','Smith','Employee'),('manager1','manager1','Pending','Manager','One','Employee'),('manager2','manager2','Approved','Manager','Two','Employee-Visitor'),('manager3','manager3','Approved','Manager','Three','Employee'),('manager4','manager4','Approved','Manager','Four','Employee-Visitor'),('manager5','manager5','Approved','Manager','Five','Employee-Visitor'),('maria.rodriguez','mrodriguez','Declined','Maria','Rodriguez','Visitor'),('mary.smith','msmith789','Approved','Mary','Smith','Visitor'),('maria.hernandez','mhernandez','Approved','Maria','Hernandez','User'),('staff1','staff1234','Approved','Staff','One','Employee'),('staff2','staff4567','Approved','Staff','Two','Employee-Visitor'),('staff3','staff7890','Approved','Staff','Three','Employee-Visitor'),('user1','user123456','Pending','User','One','User'),('visitor1','visitor123','Approved','Visitor','One','Visitor')"
cur.execute(userInsertQ)
'''
'''
#########################################
userEmailInsertQ = "INSERT INTO USEREMAIL(Username,Email) VALUES ('james.smith','jsmith@gmail.com'), ('james.smith','jsmith@hotmail.com'), ('james.smith','jsmith@gatech.edu'), ('james.smith','jsmith@outlook.com'), ('michael.smith','msmith@gmail.com'), ('robert.smith','rsmith@hotmail.com'), ('maria.garcia','mgarcia@yahoo.com'), ('maria.garcia','mgarcia@gatech.edu'), ('david.smith','dsmith@outlook.com'), ('maria.rodriguez','mrodriguez@gmail.com'), ('mary.smith','mary@outlook.com'), ('maria.hernandez','mh@gatech.edu'), ('maria.hernandez','mh123@gmail.com'), ('manager1','m1@beltline.com'), ('manager2','m2@beltline.com'), ('manager3','m3@beltline.com'), ('manager4','m4@beltline.com'), ('manager5','m5@beltline.com'), ('staff1','s1@beltline.com'), ('staff2','s2@beltline.com'), ('staff3','s3@beltline.com'), ('user1','u1@beltline.com'), ('visitor1','v1@beltline.com')"
cur.execute(userEmailInsertQ)
##########################
employeeInsertQ = "INSERT INTO EMPLOYEE(Username,EmployeeID,Phone,EmployeeAddress,EmployeeCity,EmployeeState,EmployeeZipcode,EmployeeType)VALUES ('james.smith',000000001,'4043721234','123 East Main Street','Rochester','NY','14604','Admin'),('michael.smith',000000002,'4043726789','350 Ferst Drive','Atlanta','GA','30332','Staff'),('robert.smith',000000003,'1234567890','123 East Main Street','Columbus','OH','43215','Staff'),('maria.garcia',000000004,'7890123456','123 East Main Street','Richland','PA','17987','Manager'),('david.smith',000000005,'5124776435','350 Ferst Drive','Atlanta','GA','30332','Manager'),('manager1',000000006,'8045126767','123 East Main Street','Rochester','NY','14604','Manager'),('manager2',000000007,'9876543210','123 East Main Street','Rochester','NY','14604','Manager'),('manager3',000000008,'5432167890','350 Ferst Drive','Atlanta','GA','30332','Manager'),('manager4',000000009,'8053467565','123 East Main Street','Columbus','OH','43215','Manager'), ('manager5',000000010,'8031446782','801 Atlantic Drive','Atlanta','GA','30332','Manager'),('staff1',000000011,'8024456765','266 Ferst Drive Northwest','Atlanta','GA','30332','Staff'),('staff2',000000012,'8888888888','266 Ferst Drive Northwest','Atlanta','GA','30332','Staff'),('staff3',000000013,'3333333333','801 Atlantic Drive','Atlanta','GA','30332','Staff')"
cur.execute(employeeInsertQ)
#############################
visitorInsertQ = "INSERT INTO VISITOR(Username) VALUES ('michael.smith'),('maria.garcia'),('manager2'),('manager4'),('manager5'),('maria.rodriguez'),('mary.smith'),('staff2'),('staff3'),('visitor1')"
cur.execute(visitorInsertQ)
#############################
adminInsertQ = "INSERT INTO ADMINISTRATOR(Username) VALUES ('james.smith')"
cur.execute(adminInsertQ)
#############################
managerInsertQ = "INSERT INTO MANAGER(Username) VALUES ('maria.garcia'),('david.smith'),('manager1'),('manager2'),('manager3'),('manager4')"
cur.execute(managerInsertQ)
#############################
staffInsertQ = "INSERT INTO STAFF(Username) VALUES ('michael.smith'),('robert.smith')"
cur.execute(staffInsertQ)
#############################
siteInsertQ = "INSERT INTO Site(SiteName,SiteAddress,SiteZipcode,OpenEveryday,ManagerUsername) VALUES('Piedmont Park','400 Park Drive Northeast','30306','Yes','manager2'), ('Atlanta Beltline Center','112 Krog Street Northeast','30307','No','manager3'), ('Historic Fourth Ward Park','680 Dallas Street Northeast','30308','Yes','manager4'), ('Westview Cemetery','1680 Westview Drive Southwest','30310','No','manager5'), ('Inman Park',NULL,'30307','Yes','david.smith')"
cur.execute(siteInsertQ)
##################
eventInsertQ = "INSERT INTO EVENT(EventName,StartDate,SiteName,EndDate,EventPrice,Capacity,MinStaffRequired,Description) VALUES ('Eastside Trail','2019-02-04','Piedmont Park','2019-02-05','0',99999,1,'A combination of multi-use trail and linear greenspace, the Eastside Trail was the first finished section of the Atlanta BeltLine trail in the old rail corridor. The Eastside Trail, which was funded by a combination of public and private philanthropic sources, runs from the tip of Piedmont Park to Reynoldstown. More details at https://beltline.org/explore-atlanta-beltline-trails/eastside-trail/'), ('Eastside Trail','2019-02-04','Inman Park','2019-02-05','0',99999,1,'A combination of multi-use trail and linear greenspace, the Eastside Trail was the first finished section of the Atlanta BeltLine trail in the old rail corridor. The Eastside Trail, which was funded by a combination of public and private philanthropic sources, runs from the tip of Piedmont Park to Reynoldstown. More details at https://beltline.org/explore-atlanta-beltline-trails/eastside-trail/'), ('Eastside Trail','2019-03-01','Inman Park','2019-03-02','0',99999,1,'A combination of multi-use trail and linear greenspace, the Eastside Trail was the first finished section of the Atlanta BeltLine trail in the old rail corridor. The Eastside Trail, which was funded by a combination of public and private philanthropic sources, runs from the tip of Piedmont Park to Reynoldstown. More details at https://beltline.org/explore-atlanta-beltline-trails/eastside-trail/'), ('Eastside Trail','2019-02-13','Historic Fourth Ward Park','2019-02-14','0',99999,1,'A combination of multi-use trail and linear greenspace, the Eastside Trail was the first finished section of the Atlanta BeltLine trail in the old rail corridor. The Eastside Trail, which was funded by a combination of public and private philanthropic sources, runs from the tip of Piedmont Park to Reynoldstown. More details at https://beltline.org/explore-atlanta-beltline-trails/eastside-trail/'), ('Westside Trail','2019-02-18','Westview Cemetery','2019-02-21','0',99999,1,'The Westside Trail is a free amenity that offers a bicycle and pedestrian-safe corridor with a 14-foot-wide multi-use trail surrounded by mature trees and grasses thanks to Trees Atlanta’s Arboretum. With 16 points of entry, 14 of which will be ADA-accessible with ramp and stair systems, the trail provides numerous access points for people of all abilities. More details at: https://beltline.org/explore-atlanta-beltline-trails/westside-trail/'), ('Bus Tour','2019-02-01','Inman Park','2019-02-02','25',6,2,'The Atlanta BeltLine Partnership’s tour program operates with a natural gas-powered, ADA accessible tour bus funded through contributions from 10th & Monroe, LLC, SunTrust Bank Trusteed Foundations – Florence C. and Harry L. English Memorial Fund and Thomas Guy Woolford Charitable Trust, and AGL Resources'), ('Bus Tour','2019-02-08','Inman Park','2019-02-10','25',6,2,'The Atlanta BeltLine Partnership’s tour program operates with a natural gas-powered, ADA accessible tour bus funded through contributions from 10th & Monroe, LLC, SunTrust Bank Trusteed Foundations – Florence C. and Harry L. English Memorial Fund and Thomas Guy Woolford Charitable Trust, and AGL Resources'), ('Private Bus Tour','2019-02-01','Inman Park','2019-02-02','40',4,1,'Private tours are available most days, pending bus and tour guide availability. Private tours can accommodate up to 4 guests per tour, and are subject to a tour fee (nonprofit rates are available). As a nonprofit organization with limited resources, we are unable to offer free private tours. We thank you for your support and your understanding as we try to provide as many private group tours as possible. The Atlanta BeltLine Partnership’s tour program operates with a natural gas-powered, ADA accessible tour bus funded through contributions from 10th & Monroe, LLC, SunTrust Bank Trusteed Foundations – Florence C. and Harry L. English Memorial Fund and Thomas Guy Woolford Charitable Trust, and AGL Resources'), ('Arboretum Walking Tour','2019-02-08','Inman Park','2019-02-11','5',5,1,'Official Atlanta BeltLine Arboretum Walking Tours provide an up-close view of the Westside Trail and the Atlanta BeltLine Arboretum led by Trees Atlanta Docents. The one and a half hour tours step off at at 10am (Oct thru May), and 9am (June thru September). Departure for all tours is from Rose Circle Park near Brown Middle School. More details at: https://beltline.org/visit/atlanta-beltline-tours/#arboretum-walking'), ('Official Atlanta BeltLine Bike Tour','2019-02-09','Atlanta BeltLine Center','2019-02-14','5',5,1,'These tours will include rest stops highlighting assets and points of interest along the Atlanta BeltLine. Staff will lead the rides, and each group will have a ride sweep to help with any unexpected mechanical difficulties.')"
cur.execute(eventInsertQ)
##############################

transitInsertQ = "INSERT INTO transit (TransitType,TransitRoute,TransitPrice) VALUES ('MARTA','Blue',2.00), ('Bus','152',2.00), ('Bike','Relay',1.00)"
cur.execute(transitInsertQ)

###########################
connectInsertQ = "INSERT INTO Connect(SiteName,TransitType,TransitRoute) VALUES('Inman Park','MARTA','Blue'), ('Piedmont Park','MARTA','Blue'), ('Historic Fourth Ward Park','MARTA','Blue'), ('Westview Cemetery','MARTA','Blue'), ('Inman Park','Bus','152'), ('Piedmont Park','Bus','152'), ('Historic Fourth Ward Park','Bus','152'), ('Piedmont Park','Bike','Relay'), ('Historic Fourth Ward Park','Bike','Relay')"
cur.execute(connectInsertQ)


taketransitInsertQ = "INSERT INTO taketransit (Username,TransitType,TransitRoute,TransitDate) VALUES ('manager2','MARTA','Blue','2019-03-20'),('manager2','Bus','152','2019-03-20'),('manager3','Bike','Relay','2019-03-20'),('manager2','MARTA','Blue','2019-03-21'),('maria.hernandez','Bus','152','2019-03-20'),('maria.hernandez','Bike','Relay','2019-03-20'),('manager2','MARTA','Blue','2019-03-22'),('maria.hernandez','Bus','152','2019-03-22'),('mary.smith','Bike','Relay','2019-03-23'),('visitor1','MARTA','Blue','2019-03-21')"
cur.execute(taketransitInsertQ)
###########################

assignToInsertQ = "INSERT INTO ASSIGN_TO(StaffUsername,EventName,StartDate,SiteName) VALUES ('staff1','Eastside Trail','2019-02-04','Piedmont Park'), ('robert.smith','Eastside Trail','2019-02-04','Inman Park'), ('staff2','Eastside Trail','2019-02-04','Inman Park'), ('staff1','Eastside Trail','2019-03-01','Inman Park'), ('michael.smith','Eastside Trail','2019-02-13','Historic Fourth Ward Park'), ('staff1','Westside Trail','2019-02-18','Westview Cemetery'), ('staff3','Westside Trail','2019-02-18','Westview Cemetery'), ('michael.smith','Bus Tour','2019-02-01','Inman Park'), ('staff2','Bus Tour','2019-02-01','Inman Park'), ('robert.smith','Bus Tour','2019-02-08','Inman Park'), ('michael.smith','Bus Tour','2019-02-08','Inman Park'), ('robert.smith','Private Bus Tour','2019-02-01','Inman Park'), ('staff3','Arboretum Walking Tour','2019-02-08','Inman Park'), ('staff1','Official Atlanta BeltLine Bike Tour','2019-02-09','Atlanta BeltLine Center')"
cur.execute(assignToInsertQ)




visitSiteQ = "INSERT INTO visit_site (VisitorUsername,SiteName,VisitSiteDate) VALUES ('mary.smith','Inman Park','2019-02-01'),('mary.smith','Inman Park','2019-02-02'),('mary.smith','Inman Park','2019-02-03'),('mary.smith','Atlanta Beltline Center','2019-02-01'),('mary.smith','Atlanta Beltline Center','2019-02-10'),('mary.smith','Historic Fourth Ward Park','2019-02-02'),('mary.smith','Piedmont Park','2019-02-02'),('visitor1','Piedmont Park','2019-02-11'),('visitor1','Atlanta Beltline Center','2019-02-13'),('visitor1','Historic Fourth Ward Park','2019-02-11'),('visitor1','Westview Cemetery','2019-02-06'),('visitor1','Inman Park','2019-02-01'),('visitor1','Piedmont Park','2019-02-01'),('visitor1','Atlanta Beltline Center','2019-02-09')"
cur.execute(visitSiteQ)
visitEventInsertQ = "INSERT INTO Visit_Event(VisitorUsername,EventName,StartDate,SiteName,VisitEventDate) VALUES('mary.smith','Bus Tour','2019-02-01','Inman Park','2019-02-01'), ('maria.garcia','Bus Tour','2019-02-01','Inman Park','2019-02-02'), ('manager2','Bus Tour','2019-02-01','Inman Park','2019-02-02'), ('manager4','Bus Tour','2019-02-01','Inman Park','2019-02-01'), ('manager5','Bus Tour','2019-02-01','Inman Park','2019-02-02'), ('staff2','Bus Tour','2019-02-01','Inman Park','2019-02-02'), ('mary.smith','Westside Trail','2019-02-18','Westview Cemetery','2019-02-19'), ('mary.smith','Private Bus Tour','2019-02-01','Inman Park','2019-02-01'), ('mary.smith','Private Bus Tour','2019-02-01','Inman Park','2019-02-02'), ('mary.smith','Official Atlanta BeltLine Bike Tour','2019-02-09','Atlanta BeltLine Center','2019-02-10'),('mary.smith','Arboretum Walking Tour','2019-02-08','Inman Park','2019-02-10'),('mary.smith','Eastside Trail','2019-02-04','Piedmont Park','2019-02-04'),('mary.smith','Eastside Trail','2019-02-13','Historic Fourth Ward Park','2019-02-13'),('mary.smith','Eastside Trail','2019-02-13','Historic Fourth Ward Park','2019-02-14'),('visitor1','Eastside Trail','2019-02-13','Historic Fourth Ward Park','2019-02-14'),('visitor1','Official Atlanta BeltLine Bike Tour','2019-02-09','Atlanta BeltLine Center','2019-02-10'),('visitor1','Westside Trail','2019-02-18','Westview Cemetery','2019-02-19')"
cur.execute(visitEventInsertQ)

connection.commit()
connection.close()
