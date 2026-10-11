// Provisional block-to-destination map for this navigation study.
// Page names follow the R4 pages index. The last four blocks are research concepts.
export const modules = [
  { block: 1, code: 'HUB', title: 'The drafting table', verb: 'See today', detail: 'The three things next, and what each is waiting on.' },
  { block: 2, code: 'A-01', title: 'Layout canvas', verb: 'Arrange', detail: 'Place sections and see whether the train circle fits.' },
  { block: 3, code: 'M-01', title: 'Measure and check', verb: 'Confirm', detail: 'Record the measurements that later checks depend on.', marker: 'Agent run' },
  { block: 4, code: 'V-01', title: 'Reading the instructions', verb: 'Look up', detail: 'Find measurements already stated in the build instructions.' },
  { block: 5, code: 'V-02', title: 'Replaying the build', verb: 'Arrange', detail: 'Derive fit from the way a section is built.' },
  { block: 6, code: 'B-01', title: 'When the AI is not sure', verb: 'Answer', detail: 'See the question, the evidence, and the answer that becomes the record.' },
  { block: 7, code: 'C-01', title: 'The railbed parts list', verb: 'Approve', detail: 'Review the parts and their basis before a purchase decision.', marker: 'Review' },
  { block: 9, code: 'P-01', title: 'Buying the gap', verb: 'Buy', detail: 'See shop options and price ranges after the list is released.' },
  { block: 10, code: 'I-01', title: 'What we have', verb: 'Look up', detail: 'Separate what is owned, built, and free to use.' },
  { block: 11, code: 'I-02', title: 'Documenting the boxes', verb: 'Confirm', detail: 'Record what is actually inside each box.' },
  { block: 12, code: 'I-03', title: 'One set', verb: 'Look closely', detail: 'See the evidence and open work for one set.' },
  { block: 13, code: 'T-01', title: 'The queue', verb: 'See today', detail: 'See waiting work and the reason each item is waiting.' },
  { block: 14, code: 'R-01', title: 'Bringing things in', verb: 'Confirm', detail: 'Review receipts and parcels before anything counts as in the house.' },
  { block: 15, code: 'F-01', title: 'Family workbench', verb: 'Arrange', detail: 'Use the village tools together at the table.' },
  { block: 16, code: 'J-01', title: 'The thirteen journeys', verb: 'Find your way', detail: 'See how the sheets and decisions connect.' },
  { block: 17, code: 'H-01', title: 'The handoff', verb: 'Hand over', detail: 'See what was settled and what agents may use next.' },
  { block: 18, code: 'W-00', title: 'Workbench frame', verb: 'Study', detail: 'Explore the optional rails, ledger, and change ripple.', status: 'Wireframe study' },
  { block: 19, code: 'F5', title: 'Your model, your story', verb: 'Tell', detail: 'The builder gives the model its meaning. Brick facts stay separate.', status: 'Open research', issue: 38, marker: 'Story' },
  { block: 20, code: 'F6', title: 'Compare ideas', verb: 'Compare', detail: 'See each proposal before discussing a shared version.', status: 'Open research', issue: 39 },
  { block: 21, code: 'F7', title: 'What if', verb: 'Explore', detail: 'Test a change against a real village constraint.', status: 'Open research', issue: 40 },
  { block: 22, code: 'F8', title: 'How agents work', verb: 'Learn', detail: 'Build, check, decide, and retain the evidence.', status: 'Open research', issue: 41 },
];

export const moduleByBlock = new Map(modules.map((item) => [item.block, item]));

export const workBox = { block: 1, code: 'BOX', title: 'A box of work', verb: 'Begin', detail: 'Agree on the result, read its book, and open one numbered bag at a time.', status: 'Work metaphor study' };
export const pages = [...modules, workBox];
