function makeMove(cId) {
    var canv = document.getElementById("space-"+cId);
    var con = canv.getContext("2d");
    drawO(con);

    function drawX(ctx) {
        ctx.beginPath();
        ctx.moveTo(15,15);
        ctx.lineTo(60,60);
        ctx.moveTo(60,15);
        ctx.lineTo(15,60);
        ctx.stroke();
        ctx.closePath();
    }

    function drawO(ctx) {
        ctx.beginPath();
        ctx.arc(37,38,28,0,Math.PI*2,true);
        ctx.stroke();
        ctx.closePath();
    }
}