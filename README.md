create table students (
    student_id number (8) primary key , 
    student_name varchar (50),
    phone varchar (17), 
    email varchar (50)  
); 

create table departments (
    department_id number (7) primary key , 
    department_name varchar (50) not null , 
    student_id number (8), 
    constraint dept_fk foreign key (student_id) references students (student_id ) 
);
create table courses (
    course_id number (3) primary key , 
    course_name varchar (50) not null  , 
    department_id number (7), 
    constraint department_fk foreign key ( department_id )references departments (department_id ) 
);
create table college (
    college_name varchar (50),
    college_id number(8) primary key , 
    email varchar(50) not null , 
    department_id number (8) , 
    constraint dpart_fk foreign key (department_id )references departments (department_id)
); 
create table enrollment (
    course_id number (3), 
    student_id number (8), 
    grade varchar (50), 
    semester varchar (34),  
    constraint stud_fk foreign key (student_id) references students (student_id) , 
    
    constraint fsdjfsaljf foreign key (course_id)references courses (course_id)  
);
create table schedual (
   schedual_id number (8) primary key ,  
   college_id number (8) , 
   course_id number  (3),
    time  number (4,2), 
    day varchar(50) , 
    venue varchar(50) , 
    constraint scd_fk foreign key ( college_id) references college ( college_id), 
    constraint sckdjf_fk foreign key (course_id)references courses (course_id)
); 

---insert values in table students 
insert into students values (1,'mohamed', '01061619748','ahmedkoka2@gmail.com'); 
insert into students values (2,'ahmed', '010420058342','ahmedko2@gmail.com'); 
insert into students values (3,'sara ', '01043028458','ahmed2@gmail.com'); 
insert into students values (4,'karim', '01040298420','ahmedko2@gmail.com'); 
insert into students values (5,'mostafa','010972934792','amedkoka2@gmail.com'); 
insert into students values (6,'yousef', '01043249475','ahdkoka2@gmail.com'); 
insert into students values (7,'ziad', '010082843432','ahmeoka2@gmail.com'); 
---insert values in table department 
insert into departments values (100, 'cse', 1) ; 
insert into departments values (101, 'wer', 2) ; 
insert into departments values (102, 'cre', 3) ; 
insert into departments values (103, 'cewrjl', 4) ; 
insert into departments values (104, 'clsjfla', 5) ; 
select *from departments ; 
-----insert values in table courses 
insert into courses values (1,'database',100) ; 
insert into courses values (2,'machinelearning ',103) ; 
insert into courses values (3,'data_analist',101) ; 
insert into courses values (4,'embeded system',102) ; 
insert into courses values (5,'software enginering',103) ; 
insert into courses values (6,'webdesign',104) ; 
insert into courses values (7,'frontend ',101) ; 
select *from courses ; 
---insert values in table college 
insert into college values ('engineering',50, 'menofiauniverysity.edu.eg',100) ;
---insert values in enrolment 
insert into enrollment values (1,2,'verygood','22-9-2022')  ;
insert into enrollment values (2,3,'excellent','22-10-2023')  ;
insert into enrollment values (4,5,'good','22-11-2021')  ;
insert into enrollment values (3,2,'bad','22-6-2023')  ;
insert into enrollment values (5,4 , 'A+','22-12-2024')  ;
insert into enrollment values (6,2,'B+','22-12-2020')  ;
select*from enrollment ; 
---insert values in schedual
insert into schedual values (23, 50 , 3, 2, 'sutarday','room1') ; 
--querys give me student_name , phone, department_name , course_name --->that enroll in 
select student_name , phone , department_name , course_name from departments d , students s, courses  c where s.student_id =d.student_id and c.department_id =d.department_id ; 
--- change values in studnets
update students 
set student_name ='3bas'
where student_id =3; 
select *from students ; 
