Cursos= {    {%for curso in cursos%}{% if curso.curso != "" %}
"{{curso.codigo}}": {curso:'{{curso.curso}}', profesor:"{{ curso.profesor}}", bloque:"{{curso.bloque}}", sala:"{{curso.sala}}", seccion: "{{curso.seccion}}", tipo:"{{curso.tipo}}"    }
,
    {%endif %}
    {% endfor %}

};
Dia={fecha :"Lunes 4 de Abril"};
version = {{version}}