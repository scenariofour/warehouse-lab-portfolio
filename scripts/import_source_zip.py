"""Validate known publisher files before importing; never replace preserved raw bytes."""
import hashlib
from pathlib import Path, PurePosixPath
import tempfile
import zipfile

def import_source_zip(archive: Path, raw: Path, files: list[dict]) -> list[str]:
    expected={f['filename']:f['content_details']['sha256_hash'] for f in files}
    staged={}
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            if member.is_dir():continue
            name=PurePosixPath(member.filename).name
            if name not in expected:continue
            if name in staged:raise ValueError(f'Duplicate source filename in ZIP: {name}')
            payload=z.read(member)
            if hashlib.sha256(payload).hexdigest()!=expected[name]:
                raise ValueError(f'Hash mismatch in ZIP: {name}; no source files imported')
            target=raw/name
            if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()!=expected[name]:
                raise ValueError(f'Existing source differs from publisher hash: {name}; preserved for review')
            staged[name]=payload
    if not staged:raise ValueError('ZIP contains no recognized publisher files')
    raw.mkdir(parents=True,exist_ok=True)
    imported=[]
    with tempfile.TemporaryDirectory(dir=raw) as tmp:
        for name,payload in staged.items():
            target=raw/name
            if target.exists():continue
            p=Path(tmp)/name;p.write_bytes(payload);p.replace(target);imported.append(name)
    return imported
