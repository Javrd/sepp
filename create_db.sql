drop database if exists `aib_db`;
drop user if exists 'aib-manager'@'%';
create database `aib_db`;
use `aib_db`;
create user 'aib-manager'@'%' identified by password '*2B8C05FA01D31C12C56D2B9390ACA60504E17D3C';
grant select, insert, update, delete, create, drop, references, index, alter, 
create temporary tables, lock tables, create view, create routine,
 alter routine, execute, trigger, show view 
on `aib_db`.* to 'aib-manager'@'%';
grant select, insert, update, delete, create, drop, references, index, alter, 
create temporary tables, lock tables, create view, create routine,
 alter routine, execute, trigger, show view 
on `test_aib_db`.* to 'aib-manager'@'%';
