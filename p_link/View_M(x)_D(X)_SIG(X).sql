Create View MDSIG
AS

Select N = 'S1',  SUM(S*PS) as M,SUM(S*S*PS)-SUM(S*PS)*SUM(S*PS) as DS, SQRT(SUM(S*S*PS)-SUM(S*PS)*SUM(S*PS)) as SIGS From
(Select Cast(S1 as INT) as S,CAST(count(*) as decimal(8,1))/(Select count(*) From dbo.llink) as PS From dbo.llink
Group by S1) as tmp

UNION ALL

Select N = 'S2',  SUM(S*PS) as M,SUM(S*S*PS)-SUM(S*PS)*SUM(S*PS) as DS, SQRT(SUM(S*S*PS)-SUM(S*PS)*SUM(S*PS)) as SIGS From
(Select Cast(S2 as INT) as S,CAST(count(*) as decimal(8,1))/(Select count(*) From dbo.llink) as PS From dbo.llink
Group by S2) as tmp


UNION ALL

Select N = 'S1+S2',  SUM(S*PS) as M,SUM(S*S*PS)-SUM(S*PS)*SUM(S*PS) as DS, SQRT(SUM(S*S*PS)-SUM(S*PS)*SUM(S*PS)) as SIGS From
(Select Cast(S1 as INT)+Cast(S2 as INT) as S,CAST(count(*) as decimal(8,1))/(Select count(*) From dbo.llink) as PS From dbo.llink
Group by Cast(S1 as INT)+Cast(S2 as INT)) as tmp

UNION ALL

Select N = 'S1-S2',  SUM(S*PS) as M,SUM(S*S*PS)-SUM(S*PS)*SUM(S*PS) as DS, SQRT(SUM(S*S*PS)-SUM(S*PS)*SUM(S*PS)) as SIGS From
(Select Cast(S1 as INT)-Cast(S2 as INT) as S,CAST(count(*) as decimal(8,1))/(Select count(*) From dbo.llink) as PS From dbo.llink
Group by Cast(S1 as INT)-Cast(S2 as INT)) as tmp