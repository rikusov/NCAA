CREATE TRIGGER NO_Insert
On dbo.llink
INSTEAD OF INSERT
AS 
Insert into dbo.llink
Select * From inserted Where link not in (Select link From dbo.llink)