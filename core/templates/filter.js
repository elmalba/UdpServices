aas = function ( data ) {
    return ! data ?
        '' :
        typeof data === 'string' ?
            data
                .replace( /\n/g, ' ' )
                .replace( /[áâàä]/g, 'a' )
                .replace( /[éêèë]/g, 'e' )
                .replace( /[íîìï]/g, 'i' )
                .replace( /[óôòö]/g, 'o' )
                .replace( /[úûùü]/g, 'u' )
                .replace( /ç/g, 'c' ) :
            data;
};

var text,filttext,d;
startsWithSearch = function( idx, searchValue ) {
    var ret = false;
    if (searchValue) {
        text = aas($(this).text().toLowerCase());
        filttext = aas(searchValue);
        filttext = filttext.toLowerCase();
        dass = text.match(filttext);
        if (dass == null) {
            return true;
        }
    }
    return ret;
};


 var output = '';

     {% for curso in cursos%}{% if curso.curso != "" %}
        output += '<li>{{curso.curso}} <br>{{ curso.profesor}}<br>Sección #{{curso.codigo.split("-")[1]}} <br>Bloque {{curso.bloque}} <br>Sala {{curso.sala}}</li>';    {%endif%}

    {%endfor%}


 $('#filter').append(output);
    $("document").ready( function (){


 $("#filter").filterable('option', 'filterCallback', startsWithSearch);

});

