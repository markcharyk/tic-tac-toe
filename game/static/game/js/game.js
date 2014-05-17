function makeMove(cId) {
    $.ajax({
        type: 'POST',
        url: '/play/',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            id: cId,
        },
        dataType: 'json',
        success: function(data) {
            alert(data.msg);
            drawX(con);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert('HTTP Error: '+errorThrown+' | Error Message: '+textStatus);
        }
    });

    var canv = document.getElementById("space-"+cId);
    var con = canv.getContext("2d");

    function drawX(ctx) {
        ctx.beginPath();
        ctx.moveTo(15,15);
        ctx.lineTo(60,60);
        ctx.moveTo(60,15);
        ctx.lineTo(15,60);
        ctx.stroke();
        ctx.closePath();
    }
}


function drawO(ctx) {
    ctx.beginPath();
    ctx.arc(37,38,28,0,Math.PI*2,true);
    ctx.stroke();
    ctx.closePath();
}