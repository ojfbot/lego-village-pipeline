import { readFileSync } from 'node:fs';
import { flightChapters } from './flight-path.js';

// Audited pronunciations for this copy. Unknown words require human review;
// guessing syllables would silently weaken the rule.
const syllables = {
  loose:1, bricks:1, greet:1, the:1, dawn:1,
  soft:1, light:1, slips:1, through:1, open:2, doors:1,
  green:1, leaves:1, find:1, their:1, home:1,
  steps:1, rise:1, from:1, floor:1,
  small:1, rooms:1, gather:2, round:1, tree:1,
  new:1, worlds:1, wait:1, for:1, hands:1,
};
export function checkChapters(chapters) {
  if (chapters.length!==6) throw new Error('Exactly six chapters must form two haikus.');
  const counts = chapters.map((chapter,index)=>{
    if (!chapter.title.trim() || !chapter.detail.trim() || /[\r\n]/.test(chapter.detail)) throw new Error(`Chapter ${index+1} needs a label and one haiku line.`);
    if (/[^a-zA-Z .,!?;:'’–—-]/.test(chapter.detail)) throw new Error(`Chapter ${index+1} contains unreviewed notation; write the words out.`);
    if (chapter.at<0 || chapter.at>=1 || (index===0 ? chapter.at!==0 : chapter.at<=chapters[index-1].at)) throw new Error('Chapter positions must start at zero and increase before the end.');
    const words = chapter.detail.toLowerCase().match(/[a-z]+(?:['’-][a-z]+)*/g);
    if (!words?.length) throw new Error(`Chapter ${index+1} has no words.`);
    const count = words.reduce((total,word)=>{
      if (!Object.hasOwn(syllables,word)) throw new Error(`Review the syllable count of "${word}" before using it.`);
      return total+syllables[word];
    },0);
    const expected = [5,7,5][index%3];
    if (count!==expected) throw new Error(`Chapter ${index+1} has ${count} syllables; requires ${expected}.`);
    return count;
  });
  return counts;
}
const counts = checkChapters(flightChapters);
const html = readFileSync(new URL('./index.html',import.meta.url),'utf8');
if (!html.includes(`<p id="world-instruction">${flightChapters[0].detail}</p>`)) throw new Error('The initial caption must use the first haiku line.');
console.log(`Chapter copy passes: ${counts.slice(0,3).join('–')} / ${counts.slice(3).join('–')}.`);
