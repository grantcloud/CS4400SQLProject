##########Editing User 
select * from user;

#### Edit Username 
update beltline.user set Username = "celine2" where Username = "celine1" ;

#### Edit Password
Update beltline.user set Password = "Natalie34" where Password = "sadie456" and Username = "celine2";
#or 
Update beltline.user set Password = "Natalie34" where  Username = "celine2";

#### Edit Satus
Update beltline.user set Status = "Pending" where Status = "Approved" and Username = "celine2";

#### Edit Firstname
Update beltline.user set Firstname = "Celine" where Firstname = "CelineD" and Username = "celine2";

####Edit Lastname
Update beltline.user set LastName = "Lucco" where Lastname = "Montrose" and Username = "celine2";

#### Edit UserType
Update beltline.user set UserType = "Employee, Visitor" where UserType = "Employee" and Username = "celine2";



####User Login (1)####
SELECT * FROM Database WHERE email = (what is inputed) AND Password = (what is inputed);

####Register User Only (2)####
SELECT * FROM Database WHERE Username = (what is inputed);

####Register User Only (3)####
SELECT * FROM Database WHERE Username = (what is inputed);

####Register Visitor Only (4)####
SELECT * FROM Database WHERE Username = (what is inputed);

####Regiser Employee Only (5)####
SELECT * FROM Database WHERE Username = (what is inputed);

####Register Employee/Visitor Only (6)####
SELECT * FROM Database WHERE Username = (what is inputed);
SELECT * FROM Database WHERE Phone = (what is inputed);

#### User Take Transit (15) ####
SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
	# 1. SELECT sitename from site; ->List of all sites
    # 2. SELECT transittype from transit; ->List of all transport types
    
#SELECT ALL
SELECT A.TransitRoute, A.TransitType, A.TransitPrice, count(C.sitename)
from beltline.TRANSIT AS A NATURAL JOIN beltline.CONNECT AS C 
GROUP BY TransitRoute;

#SELECT ALL with TransitType
SELECT A.TransitRoute, A.TransitType, A.TransitPrice, count(C.sitename)
from beltline.TRANSIT AS A NATURAL JOIN beltline.CONNECT AS C 
where A.TransitType = ‘{}’
GROUP BY TransitRoute;

#SELECT ALL with ContainSite
SELECT A.TransitRoute, A.TransitType, A.TransitPrice, count(C.SiteName)
from beltline.TRANSIT AS A NATURAL JOIN beltline.CONNECT AS C 
where C.SiteName = ‘{}
GROUP BY TransitRoute;

#SELECT ALL with PriceRange
SELECT A.TransitRoute, A.TransitType, A.TransitPrice, count(C.SiteName)
from beltline.TRANSIT AS A NATURAL JOIN beltline.CONNECT AS C 
where A.TransitPrice >= 1 and A.TransitPrice <= 3
GROUP BY TransitRoute;

#SELECT ALL with TransitType and ContainSite
SELECT A.TransitRoute, A.TransitType, A.TransitPrice, count(C.sitename)
from beltline.TRANSIT AS A NATURAL JOIN beltline.CONNECT AS C 
where (A.TransitType = ‘{}’) AND (C.SiteName = ‘{}’)
GROUP BY TransitRoute;

#SELECT ALL with PriceRange and TransitType
SELECT A.TransitRoute, A.TransitType, A.TransitPrice, count(C.sitename)
from beltline.TRANSIT AS A NATURAL JOIN beltline.CONNECT AS C 
where (A.TransitPrice >= {} AND A.TransitPrice <={}) AND (A.TransitType = ‘{}’) 
GROUP BY TransitRoute;

#SELECT ALL with PriceRange and ContainSite
SELECT A.TransitRoute, A.TransitType, A.TransitPrice, count(C.sitename)
from beltline.TRANSIT AS A NATURAL JOIN beltline.CONNECT AS C 
where (A.TransitPrice >= {} AND A.TransitPrice <={}) AND (C.SiteName = '{}')
GROUP BY TransitRoute;

#SELECT ALL with TransitType, PriceRange, and ContainSite
SELECT A.TransitRoute, A.TransitType, A.TransitPrice, count(C.sitename)
from beltline.TRANSIT AS A NATURAL JOIN beltline.CONNECT AS C 
where (A.TransitPrice >= {} AND A.TransitPrice <={}) AND (C.SiteName = '{}')
AND (A.TransitType = ‘{}’)
GROUP BY TransitRoute;

#LOG TRANSIT QUERY
INSERT INTO takeTransit VALUES (‘{}’,’{}’,’{}’,’{}’).format();


####User Transit History (16)####
#ALL only selected; no other filters
SELECT B.TransitDate, A.TransitRoute, B.TransitType, A.TransitPrice
from beltline.TRANSIT AS A NATURAL JOIN beltline.TAKETRANSIT AS B 
where (B.Username="maria.hernandez");

#SELECT ‘ALL’ for just TransitType
SELECT B.TransitDate, A.TransitRoute, B.TransitType, A.TransitPrice
from beltline.TRANSIT AS A NATURAL JOIN beltline.TAKETRANSIT AS B
where (B.Username="{}") AND (B.TransitDate >='{}' AND B.TransitDate<='{}') 
AND (A.TransitRoute IN (SELECT TransitRoute FROM beltline.CONNECT WHERE SiteName = '{}')) 
AND (A.TransitRoute = '{}');

#SELECT ‘ALL’ with both TransitType and ContainSite
SELECT B.TransitDate, A.TransitRoute, B.TransitType, A.TransitPrice
from beltline.TRANSIT AS A NATURAL JOIN beltline.TAKETRANSIT AS B 
where (B.Username="{}") AND (B.TransitDate >='{}' AND B.TransitDate<='{}') 
AND (A.TransitRoute IN (select TransitRoute from beltline.CONNECT where SiteName = '{}')) AND (A.TransitRoute = '{}')
AND (A.TransitRoute IN (select TransitRoute from beltline.CONNECT where SiteName IN (SELECT SiteName from beltline.CONNECT)));

#SELECT anything but ALL
SELECT B.TransitDate, A.TransitRoute, B.TransitType, A.TransitPrice
from beltline.TRANSIT AS A NATURAL JOIN beltline.TAKETRANSIT AS B
where (B.Username="{}") AND (B.TransitDate >='{}' AND B.TransitDate<='{}') AND 
(B.TransitType IN (select TransitType from beltline.TRANSIT where TransitType = '{}')) AND 
(A.TransitRoute IN (select TransitRoute from beltline.CONNECT where SiteName = '{}')) AND (A.TransitRoute = '{}');

#### Employee Manage Profile (17)####
select Sitename, Concat(Firstname, " ",Lastname) AS Manager, User.username
from beltline.USER, beltline.SITE 
where SITE.ManagerUsername = USER.Username;

####Administrator Manage User(18)####
select exists (select Username from beltline.USER where Username in 
(select Username from beltline.Employee) and Username ="{}");

select username, count(*), UserType, Status from beltline.USER Natural join beltline.USEREMAIL group by username;

#Select “ALL” status, distinct user type
select username, count(*), UserType, Status from beltline.USER Natural join beltline.USEREMAIL
where UserType = "{}"  group by username;

#Select distinct status
select username, count(*), UserType, Status from beltline.USER Natural join beltline.USEREMAIL
where UserType = {} and Status={}  group by username;

#Select distinct status, filter by username
select username, count(*), UserType, Status from beltline.USER Natural join beltline.USEREMAIL
where UserType = {} and Status={} and username={} group by username;		 	 

#Select “ALL” status, filter by username
select username, count(*), UserType, Status from beltline.USER Natural join beltline.USEREMAIL
where UserType = {}  and username={} group by username;	


####Administrator Manage Site (19)####
CREATE or Replace VIEW SiteTable AS 
SELECT SiteName, Concat(Firstname, ' ',Lastname) as Manager, OpenEveryday
from beltline.USER, beltline.SITE where SITE.ManagerUsername = USER.Username;

#views 
Create or replace View SiteTable as 
select SiteName, Concat(Firstname, " ",Lastname) AS SiteManager, OpenEveryday
from beltline.USER, beltline.SITE 
where SITE.ManagerUsername = USER.Username;

Create or replace view ManagerNameMS as
select Concat(Firstname, " ", Lastname) as ManagerName, Username from beltline.user natural join beltline.employee
where EmployeeType = "Manager";

#Select “ALL” Filter 	 
select * from SiteTable;

#Filter by ‘Open Everyday’ 
select * from SiteTable where OpenEveryday = {};

#Filter by ‘Manager’
select * from SiteTable where Manager = {};

#Filter by ‘SiteName’ 
select * from SiteTable where SiteName = {};

#Filter by ‘Open Everyday’, ‘SiteName’, and ‘Manager’
select * from SiteTable where SiteName = {} and Manager = {} and OpenEveryday = {} ;

#Delete Site 
CREATE OR REPLACE VIEW Managers AS
SELECT Username, concat(FirstName," ",Lastname) as ManagerName FROM beltline.USER 
WHERE Username in(select Username from beltline.EMPLOYEE where employeetype="Manager");

delete from beltline.SITE where SiteName="{}" and ManagerUsername in 
(select Username from Managers where ManagerName = "{}") and OpenEveryday = "{}";

#### Administrator Edit Site (20) ####
SELECT concat(FirstName," ",Lastname) as ManagerName FROM beltline.USER 
where Username in(select Username from beltline.EMPLOYEE where employeetype="Manager")
and Username not in (select ManagerUsername from beltline.SITE);

#Updating the Sitename: 
update beltline.site set SiteName = "UniversityHouse" where Sitename= "Hell on Earth";

#Updating the ZipCode:
update beltline.site set SiteZipcode = 69696 where SiteZipcode= 30309 and SiteName = "UniversityHouse";

#Updating the Address: 
update beltline.site set SiteAddress = "I live here" where SiteAddress= "930 Spring Street NW" and SiteName = "UniversityHouse";

#Updating the Manger Username: 
select * from SiteManagerList ; #to get the managers you can put in the drop down 
update beltline.site set ManagerUsername = “{}” where ManagerUsername= “{}”;

#Updating the OpenEveryday: 
update beltline.site set OpenEveryday = "Yes" where OpenEveryday= "No" and SiteName = "UniversityHouse";

####Administrator Create Site (21)####
create or replace view SiteManagerList as
select Concat(Firstname, " ", Lastname) as Manager, user.Username
from beltline.employee, beltline.user
where employee.Username =user.Username and Employee.EmployeeType = "Manager";

#The query that pulls all of the Managers that manage a site:
select Concat(Firstname, " ",Lastname) AS Manager
from beltline.USER, beltline.SITE 
where SITE.ManagerUsername = USER.Username;
 
insert INTO beltline.SITE values("Brusters", "By Trader Joes", 34567, "Yes", "alucco");

####Administrator Manage Transit (22)####
 

### number 17 ####

# phone Number
update employee set Phone = "6969696969" where Username = "alucco";
#first and last name 
update user set Firstname = "Alexander" where Username = "alucco";
update user set Lastname = "Alexander" where Username = "alucco";
# Insert Email  
insert into Useremail values ("alucco", "wegotthis@gamil.com");
#Delete email 
delete from Useremail where email = "wegotthis@gamil.com";
