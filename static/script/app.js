
const figuresEl = document.getElementById("increaseFigures");
const  figureEl = document.getElementById("increaseFigure");

// REGISTER PASSWORD REAVELS
const passwordInput = document.querySelector('input[name="password1"]');
const passwordInput2 = document.querySelector("input[name='password2']");
const showPassword = document.getElementById('show-password');
const showPassword2 = document.getElementById('show-password2');
// MESSAGE REGISTER CANCEL
const msgBtnEl = document.getElementById('msg-btn');
const msgContainerEl = document.getElementById('msg-container');


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



// REGISTER PASSWORD REAVELS
showPassword.addEventListener('click', () => {
  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    showPassword.textContent = 'Hide password';
    showPassword.classList.remove('img');
    showPassword.classList.add('img');
  } else {
    passwordInput.type = 'password';
    showPassword.textContent = 'show password';
    showPassword.classList.remove('img');
    showPassword.classList.add('img');
  }
});


showPassword2.addEventListener('click', () => {
  if (passwordInput2.type === 'password') {
    passwordInput2.type = 'text';
    showPassword2.textContent = 'Hide password';
    showPassword2.classList.remove('img');
    showPassword2.classList.add('img');
  } else {
    passwordInput2.type = 'password';
    showPassword2.textContent = 'show password';
    showPassword2.classList.remove('img');
    showPassword2.classList.add('img');
  }
});



    
// MESSAGE REGISTER CANCEL
msgBtnEl.addEventListener('click', show);

function show() {
  msgContainerEl.style.display = 'none';
  msgBtnEl.style.display = 'none';
};





<button onclick="pay()">Pay</button>


function pay() {
    let handler = PaystackPop.setup({
        key: "{{ paystack_public_key }}",
        email: "{{ payment.user.email }}",
        amount: "{{ payment.amount }}" * 100,
        ref: "{{ payment.reference }}",

        callback: function(response) {
            window.location.href = "/verify/" + response.reference + "/";
        }
    });

    handler.openIframe();
}



