// PROTOTYPE: no network writes, no durable state, no live agent service.
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { flightChapters } from './flight-path.js';
import { HouseWorld } from './world.js';
import { pages } from './modules.js';
import { initialState, facts, demoProposals } from './demo-state.js';
import { renderSheet, escapeHTML as e, proposalSketch } from './sheets.js';

const $ = (selector) => document.querySelector(selector);
let state = initialState();
let current = null;
let entryElement = null;
let entering = false;
let enterToken = 0;
let callers = [];
const announce = (message) => {
  $('#announcer').textContent = '';
  requestAnimationFrame(() => { $('#announcer').textContent = message; });
};
const record = (text, origin = 'Human · demo') => { state.log.push({ text, origin }); announce(text); };
const findPage = (code) => pages.find((item) => item.code === code);
gsap.registerPlugin(ScrollTrigger);
const world = new HouseWorld($('#house-stage'), (module) => enter(module, $('#module-search')), announce);

let roomMatches = [];
let activeRoomCode = null;
const roomInput = $('#module-search');
const normalize = (text) => text.normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
function renderIndex(reset = false) {
  const query = normalize(roomInput.value).trim();
  const words = query.split(/\s+/).filter(Boolean);
  const compactCode = query.replace(/[-\s]/g,'');
  roomMatches = pages.map((item,index) => {
    const title = normalize(item.title), code = normalize(item.code);
    const text = normalize(`${item.code} ${item.title} ${item.verb} ${item.detail} ${item.status || ''}`);
    const codeMatch = compactCode && code.replace(/-/g,'') === compactCode;
    return {item,index,matches:!query || codeMatch || words.every(word=>text.includes(word)),rank:codeMatch?0:query && title.startsWith(query)?1:query && title.includes(query)?2:3};
  }).filter(result=>result.matches).sort((a,b)=>a.rank-b.rank || a.index-b.index).map(result=>result.item);
  if (reset || !roomMatches.some(item=>item.code===activeRoomCode)) activeRoomCode = null;
  $('#result-count').textContent = `${roomMatches.length} ${roomMatches.length===1?'room':'rooms'}${query?' found':' to explore'}`;
  $('#module-list').innerHTML = roomMatches.map(item=>`<li id="room-option-${item.code}" role="option" aria-selected="false" data-room="${item.code}" class="room-option"><span class="module-code">${item.code}</span><span class="module-title">${e(item.title)}</span><span class="module-sub">${e(item.status || item.verb)}${item.marker?' · demo figure':''}</span></li>`).join('');
  $('#room-empty').hidden = roomMatches.length>0;
  setActiveRoom(activeRoomCode,false);
}
function setActiveRoom(code, scroll = true) {
  activeRoomCode = code;
  const open = !$('#room-drawer').hidden;
  for (const option of $('#module-list').children) option.setAttribute('aria-selected',String(open && option.dataset.room===code));
  const option = code ? document.getElementById(`room-option-${code}`) : null;
  if (open && option) {
    roomInput.setAttribute('aria-activedescendant',option.id);
    if (scroll) option.scrollIntoView({block:'nearest'});
    world.highlight(findPage(code).block);
  } else { roomInput.removeAttribute('aria-activedescendant'); world.highlight(null); }
}
roomInput.addEventListener('focus',()=>toggleRooms(true));
roomInput.addEventListener('click',()=>{if ($('#room-drawer').hidden) toggleRooms(true);});
roomInput.addEventListener('input',()=>{renderIndex(true);toggleRooms(true);});
roomInput.addEventListener('keydown',event=>{
  if (event.isComposing) return;
  if (event.key==='ArrowDown' || event.key==='ArrowUp') {
    event.preventDefault();
    if ($('#room-drawer').hidden) toggleRooms(true);
    if (!roomMatches.length) return;
    const index = roomMatches.findIndex(item=>item.code===activeRoomCode);
    const next = index<0 ? (event.key==='ArrowDown'?0:roomMatches.length-1) : Math.max(0,Math.min(roomMatches.length-1,index+(event.key==='ArrowDown'?1:-1)));
    setActiveRoom(roomMatches[next].code);
  } else if (event.key==='Enter') {
    event.preventDefault();
    if ($('#room-drawer').hidden) {toggleRooms(true);return;}
    const choice = roomMatches.find(item=>item.code===activeRoomCode) || (roomMatches.length===1?roomMatches[0]:null);
    if (choice) enter(choice,roomInput);
    else announce(roomMatches.length?'Choose a room with the arrow keys, then press Enter.':'No rooms match. Try a page name or code.');
  } else if (event.key==='Escape') {
    if (!$('#room-drawer').hidden) {event.preventDefault();event.stopPropagation();toggleRooms(false);}
  } else if (event.key==='Tab') toggleRooms(false);
});
$('#room-finder').addEventListener('submit',event=>event.preventDefault());
$('#module-list').addEventListener('pointerdown',event=>{if(event.pointerType==='mouse')event.preventDefault();});
$('#module-list').addEventListener('pointermove',event=>{
  if(event.pointerType!=='mouse')return;
  const option = event.target.closest('[data-room]');
  if(option && option.dataset.room!==activeRoomCode)setActiveRoom(option.dataset.room,false);
});
$('#module-list').addEventListener('click',event=>{
  const option = event.target.closest('[data-room]');
  if(option){setActiveRoom(option.dataset.room,false);enter(findPage(option.dataset.room),roomInput);}
});
document.addEventListener('pointerdown',event=>{if(!$('#room-finder').contains(event.target))toggleRooms(false);});
document.addEventListener('focusin',event=>{if(!$('#room-finder').contains(event.target))toggleRooms(false);});

async function enter(module, origin = null, skipFlight = false, push = true) {
  if (!module) return;
  const token = ++enterToken;
  if (current) { showSheet(module); return; }
  entryElement = origin || $(`[data-block="${module.block}"]`) || $('#module-search');
  entering = true;
  // Sheet entry preserves the route frame; no camera travel is attached to selection.
  if (token !== enterToken) return;
  entering = false;
  callers = [];
  showSheet(module,push);
}
function showSheet(module, push = true, restore = null) {
  current = module;
  toggleRooms(false);
  $('#scene-settings').hidden = true;
  $('#settings-toggle').setAttribute('aria-expanded','false');
  $('#dashboard-code').textContent = `${module.code} · Block ${String(module.block).padStart(2,'0')}`;
  $('#dashboard-title').textContent = module.title;
  $('#dashboard-verb').textContent = module.verb;
  $('#dashboard-description').textContent = module.detail;
  $('#dashboard-state').textContent = module.status || 'MOCK WORK · in this tab only';
  $('#research-link').hidden = !module.issue;
  if (module.issue) $('#research-link').href = `https://github.com/ojfbot/lego-village-pipeline/issues/${module.issue}`;
  const caller = callers.at(-1);
  $('#dashboard-content').innerHTML = (caller ? `<div class="caller-bar"><span>You came from ${e(caller.module.title)}.</span><button type="button" data-action="return-caller">← Back to ${e(caller.module.code)}</button></div>` : '') + renderSheet(module,state);
  $('#dashboard').hidden = false;
  $('#dashboard').classList.add('is-visible');
  $('.app-header').inert = true;
  $('.work-area').inert = true;
  document.body.classList.add('sheet-open');
  document.title = `${module.title} · House at the drafting table`;
  if (push) history.pushState({ page: module.code }, '', `#${encodeURIComponent(module.code)}`);
  if (restore) {
    $('.dashboard-sheet').scrollTop = restore.scroll;
    const focus = restore.action ? $('#dashboard-content').querySelector(restore.action) : null;
    (focus || $('#dashboard-title')).focus({ preventScroll: true });
  } else {
    $('.dashboard-sheet').scrollTop = 0;
    $('#dashboard-title').focus({ preventScroll: true });
  }
  announce(`${module.title}. ${module.status || 'Demo sheet'}. All work is mock and stays in this tab.`);
}
function refreshSheet(message, focusAction) {
  const scroll = $('.dashboard-sheet').scrollTop;
  const caller = callers.at(-1);
  $('#dashboard-content').innerHTML = (caller ? `<div class="caller-bar"><span>You came from ${e(caller.module.title)}.</span><button type="button" data-action="return-caller">← Back to ${e(caller.module.code)}</button></div>` : '') + renderSheet(current,state);
  $('.dashboard-sheet').scrollTop = scroll;
  const focus = focusAction ? $(`[data-action="${focusAction}"]`) : $('#dashboard-title');
  (focus && !focus.disabled ? focus : $('#dashboard-title')).focus({ preventScroll: true });
  if (message) announce(message);
}
function closeSheet(push = true) {
  enterToken++;
  entering = false;
  current = null;
  callers = [];
  $('#dashboard').hidden = true;
  $('#dashboard').classList.remove('is-visible');
  $('#benny-panel').hidden = true;
  $('#benny-toggle').setAttribute('aria-expanded','false');
  document.body.classList.remove('sheet-open');
  $('.app-header').inert = false;
  $('.work-area').inert = false;
  world.restore();
  lastChapter = null;
  drawFlight();
  document.title = 'Play Well — a village in the making';
  if (push) history.pushState({}, '', location.pathname + location.search);
  renderIndex();
  const target = entryElement?.isConnected ? entryElement : roomInput;
  target?.focus({ preventScroll: true });
  announce('Back at the house. Your view and demo work are retained.');
}
$('#dashboard-back').addEventListener('click', () => closeSheet());
$('#dashboard-content').addEventListener('click', (event) => {
  const destination = event.target.closest('[data-page]');
  if (destination) {
    callers.push({ module: current, scroll: $('.dashboard-sheet').scrollTop, action: `[data-page="${destination.dataset.page}"]` });
    showSheet(findPage(destination.dataset.page));
    return;
  }
  const action = event.target.closest('[data-action]')?.dataset.action;
  if (action) act(action);
});
$('#dashboard-content').addEventListener('input', (event) => {
  if (event.target.id === 'measurement-input') state.measurementDraft = Number(event.target.value);
  if (event.target.id === 'story-input') state.storyDraft = event.target.value;
  if (event.target.id === 'answer-input') state.answer = event.target.value;
  if (event.target.id === 'offset-input') {
    state.offset = Number(event.target.value);
    state.checked = false;
    state.approved = false;
    // Keep the focused range while replacing only the preview and check text.
    const temp = document.createElement('div');
    temp.innerHTML = renderSheet(current,state);
    $('.plan-drawing').replaceWith(temp.querySelector('.plan-drawing'));
    $('.dashboard-rail').replaceWith(temp.querySelector('.dashboard-rail'));
    $('#offset-value').textContent = `${state.offset} studs`;
  }
});
$('#dashboard-content').addEventListener('change', (event) => {
  if (event.target.id === 'story-consent') { state.storyConsent = event.target.checked; const visibleStory = $('.builder-story'); if (visibleStory) visibleStory.hidden = !state.storyConsent; }
  if (event.target.id === 'offset-input') record(`Ring centre moved to ${state.offset} studs. Layout check and demo review reopened.`);
});
function invalidateMeasurement(value, reason) {
  state.revisions.push(state.measurement);
  state.measurement = value;
  state.measurementDraft = value;
  state.measured = true;
  state.checked = false;
  state.approved = false;
  state.pendingMeasurement = null;
  record(`${reason}: ${value} studs. Earlier reading retained; layout and parts review reopened. Inventory unchanged.`);
}
function act(action) {
  switch (action) {
    case 'return-caller': {
      const caller = callers.pop();
      if (caller) showSheet(caller.module,true,caller);
      return;
    }
    case 'document-box': state.physicalBoxDocumented = true; record('Sample physical box documented in this tab. No real inventory evidence was saved.'); break;
    case 'open-box': state.boxOpened = true; record('Demo box opened: a train around the tree.'); break;
    case 'read-book': state.bookRead = true; record('Instruction book read. Bag 1 is next.'); showSheet(findPage('M-01')); return;
    case 'propose-measurement':
      if (!Number.isInteger(state.measurementDraft) || state.measurementDraft < 8 || state.measurementDraft > 28) {
        announce('Enter a whole-stud reading from 8 to 28 for this demo.');
        $('#measurement-input').focus(); return;
      }
      state.pendingMeasurement = state.measurementDraft; break;
    case 'confirm-measurement':
      if (state.pendingMeasurement === null) return;
      invalidateMeasurement(state.pendingMeasurement,'Demo measurement recorded'); break;
    case 'cancel-measurement': state.pendingMeasurement = null; state.measurementDraft = state.measurement; record('Left the measurement as it was.'); break;
    case 'clear-fit': state.offset = Math.ceil(state.measurement / 2); state.checked = false; state.approved = false; record(`Tried a ${state.offset}-stud ring offset. Check the layout next.`); break;
    case 'check-layout':
      if (!state.measured) { announce('Record the measurement on Bag 1 first.'); return; }
      state.checked = true; record(facts(state).fit ? 'Layout checked: the simplified base-clearance test passes.' : 'Layout checked: the base still overlaps the corner.'); break;
    case 'approve': {
      const initials = $('#initials-input').value.trim();
      if (!initials) { announce('Add initials for the demo review.'); $('#initials-input').focus(); return; }
      if (!state.measured || !facts(state).fit || !state.checked) return;
      state.approved = true;
      record(`Demo parts review initialled by ${initials}. No real BOM has been released.`);
      showSheet(findPage('H-01')); return;
    }
    case 'receive': if (!state.received) { state.received = true; record('Eight sample support plates counted into demo inventory.'); } break;
    case 'answer': record('Human answer retained in the demo. The scripted AI did not change the layout.'); break;
    case 'story':
      if (!state.storyDraft.trim()) { announce('Tell your story in your own words first.'); $('#story-input').focus(); return; }
      if (!state.storyConsent) { announce('Choose whether to show your story in this local session.'); $('#story-consent').focus(); return; }
      state.story = state.storyDraft; record('Builder story retained verbatim in this tab. Nothing published.'); break;
    case 'hear-A': case 'hear-B': {
      const id = action.slice(-1);
      if (!state.heard.includes(id)) state.heard.push(id);
      record(`Demo builder ${id}’s story heard. Their model and words remain separate.`); break;
    }
    case 'shared': if (state.heard.length===2) { state.shared=true; record('Shared concept preview opened. Both original stories remain visible.'); } break;
    case 'what-if': invalidateMeasurement(Math.min(28,state.measurement+2),'What-if sample'); state.whatIf = true; break;
    case 'replay-prev': state.replayStep = Math.max(0,state.replayStep-1); break;
    case 'replay-next': state.replayStep = Math.min(2,state.replayStep+1); break;
    case 'reset': state = initialState(); record('Demo work reset. No real record was changed.','System demo'); break;
    default: return;
  }
  refreshSheet(null, action === 'propose-measurement' ? 'confirm-measurement' : action);
}

$('#theme-toggle').addEventListener('click', (event) => {
  const blueprint = document.body.classList.toggle('dt-blueprint');
  event.currentTarget.setAttribute('aria-pressed',String(blueprint));
  event.currentTarget.textContent = blueprint ? 'Paper' : 'Blueprint';
  announce(`${blueprint ? 'Blueprint' : 'Paper'} theme.`);
  world.render();
});
$('#quality-toggle').addEventListener('click', (event) => {
  const lite = event.currentTarget.getAttribute('aria-pressed') !== 'true';
  event.currentTarget.setAttribute('aria-pressed',String(lite));
  world.toggleLite(lite);
  announce(lite ? 'Lite house selected. Same page destinations.' : 'Detailed brick model selected.');
});
$('#motion-toggle').addEventListener('click', () => {
  world.setStill(!world.still);
  updateMotionControl();
  drawFlight();
  announce(world.still ? 'Still view. The scene stays where it is while you scroll.' : 'Scroll flight enabled. The scene follows the scroll position.');
});
function updateMotionControl() {
  $('#motion-toggle').setAttribute('aria-pressed',String(world.still));
  $('#motion-toggle').textContent = world.still ? 'Follow scroll' : 'Still view';
  document.body.classList.toggle('still-view',world.still);
}
$('#reset-view').addEventListener('click', () => world.reset());

function setVariant(variant, updateURL = true) {
  if (!['house','exploded','landscape'].includes(variant)) variant = 'exploded';
  $('#view-mode').value = variant;
  document.body.classList.toggle('builder-landscape',variant === 'landscape');
  world.setMode(variant);
  const landscape = variant === 'landscape';
  $('#landscape').hidden = !landscape;
  $('#house-stage').hidden = landscape;
  if (updateURL) {
    const url = new URL(location.href);
    url.searchParams.set('variant',variant);
    history.replaceState(history.state,'',url);
  }
  world.resize();
  announce(`${variant === 'house' ? 'House portal' : variant === 'exploded' ? 'Exploded systems table' : 'Builder landscape'} view.`);
}
$('#view-mode').addEventListener('change', (event) => setVariant(event.target.value));
$('#landscape').innerHTML = `<div class="landscape-head"><p class="eyebrow">Research direction C</p><h3>Before a shared village</h3><p>Build → tell → compare. Technical facts sit alongside the stories.</p></div><div class="landscape-models">${demoProposals.map((idea) => `<article><span class="micro">${idea.builder}</span><h3>${idea.name}</h3>${proposalSketch(idea.shape,idea.name)}<blockquote>${idea.story}</blockquote><button type="button" data-landscape-page="F6">Hear and compare the stories ↗</button></article>`).join('')}</div><div class="landscape-actions"><button type="button" data-landscape-page="F5">Your model, your story ↗</button><button type="button" data-landscape-page="F7">Explore a what-if ↗</button></div>`;
$('#landscape').addEventListener('click', (event) => { const button = event.target.closest('[data-landscape-page]'); if (button) enter(findPage(button.dataset.landscapePage),button,true); });

// Benny proposes questions or routes. It never edits a sheet or interprets a story.
$('#benny-toggle').addEventListener('click', () => {
  const open = $('#benny-panel').hidden;
  $('#benny-panel').hidden = !open;
  $('#benny-toggle').setAttribute('aria-expanded',String(open));
  if (open) $('#benny-input').focus();
});
$('#benny-form').addEventListener('submit', (event) => {
  event.preventDefault();
  const query = $('#benny-input').value.toLowerCase();
  const page = /story|meaning|model/.test(query) ? 'F5' : /bag|book|instruction/.test(query) ? 'V-01' : /part|buy|list/.test(query) ? 'C-01' : /measure|base|fit/.test(query) ? 'M-01' : 'HUB';
  const question = page === 'F5' ? 'Could you show us the part of the model you want us to notice? The builder supplies its meaning.' : `I can point you to ${findPage(page).title}. The sheet will stay as it is until you choose an action.`;
  $('#benny-response').innerHTML = `<p class="origin-label">AI · scripted response</p><p>${question}</p><button type="button" data-benny-page="${page}">Open ${e(findPage(page).title)} ↗</button>`;
  announce(`Scripted AI response. ${question}`);
});
$('#benny-response').addEventListener('click', (event) => {
  const button = event.target.closest('[data-benny-page]');
  if (button) { callers.push({module:current,scroll:$('.dashboard-sheet').scrollTop}); showSheet(findPage(button.dataset.bennyPage)); $('#benny-panel').hidden=true; $('#benny-toggle').setAttribute('aria-expanded','false'); }
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    if (!$('#benny-panel').hidden) { $('#benny-panel').hidden=true; $('#benny-toggle').setAttribute('aria-expanded','false'); $('#benny-toggle').focus(); }
    else if (current || entering) closeSheet();
    else if (!$('#room-drawer').hidden) toggleRooms(false);
    else if (!$('#scene-settings').hidden) { $('#scene-settings').hidden=true; $('#settings-toggle').setAttribute('aria-expanded','false'); $('#settings-toggle').focus(); }
  }
  if (event.key === 'Tab' && current) {
    const focusable = [...$('#dashboard').querySelectorAll('button:not(:disabled),a[href],input,textarea,select')].filter((node) => node.getClientRects().length);
    const first = focusable[0], last = focusable.at(-1);
    if (event.shiftKey && (document.activeElement === first || document.activeElement === $('#dashboard-title'))) { event.preventDefault(); last?.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
  }
});
window.addEventListener('popstate', () => {
  const module = findPage(decodeURIComponent(location.hash.slice(1)));
  if (module) { callers=[]; if (current) showSheet(module,false); else enter(module,null,true,false); }
  else closeSheet(false);
});
renderIndex();
const params = new URLSearchParams(location.search);
if (params.has('lite')) $('#quality-toggle').setAttribute('aria-pressed','true');
document.body.classList.add('motion-off'); world.motion=false;
if (params.get('motion') === 'off') world.setStill(true);
updateMotionControl();
setVariant(params.get('variant') || 'exploded',false);
const initialPage = findPage(decodeURIComponent(location.hash.slice(1)));
if (initialPage) enter(initialPage,null,true,false);
// Read-only observability for verifying this prototype against its real scene/state.
window.houseDemo = {
  getState: () => structuredClone(state),
  diagnostics: () => world.diagnostics(),
};

function toggleRooms(open) {
  const wasOpen = !$('#room-drawer').hidden;
  $('#room-drawer').hidden = !open;
  roomInput.setAttribute('aria-expanded',String(open));
  if (open && !wasOpen) {renderIndex();$('#module-list').scrollTop=0;}
  setActiveRoom(activeRoomCode,false);
}
$('#settings-toggle').addEventListener('click', () => {
  const open = $('#scene-settings').hidden;
  $('#scene-settings').hidden = !open;
  $('#settings-toggle').setAttribute('aria-expanded',String(open));
  if (open) $('#motion-toggle').focus();
});
const flight = {progress:0};
let lastChapter = null, lastPercent = null;
function drawFlight() {
  if (!current && !document.body.classList.contains('builder-landscape')) world.setJourney(flight.progress);
  $('#flight-progress').value = Math.round(flight.progress*1000);
  const percent = Math.round(flight.progress*100);
  if (percent !== lastPercent) {
    $('#flight-percent').textContent = `${percent}%`;
    lastPercent = percent;
  }
  const poster = $('.landing-poster');
  const titleProgress = world.still ? (world.frozenProgress || 0) : flight.progress;
  const titlePhase = Math.min(1,titleProgress/.085);
  const titleEase = .5-.5*Math.cos(Math.PI*titlePhase);
  const initialScale = matchMedia('(max-width:740px)').matches ? 1.05 : 1.28;
  gsap.set('.landing-poster h1',{scale:1+(initialScale-1)*(1-titleEase),y:20*(1-titleEase),'--wordmark-gradient':`${titleEase*100}%`});
  const fade = Math.max(0,Math.min(1,(flight.progress-.09)/.07));
  poster.style.opacity = String(1-fade*fade*(3-2*fade));
  const chapterIndex = Math.max(0,flightChapters.findLastIndex(chapter=>flight.progress>=chapter.at));
  const chapter = flightChapters[chapterIndex];
  if (chapter !== lastChapter) {
    $('#chapter-title').textContent = chapter.title;
    $('#world-instruction').textContent = chapter.detail;
    lastChapter = chapter;
  }
  // One scroll-owned caption fades to zero before its text changes.
  const captionEase = value => {const t=Math.max(0,Math.min(1,value));return t*t*(3-2*t);};
  const captionStart = Math.max(.16,chapter.at);
  const nextChapter = flightChapters[chapterIndex+1];
  const captionIn = captionEase((flight.progress-captionStart)/.025);
  const captionOut = nextChapter ? captionEase((nextChapter.at-flight.progress)/.025) : 1;
  const captionOpacity = Math.min(captionIn,captionOut);
  gsap.set('.flight-caption',{opacity:captionOpacity,y:world.still?0:6*(1-captionOpacity)});
  $('#flight-label').textContent = flight.progress === 0 ? 'Scroll to fly through' : flight.progress > .98 ? 'Back at the front' : chapter.title;
  $('#flight-progress').setAttribute('aria-valuetext', `${Math.round(flight.progress*100)} percent. ${chapter.title}. ${chapter.detail}`);
}
const flightTimeline = gsap.timeline({
  scrollTrigger:{ trigger:'.scene-scroll',start:'top top',end:'bottom bottom',scrub:true,invalidateOnRefresh:true },
});
flightTimeline.to(flight,{progress:1,duration:1,ease:'none',onUpdate:drawFlight},0);

function seekFlight(progress) {
  const trigger = flightTimeline.scrollTrigger;
  window.scrollTo({top:trigger.start+(trigger.end-trigger.start)*progress,behavior:'instant'});
  ScrollTrigger.update();
}
$('#flight-progress').addEventListener('input',(event)=>seekFlight(Number(event.target.value)/1000));
$('#restart-flight').addEventListener('click',()=>seekFlight(0));
$('.studio-mark').addEventListener('click',(event)=>{event.preventDefault();seekFlight(0);});
matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',(event)=>{world.setStill(event.matches);updateMotionControl();});
function syncRestoredScroll() {
  ScrollTrigger.refresh();
  const trigger = flightTimeline.scrollTrigger;
  flightTimeline.progress(Math.max(0,Math.min(1,(scrollY-trigger.start)/(trigger.end-trigger.start))));
  drawFlight();
}
window.addEventListener('load',()=>requestAnimationFrame(syncRestoredScroll));
window.addEventListener('pageshow',()=>requestAnimationFrame(syncRestoredScroll));
requestAnimationFrame(syncRestoredScroll);
updateMotionControl();
drawFlight();
