    DECLARE @record_id int;
    DECLARE @xml_doc XML;
    
    set @record_id = 901
    
    SELECT @xml_doc = xml_doc  from dbo.border_wait_time_XML2 where record_id = @record_id
	
	--SY PV Standard
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250401, 1

	--SY PV Ready
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250401, 4

	--SY PV SENTRI
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250401, 7

	--SY Ped Standard
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250401, 10

	--SY Ped Ready
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250401, 13

	--OM PV Standard
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250601, 1

	--OM PV Ready
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250601, 4

	--OM PV SENTRI
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250601, 7

	--OM CV Standard
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250602, 19

	--OM CV FAST
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250602, 22

	--OM Ped Standard
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250601, 10
	
	--OM Ped Ready
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250601, 13

	--Tecate PV Standard
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250501, 1

	--Tecate CV Standard
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250501, 19

	--Tecate Ped Standard
	EXECUTE [dbo].[normalize_xml_record] @record_id, @xml_doc, 250501, 10