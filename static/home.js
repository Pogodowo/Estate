console.log('działa')

function PageUpdate (){
        $.ajax({
                        type: 'GET',
                        url: 'PageUpdateUrl',
                        success : function(response){console.log('sukces ajaxa ');

                        },//koniec sukcesa
                        error : function (error){console.log('brak sukcesu ajaxa ')},
                        })

}

PageUpdate()