getactivejobs = """SELECT jb.id,jb.superid,jb.processurl,jb.startdate,jb.starttime,jb.endtime,jb.interval,jb.intervaltype,MAX(al.lastcalled) AS lastcalled
FROM [dbo].[ScheduleJobs] jb
left JOIN [dbo].[APILogs] al ON al.JobsId = jb.Id
WHERE jb.startdate <= GETDATE()  and jb.IsActive = 1  and jb.DeviceId = {0}
GROUP BY jb.id,jb.superid,jb.processurl,jb.startdate,jb.starttime,jb.endtime,jb.interval,jb.intervaltype
ORDER BY LastCalled DESC;
"""

getfailedNotifyData = """SELECT jb.id,jb.superid,jb.processurl,jb.intervaltype
,count(al.lastcalled) AS lastcalled,jb.Notify,jb.FailedAttemptstoNotify,jb.DeviceId,jb.notes,
 (
        SELECT TOP 1 al_sub.ApiResponce
        FROM [dbo].[APILogs] al_sub 
        WHERE al_sub.JobsId = jb.Id
        ORDER BY al_sub.lastcalled DESC -- Get the latest response
    ) AS ApiResponce
FROM [dbo].[ScheduleJobs] jb
left JOIN [dbo].[APILogs] al ON al.JobsId = jb.Id
WHERE jb.startdate <= GETDATE()  and jb.IsActive = 1 and jb.Notify=1 
GROUP BY jb.id,jb.superid,jb.processurl,jb.intervaltype,jb.Notify,jb.FailedAttemptstoNotify,jb.DeviceId,jb.notes
HAVING 
    COUNT(al.lastcalled) >= jb.FailedAttemptstoNotify;"""