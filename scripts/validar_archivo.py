#!/usr/bin/env python3
"""Valida estructura, metadatos, contenido e índices del archivo generado."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


MINIMUM_TRANSCRIPTS = 300
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKER = "\n## Transcripción\n\n"
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")


def fail(message: str) -> None:
    raise RuntimeError(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Valida el archivo de transcripciones.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--minimum", type=int, default=MINIMUM_TRANSCRIPTS)
    return parser.parse_args()


def required_string(record: dict[str, Any], key: str, slug: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f"{slug}: falta {key}")
    return value


def validate_episode(root: Path, record: dict[str, Any]) -> None:
    slug = required_string(record, "slug", "<sin-slug>")
    if not SLUG_PATTERN.fullmatch(slug):
        fail(f"{slug}: formato de slug inválido")

    for key in (
        "titulo",
        "fecha_publicacion",
        "url_canonica",
        "sha256_transcripcion",
    ):
        required_string(record, key, slug)

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", record["fecha_publicacion"]):
        fail(f"{slug}: fecha inválida")
    if not record["url_canonica"].endswith(f"/episodios/{slug}"):
        fail(f"{slug}: URL canónica no corresponde al slug")
    if not re.fullmatch(r"[0-9a-f]{64}", record["sha256_transcripcion"]):
        fail(f"{slug}: SHA-256 inválido")
    if not isinstance(record.get("temas"), list):
        fail(f"{slug}: temas inválidos")

    path = root / "episodios" / slug / "transcripcion.md"
    if not path.is_file():
        fail(f"{slug}: falta {path.relative_to(root)}")
    text = path.read_text("utf-8")
    if not text.startswith("---\n") or MARKER not in text:
        fail(f"{slug}: estructura Markdown inválida")

    body = text.split(MARKER, 1)[1]
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    if digest != record["sha256_transcripcion"]:
        fail(f"{slug}: la huella del cuerpo no coincide con el catálogo")
    if len(body.split()) != record.get("palabras"):
        fail(f"{slug}: el conteo de palabras no coincide")
    if len(body.split()) < 50:
        fail(f"{slug}: transcripción inesperadamente corta")

    expected_lines = {
        f"titulo: {json.dumps(record['titulo'], ensure_ascii=False)}",
        f"slug: {json.dumps(slug, ensure_ascii=False)}",
        f"fecha_publicacion: {json.dumps(record['fecha_publicacion'])}",
        f"url_canonica: {json.dumps(record['url_canonica'])}",
        "programa: \"Venezolanos\"",
        "presentador: \"Rafael Arráiz Lucca\"",
        "idioma: \"es-VE\"",
    }
    frontmatter = text.split("---", 2)[1]
    missing = [line for line in expected_lines if line not in frontmatter.splitlines()]
    if missing:
        fail(f"{slug}: frontmatter incompleto: {missing}")


def validate_links(root: Path) -> int:
    checked = 0
    for index_file in sorted((root / "indice").rglob("*.md")):
        text = index_file.read_text("utf-8")
        for target in MARKDOWN_LINK.findall(text):
            if "://" in target:
                continue
            resolved = (index_file.parent / target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                fail(f"{index_file}: enlace sale del repositorio: {target}")
            if not resolved.is_file():
                fail(f"{index_file}: enlace roto: {target}")
            checked += 1
    return checked


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    manifest_path = root / "datos" / "archivo.json"
    if not manifest_path.is_file():
        fail("Falta datos/archivo.json")

    manifest = json.loads(manifest_path.read_text("utf-8"))
    records = manifest.get("episodios")
    if not isinstance(records, list):
        fail("episodios debe ser una lista")
    if len(records) < args.minimum:
        fail(f"Solo hay {len(records)} transcripciones; mínimo: {args.minimum}")
    if manifest.get("cantidad_transcripciones") != len(records):
        fail("El total del catálogo no coincide con su lista de episodios")

    slugs = [record.get("slug") for record in records if isinstance(record, dict)]
    if len(slugs) != len(records) or len(set(slugs)) != len(slugs):
        fail("Hay registros inválidos o slugs duplicados")

    for record in records:
        validate_episode(root, record)

    paths = sorted((root / "episodios").glob("*/transcripcion.md"))
    if len(paths) != len(records):
        fail(
            f"El catálogo contiene {len(records)} episodios, pero el árbol tiene "
            f"{len(paths)} archivos"
        )
    actual_slugs = {path.parent.name for path in paths}
    if actual_slugs != set(slugs):
        fail("El catálogo y las carpetas de episodios no contienen los mismos slugs")

    link_count = validate_links(root)
    print(
        f"Validación correcta: {len(records)} transcripciones y "
        f"{link_count} enlaces internos."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

