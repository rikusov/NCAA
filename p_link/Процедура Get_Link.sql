Create procedure Get_Link AS
BEGIN
	Select TOP 1 link From dbo.llink
	where link not in (Select * from dbo.use_link)
END;