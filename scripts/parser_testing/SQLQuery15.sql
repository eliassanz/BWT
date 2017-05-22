

DECLARE @in_record_id int;
DECLARE @in_xml XML;
DECLARE @port_id int;
DECLARE @crossing_type int;

    
set @in_record_id = 901
set @port_id = 250401
set @crossing_type = 7
SELECT @in_xml = xml_doc  from dbo.border_wait_time_XML2 where record_id = @in_record_id

DECLARE @xml_record_date datetime;
DECLARE @max_wait_time_date datetime;
DECLARE @wait_time smallint;
DECLARE @lanes_open smallint;
DECLARE @xpath_partial varchar(50);

-- set these to 200 instead of 100 other wise you will
-- truncate 
DECLARE @xpath_hour varchar(200);
DECLARE @xpath_datetime varchar(200);
DECLARE @xpath_wait_time varchar(200);
DECLARE @xpath_lanes_open varchar(200);

DECLARE @in_record_date_sql nvarchar(max);
DECLARE @ParamDefinition nvarchar(500);

--Get the XPATH partial string for the crossing type--
SELECT @xpath_partial = xpath_partial FROM [dbo].[crossing_type] WHERE crossing_type_id = @crossing_type

--Build the necessary XPATH's dynamically based on port id and crossing type (xpath_partial)--
SET @xpath_hour = REPLACE('(/border_wait_time/port[port_number=' + cast(@port_id as varchar(10)) + ']/' + @xpath_partial + '/update_time)[1]','''', '''''')
SET @xpath_datetime = REPLACE('(/border_wait_time/port[port_number=' + cast(@port_id as varchar(10)) + ']/date)[1]','''', '''''')
SET @xpath_wait_time = REPLACE('(/border_wait_time/port[port_number=' + cast(@port_id as varchar(10)) + ']/' + @xpath_partial + '/delay_minutes)[1]','''', '''''')
SET @xpath_lanes_open = REPLACE('(/border_wait_time/port[port_number=' + cast(@port_id as varchar(10)) + ']/' + @xpath_partial + '/lanes_open)[1]','''', '''''')

--select @xpath_wait_time
--select @xpath_hour

--Build the SQL to parse the inputted XML document-- 
SET @in_record_date_sql = N'SELECT @xml_record_dateOUT = dateadd(HH,[dbo].[time_of_day_hour_parser](
			@exec_in_xml.value(N''' + @xpath_hour + N''', ''nvarchar(max)'')), 
			cast(@exec_in_xml.value(N''' + @xpath_datetime + N''',''nvarchar(max)'') as datetime)),
			@xml_wait_timeOUT = [dbo].[border_wait_time_parser](@exec_in_xml.value(N''' + @xpath_wait_time +  N''',''varchar(25)'')),
			@xml_lanes_openOUT = @exec_in_xml.value(N''' + @xpath_lanes_open + N''',''smallint'')'

--select @in_record_date_sql
--The XPATH has to be a string literal--
--These next two lines trick T-SQL into thinking it is a string literal--
--http://www.logue.com.ar/blog/2009/11/dynamic-xpath-using-xml-datatype-in-sql-server/--
--http://social.msdn.microsoft.com/Forums/en-US/sqlxml/thread/b93d0790-e239-459e-a4e3-7511475f548b--
SET @ParamDefinition = N'@exec_in_xml xml, @xml_record_dateOUT datetime OUTPUT, @xml_wait_timeOUT smallint OUTPUT, @xml_lanes_openOUT smallint OUTPUT'
EXEC sp_executesql @in_record_date_sql, @ParamDefinition, @exec_in_xml=@in_xml, @xml_record_dateOUT=@xml_record_date OUTPUT, @xml_wait_timeOUT=@wait_time OUTPUT, @xml_lanes_openOUT=@lanes_open OUTPUT;

select @port_id as portid, @crossing_type as crossing_type, @xml_record_date as xmldate, @lanes_open as lanesopen
, @wait_time as waittime, @in_record_id as recid

