#!/usr/bin/env python3
"""Package committed source and the reviewed original patch units; never reads firmware."""
import argparse,hashlib,json,re,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tools.check_release import CODE_FILES,SHUTTER_UNIT,SOURCE_FILES,MANIFEST,TAG,check_release,need
from z8patch.compiled import compile_unit
# The unit count rides on the checked-in code allowlist, which check_release
# keeps equal to the compiled.json unit set plus the shutter-sound unit.
__doc__=f'Package committed source and {len(CODE_FILES)} reviewed original patch units; never reads firmware.'

def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def verified_upstream(path):
    """Every member of a released upstream toolkit, checked against that archive's own manifest."""
    with zipfile.ZipFile(path) as archive:
        names=[e.filename for e in archive.infolist()];listed=[n for n in names if n.endswith('/'+MANIFEST)]
        need(len(names)==len(set(names)) and len(listed)==1,'Upstream toolkit manifest missing, ambiguous or duplicated')
        prefix=listed[0][:-len(MANIFEST)-1];record=json.loads(archive.read(listed[0]))
        need('files' in record,'Upstream toolkit manifest lacks member digests')
        need({n[len(prefix)+1:] for n in names}==set(record['files'])|{MANIFEST},'Upstream toolkit member mismatch')
        members={n:archive.read(prefix+'/'+n) for n in record['files']}
    for n,m in record['files'].items():need(len(members[n])==m['bytes'] and hashlib.sha256(members[n]).hexdigest()==m['sha256'],'Upstream toolkit member digest mismatch: '+n)
    return json.loads(members['resources/compiled.json'])['units'],members
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--tag',required=True)
    ap.add_argument('--compiler',default='clang');ap.add_argument('--upstream-toolkit',type=Path)
    ap.add_argument('--shutter-unit',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    need(re.fullmatch(TAG,a.tag),'Invalid release tag');need(not a.output.exists(),'Output directory already exists')
    need(not git('status','--porcelain','--untracked-files=normal').strip(),'Commit source changes before packaging')
    commit=git('rev-parse','HEAD').decode().strip()
    need(set(git('ls-tree','-r','--name-only','HEAD').decode().splitlines())==set(SOURCE_FILES),'Tracked source differs from release allowlist')
    subprocess.run([sys.executable,'-B',str(ROOT/'tools/check_repository.py'),'--all'],cwd=ROOT,check=True)
    files={n:git('show','HEAD:'+n) for n in SOURCE_FILES}
    need(all(raw==(ROOT/n).read_bytes() for n,raw in files.items()),'Working tree differs from committed source')
    units=json.loads(files['resources/compiled.json'])['units'];upstream=None
    for name,profile in units.items():
        # A unit ships from local compilation only when every pinned field reproduces;
        # otherwise it must come byte-identical from the released upstream toolkit.
        cause=''
        try:code,detail=compile_unit(name,a.compiler);local=detail==profile
        except (OSError,ValueError,subprocess.CalledProcessError) as e:local=False;cause='; local compile failed: '+str(e)
        if local:files[profile['resource']]=code;continue
        need(a.upstream_toolkit,'Unit does not reproduce with --compiler; provide --upstream-toolkit: '+name+cause)
        if upstream is None:upstream=verified_upstream(a.upstream_toolkit)
        pins,members=upstream
        need(name in pins and pins[name]==profile,'Upstream toolkit pins a different unit: '+name+cause)
        code=members.get(profile['resource'])
        need(code is not None and len(code)==profile['bytes'] and hashlib.sha256(code).hexdigest()==profile['sha256'],'Upstream unit bytes differ from the reviewed recipe: '+name)
        files[profile['resource']]=code
    pin=json.loads(files['resources/shuttersound.json']);shutter=a.shutter_unit.read_bytes()
    need(len(shutter)==pin['bytes'] and hashlib.sha256(shutter).hexdigest()==pin['sha256'],'Shutter-sound unit differs from resources/shuttersound.json')
    files[SHUTTER_UNIT]=shutter
    record=dict(schema=3,tag=a.tag,source_commit=commit,compiled_units=units,shuttersound_unit={k:pin[k] for k in ('bytes','sha256','filled_sha256','compiler')},files={n:dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for n,raw in sorted(files.items())})
    files[MANIFEST]=(json.dumps(record,indent=2)+'\n').encode()
    a.output.mkdir(parents=True,exist_ok=False);prefix='NikonFirmwarePatch-'+a.tag
    target=a.output/(prefix+'-toolkit.zip')
    with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,raw in sorted(files.items()):
            e=zipfile.ZipInfo(prefix+'/'+name,date_time=(2026,1,1,0,0,0));e.create_system=3;e.external_attr=0o100644<<16;e.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(e,raw)
    verified=check_release(target,commit)
    with (a.output/'SHA256SUMS.txt').open('x') as f:f.write(verified['archive_sha256']+'  '+target.name+'\n')
    print(json.dumps(verified,indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,zipfile.BadZipFile,subprocess.CalledProcessError) as e:raise SystemExit('ERROR: '+str(e))
