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

getScheduleJobsqr = """SELECT 
    [SuperId], 
    [ProcessUrl], 
        CAST([StartDate] AS VARCHAR(10)) AS StartDateStr,          -- Converts date to 'YYYY-MM-DD' format
    LEFT(CAST([StartTime] AS VARCHAR(20)), 8) AS StartTimeStr, -- Extracts 'HH:MM:SS' from time
    LEFT(CAST([EndTime] AS VARCHAR(20)), 8) AS EndTimeStr,     -- Extracts 'HH:MM:SS' from time
    [intervalType], 
    [Interval], 
    [IsActive], 
    [TimeOutSec], 
    [Notes], 
    [DeviceId], 
    [Notify], 
    [FailedAttemptstoNotify] 
FROM [dbo].[ScheduleJobs] 
WHERE [IsActive] = 1 
AND [SuperId] = {0};
"""

insert_ScheduleJobs_query = """
    INSERT INTO [dbo].[ScheduleJobs] 
    ([SuperId], [ProcessUrl], [StartDate], [StartTime], [EndTime], [intervalType], 
    [Interval],  [TimeOutSec], [Notes], [CreatedBy], [DeviceId], [Notify], [FailedAttemptstoNotify]) 
    VALUES ({0}, '{1}','{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}','{9}',{10},{11},{12})
"""

insert_APILogs_query = """INSERT INTO [dbo].[APILogs] ([LastCalled],[JobsId],[ApiResponce],StatusCode,status) 
        VALUES ('{0}',{1},'{2}',{3},'{4}');"""