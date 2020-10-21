var URL = "{{url_for('updateAjax', person_id = person_id)}}";
//changes politician support.
$("#politician-list").on("click", ".rate", function(event){    
    event.preventDefault();
   /*  var feelings = $(this).find(['[name = feelings]']).val();
    var person_id = $(this).val();
    $('#person_id').val(x);
    console.log(person_id); */
    //$("#politician label").css('font-weight', 'normal');
    //$(this).closest("label").css('font-weight', 'Bold');
    //var support = $(this).attr("value");
    /* //var num = $(this).closest("tr").attr("data-tt");
    $.post(URL, {'feelings':feelings,'person_id':person_id},ratePolitician(obj)); */
    }
);

//rates politician support.
function ratePolitician(obj){
    if(obj.error){
        $("#errors").empty().html('Error: ' + obj.err);
    }
    else{
      /*   politician = obj.person;
        feeling = obj.feelings;
        $("[feelings = "+politician+"]").find("feelings").text(feeling); */
        //var num = obj.num;
        //id = "#" + num;
        //$(id).text(obj.avg_rating);
        
    }
}