
const figuresEl = document.getElementById("increaseFigures");
const  figureEl = document.getElementById("increaseFigure");

// window.addEventListener('load', updateCounter);
// window.addEventListener('load', loadCounts);

let count = 0;
let target = 10;
let speed = 100; // milliseconds between increments
let totalCount;


// const interval = setInterval(() => {
//   figureEl.textContent = count;
//   figuresEl.textContent = count;

//   if (count >= target) clearInterval(interval);
// }, 10);


function loadCounts() {
  const counts = JSON.parse(localStorage.getItem("counts"));
  if (counts) {
    count = counts.count;
    target = counts.target;
    speed = counts.speed;
    totalCount = counts.totalCount;
    figureEl.textContent = count;
    figuresEl.textContent = count;
  }
}

function saveCounts() {
  const counts = {
    count: count,
    target: target,
    speed: speed,
    totalCount: totalCount
  };
  localStorage.setItem("counts", JSON.stringify(counts));
}


// function updateIncrement() {
//   if (count < target) {
//     count++;
//     increaseFigureEl.innerText = count;
//     setTimeout(updateIncrement, speed);
//   }
// }


window.onload = function() {
  // updateIncrement();
  loadCounts()
};



// function updateCounter() {
//   if (count < target) {
//     count++;
//     incrementFigure.innerText = count;
//     setTimeout(updateCounter, speed);
//   }
// }

// window.onload = function() {
//   updateCounter();
// };



