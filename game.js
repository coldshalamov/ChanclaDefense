const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// UI Elements
const scoreEl = document.getElementById('score');
const waveEl = document.getElementById('wave');
const livesEl = document.getElementById('lives');
const startScreen = document.getElementById('start-screen');
const gameOverScreen = document.getElementById('game-over-screen');
const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const finalScoreEl = document.getElementById('final-score-val');

// Game State
let gameActive = false;
let score = 0;
let difficultyLevel = 1; // Replaces 'wave' concept
let lives = 3;
let frameCount = 0;

// Entities
let player = {
    x: 0,
    y: 0,
    radius: 20
};
let chanclas = [];
let particles = [];

// Configuration
let spawnRate = 60; // Frames between spawns

// Resize handling
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    // Center player initially
    if (!gameActive) {
        player.x = canvas.width / 2;
        player.y = canvas.height / 2;
    }
}
window.addEventListener('resize', resize);
resize();

// Input handling (Mouse movement)
canvas.addEventListener('mousemove', (e) => {
    if (!gameActive) return;
    player.x = e.clientX;
    player.y = e.clientY;
});

// Touch support 
canvas.addEventListener('touchmove', (e) => {
    if (!gameActive) return;
    e.preventDefault(); // Stop scrolling
    player.x = e.touches[0].clientX;
    player.y = e.touches[0].clientY;
}, { passive: false });


class Chancla {
    constructor() {
        // Spawn from random edge
        const edge = Math.floor(Math.random() * 4); // 0:top, 1:right, 2:bottom, 3:left

        if (edge === 0) { // Top
            this.x = Math.random() * canvas.width;
            this.y = -50;
        } else if (edge === 1) { // Right
            this.x = canvas.width + 50;
            this.y = Math.random() * canvas.height;
        } else if (edge === 2) { // Bottom
            this.x = Math.random() * canvas.width;
            this.y = canvas.height + 50;
        } else { // Left
            this.x = -50;
            this.y = Math.random() * canvas.height;
        }

        // Target the player's CURRENT position (predictive aiming is too cruel for now)
        const angle = Math.atan2(player.y - this.y, player.x - this.x);

        // Speed increases with difficulty
        const speed = (Math.random() * 3 + 4) + (difficultyLevel * 0.5);

        this.velocity = {
            x: Math.cos(angle) * speed,
            y: Math.sin(angle) * speed
        };

        this.radius = 25;
        this.rotation = 0;
        this.spinSpeed = (Math.random() - 0.5) * 0.5;
    }

    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.font = '40px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('🩴', 0, 0);
        ctx.restore();
    }

    update() {
        this.x += this.velocity.x;
        this.y += this.velocity.y;
        this.rotation += this.spinSpeed;
    }
}

class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.velocity = {
            x: (Math.random() - 0.5) * 8,
            y: (Math.random() - 0.5) * 8
        };
        this.alpha = 1;
        this.color = color;
    }

    draw() {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.beginPath();
        ctx.arc(this.x, this.y, 4, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.restore();
    }

    update() {
        this.x += this.velocity.x;
        this.y += this.velocity.y;
        this.alpha -= 0.02;
    }
}

// Game Loop
function init() {
    score = 0;
    difficultyLevel = 1;
    lives = 3;
    spawnRate = 60;
    chanclas = [];
    particles = [];

    // Set initial player pos
    player.x = canvas.width / 2;
    player.y = canvas.height / 2;

    updateUI();
}

function spawnChancla() {
    chanclas.push(new Chancla());
}

function updateUI() {
    scoreEl.innerText = score;
    waveEl.innerText = difficultyLevel; // Reusing "Wave" UI for difficulty
    livesEl.innerText = lives;
}

function endGame() {
    gameActive = false;
    finalScoreEl.innerText = score;
    gameOverScreen.classList.add('active');
}

function createHitEffect(x, y) {
    for (let i = 0; i < 10; i++) {
        particles.push(new Particle(x, y, '#ff0055'));
    }
}

function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw Player
    ctx.font = '50px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    // Change face based on danger proximity? Maybe later.
    ctx.fillText('😨', player.x, player.y);

    if (!gameActive) return;

    frameCount++;

    // Spawning logic
    if (frameCount % Math.floor(spawnRate) === 0) {
        spawnChancla();
    }

    // Scoring & Difficulty
    if (frameCount % 60 === 0) { // Every second
        score += 10;
        updateUI();

        // Increase difficulty every 10 seconds (600 frames)
        if (score % 100 === 0) {
            difficultyLevel++;
            spawnRate = Math.max(10, 60 - (difficultyLevel * 2));
            updateUI();
        }
    }

    // Update Chanclas
    chanclas.forEach((c, index) => {
        c.update();
        c.draw();

        // Remove off screen (bounds check with buffer)
        if (c.x < -100 || c.x > canvas.width + 100 ||
            c.y < -100 || c.y > canvas.height + 100) {
            setTimeout(() => {
                chanclas.splice(index, 1);
            }, 0);
        }

        // Collision Detection
        const dist = Math.hypot(player.x - c.x, player.y - c.y);

        // Hit box slightly smaller than emoji visual
        if (dist - player.radius - c.radius < -10) {
            createHitEffect(player.x, player.y);
            lives--;
            updateUI();

            // Remove the hitting chancla
            chanclas.splice(index, 1);

            // Screen shake effect (simple via CSS or just visual flash)
            document.body.style.backgroundColor = '#500';
            setTimeout(() => {
                document.body.style.backgroundColor = '';
            }, 50);

            if (lives <= 0) {
                endGame();
            }
        }
    });

    // Update Particles
    particles.forEach((p, index) => {
        if (p.alpha <= 0) {
            particles.splice(index, 1);
        } else {
            p.update();
            p.draw();
        }
    });
}

// Start Controls
startBtn.addEventListener('click', () => {
    init();
    gameActive = true;
    startScreen.classList.remove('active');
});

restartBtn.addEventListener('click', () => {
    init();
    gameActive = true;
    gameOverScreen.classList.remove('active');
});

// Start Animation Loop
animate();
