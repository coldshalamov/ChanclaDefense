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
let wave = 1;
let lives = 3;
let frameCount = 0;

// Entities
let projectiles = [];
let enemies = [];
let particles = [];

// Configuration
const SPAWN_RATE = 100; // Frames between spawns (decreases with waves)
let currentSpawnRate = SPAWN_RATE;

// Resize handling
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

// Input handling
canvas.addEventListener('mousedown', (e) => {
    if (!gameActive) return;
    
    // Shoot chancla towards click
    const angle = Math.atan2(
        e.clientY - (canvas.height - 50),
        e.clientX - (canvas.width / 2)
    );
    
    const velocity = {
        x: Math.cos(angle) * 15,
        y: Math.sin(angle) * 15
    };

    projectiles.push(new Projectile(
        canvas.width / 2,
        canvas.height - 50,
        velocity
    ));
});

// Classes
class Projectile {
    constructor(x, y, velocity) {
        this.x = x;
        this.y = y;
        this.velocity = velocity;
        this.radius = 20;
        this.rotation = 0;
        this.spinSpeed = 0.5;
    }

    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.font = '30px Arial';
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

class Enemy {
    constructor(x, y, velocity) {
        this.x = x;
        this.y = y;
        this.velocity = velocity;
        this.radius = 25;
        this.type = Math.random() > 0.5 ? '👹' : (Math.random() > 0.5 ? '👻' : '🤡');
    }

    draw() {
        ctx.font = '40px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.type, this.x, this.y);
    }

    update() {
        this.x += this.velocity.x;
        this.y += this.velocity.y;
    }
}

class Particle {
    constructor(x, y, velocity, color, text = null) {
        this.x = x;
        this.y = y;
        this.velocity = velocity;
        this.alpha = 1;
        this.color = color;
        this.text = text;
    }

    draw() {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        if (this.text) {
            ctx.font = '20px Arial';
            ctx.fillText(this.text, this.x, this.y);
        } else {
            ctx.beginPath();
            ctx.arc(this.x, this.y, 3, 0, Math.PI * 2, false);
            ctx.fillStyle = this.color;
            ctx.fill();
        }
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
    wave = 1;
    lives = 3;
    currentSpawnRate = SPAWN_RATE;
    projectiles = [];
    enemies = [];
    particles = [];
    updateUI();
}

function spawnEnemy() {
    const radius = 30;
    const x = Math.random() * (canvas.width - radius * 2) + radius;
    const y = -radius;
    
    // Wave increases speed
    const speedMultiplier = 1 + (wave * 0.1);
    const velocity = {
        x: 0,
        y: (Math.random() * 2 + 1) * speedMultiplier
    };

    enemies.push(new Enemy(x, y, velocity));
}

function createExplosion(x, y) {
    // Text particle
    particles.push(new Particle(x, y, {x:0, y:-1}, null, '💥'));
    
    // Dot particles
    for (let i = 0; i < 8; i++) {
        particles.push(new Particle(
            x, y,
            {
                x: (Math.random() - 0.5) * 5,
                y: (Math.random() - 0.5) * 5
            },
            `hsl(${Math.random() * 360}, 50%, 50%)`
        ));
    }
}

function updateUI() {
    scoreEl.innerText = score;
    waveEl.innerText = wave;
    livesEl.innerText = lives;
}

function endGame() {
    gameActive = false;
    finalScoreEl.innerText = score;
    gameOverScreen.classList.add('active');
}

function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw Player Base Position (Visual only)
    ctx.font = '60px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('👵', canvas.width / 2, canvas.height - 50);

    if (!gameActive) return;

    frameCount++;

    // Spawning
    if (frameCount % Math.floor(currentSpawnRate) === 0) {
        spawnEnemy();
    }

    // Wave progression
    if (score > 0 && score % 1000 === 0) {
        wave = Math.floor(score / 1000) + 1;
        currentSpawnRate = Math.max(20, SPAWN_RATE - (wave * 5));
        updateUI();
    }

    // Update Projectiles
    projectiles.forEach((p, pIndex) => {
        p.update();
        p.draw();

        // Remove off screen
        if (p.x + p.radius < 0 || p.x - p.radius > canvas.width || 
            p.y + p.radius < 0 || p.y - p.radius > canvas.height) {
            setTimeout(() => {
                projectiles.splice(pIndex, 1);
            }, 0);
        }
    });

    // Update Enemies
    enemies.forEach((e, eIndex) => {
        e.update();
        e.draw();

        // Hit Detection
        projectiles.forEach((p, pIndex) => {
            const dist = Math.hypot(p.x - e.x, p.y - e.y);
            if (dist - e.radius - p.radius < 1) {
                // Collision
                createExplosion(e.x, e.y);
                setTimeout(() => {
                    enemies.splice(eIndex, 1);
                    projectiles.splice(pIndex, 1);
                }, 0);
                score += 100;
                updateUI();
            }
        });

        // Bottom Detection (Lost Life)
        if (e.y - e.radius > canvas.height) {
            lives--;
            updateUI();
            enemies.splice(eIndex, 1);
            
            // Visual feedback for damage
            document.body.style.backgroundColor = '#300';
            setTimeout(() => {
                document.body.style.backgroundColor = '';
            }, 100);

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
