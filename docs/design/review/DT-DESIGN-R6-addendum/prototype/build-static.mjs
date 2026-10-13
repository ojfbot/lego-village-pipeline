import {cp,mkdir,readdir} from 'node:fs/promises';
import {join} from 'node:path';
for(const dir of ['dt','library','prototypes']) {
 await mkdir(join('dist',dir),{recursive:true});
 await cp(dir,join('dist',dir),{recursive:true,filter:src=>src!=='prototypes/House World.dc.html'});
}
for(const entry of await readdir('.', {withFileTypes:true})) {
 if(entry.isFile() && /\.(?:html|js)$/.test(entry.name) && entry.name!=='vite.config.js') await cp(entry.name,join('dist',entry.name));
}
console.log('Copied inherited Claude sheets, runtime, fonts and model assets.');
