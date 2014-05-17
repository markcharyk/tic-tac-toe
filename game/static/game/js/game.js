function makeMove(cId) {
    var canv = document.getElementById("space-"+cId);
    var con = canv.getContext("2d");

    $.ajax({
        type: 'POST',
        url: '/play/',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            id: cId,
            board_id: $('.game-board').attr('id')
        },
        dataType: 'json',
        success: function(data) {
            drawX(con);
            if(data.O) {
                canv = document.getElementById("space-"+data.O);
                con = canv.getContext("2d");
                drawO(con)
            }
            if(data.msg) {
                alert(data.msg);
            }
            if(data.end) {
                $('canvas').attr('onclick', '')
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            alert('HTTP Error: '+errorThrown+' | Error Message: '+textStatus);
        }
    });
}

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