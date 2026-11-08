"""Populate public assets from an exact, checksum-pinned preview manifest."""
import concurrent.futures,hashlib,json,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
def mirror(row):
    if not row.get('mirrored'): return None
    path=(ROOT/row['path']).resolve()
    if path.parent!=ROOT/'assets': raise ValueError('Invalid asset path')
    path.parent.mkdir(exist_ok=True)
    def valid():
        return path.exists() and path.stat().st_size==row['downloadedBytes'] and hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256']
    if valid(): return row['path']
    if row.get('transformation'): raise ValueError('Pre-remuxed MP4 must be uploaded: '+row['path'])
    temporary=path.with_suffix(path.suffix+'.part')
    for attempt in range(3):
        try:
            request=urllib.request.Request(row['url'],headers={'User-Agent':'MotionLibraryMediaMirror/1.0'})
            with urllib.request.urlopen(request,timeout=90) as response, temporary.open('wb') as output:
                size=0; digest=hashlib.sha256()
                while chunk:=response.read(1024*1024):
                    size+=len(chunk)
                    if size>row['downloadedBytes']: raise ValueError('Unexpected extra bytes')
                    digest.update(chunk);output.write(chunk)
            if size!=row['downloadedBytes'] or digest.hexdigest()!=row['sha256']: raise ValueError('Source changed: checksum mismatch')
            temporary.replace(path)
            return row['path']
        except Exception:
            temporary.unlink(missing_ok=True)
            if attempt==2: raise
            time.sleep(2**attempt)
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        count=sum(path is not None for path in pool.map(mirror,manifest['assets']))
    print(f'Verified {count} mirrored assets; all SHA-256 hashes match.')
