// Выгрузка плана объектов из ОС (tools/object-plan/js/03–05-data-*.js) → docs/plan.json
// + сверка размеров с данными ОС (data/objects/<id>.json: real_width_cm × real_height_cm).
// Запуск: node tools/sync_plan.js <путь к клону object-constructor>
const fs = require('fs'), path = require('path'), vm = require('vm');
const src = process.argv[2] || '../mrbobsterx-boop/object-constructor';
const js = path.join(src, 'tools/object-plan/js');
const ctx = { PLAN_ITEMS: [], console };
ctx.addItems = list => list.forEach(i => ctx.PLAN_ITEMS.push(i));
vm.createContext(ctx);
for (const f of ['03-data-shelter.js', '04-data-production.js', '05-data-world.js'])
  vm.runInContext(fs.readFileSync(path.join(js, f), 'utf8'), ctx, { filename: f });
// транслит — как в ОС (building-editor/01-core-utils.js)
const map = {а:'a',б:'b',в:'v',г:'g',д:'d',е:'e',ё:'e',ж:'zh',з:'z',и:'i',й:'y',к:'k',л:'l',м:'m',н:'n',о:'o',п:'p',р:'r',с:'s',т:'t',у:'u',ф:'f',х:'h',ц:'ts',ч:'ch',ш:'sh',щ:'sch',ъ:'',ы:'y',ь:'',э:'e',ю:'yu',я:'ya'};
const translit = s => (s || '').toLowerCase().split('').map(c => map[c] !== undefined ? map[c] : (/[a-z0-9]/.test(c) ? c : '_')).join('').replace(/_+/g, '_').replace(/^_|_$/g, '');
const SKIP = /слом|испорч|разбит|выпотрош|разграбл|сгорев|перевёрнут|перевернут|гнил|заброш|взлом|^открыт|пуст|использован|просроч/i;   // «сломанные» и «состояния» — пропуск
const out = [];
for (const i of ctx.PLAN_ITEMS) {
  let os = null;
  try {
    const d = JSON.parse(fs.readFileSync(path.join(src, 'data/objects', i.id + '.json'), 'utf8'));
    os = [d.behavior.real_width_cm, d.behavior.real_height_cm];
  } catch (e) {}
  const vars = (i.v || []).map(n => ({ name: n, slug: translit(n.replace(/\(.*?\)/g, ' ')), skip: SKIP.test(n) }));
  out.push({ id: i.id, name: i.n, cat: i.c, plan_size: i.sz || null, os_size: os,
             size_mismatch: !!(os && i.sz && (os[0] !== i.sz[0] || os[1] !== i.sz[1])),
             variants: vars, states: i.vis || [], fn: i.fn || '' });
}
fs.writeFileSync(path.join(__dirname, '..', 'docs', 'plan.json'), JSON.stringify(out, null, 1));
const nv = out.reduce((a, o) => a + o.variants.filter(v => !v.skip).length, 0);
console.log(`объектов ${out.length}, вариантов к модели ${nv}, расхождений размеров ${out.filter(o => o.size_mismatch).length}, нет в ОС ${out.filter(o => !o.os_size).length}`);
