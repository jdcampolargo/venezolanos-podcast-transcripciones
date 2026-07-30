#!/usr/bin/env python3
"""Sincroniza el archivo desde las páginas públicas de VenezolanosPodcast.com."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ARCHIVE_URL = "https://www.venezolanospodcast.com/for-ai.json"
MINIMUM_TRANSCRIPTS = 300
USER_AGENT = (
    "transcripciones-venezolanos-podcast-sync/1.0 "
    "(https://github.com/jdcampolargo/transcripciones-venezolanos-podcast)"
)
GENERATED_DIRECTORIES = ("episodios", "indice", "datos")
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class NextDataParser(HTMLParser):
    """Extrae el JSON del script __NEXT_DATA__ sin dependencias externas."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._inside = False
        self._parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag == "script" and dict(attrs).get("id") == "__NEXT_DATA__":
            self._inside = True

    def handle_data(self, data: str) -> None:
        if self._inside:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._inside:
            self._inside = False

    @property
    def text(self) -> str:
        return "".join(self._parts)


def fetch_bytes(url: str, attempts: int = 4, timeout: int = 45) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
            "User-Agent": USER_AGENT,
        },
    )
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_error = error
            if attempt < attempts:
                time.sleep(min(2**attempt, 8))
    raise RuntimeError(f"No se pudo recuperar {url}: {last_error}")


def fetch_json(url: str) -> dict[str, Any]:
    try:
        return json.loads(fetch_bytes(url).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"JSON inválido en {url}: {error}") from error


def normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def transcript_body(blocks: Any, slug: str) -> str:
    if not isinstance(blocks, list) or not blocks:
        raise RuntimeError(f"{slug}: la página no contiene bloques de transcripción")

    rendered: list[str] = []
    paragraph_count = 0
    for position, block in enumerate(blocks, start=1):
        if not isinstance(block, dict):
            raise RuntimeError(f"{slug}: bloque {position} no es un objeto")
        kind = block.get("type")
        text = normalize_text(block.get("text"))
        if not text:
            raise RuntimeError(f"{slug}: bloque {position} vacío")
        if kind == "heading":
            rendered.append(f"## {text}")
        elif kind == "paragraph":
            rendered.append(text)
            paragraph_count += 1
        else:
            raise RuntimeError(f"{slug}: tipo de bloque desconocido: {kind!r}")

    body = "\n\n".join(rendered).strip() + "\n"
    if paragraph_count == 0 or len(body.split()) < 50:
        raise RuntimeError(f"{slug}: transcripción inesperadamente corta")
    return body


def extract_episode(record: dict[str, Any]) -> dict[str, Any]:
    slug = record.get("slug")
    url = record.get("canonicalUrl")
    if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug):
        raise RuntimeError(f"Slug inválido en el manifiesto: {slug!r}")
    if not isinstance(url, str) or not url.endswith(f"/episodios/{slug}"):
        raise RuntimeError(f"{slug}: URL canónica inválida")

    html = fetch_bytes(url).decode("utf-8")
    parser = NextDataParser()
    parser.feed(html)
    if not parser.text:
        raise RuntimeError(f"{slug}: falta __NEXT_DATA__")

    try:
        data = json.loads(parser.text)
        page_props = data["props"]["pageProps"]
        episode = page_props["episode"]
        blocks = page_props["transcript"]
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise RuntimeError(f"{slug}: datos de página inválidos: {error}") from error

    if episode.get("slug") != slug:
        raise RuntimeError(
            f"{slug}: la página devolvió otro episodio: {episode.get('slug')!r}"
        )
    if normalize_text(episode.get("title")) != normalize_text(record.get("title")):
        raise RuntimeError(f"{slug}: el título difiere entre el índice y la página")

    body = transcript_body(blocks, slug)
    published = str(record.get("publishedAt") or "")
    try:
        published_date = datetime.fromisoformat(
            published.replace("Z", "+00:00")
        ).date().isoformat()
    except ValueError as error:
        raise RuntimeError(f"{slug}: fecha inválida: {published!r}") from error

    topics = episode.get("topics") or []
    if not isinstance(topics, list):
        raise RuntimeError(f"{slug}: temas inválidos")
    topic_slugs = [topic.get("slug") for topic in topics if isinstance(topic, dict)]
    if topic_slugs != record.get("topicSlugs"):
        raise RuntimeError(f"{slug}: los temas difieren entre el índice y la página")

    sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return {
        "slug": slug,
        "titulo": normalize_text(record.get("title")),
        "descripcion": normalize_text(record.get("description")),
        "fecha_publicacion": published_date,
        "url_canonica": url,
        "url_spotify": str(episode.get("link") or ""),
        "url_audio": str(episode.get("audioUrl") or ""),
        "serie": normalize_text(episode.get("series")),
        "serie_slug": str(episode.get("seriesSlug") or ""),
        "temas": [
            {
                "slug": str(topic.get("slug") or ""),
                "nombre": normalize_text(topic.get("name")),
            }
            for topic in topics
            if isinstance(topic, dict)
        ],
        "palabras": len(body.split()),
        "sha256_transcripcion": sha256,
        "_body": body,
    }


def yaml_scalar(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def episode_markdown(episode: dict[str, Any]) -> str:
    topic_slugs = [topic["slug"] for topic in episode["temas"]]
    lines = [
        "---",
        f"titulo: {yaml_scalar(episode['titulo'])}",
        f"slug: {yaml_scalar(episode['slug'])}",
        f"fecha_publicacion: {yaml_scalar(episode['fecha_publicacion'])}",
        'programa: "Venezolanos"',
        'presentador: "Rafael Arráiz Lucca"',
        'idioma: "es-VE"',
        f"descripcion: {yaml_scalar(episode['descripcion'])}",
        f"serie: {yaml_scalar(episode['serie'])}",
        f"serie_slug: {yaml_scalar(episode['serie_slug'])}",
        f"temas: {yaml_scalar(topic_slugs)}",
        f"url_canonica: {yaml_scalar(episode['url_canonica'])}",
        f"url_spotify: {yaml_scalar(episode['url_spotify'])}",
        f"url_audio: {yaml_scalar(episode['url_audio'])}",
        f"palabras: {episode['palabras']}",
        f"sha256_transcripcion: {yaml_scalar(episode['sha256_transcripcion'])}",
        "---",
        "",
        f"# {episode['titulo']}",
        "",
        "## Transcripción",
        "",
        episode["_body"].rstrip(),
        "",
    ]
    return "\n".join(lines)


def markdown_link(text: str) -> str:
    return text.replace("[", r"\[").replace("]", r"\]")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def build_generated_tree(
    root: Path,
    archive: dict[str, Any],
    episodes: list[dict[str, Any]],
    source_url: str,
) -> None:
    episode_root = root / "episodios"
    index_root = root / "indice"
    data_root = root / "datos"
    for directory in (episode_root, index_root / "temas", data_root):
        directory.mkdir(parents=True, exist_ok=True)

    for episode in episodes:
        write_text(
            episode_root / episode["slug"] / "transcripcion.md",
            episode_markdown(episode),
        )

    episode_lines = [
        "# Todos los episodios con transcripción",
        "",
        f"Total: **{len(episodes)}**.",
        "",
    ]
    for episode in episodes:
        title = markdown_link(episode["titulo"])
        episode_lines.append(
            f"- [{title}](../episodios/{episode['slug']}/transcripcion.md)"
            f" — {episode['fecha_publicacion']}"
        )
    write_text(index_root / "episodios.md", "\n".join(episode_lines) + "\n")

    by_series: dict[str, list[dict[str, Any]]] = {}
    for episode in episodes:
        series = episode["serie"] or "Sin serie"
        by_series.setdefault(series, []).append(episode)

    series_lines = ["# Series", ""]
    for series, members in sorted(
        by_series.items(), key=lambda item: (-len(item[1]), item[0].casefold())
    ):
        series_lines.extend([f"## {series}", "", f"{len(members)} episodios.", ""])
        for episode in members:
            title = markdown_link(episode["titulo"])
            series_lines.append(
                f"- [{title}](../episodios/{episode['slug']}/transcripcion.md)"
                f" — {episode['fecha_publicacion']}"
            )
        series_lines.append("")
    write_text(index_root / "series.md", "\n".join(series_lines))

    episodes_by_topic: dict[str, list[dict[str, Any]]] = {}
    for episode in episodes:
        for topic in episode["temas"]:
            episodes_by_topic.setdefault(topic["slug"], []).append(episode)

    topic_lines: list[str] = []
    for topic in archive.get("topics", []):
        slug = topic.get("slug")
        members = episodes_by_topic.get(slug, [])
        if not slug or not members:
            continue
        title = normalize_text(topic.get("name"))
        topic_lines.append(
            f"- [{markdown_link(title)}](temas/{slug}.md) — "
            f"{len(members)} transcripciones"
        )
        page_lines = [
            f"# {title}",
            "",
            normalize_text(topic.get("description")),
            "",
            f"[Explorar este tema en VenezolanosPodcast.com]({topic.get('url')})",
            "",
            f"## {len(members)} transcripciones",
            "",
        ]
        for episode in members:
            episode_title = markdown_link(episode["titulo"])
            page_lines.append(
                f"- [{episode_title}]"
                f"(../../episodios/{episode['slug']}/transcripcion.md)"
                f" — {episode['fecha_publicacion']}"
            )
        write_text(
            index_root / "temas" / f"{slug}.md", "\n".join(page_lines) + "\n"
        )

    index_lines = [
        "# Índice del archivo",
        "",
        f"Este repositorio contiene **{len(episodes)} transcripciones publicadas** "
        "de Venezolanos.",
        "",
        "## Entradas",
        "",
        "- [Todos los episodios](episodios.md)",
        "- [Series](series.md)",
        "- [Catálogo JSON](../datos/archivo.json)",
        "",
        "## Temas",
        "",
        *topic_lines,
        "",
    ]
    write_text(index_root / "README.md", "\n".join(index_lines))

    public_episodes = []
    for episode in episodes:
        public_episodes.append(
            {key: value for key, value in episode.items() if key != "_body"}
        )
    payload = {
        "schema_version": 1,
        "programa": "Venezolanos",
        "presentador": "Rafael Arráiz Lucca",
        "idioma": "es-VE",
        "sitio": "https://www.venezolanospodcast.com",
        "fuente_indice": source_url,
        "cantidad_transcripciones": len(public_episodes),
        "episodios": public_episodes,
    }
    write_text(
        data_root / "archivo.json",
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    )


def validate_generated_tree(root: Path, expected_count: int) -> None:
    manifest = json.loads((root / "datos" / "archivo.json").read_text("utf-8"))
    episodes = manifest.get("episodios")
    if not isinstance(episodes, list) or len(episodes) != expected_count:
        raise RuntimeError("El catálogo generado no conserva todos los episodios")

    paths = list((root / "episodios").glob("*/transcripcion.md"))
    if len(paths) != expected_count:
        raise RuntimeError("El árbol generado no conserva todas las transcripciones")

    for episode in episodes:
        path = root / "episodios" / episode["slug"] / "transcripcion.md"
        text = path.read_text("utf-8")
        marker = "\n## Transcripción\n\n"
        if marker not in text:
            raise RuntimeError(f"{episode['slug']}: falta el cuerpo de transcripción")
        body = text.split(marker, 1)[1]
        digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if digest != episode["sha256_transcripcion"]:
            raise RuntimeError(f"{episode['slug']}: huella de contenido inconsistente")


def current_count(root: Path) -> int:
    path = root / "datos" / "archivo.json"
    if not path.exists():
        return 0
    try:
        data = json.loads(path.read_text("utf-8"))
        return int(data.get("cantidad_transcripciones", 0))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        raise RuntimeError("El catálogo existente no se puede validar")


def replace_generated_directories(root: Path, generated: Path) -> None:
    backup = generated / ".backup"
    backup.mkdir()
    installed: list[str] = []
    backed_up: list[str] = []
    try:
        for name in GENERATED_DIRECTORIES:
            destination = root / name
            previous = backup / name
            if destination.exists():
                os.replace(destination, previous)
                backed_up.append(name)
            os.replace(generated / name, destination)
            installed.append(name)
    except Exception:
        for name in reversed(installed):
            destination = root / name
            if destination.exists():
                shutil.rmtree(destination)
        for name in reversed(backed_up):
            previous = backup / name
            if previous.exists():
                destination = root / name
                if not destination.exists():
                    os.replace(previous, destination)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sincroniza transcripciones desde la web pública."
    )
    parser.add_argument("--archive-url", default=ARCHIVE_URL)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--minimum", type=int, default=MINIMUM_TRANSCRIPTS)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--allow-decrease",
        action="store_true",
        help="Permite una disminución deliberada del número de transcripciones.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    archive = fetch_json(args.archive_url)
    records = [
        record
        for record in archive.get("episodes", [])
        if isinstance(record, dict) and record.get("hasTranscript")
    ]
    announced = archive.get("counts", {}).get("transcripts")
    if announced != len(records):
        raise RuntimeError(
            f"El manifiesto anuncia {announced} transcripciones, pero enumera "
            f"{len(records)}"
        )
    if len(records) < args.minimum:
        raise RuntimeError(
            f"Solo se encontraron {len(records)} transcripciones; mínimo: "
            f"{args.minimum}"
        )

    previous_count = current_count(root)
    if previous_count and len(records) < previous_count and not args.allow_decrease:
        raise RuntimeError(
            f"El total bajaría de {previous_count} a {len(records)}. "
            "Revise la fuente y use --allow-decrease solo si es intencional."
        )

    print(f"Recuperando {len(records)} transcripciones públicas…", flush=True)
    episodes: list[dict[str, Any]] = []
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {executor.submit(extract_episode, record): record for record in records}
        for position, future in enumerate(as_completed(futures), start=1):
            record = futures[future]
            try:
                episodes.append(future.result())
            except Exception as error:
                failures.append(f"{record.get('slug')}: {error}")
            if position % 25 == 0 or position == len(records):
                print(f"  {position}/{len(records)} páginas revisadas", flush=True)

    if failures:
        sample = "\n".join(f"  - {failure}" for failure in failures[:20])
        raise RuntimeError(
            f"Fallaron {len(failures)} episodios; no se modificó el archivo:\n{sample}"
        )

    episodes.sort(
        key=lambda episode: (episode["fecha_publicacion"], episode["slug"]),
        reverse=True,
    )
    slugs = [episode["slug"] for episode in episodes]
    if len(slugs) != len(set(slugs)):
        raise RuntimeError("La fuente contiene slugs duplicados")

    temporary = Path(tempfile.mkdtemp(prefix=".sync-", dir=root))
    try:
        build_generated_tree(temporary, archive, episodes, args.archive_url)
        validate_generated_tree(temporary, len(episodes))
        replace_generated_directories(root, temporary)
    finally:
        shutil.rmtree(temporary, ignore_errors=True)

    print(f"Archivo sincronizado: {len(episodes)} transcripciones.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
