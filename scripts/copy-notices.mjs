import {readFileSync,writeFileSync} from 'node:fs';
const notices=['THIRD_PARTY_NOTICES.md','node_modules/three/LICENSE','node_modules/lucide/LICENSE'];
writeFileSync('dist/THIRD_PARTY_NOTICES.txt',notices.map(path=>path+'\n\n'+readFileSync(path,'utf8')).join('\n\n'));
