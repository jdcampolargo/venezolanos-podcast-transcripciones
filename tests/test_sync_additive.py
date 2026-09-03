import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "sincronizar_desde_web.py"
SPEC = importlib.util.spec_from_file_location("sync_archive", MODULE_PATH)
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


def episode(slug, title):
    body = f"Texto histórico de {title}. " * 20 + "\n"
    return {
        "slug": slug,
        "titulo": title,
        "fecha_publicacion": "2026-01-01",
        "url_canonica": f"https://www.venezolanospodcast.com/episodios/{slug}",
        "temas": [],
        "palabras": len(body.split()),
        "sha256_transcripcion": "0" * 64,
        "_body": body,
    }


class AdditiveSyncTests(unittest.TestCase):
    def test_default_merge_updates_overlap_and_preserves_orphan(self):
        old_overlap = episode("episodio-actual", "Título anterior")
        fresh_overlap = episode("episodio-actual", "Título actualizado")
        orphan = episode("episodio-historico", "Título histórico")

        merged, preserved = SYNC.merge_with_existing(
            [fresh_overlap], [old_overlap, orphan]
        )

        self.assertEqual(preserved, 1)
        self.assertEqual({item["slug"] for item in merged}, {
            "episodio-actual", "episodio-historico"
        })
        self.assertEqual(
            next(item for item in merged if item["slug"] == "episodio-actual")["titulo"],
            "Título actualizado",
        )

    def test_allow_decrease_is_the_only_way_to_prune_orphans(self):
        fresh = episode("episodio-actual", "Título actualizado")
        orphan = episode("episodio-historico", "Título histórico")

        merged, preserved = SYNC.merge_with_existing(
            [fresh], [orphan], allow_decrease=True
        )

        self.assertEqual(merged, [fresh])
        self.assertEqual(preserved, 0)


if __name__ == "__main__":
    unittest.main()
