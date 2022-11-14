var pageNo=0,area_code="",area_flag=1;
var pageFlag="1";
$(function(){
	pageFlag=getQueryString("page");

	$("#top").load("../common/noLoginTop.html");
	$("#footer").load("../common/footer.html");
	bindDivisionDropdownList();
	
})

//获取地址栏参数
function getQueryString(name){
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}
/**
 * 初始化方法
 */

// 翻页
function goPage(code){
//	debugger;
	var rcont=parseInt($("#pageBox .ucPageNum strong").text());// 列表所有条数
		pageOver = 1;
		if(rcont>10){
			pageOver = rcont/10>parseInt(rcont/10)?parseInt(rcont/10)+1:parseInt(rcont/10);
		}
	switch(code) {
		case "first":
			pageNo = 0;
			break;
		case "pre":
			if(pageNo>0){
				pageNo--
			}else{
				return false;
			}
			break;
		case "next":
			if(pageNo+1<pageOver){
				pageNo++
			}else{
				return false;
			}
			break;
		case "last":
			pageNo = pageOver-1;
			break;
		default:
			break;
	}
	$("#pageBox .ucPageFlip .cur").text(pageNo+1);
	noticeOfPublicity(area_code);
}

function showProjectInfo(pUid,sendid){
	window.location.href="notice_of_publicity_content.html?pUid="+pUid+"&sendid="+sendid;
}

//获取地区名称
function bindDivisionDropdownList() {
	//debugger;
	if(pageFlag=='2'){
		postData('/publicannouncement.do?method=getxzTreeNodes','',function(res){
			cityCodeListnb_nb(res);
		})
	}else{
		postData('/publicannouncement.do?method=getxzTreeNodes','',function(res){
			cityCodeList(res);
		})
	}
}
// 初始化所属区划-省市
function cityCodeList(data){
	var str="";
	$("#cityList").empty();
	$.each(data,function(i,k){
		if(k.id == "330000"){
			str+='<li class="cur"><a id="'+k.id.substring(0,4)+'">'+k.name+'</a></li>';
		}else if (k.id.substring(0,4) != "3302"){
			if(k.id.substring(4,6)=="00") str+='<li><a id="'+k.id.substring(0,4)+'">'+k.name+'</a></li>';
		}
	
	})
	area_code = "3300";
	area_flag = 1;
	// 初始化页面搜索
	noticeOfPublicity(area_code);
	$("#cityList").append(str).on("click","li",function(){
		pageNo = 0;
		$("#pageBox .ucPageFlip .cur").text(pageNo+1);
		$(this).addClass("cur").siblings().removeClass("cur");
		var _id = $(this).children("a").attr("id"),
			cstr = "";
		area_code = _id;
		area_flag = 1;
		$("#district_and_county").empty();
		$.each(data,function(i,k){
			if(_id.substring(2,4)!="00"){
				if(k.id.substring(0,4)==_id&&k.id.substring(4,6)!="00") cstr+='<li><a id="'+k.id+'">'+k.name+'</a></li>';
			}else{
				cstr ='<li class="cur"><a id="3300">省本级</a></li>'
			}
		})
		// 省市级查询
		noticeOfPublicity(area_code);
		$("#district_and_county").append(cstr);
	})
	$("#district_and_county").on("click","li",function(){
		pageNo = 0;
		$("#pageBox .ucPageFlip .cur").text(pageNo+1);
		$(this).addClass("cur").siblings().removeClass("cur");
		var _id_ = $(this).children("a").attr("id"),
		area_code = _id_;
		_id_.length>4?area_flag = 0:area_flag = 1;
		// 区县级查询
		noticeOfPublicity(area_code);
	});
}





function cityCodeListnb_nb(data){
	var str="";
	$("#cityList").empty();
	$("#district_and_county").empty();
	$.each(data,function(i,k){
		if(k.id == "330200"){
			str+='<li class="cur"><a id="'+k.id.substring(0,4)+'">'+k.name+'</a></li>';
		}else if(k.id.substring(0,4)== "3302"){
			if(k.id.substring(4,6)=="00") str+='<li><a id="'+k.id.substring(0,4)+'">'+k.name+'</a></li>';
		}
	
	})
	area_code = "3302";
	area_flag = 1;
	// 初始化页面搜索
	noticeOfPublicity(area_code);
	$("#cityList").append(str).on("click","li",function(){
		pageNo = 0;
		$("#pageBox .ucPageFlip .cur").text(pageNo+1);
		$(this).addClass("cur").siblings().removeClass("cur");
		var _id = $(this).children("a").attr("id"),
			cstr = "";
		area_code = _id;
		area_flag = 1;
		$("#district_and_county").empty();
		$.each(data,function(i,k){
			if(_id.substring(2,4)!="00"){
				if(k.id.substring(0,4)==_id&&k.id.substring(4,6)!="00") cstr+='<li><a id="'+k.id+'">'+k.name+'</a></li>';
			}
		})
		// 省市级查询
		noticeOfPublicity(area_code);
		$("#district_and_county").append(cstr);
	})
	$("#"+area_code).click();
	$("#district_and_county").on("click","li",function(){
		pageNo = 0;
		$("#pageBox .ucPageFlip .cur").text(pageNo+1);
		$(this).addClass("cur").siblings().removeClass("cur");
		var _id_ = $(this).children("a").attr("id"),
		area_code = _id_;
		_id_.length>4?area_flag = 0:area_flag = 1;
		// 区县级查询
		noticeOfPublicity(area_code);
	});
	
	
}



function noticeOfPublicity(acode){
	area_code = acode;
	var info = {
		"pageFlag":pageFlag,
		"pageNo":pageNo, // 页码
		"area_code":acode, // 区划代码
		"area_flag":area_flag, // 省市/区县区分代码：1:市本级,0:区县
		"deal_code":isNull($("#projectUuid").val()), // 项目代码
		"item_name":isNull($("#projectName").val()) // 项目名称
	}
	postData('/publicannouncement.do?method=queryItemList',info,function(res){
		console.log(res);
		$("#pageBox .ucPageNum strong").text(res[0].counts);
		$(".query-count").text(res[0].counts);
		var list = res[0].itemList,listStr="";
		$("#bgx_tbody").empty();
		$.each(list,function(j,key){
			listStr += '<tr>'+
					   '<td><a style="color: #0d83bf;" onclick=showProjectInfo("'+key.projectuuid+'","'+key.SENDID+'")>'+key.deal_code+'<br/>'+key.apply_project_name+'</a></td>'+
//					   '<td><a onclick=showProjectInfo("'+key.projectuuid+'","'+key.SENDID+'")>'+key.apply_project_name+'</a></td>'+
					   '<td align="center">'+key.ITEM_NAME+'</td>'+
					   '<td align="center">'+key.DEPT_NAME+'</td>'+
					   '<td align="center">'+key.DEAL_NAME+'</td>'+
					   '<td align="center">'+key.DEAL_TIME.substring(0,10)+'</td>'+
					   '</tr>';
		});
		$("#bgx_tbody").append(listStr);
	})
}