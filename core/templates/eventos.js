Eventos=[    {%for evento in Eventos%}

{

    fecha : "{{evento.fecha}}",
    sala  :"{{evento.sala}}",
    bloque :"{{evento.bloque}}",
    curso  :"{{evento.curso}}",
    cursos : [{%for curso in evento.output%}"{{curso}}",{%endfor%}],
    profesor :"{{evento.profesor}}",
    tipo     :"{{evento.tipo}}",

    codigo  :"",
    seccion :"01"


},

{% endfor %}];
