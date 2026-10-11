// PROTOTYPE: seeded fictional work, held only in this browser tab.
export const initialState = () => ({
  boxOpened: false, physicalBoxDocumented: false, bookRead: false, received: false, replayStep: 0,
  measurement: 16, measurementDraft: 16, pendingMeasurement: null, revisions: [],
  measured: false, offset: 0, checked: false, approved: false,
  storyDraft: '', story: '', storyConsent: false,
  heard: ['A'], shared: false, whatIf: false, answer: '',
  log: [{ text: 'Opened a local navigation study. Every number is MOCK MATH.', origin: 'System demo' }],
});
export const facts = (state) => ({
  fit: state.measured && state.offset >= state.measurement / 2,
  need: 48 + Math.max(0, state.measurement - 16) * 2,
  owned: 32,
  stale: state.measured && !state.checked,
});
export const steps = [
  { page: 'BOX', title: 'The box', kind: 'Box', hint: 'Agree on the picture on the box.' },
  { page: 'V-01', title: 'The book', kind: 'Instructions', hint: 'Read the three numbered bags.' },
  { page: 'M-01', title: 'Measure', kind: 'Bag 1', hint: 'Record the base in your own words.' },
  { page: 'A-01', title: 'Make it fit', kind: 'Bag 2', hint: 'Move the ring away from the base.' },
  { page: 'C-01', title: 'Step back', kind: 'Bag 3', hint: 'Review the parts and evidence.' },
];
export const demoProposals = [
  { id: 'A', builder: 'Demo builder A', name: 'A lantern by the station', story: 'The light helps late visitors find the train.', shape: 'lantern' },
  { id: 'B', builder: 'Demo builder B', name: 'A bridge across the snow', story: 'The bridge lets neighbours meet without going around the track.', shape: 'bridge' },
];
