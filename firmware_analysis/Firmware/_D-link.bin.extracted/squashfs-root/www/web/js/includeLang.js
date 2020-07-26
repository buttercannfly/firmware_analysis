var DebugMode=0;
var G_Language="zh-cn";

/*function detectLanguage()
{
	var sysLanguage=navigator.systemLanguage?navigator.systemLanguage:navigator.language;
	if(sysLanguage == null || sysLanguage == undefined)
	{
		G_Language="en-us";
		InitLANG("en-us");
	}
	else
	{
		var language=sysLanguage.toLowerCase();
		if(language.indexOf('zh')>-1)
		{
			G_Language="zh-cn";
			InitLANG("zh-cn");
		}
		else
		{
			G_Language="en-us";
			InitLANG("en-us");
		}
	}
	
	
	
}
detectLanguage();*/

//检测当前工作模式
function detectWorkMode()
{
	var HNAP = new HNAP_XML();
	var result_xml = new StringDoc();
	if (result_xml != null)
	{
		result_xml.Set("GetNetworkModeSettings");
		HNAP.SetXMLAsync("GetNetworkModeSettings", result_xml, function(xml)	{	GetLangResult_1nd(xml);	});
	}
}
function GetLangResult_1nd(result_xml)
{
	var GetLangResult_1nd = result_xml.Get("GetNetworkModeSettingsResponse/GetNetworkModeSettingsResult");
	if (GetLangResult_1nd == "OK")
	{
		var work_mode = result_xml.Get("GetNetworkModeSettingsResponse/global_network_mode");
		if(work_mode == "router")
		{
			work_mode = "router";
		}
		$.cookie('work_mode', work_mode, { path: '/' });
		window.location.reload();
	}
}