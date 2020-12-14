CREATE TRIGGER Delete_None_Link
On dbo.llink
AFTER INSERT
AS 
DELETE FROM dbo.llink Where link = 'None'