function search_tweets() {
    let input = document.getElementById('searchbar').value
    let x =document.getElementById('list');
    x.innerHTML='';
    $.getJSON("search_twitter?count=10&query="+input,
        function(data) {
            for (i =0 ; i <data.value.length ; i++ ){
                let color="";
                if (data.result[i]=="0"){
                    color="list-group-item-success";
                }else if(data.result[i]=="1"){
                    color="list-group-item-dark";
                }else{
                    color="list-group-item-danger";
                }
                x.innerHTML+="<li class='list-group-item "+color+"'><span>"+data.value[i]+"</span></li>";
            }
        });
}
function evaluating() {
    let input = document.getElementById('manual_text');
    $.getJSON("predict?str="+input.value,
        function(data) {
            if (data.value=="0"){
                input.style="padding-left: 0px;margin-left: 28px;margin-right: 28px;padding-right: 5px ; border:solid 3px green;";
            }else if(data.value=="1"){
                input.style="padding-left: 0px;margin-left: 28px;margin-right: 28px;padding-right: 5px ;border:solid 3px gray;";
            }else{
                input.style="padding-left: 0px;margin-left: 28px;margin-right: 28px;padding-right: 5px ;border:solid 3px red;";
            }
        });
}


