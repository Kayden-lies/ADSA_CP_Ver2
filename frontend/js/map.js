// ================= MAP INIT =================
const map = L.map('map').setView([18.4635, 73.8680], 17);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap'
}).addTo(map);

// ================= GLOBAL =================
let nodesData = {};
let currentRoute = null;

let arrowMarker = null;
let trailLine = null;

let animationId = null;


// ================= LOAD NODES =================
async function loadNodes() {
  const res = await fetch("http://localhost:8000/nodes");
  const data = await res.json();

  nodesData = data;
  populateDropdowns(data);
}


// ================= POPULATE DROPDOWNS =================
function populateDropdowns(nodes) {
  const start = document.getElementById("start");
  const end = document.getElementById("end");

  start.innerHTML = "";
  end.innerHTML = "";

  Object.keys(nodes).forEach(node => {
    start.add(new Option(node, node));
    end.add(new Option(node, node));
  });
}


// ================= ROUTE FETCH =================
async function findRoute() {

  if (animationId) {
    cancelAnimationFrame(animationId);
    animationId = null;
  }

  const start = document.getElementById("start").value;
  const end = document.getElementById("end").value;
  const algo = document.getElementById("algo").value;

  const res = await fetch(
    `http://localhost:8000/route?start=${start}&end=${end}&algo=${algo}`
  );

  const data = await res.json();

  handleRouteResponse(data, algo);
}


// ================= HANDLE RESPONSE =================
function handleRouteResponse(data, algo) {

  // CLEAN
  if (currentRoute) {
    map.removeLayer(currentRoute);
    currentRoute = null;
  }

  if (arrowMarker) {
    map.removeLayer(arrowMarker);
    arrowMarker = null;
  }

  if (trailLine) {
    map.removeLayer(trailLine);
    trailLine = null;
  }

  // 🔥 ADD TERMINAL STEPS
  if (data.steps) {
    updateTerminal(data.steps);
  }

  // K-SHORTEST
  if (data.routes) {
    showKShortest(data.routes);
    return;
  }

  // FLOYD
  if (data.matrix) {
    alert("Floyd gives full distance matrix, not a single path");
    return;
  }

  // NORMAL PATH
  const coords = data.coordinates.map(c => [c[0], c[1]]);

  map.fitBounds(coords);

  animateArrow(coords);

  document.getElementById("status-distance").innerText =
    `Distance: ${data.distance} m`;

  document.getElementById("status-algo").innerText =
    `Algo: ${algo}`;
}


// ================= TERMINAL =================
function updateTerminal(steps) {

  const terminal = document.getElementById("terminalOutput");
  if (!terminal) return;

  terminal.innerHTML = "";

  if (!steps || steps.length === 0) {
    terminal.innerHTML = `<div class="code"><span class="text">No steps</span></div>`;
    return;
  }

  steps.slice(0, 120).forEach((s, i) => {

    let text = "";

    if (s.type === "visit") {
      text = `Visit → ${s.node}`;
    }
    else if (s.type === "relax") {
      text = `Relax → ${s.from} → ${s.to}`;
    }
    else if (s.type === "update") {
      text = `Update → ${s.via}`;
    }

    const line = document.createElement("div");
    line.className = "code";

    // optional colors
    if (s.type === "visit") line.style.color = "#22c55e";
    if (s.type === "relax") line.style.color = "#facc15";
    if (s.type === "update") line.style.color = "#38bdf8";

    line.innerHTML = `<span class="text">[${i}] ${text}</span>`;

    terminal.appendChild(line);
  });

  terminal.scrollTop = terminal.scrollHeight;
}


// ================= K SHORTEST =================
function showKShortest(routes) {
  const container = document.getElementById("routes");
  container.innerHTML = "";

  routes.forEach((r, i) => {
    const div = document.createElement("div");
    div.style.color = "lime";
    div.style.fontSize = "11px";
    div.innerText = `Route ${i+1}: ${r.distance} m`;

    div.onclick = () => {
      drawRouteFromPath(r.path);
    };

    container.appendChild(div);
  });
}


// ================= DRAW FROM PATH =================
function drawRouteFromPath(path) {

  if (animationId) {
    cancelAnimationFrame(animationId);
    animationId = null;
  }

  if (arrowMarker) map.removeLayer(arrowMarker);
  if (trailLine) map.removeLayer(trailLine);

  const coords = path.map(n => nodesData[n]);

  map.fitBounds(coords);

  animateArrow(coords);
}


// ================= ARROW ICON =================
function createArrowIcon(angle = 0) {
  return L.divIcon({
    className: "",
    html: `
      <div style="
        width: 0;
        height: 0;
        border-left: 10px solid transparent;
        border-right: 10px solid transparent;
        border-bottom: 18px solid #ff0000;
        transform: rotate(${angle}deg);
      "></div>
    `,
    iconSize: [20, 20],
    iconAnchor: [10, 10]
  });
}


// ================= ANGLE =================
function getAngle(p1, p2) {
  const dy = p2[0] - p1[0];
  const dx = p2[1] - p1[1];
  return Math.atan2(dy, dx) * 180 / Math.PI;
}


// ================= ANIMATION =================
function animateArrow(coords) {

  if (!coords || coords.length < 2) return;

  trailLine = L.polyline([], {
    color: "#ff0000",
    weight: 5
  }).addTo(map);

  arrowMarker = L.marker(coords[0], {
    icon: createArrowIcon(0)
  }).addTo(map);

  let segmentIndex = 0;
  let t = 0;

  const speed = 0.035;

  function step() {

    if (segmentIndex >= coords.length - 1) {
      trailLine.addLatLng(coords[coords.length - 1]);
      return;
    }

    const start = coords[segmentIndex];
    const end = coords[segmentIndex + 1];

    const lat = start[0] + (end[0] - start[0]) * t;
    const lng = start[1] + (end[1] - start[1]) * t;

    const pos = [lat, lng];
    const angle = getAngle(start, end);

    arrowMarker.setLatLng(pos);
    arrowMarker.setIcon(createArrowIcon(angle));

    trailLine.addLatLng(pos);

    t += speed;

    if (t >= 1) {
      t = 0;
      segmentIndex++;
    }

    animationId = requestAnimationFrame(step);
  }

  step();
}


// ================= BUTTON =================
document.getElementById("findRoute").addEventListener("click", findRoute);


// ================= INIT =================
loadNodes();