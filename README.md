# Archivo abierto de transcripciones de Venezolanos

Un archivo en español de las transcripciones publicadas por
[VenezolanosPodcast.com](https://www.venezolanospodcast.com), organizado para
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
git clone https://github.com/jdcampolargo/venezolanos-podcast-transcripts.git
cd venezolanos-podcast-transcripts
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

## ¿Qué podemos construir?

La ambición no es guardar texto por guardar texto. Es convertir décadas de
historia venezolana narrada en una base abierta para aprender, investigar y
crear. Algunas posibilidades:

- un buscador semántico que responda con citas y enlaces al episodio exacto;
- líneas de tiempo de personas, instituciones, gobiernos, empresas y ciudades;
- mapas de relaciones entre episodios, temas y series;
- guías de estudio para colegios, universidades y la diáspora venezolana;
- visualizaciones de los cambios políticos, económicos y culturales del país;
- comparadores que encuentren ideas recurrentes, tensiones y cambios de enfoque;
- un grafo de conocimiento sobre la historia de Venezuela;
- herramientas de audio, lectura accesible y aprendizaje bilingüe;
- investigaciones, artículos, clubes de lectura y materiales docentes con
  referencias verificables.

¿Construiste algo con estas transcripciones? Abre un pull request y agrégalo a
la sección **Proyectos construidos con el archivo**.

## Proyectos construidos con el archivo

Todavía estamos abriendo este camino. El primer proyecto es
[VenezolanosPodcast.com](https://www.venezolanospodcast.com): un archivo
navegable por episodios, series y temas, con páginas preparadas para búsqueda e
IA.

## Actualización automática

Una acción de GitHub consulta mensualmente el índice público y las páginas
canónicas de VenezolanosPodcast.com. Solo publica una actualización si:

1. puede recuperar todas las transcripciones anunciadas como públicas;
2. el total no cae respecto del archivo anterior;
3. cada episodio conserva metadatos completos;
4. la huella del texto coincide con el catálogo JSON;
5. todos los enlaces internos generados apuntan a archivos existentes.

También puede ejecutarse manualmente desde la pestaña **Actions**. La
automatización lee únicamente la web pública y no modifica el sitio ni su
pipeline de publicación.

## Precisión y derechos

Las transcripciones pueden contener errores involuntarios. Las correcciones
deben conservar el significado del audio y quedar vinculadas al episodio
original. Consulta [AVISO-DE-USO.md](AVISO-DE-USO.md) antes de reutilizar el
contenido.

