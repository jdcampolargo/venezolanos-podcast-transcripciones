# Transcripciones abiertas de Venezolanos

Archivo abierto en español de las transcripciones de **Venezolanos**, el podcast
de **Rafael Arráiz Lucca** sobre Venezuela y su historia. Está organizado para
leer, buscar, citar y construir herramientas educativas o de investigación con
IA.

**Venezolanos**, presentado por **Rafael Arráiz Lucca**, es un programa sobre el
país y su historia. El archivo reúne episodios sobre historia, democracia,
economía, petróleo, cultura, literatura, ciencia, ciudades, empresas,
instituciones y personajes venezolanos.

## Escuchar y explorar

- [VenezolanosPodcast.com](https://www.venezolanospodcast.com)
- [Todos los episodios](https://www.venezolanospodcast.com/episodios)
- [Explorar por temas](https://www.venezolanospodcast.com/temas)
- [Comienza aquí](https://www.venezolanospodcast.com/comienza-aqui)
- [Spotify](https://open.spotify.com/show/0sn3U68FaP08g9sRtDTO6o)
- [Apple Podcasts](https://podcasts.apple.com/us/podcast/venezolanos/id1482990657)
- [YouTube](https://www.youtube.com/@venezolanospodcast)
- [Overcast](https://overcast.fm/itunes1482990657)
- [RSS](https://anchor.fm/s/efcb9f4/podcast/rss)
- [Sobre Rafael Arráiz Lucca](https://www.venezolanospodcast.com/rafael)
- [Sobre el proyecto](https://www.venezolanospodcast.com/nosotros)
- [Apoyar el proyecto](https://www.venezolanospodcast.com/apoya)

Para buscadores, agentes y modelos de lenguaje:

- [Guía para IA](https://www.venezolanospodcast.com/for-ai)
- [Índice de texto](https://www.venezolanospodcast.com/for-ai.txt)
- [Manifiesto JSON](https://www.venezolanospodcast.com/for-ai.json)
- [llms.txt](https://www.venezolanospodcast.com/llms.txt)
- [Sitemap](https://www.venezolanospodcast.com/sitemap.xml)

## Empieza por aquí

- [Índice por temas, series y episodios](indice/README.md)
- [Catálogo completo en JSON](datos/archivo.json)
- [Cómo contribuir](CONTRIBUTING.md)
- [Aviso de uso y atribución](AVISO-DE-USO.md)

Busca una palabra o una idea en todo el archivo:

```bash
git clone https://github.com/jdcampolargo/venezolanos-podcast-transcripciones.git
cd venezolanos-podcast-transcripciones
rg -i "pacto de puntofijo|constitución de 1961" episodios/
```

Cada episodio vive en una carpeta propia y contiene metadatos estructurados,
la URL canónica y la transcripción:

```text
episodios/
└── la-energia-electrica-en-venezuela-cap-1/
    └── transcripcion.md
```

## Estructura

```text
├── episodios/                  # Una transcripción Markdown por episodio
├── indice/
│   ├── README.md               # Entrada principal
│   ├── episodios.md            # Lista cronológica
│   ├── series.md               # Episodios agrupados por serie
│   └── temas/                  # Índices temáticos
├── datos/
│   └── archivo.json            # Catálogo legible por máquinas
├── scripts/
│   ├── sincronizar_desde_web.py
│   └── validar_archivo.py
└── .github/workflows/
    └── actualizar-archivo.yml  # Sincronización mensual y manual
```

## Usarlo con IA

Los archivos Markdown funcionan directamente con asistentes de programación,
herramientas de búsqueda, cuadernos y sistemas RAG. El frontmatter de cada
episodio incluye título, fecha, serie, temas, enlaces de origen y una huella
SHA-256 de la transcripción.

Ejemplo mínimo en Python:

```python
from pathlib import Path

ruta = Path(
    "episodios/la-energia-electrica-en-venezuela-cap-1/transcripcion.md"
)
documento = ruta.read_text(encoding="utf-8")
metadatos, transcripcion = documento.split("---", 2)[1:]
print(transcripcion[:500])
```

Al generar respuestas, conviene citar el título del episodio, **Venezolanos**,
Rafael Arráiz Lucca y la URL canónica incluida en el archivo. Una respuesta útil
debe permitir volver a la fuente.

## Solicitudes abiertas de proyectos

Inspirada en las *Requests for Startups* de Y Combinator, esta es una lista de
cosas que nos encantaría ver construidas con el archivo. No son tareas
asignadas ni ideas reservadas: cualquier persona puede tomar una, mejorarla o
combinarla con otra.

`[ ]` significa que la solicitud sigue abierta. Cuando exista una versión
pública y funcional, la marcamos como `[x]` y agregamos el proyecto a la
siguiente sección.

- [ ] **Pregúntale a Venezolanos.** Un asistente que responda preguntas usando
  fragmentos verificables y enlaces al episodio exacto.
- [ ] **Buscador semántico.** Encontrar episodios por ideas y preguntas aunque
  el usuario no conozca las palabras empleadas en la transcripción.
- [ ] **Cronología interactiva de Venezuela.** Conectar fechas, gobiernos,
  acontecimientos, personas y episodios en una línea de tiempo explorable.
- [ ] **Mapa histórico de Venezuela.** Ubicar ciudades, batallas,
  infraestructuras, instituciones y transformaciones territoriales con sus
  fuentes.
- [ ] **Grafo de conocimiento venezolano.** Mostrar las relaciones entre
  personas, empresas, partidos, universidades, obras, lugares y acontecimientos.
- [ ] **Expedientes de personajes.** Reunir en una página cada mención y episodio
  relacionado con una figura venezolana, con contexto y citas.
- [ ] **Rutas para profesores.** Crear planes de clase y selecciones de episodios
  por edad, duración, tema y objetivo educativo.
- [ ] **Guías de estudio para estudiantes.** Producir preguntas, conceptos,
  cronologías y fuentes adicionales para secundaria y universidad.
- [ ] **Juego de preguntas y memoria espaciada.** Convertir el archivo en
  cuestionarios verificables, tarjetas y retos para aprender historia.
- [ ] **Rutas de aprendizaje personalizadas.** Recomendar qué escuchar después
  según lo que una persona ya sabe, su edad y los temas que le interesan.
- [ ] **Buscador de momentos en audio.** Alinear texto y audio para llegar al
  minuto exacto de una cita y crear fragmentos compartibles.
- [ ] **Atlas de ideas y desacuerdos.** Encontrar conceptos recurrentes,
  tensiones, cambios de enfoque y explicaciones distintas entre episodios.
- [ ] **Historia económica en datos.** Extraer series, cifras, empresas,
  políticas y acontecimientos económicos para analizarlos y visualizarlos.
- [ ] **Rutas históricas de ciudades.** Transformar episodios sobre Caracas y
  otras ciudades en recorridos de arquitectura, instituciones y memoria urbana.
- [ ] **Compañero bilingüe español-inglés.** Ayudar a la diáspora y a estudiantes
  de español a comprender conceptos venezolanos sin perder la fuente original.
- [ ] **Lector accesible.** Ofrecer tipografía adaptable, lectura en voz alta,
  navegación por teclado, resúmenes estructurales y modos de baja distracción.
- [ ] **Servidor MCP de Venezolanos.** Permitir que ChatGPT, Claude y otros
  agentes consulten el archivo con citas y metadatos estructurados.
- [ ] **API y bibliotecas abiertas.** Publicar una API sencilla y clientes para
  Python o JavaScript que permitan consultar episodios, temas, series y textos.
- [ ] **Kit reproducible de RAG o NotebookLM.** Un proyecto inicial que cualquier
  estudiante o desarrollador pueda desplegar y adaptar.
- [ ] **Fábrica de piezas educativas.** Generar tarjetas, hilos, gráficos y
  pequeños videos con una idea verificable y un enlace claro al episodio.

¿Construiste una? Abre un issue para mostrar el trabajo o un pull request que
marque la solicitud, y agrega el nombre, autor, enlace público, código fuente
cuando exista y una frase sobre lo que hace.

## Proyectos construidos con el archivo

Todavía estamos abriendo este camino. El primer proyecto es
[VenezolanosPodcast.com](https://www.venezolanospodcast.com): un archivo
navegable por episodios, series y temas, con páginas preparadas para búsqueda e
IA.

## Precisión y derechos

Las transcripciones pueden contener errores involuntarios. Las correcciones
deben conservar el significado del audio y quedar vinculadas al episodio
original. Consulta [AVISO-DE-USO.md](AVISO-DE-USO.md) antes de reutilizar el
contenido.
