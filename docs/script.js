"use strict";
const filterButtons = [...document.querySelectorAll("[data-filter]")];
document.querySelector(".filters").hidden = false;
for (const button of filterButtons)
  button.addEventListener("click", () => {
    for (const item of filterButtons)
      item.setAttribute("aria-pressed", String(item === button));
    let visible = 0;
    for (const project of document.querySelectorAll("[data-category]")) {
      project.hidden =
        button.dataset.filter !== "all" &&
        !project.dataset.category.split(" ").includes(button.dataset.filter);
      if (!project.hidden) visible++;
    }
    document.querySelector("#filter-status").textContent =
      `${visible} projects shown.`;
  });
document.querySelector("#year").textContent = new Date().getFullYear();
const copy = document.querySelector("#copy-email");
copy.hidden = false;
copy.addEventListener("click", async () => {
  const status = document.querySelector("#copy-status");
  try {
    await navigator.clipboard.writeText("ritamghosh548@gmail.com");
    status.textContent = "Email address copied.";
  } catch {
    status.textContent =
      "Select and copy the email address above, or click it to open your mail app.";
  }
});
const width = 12,
  height = 10,
  start = 13,
  goal = 106;
const grid = document.querySelector("#maze"),
  run = document.querySelector("#run"),
  reset = document.querySelector("#reset");
const status = document.querySelector("#demo-status");
let walls = new Set(),
  cells = [],
  busy = false;
function neighbors(index) {
  const x = index % width,
    y = Math.floor(index / width);
  return [
    [x + 1, y],
    [x, y + 1],
    [x - 1, y],
    [x, y - 1],
  ]
    .filter(([a, b]) => a >= 0 && a < width && b >= 0 && b < height)
    .map(([a, b]) => b * width + a);
}
function generate() {
  walls = new Set();
  // Keep a guaranteed route so every generated maze can be solved.
  const protectedCells = new Set([start, goal]);
  let cursor = start;
  while (cursor % width < goal % width) protectedCells.add(++cursor);
  while (cursor < goal) {
    cursor += width;
    protectedCells.add(cursor);
  }
  for (let i = 0; i < width * height; i++)
    if (!protectedCells.has(i) && Math.random() < 0.29) walls.add(i);
  grid.replaceChildren();
  cells = [];
  for (let i = 0; i < width * height; i++) {
    const cell = document.createElement("span");
    cell.className = "cell";
    cell.setAttribute("aria-hidden", "true");
    if (walls.has(i)) cell.classList.add("wall");
    if (i === start) {
      cell.classList.add("start");
      cell.textContent = "S";
    }
    if (i === goal) {
      cell.classList.add("end");
      cell.textContent = "G";
    }
    cells.push(cell);
    grid.append(cell);
  }
  grid.setAttribute(
    "aria-label",
    "A 12 by 10 maze. S marks the start, G marks the goal. Use Find the shortest path to solve it.",
  );
  status.textContent = "Ready. Find the shortest route from S to G.";
}
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
run.addEventListener("click", async () => {
  if (busy) return;
  busy = true;
  run.disabled = reset.disabled = true;
  try {
    for (const cell of cells) cell.classList.remove("visited", "path");
    const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const queue = [start],
      visited = new Set([start]),
      parents = new Map();
    status.textContent = "Exploring the maze, one layer at a time…";
    for (let head = 0; head < queue.length; head++) {
      const current = queue[head];
      if (current === goal) break;
      for (const next of neighbors(current))
        if (!visited.has(next) && !walls.has(next)) {
          visited.add(next);
          parents.set(next, current);
          queue.push(next);
          cells[next].classList.add("visited");
        }
      if (!reduced) await sleep(16);
    }
    if (!visited.has(goal)) {
      status.textContent = "No path found. Try a new maze.";
      return;
    }
    let current = goal,
      path = [goal];
    while (current !== start) {
      current = parents.get(current);
      path.push(current);
    }
    for (const index of path.reverse()) {
      cells[index].classList.add("path");
      if (!reduced) await sleep(25);
    }
    status.textContent = `Found it: ${path.length - 1} moves. ${visited.size} cells discovered.`;
    grid.setAttribute(
      "aria-label",
      `Solved maze. The shortest path from S to G is ${path.length - 1} moves, shown in blue.`,
    );
  } finally {
    busy = false;
    run.disabled = reset.disabled = false;
  }
});
reset.addEventListener("click", generate);
document.querySelector(".demo-controls").hidden = false;
generate();
