"use strict";

const minInput = document.getElementById("minNumber");
const maxInput = document.getElementById("maxNumber");
const startButton = document.getElementById("startButton");

const gameSection = document.getElementById("gameSection");
const hintRange = document.getElementById("hintRange");

const guessInput = document.getElementById("guessInput");
const guessButton = document.getElementById("guessButton");

const message = document.getElementById("message");
const attemptCount = document.getElementById("attemptCount");

const successBox = document.getElementById("successBox");
const correctAnswer = document.getElementById("correctAnswer");
const finalAttempts = document.getElementById("finalAttempts");

const renewButton = document.getElementById("renewButton");


// 開始遊戲
async function startGame() {

    const min = Number(minInput.value);
    const max = Number(maxInput.value);

    const response = await fetch("/start", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            min: min,
            max: max
        })
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.message);
        return;
    }

    gameSection.classList.remove("hidden");

    hintRange.textContent =
        `${data.min} ～ ${data.max}`;

    attemptCount.textContent = "0";

    message.textContent =
        "請輸入數字後按 Enter 或按下「猜測」";

    successBox.classList.add("hidden");

    guessInput.disabled = false;
    guessButton.disabled = false;

    guessInput.value = "";
    guessInput.focus();
}


// 猜測
async function makeGuess() {

    const guess = Number(guessInput.value);

    if (!Number.isInteger(guess)) {

        message.textContent =
            "請輸入有效的整數。";

        guessInput.focus();

        return;
    }


    const response = await fetch("/guess", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            guess: guess
        })
    });


    const data = await response.json();


    if (!response.ok) {

        message.textContent =
            data.message;

        return;
    }


    // 猜中
    if (data.correct) {

        message.textContent =
            "🎉 你中獎了！";

        correctAnswer.textContent =
            data.answer;

        finalAttempts.textContent =
            data.attempts;

        attemptCount.textContent =
            data.attempts;

        successBox.classList.remove(
            "hidden"
        );

        guessInput.disabled = true;
        guessButton.disabled = true;

        return;
    }


    // 更新猜測次數
    attemptCount.textContent =
        data.attempts;


    // 更新提示
    hintRange.textContent =
        `${data.current_min} ～ ${data.current_max}`;


    // 顯示結果
    message.textContent =
        data.message;


    guessInput.value = "";
    guessInput.focus();
}


// Renew
async function renewGame() {

    const response = await fetch("/renew", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    });


    const data = await response.json();


    if (!response.ok) {

        alert(data.message);

        return;
    }


    hintRange.textContent =
        `${data.min} ～ ${data.max}`;

    attemptCount.textContent = "0";

    message.textContent =
        "請輸入數字後按 Enter 或按下「猜測」";

    successBox.classList.add("hidden");

    guessInput.disabled = false;
    guessButton.disabled = false;

    guessInput.value = "";
    guessInput.focus();
}


// 按鈕
startButton.addEventListener(
    "click",
    startGame
);

guessButton.addEventListener(
    "click",
    makeGuess
);

renewButton.addEventListener(
    "click",
    renewGame
);


// Enter
guessInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            makeGuess();
        }
    }
);