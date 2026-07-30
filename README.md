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
- [Cómo contribuir](COMO-CONTRIBUIR.md)
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

Estas no son veinte variaciones del mismo buscador. Son apuestas independientes
para convertir el archivo en educación, investigación, infraestructura pública,
cultura y nuevas instituciones. Algunas pueden comenzar como un proyecto de fin
de semana; otras podrían convertirse en una organización.

`[ ]` significa que la solicitud sigue abierta. Cuando exista una versión
pública y funcional, la marcamos como `[x]` y agregamos el proyecto a la
siguiente sección.

### Infraestructura de conocimiento

- [ ] **RAG abierto de Venezolanos.** Un sistema que permita conversar con todo
  el archivo, muestre la cita y el episodio detrás de cada respuesta, reconozca
  cuando no sabe algo y pueda desplegarse o adaptarse con facilidad.
- [ ] **Identidades históricas abiertas.** Asignar identificadores estables a
  personas, instituciones, empresas, lugares, gobiernos y obras para conectar
  este archivo con bibliotecas, museos, Wikipedia y otros repositorios.
- [ ] **Prueba pública para la IA venezolana.** Crear un conjunto de preguntas
  difíciles, respuestas documentadas y métricas que revelen cuándo un modelo
  inventa nombres, fechas o hechos sobre Venezuela.
- [ ] **Infraestructura lingüística venezolana.** Construir un diccionario de
  pronunciaciones, topónimos, apellidos y correcciones para mejorar
  transcripción, síntesis de voz y traducción del español venezolano.

### Educación para una generación

- [ ] **Libro de texto vivo de Venezuela.** Convertir episodios y fuentes
  adicionales en una obra abierta, modular y actualizable para estudiantes,
  con versiones por edad y rutas para docentes.
- [ ] **Biblioteca venezolana sin internet.** Empaquetar audio autorizado,
  transcripciones y materiales educativos para escuelas, bibliotecas y
  comunidades con conectividad limitada.
- [ ] **El reto venezolano.** Un juego diario de preguntas con rachas, ligas
  entre colegios, desafíos familiares y resultados compartibles, donde cada
  respuesta revele el episodio y la historia detrás del dato.
- [ ] **Universo infantil de historia venezolana.** Crear libros ilustrados,
  animaciones, juegos y actividades que presenten personajes e instituciones
  sin convertir la historia en propaganda ni sacrificar precisión.

### Investigación y memoria pública

- [ ] **Laboratorio de memoria de políticas públicas.** Rastrear el origen, los
  objetivos, los resultados y las consecuencias de decisiones sobre petróleo,
  electricidad, educación, democracia e infraestructura.
- [ ] **Venezuela económica en datos.** Transformar cifras y acontecimientos
  dispersos en conjuntos de datos revisables sobre empresas, moneda, comercio,
  energía, empleo e industrialización.
- [ ] **Rescate de citas para Wikipedia.** Detectar páginas débiles o ausentes
  sobre Venezuela y preparar paquetes de evidencia para que editores humanos
  mejoren artículos con fuentes confiables.
- [ ] **Red de historia oral venezolana.** Extender el archivo con testimonios
  de distintas regiones, generaciones y oficios mediante consentimiento claro,
  preservación de originales y reglas contra la explotación.

### Cultura y experiencias

- [ ] **Museo digital de Venezuela.** Un espacio inmersivo donde episodios,
  documentos, fotografías, mapas y objetos permitan recorrer épocas y temas
  como una exposición, no como una lista de enlaces.
- [ ] **Videojuego de decisiones históricas.** Una experiencia narrativa donde
  el jugador dirija una ciudad, una empresa, un periódico o un gobierno en un
  momento decisivo y luego compare su recorrido con lo que ocurrió realmente.
- [ ] **Rutas de memoria aumentada.** Recorridos físicos por Caracas y otras
  ciudades que activen historias, planos, fotografías y audio al llegar a cada
  lugar.
- [ ] **Estudio abierto de documentales y animación.** Convertir las mejores
  series en piezas audiovisuales rigurosas para YouTube, escuelas, televisión y
  festivales, con una cadena editorial y de derechos explícita.

### Distribución e instituciones

- [ ] **Venezolanos por WhatsApp.** Un producto diseñado para llegar a familias
  y comunidades con una historia breve, una pregunta y una fuente cada día, sin
  exigir que el usuario descubra primero el archivo.
- [ ] **Red de sindicación educativa.** Preparar paquetes con derechos claros
  para radios comunitarias, colegios, bibliotecas, boletines y medios de la
  diáspora que quieran compartir el contenido.
- [ ] **Fondo de proyectos de memoria venezolana.** Organizar becas, premios y
  residencias para estudiantes, docentes, investigadores, artistas y
  desarrolladores que conviertan el archivo en trabajo público duradero.
- [ ] **Programa mundial de estudios venezolanos.** Crear un curso común,
  clubes locales y materiales bilingües para universidades y comunidades de la
  diáspora, conectando cada sede con investigadores y archivos venezolanos.

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
