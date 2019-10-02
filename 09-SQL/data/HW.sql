drop table employees cascade;
drop table departments cascade;
drop table dept_manager cascade;
drop table dept_emp cascade;
drop table salaries cascade;
drop table titles cascade;

-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/kZ3Izp

CREATE TABLE "employees" (
    "emp_no" int   NOT NULL,
    "birth_date" date   NOT NULL,
    "first_name" varchar   NOT NULL,
    "last_name" varchar   NOT NULL,
    "gender" varchar   NOT NULL,
    "hire_date" date   NOT NULL,
    CONSTRAINT "pk_employees" PRIMARY KEY (
        "emp_no"
     )
);

CREATE TABLE "departments" (
    "dept_no" varchar   NOT NULL,
    "dept_name" varchar   NOT NULL,
    CONSTRAINT "pk_departments" PRIMARY KEY (
        "dept_no"
     )
);

CREATE TABLE "dept_emp" (
    "emp_no" int   NOT NULL,
    "dept_no" varchar   NOT NULL,
    "from_date" date   NOT NULL,
    "to_date" date   NOT NULL,
    CONSTRAINT "pk_dept_emp" PRIMARY KEY (
        "emp_no","dept_no"
     )
);

CREATE TABLE "dept_manager" (
    "dept_no" varchar   NOT NULL,
    "emp_no" int   NOT NULL,
    "from_date" date   NOT NULL,
    "to_date" date   NOT NULL,
    CONSTRAINT "pk_dept_manager" PRIMARY KEY (
        "dept_no","emp_no"
     )
);

CREATE TABLE "salaries" (
    "emp_no" int   NOT NULL,
    "salary" int   NOT NULL,
    "from_date" date   NOT NULL,
    "to_date" date   NOT NULL,
    CONSTRAINT "pk_salaries" PRIMARY KEY (
        "emp_no"
     )
);


CREATE TABLE "titles" (
    "emp_no" int   NOT NULL,
    "title" varchar   NOT NULL,
    "from_date" date   NOT NULL,
    "to_date" date   NOT NULL,
    CONSTRAINT "pk_titles" PRIMARY KEY (
        "emp_no","from_date"
     )
);

ALTER TABLE "dept_emp" ADD CONSTRAINT "fk_dept_emp_emp_no" FOREIGN KEY("emp_no")
REFERENCES "employees" ("emp_no");

ALTER TABLE "dept_emp" ADD CONSTRAINT "fk_dept_emp_dept_no" FOREIGN KEY("dept_no")
REFERENCES "departments" ("dept_no");

ALTER TABLE "dept_manager" ADD CONSTRAINT "fk_dept_manager_dept_no" FOREIGN KEY("dept_no")
REFERENCES "departments" ("dept_no");

ALTER TABLE "dept_manager" ADD CONSTRAINT "fk_dept_manager_emp_no" FOREIGN KEY("emp_no")
REFERENCES "employees" ("emp_no");

ALTER TABLE "salaries" ADD CONSTRAINT "fk_salaries_emp_no" FOREIGN KEY("emp_no")
REFERENCES "employees" ("emp_no");

ALTER TABLE "titles" ADD CONSTRAINT "fk_titles_emp_no" FOREIGN KEY("emp_no")
REFERENCES "employees" ("emp_no");


-- 96.7% of 300,024 associates worked for exactly 1 year.
-- the emp_no numbers do not repeat...  so these are not annual raises and
-- when employee titles change, their pay doesn't seem to...
-- This also is a pretty big company...  there's a lot that is fishy about
-- this data...

select * from salaries;
select * from titles;
select * from dept_manager;
select * from departments;
select * from employees;
select * from dept_emp;

-- 1. List the following details of each employee: employee number, last name, 
-- first name, gender, and salary.
select employees.emp_no, employees.last_name, employees.first_name, employees.gender, salaries.salary
from employees
left outer join salaries on salaries.emp_no = employees.emp_no;

-- 2. List employees who were hired in 1986.
select emp_no, last_name, first_name, gender, date_part('year',hire_date)
from employees
where date_part('year',hire_date) = 1986;

-- 3. List the manager of each department with the following information: 
-- department number, department name, the manager's employee number, last name, 
-- first name, and start and end employment dates.
select departments.dept_no, departments.dept_name, dept_manager.emp_no, employees.last_name, employees.first_name,
	employees.hire_date, salaries.to_date
from departments
left outer join dept_manager on dept_manager.dept_no = departments.dept_no
left outer join employees on dept_manager.emp_no = employees.emp_no
left outer join salaries on salaries.emp_no = employees.emp_no;

-- 4. List the department of each employee with the following information: 
-- employee number, last name, first name, and department name.
select departments.dept_name, employees.emp_no, employees.last_name, employees.first_name
from employees
left outer join dept_emp on dept_emp.emp_no = employees.emp_no
left outer join departments on dept_emp.dept_no = departments.dept_no
order by departments.dept_name;

-- 5. List all employees whose first name is "Hercules" and last names begin with "B."
select employees.emp_no, employees.first_name, employees.last_name
from employees
where employees.first_name = 'Hercules' and employees.last_name like 'B%';

-- 6. List all employees in the Sales department, including their employee number, 
-- last name, first name, and department name.
select departments.dept_name, employees.emp_no, employees.last_name, employees.first_name
from departments
left outer join dept_emp on dept_emp.dept_no = departments.dept_no
left outer join employees on employees.emp_no = dept_emp.emp_no
where departments.dept_name = 'Sales';

-- 7. List all employees in the Sales and Development departments, including their 
-- employee number, last name, first name, and department name.
select departments.dept_name, employees.emp_no, employees.last_name, employees.first_name
from departments
left outer join dept_emp on dept_emp.dept_no = departments.dept_no
left outer join employees on employees.emp_no = dept_emp.emp_no
where departments.dept_name = 'Sales' or departments.dept_name = 'Development'
order by departments.dept_name;

-- 8. In descending order, list the frequency count of employee last names, 
-- i.e., how many employees share each last name.

Select * from
(
select distinct(employees.last_name), count(1)over(partition by employees.last_name) as ct
from employees
)a
Where ct > 0
order by ct desc;

