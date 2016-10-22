function TimeLeft (char, least) {
    this.char = char;
    this.Enable = new Boolean(false);
    this.start_from = Date.now();
    this.end_at = this.start_from+ least*1000;
    this.least = least;
    this.timerId = 0;
    this.interval = 1000;
    this.percent = 0;
    var thisObject = this;
    this.showCircle = function () {$(".radial-progress").css('display', 'block'); this.progressIt(this.percent);};
    this.hideCircle = function () {$(".radial-progress").css('display', 'none');};
    this.progressIt = function(progress) { if (this.char==charListContainer.char) $('.radial-progress').attr('data-progress', 100-progress);};
    
    this.tick = function (){
        const t = Date.now();
        var pos = t - thisObject.start_from;
        var percent = Math.round(pos*0.1/thisObject.least);
        if (percent>99) percent=99;
        // 显示大的步进
        if (percent - thisObject.percent > 2)
        {
          thisObject.percent = percent;
          thisObject.progressIt(percent);
        }
        if (t>=thisObject.end_at){
          thisObject.Stop();
          return;
        }
       
    };
    


    this.Start = function()
    {
        this.Enable = new Boolean(true);
        this.showCircle();
        thisObject = this;
        if (thisObject.Enable)
        {
            thisObject.timerId = setInterval(
            function()
            {
                thisObject.tick(); 
            }, thisObject.interval);
        }
    };

    this.Stop = function()
    {            
        thisObject.hideCircle();
        thisObject.Enable = new Boolean(false);
        clearInterval(thisObject.timerId);
    };

}
 