# Cómo contribuir

Gracias por ayudar a que la historia venezolana sea más fácil de encontrar,
estudiar y citar.

## Corregir una transcripción

Abre un issue con:

- el título y la URL canónica del episodio;
- el fragmento que parece incorrecto;
- la corrección propuesta;
- el minuto aproximado del audio o una fuente confiable para verificar nombres,
  fechas y lugares.

No se aceptan reescrituras que cambien el sentido, agreguen hechos no dichos o
conviertan la transcripción en un resumen.

Las transcripciones se sincronizan desde VenezolanosPodcast.com. Una corrección
permanente debe incorporarse primero en la fuente pública; de lo contrario, la
siguiente sincronización automática podría reemplazarla.

## Proponer un proyecto

Si construiste una herramienta, visualización, investigación, guía educativa o
experimento con este archivo, agrega una entrada breve a la sección **Proyectos
construidos con el archivo** de `README.md`. Incluye:

- nombre y enlace público;
- una frase concreta sobre lo que hace;
- autor o equipo;
- cómo usa o cita las transcripciones.

## Cambiar scripts o índices

Antes de abrir un pull request:

```bash
python3 scripts/sincronizar_desde_web.py
python3 scripts/validar_archivo.py
git diff --check
```

Los validadores comprueban estructura, conteos, huellas de contenido y enlaces.
No certifican que cada afirmación histórica sea correcta: esa revisión exige
escuchar el audio y consultar fuentes.

