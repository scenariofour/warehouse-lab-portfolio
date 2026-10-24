"""Regression fixtures only; never touch the published raw dataset."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, tempfile, unittest, zipfile
ROOT=Path(__file__).resolve().parents[1]

class ImportRegression(unittest.TestCase):
    def test_corrupt_zip_does_not_overwrite_preserved_raw_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'scripts').mkdir();(root/'data/raw').mkdir(parents=True)
            shutil.copyfile(ROOT/'scripts/prepare_data.py',root/'scripts/prepare_data.py')
            helper=ROOT/'scripts/import_source_zip.py'
            if helper.exists():shutil.copyfile(helper,root/'scripts/import_source_zip.py')
            original=b'Reference;ABCCOD;Sector\nTEST;A;PF\n'
            (root/'data/raw/Product.csv').write_bytes(original)
            entry={'filename':'Product.csv','content_details':{'sha256_hash':hashlib.sha256(original).hexdigest()}}
            (root/'data/manifest.json').write_text(json.dumps({'version':1,'files':[entry]}))
            zpath=root/'corrupt.zip'
            with zipfile.ZipFile(zpath,'w') as z:z.writestr('dataset/Product.csv',b'corrupted payload')
            run=subprocess.run([sys.executable,str(root/'scripts/prepare_data.py'),'--zip',str(zpath)],capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0)
            self.assertEqual((root/'data/raw/Product.csv').read_bytes(),original,'Rejected ZIP replaced the original source bytes')

class ValidatedImportTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0,str(ROOT/'scripts'))
        from import_source_zip import import_source_zip
        self.import_zip=import_source_zip
    def fixture(self,root,entries):
        return [{'filename':name,'content_details':{'sha256_hash':hashlib.sha256(payload).hexdigest()}} for name,payload in entries.items()]
    def test_valid_files_import_and_identical_original_is_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);raw=root/'raw';raw.mkdir();a=b'original';b=b'new verified file';(raw/'Product.csv').write_bytes(a)
            stamp=(raw/'Product.csv').stat().st_mtime_ns;zpath=root/'valid.zip'
            with zipfile.ZipFile(zpath,'w') as z:z.writestr('folder/Product.csv',a);z.writestr('folder/README.txt',b)
            self.assertEqual(self.import_zip(zpath,raw,self.fixture(root,{'Product.csv':a,'README.txt':b})),['README.txt'])
            self.assertEqual((raw/'README.txt').read_bytes(),b);self.assertEqual((raw/'Product.csv').stat().st_mtime_ns,stamp)
    def test_late_bad_member_prevents_all_new_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);raw=root/'raw';raw.mkdir();zpath=root/'bad.zip'
            with zipfile.ZipFile(zpath,'w') as z:z.writestr('README.txt',b'valid');z.writestr('Product.csv',b'invalid')
            with self.assertRaises(ValueError):self.import_zip(zpath,raw,self.fixture(root,{'README.txt':b'valid','Product.csv':b'expected'}))
            self.assertEqual(list(raw.iterdir()),[])
    def test_duplicate_basename_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);raw=root/'raw';raw.mkdir();zpath=root/'duplicate.zip'
            with zipfile.ZipFile(zpath,'w') as z:z.writestr('a/Product.csv',b'valid');z.writestr('b/Product.csv',b'valid')
            with self.assertRaisesRegex(ValueError,'Duplicate'):self.import_zip(zpath,raw,self.fixture(root,{'Product.csv':b'valid'}))
            self.assertEqual(list(raw.iterdir()),[])
    def test_existing_nonpublisher_bytes_are_preserved_for_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);raw=root/'raw';raw.mkdir();(raw/'Product.csv').write_bytes(b'preserve me');zpath=root/'valid.zip'
            with zipfile.ZipFile(zpath,'w') as z:z.writestr('Product.csv',b'publisher')
            with self.assertRaisesRegex(ValueError,'Existing source'):self.import_zip(zpath,raw,self.fixture(root,{'Product.csv':b'publisher'}))
            self.assertEqual((raw/'Product.csv').read_bytes(),b'preserve me')

if __name__=='__main__':unittest.main()
