(function($){
	var ms = {
		init:function(totalsubpageTmep,args){
			return (function(){
				ms.fillHtml(totalsubpageTmep,args);
				ms.bindEvent(totalsubpageTmep,args);
			})();
		},
		//���html
		fillHtml:function(totalsubpageTmep,args){
			return (function(){
				totalsubpageTmep="";
				/************************START*********************/
				if(args.currPage > 1){
					totalsubpageTmep += "<li class='ali'><a href='javascript:void(0);' class='geraltTb_pager' data-go='' >prev</a></li>";
				}else{
					totalsubpageTmep += "<li class='ali'><a href='javascript:void(0);' class='geraltTb_pager' data-go='' >prev</a></li>";
				}
				
				// ҳ����ڵ���4��ʱ����ӵ�һ��ҳ��Ԫ��
				if(args.currPage!=1 && args.currPage>=4 && args.totalPage!=4) {
					totalsubpageTmep += "<li class='ali'><a href='javascript:void(0);' class='geraltTb_pager' data-go='' >"+1+"</a></li>";
				}
				/* ��ǰҳ��>4, ����<=��ҳ�룬��ҳ��>5����ӡ���������*/
				if(args.currPage-2>2 && args.currPage<=args.totalPage && args.totalPage>5) {
					totalsubpageTmep += "<li class='ali'><a href='javascript:void(0);' class='geraltTb_' data-go='' >...</a></li>";
				}
				/* ��ǰҳ���ǰ��ҳ */
				var start = args.currPage-2;
				/* ��ǰҳ��ĺ���ҳ */
				var end = args.currPage+2;
				
				if((start>1 && args.currPage<4) || args.currPage==1) {
					end++;
				}
				if(args.currPage>args.totalPage-4 && args.currPage>=args.totalPage) {
					start--;
				}
				
				for(; start<=end; start++) {
					if(start<=args.totalPage && start>=1) {
						if(start != args.currPage) {
							totalsubpageTmep += "<li class='ali'><a href='javascript:void(0);' class='geraltTb_pager' data-go='' >"+start+"</a></li>";
						}else{
							totalsubpageTmep += "<li class='ali'><a href='javascript:void(0);' class='geraltTb_pager' data-go='' >"+start+"</a></li>";
						}
					}
				}
				
				if(args.currPage+2<args.totalPage-1 && args.currPage>=1 && args.totalPage>5) {
					totalsubpageTmep += "<li class='ali'><a href='javascript:void(0);' class='geraltTb_' data-go='' >...</a></li>";
				}
				
				if(args.currPage!=args.totalPage && args.currPage<args.totalPage-2 && args.totalPage!=4) {
					totalsubpageTmep += "<li class='ali'><a href='javascript:void(0);' class='geraltTb_pager' data-go='' >"+args.totalPage+"</a></li>";
				}
				
				if(args.current < args.totalPage){
					totalsubpageTmep += "<li class='ali'><a href='javascript:void(0);' class='geraltTb_pager' data-go='' >next</a></li>";
				}else{
					totalsubpageTmep += "<li class='ali'><a href='javascript:void(0);' class='geraltTb_pager' data-go='' >next</a></li>";
				}
				$(".pagination").html(totalsubpageTmep);
                $(".pagination li").eq(args.currPage).addClass('active');
			})();
		},
		//���¼�
		bindEvent:function(totalsubpageTmep,args){
			return (function(){
				totalsubpageTmep.on("click","a.geraltTb_pager",function(event){
					var current = parseInt($(this).text());
                    var index = $(this).closest('li').index();
					ms.fillHtml(totalsubpageTmep,{"currPage":current,"totalPage":args.totalPage,"turndown":args.turndown});
					if(typeof(args.backFn)=="function"){
						args.backFn(current);
					}
				});
				//��һҳ
				/*
				totalsubpageTmep.on("click",".geraltTb_pager",function(){
					var current = parseInt($(".geraltTb_pager a").text());
					ms.fillHtml(totalsubpageTmep,{"currPage":current-1,"pageCount":args.pageCount,"turndown":args.turndown});
					if(typeof(args.backFn)=="function"){
						console.log("b:"+current-1);
						args.backFn(current-1);
					}
				});
				//��һҳ
				totalsubpageTmep.on("click",".geraltTb_pager",function(){
					var current = parseInt($(".geraltTb_pager a").text());
					ms.fillHtml(totalsubpageTmep,{"currPage":current+1,"pageCount":args.pageCount,"turndown":args.turndown});
					if(typeof(args.backFn)=="function"){
						console.log("c:"+current+1);
						args.backFn(current+1);
					}
				});
				*/
			})();
		}
	}
	$.fn.createPage = function(options){		
		ms.init(this,options);
	}
})(jQuery);
