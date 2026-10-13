// PROTOTYPE: scroll-owned route through the supplied model, with no autoplay.
import * as THREE from 'three';
export const assemblyEase = (progress, finish) => .5-.5*Math.cos(Math.PI*THREE.MathUtils.clamp(progress/finish,0,1));
const vector = (values) => new THREE.Vector3(...values);
const curve = (points) => new THREE.CatmullRomCurve3(points.map(vector), false, 'centripetal');
export const flightChapters = [
  { at: 0, title: 'Pieces at dawn', detail: 'Loose bricks greet the dawn' },
  { at: .25, title: 'Come on in', detail: 'Soft light slips through open doors' },
  { at: .34, title: 'Around the trees', detail: 'Green leaves find their home' },
  { at: .46, title: 'Step by step', detail: 'Steps rise from the floor' },
  { at: .58, title: 'Through the other side', detail: 'Small rooms gather round the tree' },
  { at: .86, title: 'One house, many builds', detail: 'New worlds wait for hands' },
];
const positions = curve([
  [5.6,4.7,6.8],[4,3.5,5.5],[2.2,2.3,4.2],[.85,1.25,2.7],
  [.36,.58,1.8],[.36,.55,1.1],[.48,.58,.78],
  [.9,.59,.43],[.95,.6,-.12],[.64,.6,-.67],[.16,.62,-1.05],
  [.12,.65,-1.55],[.25,.8,-2.2],[.65,1.3,-3.3],[1.3,2.3,-5],
  [4.2,2.8,-4.5],[5.8,3.2,-1.8],[6.1,3.8,1.8],[4.8,4.35,5.2],[3.6,4.15,6.3],
]);
const gaze = curve([
  [.15,.65,.2],[.15,.65,.2],[.05,.6,.05],[-.1,.5,0],
  [-.23,.49,0],[-.23,.49,0],[-.23,.49,0],
  [-.23,.5,0],[-.23,.5,0],[-.23,.5,0],[-.23,.5,0],
  [-.18,.6,.05],[.1,.65,.2],[.15,.65,.2],[.15,.65,.2],
  [.15,.7,.2],[.15,.75,.2],[.15,.75,.2],[.15,.7,.2],[.15,.65,.2],
]);
// A monotone Hermite clock gives the lobby more scroll space while keeping
// velocity continuous at chapter boundaries. Position and gaze use one clock.
const beats = [[0,0],[.28,6/19],[.54,10/19],[.69,14/19],[1,1]];
const slopes = beats.slice(1).map(([x,y],i)=>(y-beats[i][1])/(x-beats[i][0]));
const tangents = beats.map((_,i)=>i===0?slopes[0]:i===beats.length-1?slopes.at(-1):2/(1/slopes[i-1]+1/slopes[i]));
function routeTime(p) {
  const i = Math.min(beats.length-2,beats.findIndex((b,j)=>j>0 && p<=b[0])-1);
  const [a,b] = [beats[Math.max(0,i)],beats[Math.max(0,i)+1]];
  const d=b[0]-a[0], t=(p-a[0])/d, t2=t*t, t3=t2*t;
  return (2*t3-3*t2+1)*a[1]+(t3-2*t2+t)*d*tangents[Math.max(0,i)]+(-2*t3+3*t2)*b[1]+(t3-t2)*d*tangents[Math.max(0,i)+1];
}
export function sampleFlight(progress) {
  const p = THREE.MathUtils.clamp(progress,0,1);
  const opening = p/.16;
  const cameraProgress = p<.16 ? .16*(2*opening*opening-opening*opening*opening) : p;
  const t = THREE.MathUtils.clamp(routeTime(cameraProgress),0,1);
  const openingView = 1-assemblyEase(p,.18);
  const position = positions.getPoint(t);
  position.x += 3*openingView;
  position.y += 2.5*openingView;
  position.z += 3.4*openingView;
  const target = gaze.getPoint(t);
  target.y += .55*openingView;
  return {
    position,
    target,
    fov: 38 + 20 * THREE.MathUtils.smoothstep(p,.16,.28) * (1-THREE.MathUtils.smoothstep(p,.57,.8)),
    separation: 1-assemblyEase(p,.82),
    rearSeparation: 1-.035*assemblyEase(p,.58)-.965*THREE.MathUtils.smootherstep(p,.58,.84),
    interior: THREE.MathUtils.smoothstep(p,.08,.22)*(1-THREE.MathUtils.smoothstep(p,.72,.95)),
    openingSpread: .4+.6*assemblyEase(p,.16),
    courseSpread: .2+.8*assemblyEase(p,.16),
    posterOffset: .22*(1-THREE.MathUtils.smoothstep(p,0,.2)),
  };
}
