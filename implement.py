with open("index.html", "r") as f:
    content = f.read()

# Step 3.1
content = content.replace("let meteorTimer = 0;", "let meteorTimer = 0;\n            let laserTimer = 0;\n            const laser = { active: false, warningTimer: 0, duration: 0, x: 0, width: 60 };")

# Step 3.2
content = content.replace("hitStop = 0;\n                meteorTimer = 0;", "hitStop = 0;\n                meteorTimer = 0;\n                laserTimer = 0;\n                laser.active = false;\n                laser.warningTimer = 0;\n                laser.duration = 0;")

# Step 3.3
update_logic = """if (isa.enraged) {
                    laserTimer += dt;
                    if (laserTimer >= 8 && !laser.active && laser.warningTimer <= 0) {
                        laser.warningTimer = 1.5;
                        laser.x = player.x;
                        playSound(1000, 0.4);
                        addFloatText('¡MIRADA MORTAL!', canvas.width / 2, 120, '#ff0000');
                    }

                    if (laser.warningTimer > 0) {
                        laser.warningTimer -= dt;
                        // Track player slightly during warning
                        laser.x += (player.x - laser.x) * 5 * dt;
                        if (laser.warningTimer <= 0) {
                            laser.active = true;
                            laser.duration = 1.5;
                            triggerShake(20, 1.5);
                            playSound(1200, 0.8);
                        }
                    } else if (laser.active) {
                        laser.duration -= dt;
                        if (laser.duration <= 0) {
                            laser.active = false;
                            laserTimer = 0;
                        } else if (dashTimer <= 0 && player.hitTimer <= 0 && !player.shield) {
                            // Damage check
                            if (player.x + player.w/2 > laser.x - laser.width/2 &&
                                player.x - player.w/2 < laser.x + laser.width/2) {
                                triggerFlash(0.3, '#ff0000');
                                triggerShake(15, 0.4);
                                player.lives -= 1;
                                player.hitTimer = 1.0;
                                sayPlayer('hit');
                                if (player.lives <= 0) {
                                    endGame();
                                    return;
                                }
                            }
                        } else if (dashTimer > 0 && player.x + player.w/2 > laser.x - laser.width/2 && player.x - player.w/2 < laser.x + laser.width/2) {
                             if (Math.random() < 0.1) {
                                score += 1;
                                specialAttackBar = Math.min(maxSpecialAttack, specialAttackBar + 1);
                             }
                        }
                    }

                    meteorTimer += dt;"""
content = content.replace("if (isa.enraged) {\n                    meteorTimer += dt;", update_logic)

# Step 3.4
draw_laser_func = """function drawLaser() {
                if (laser.warningTimer > 0) {
                    ctx.save();
                    ctx.fillStyle = `rgba(255, 0, 0, ${0.2 + (Math.sin(Date.now() / 50) * 0.1)})`;
                    ctx.fillRect(laser.x - laser.width/2, 0, laser.width, canvas.height);

                    ctx.setLineDash([10, 10]);
                    ctx.strokeStyle = '#ff0000';
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(laser.x - laser.width/2, 0);
                    ctx.lineTo(laser.x - laser.width/2, canvas.height);
                    ctx.moveTo(laser.x + laser.width/2, 0);
                    ctx.lineTo(laser.x + laser.width/2, canvas.height);
                    ctx.stroke();
                    ctx.restore();
                } else if (laser.active) {
                    ctx.save();
                    ctx.shadowColor = '#ff0000';
                    ctx.shadowBlur = 20;

                    // Core
                    ctx.fillStyle = '#ffffff';
                    ctx.fillRect(laser.x - laser.width/3, 0, laser.width*0.66, canvas.height);

                    // Outer aura
                    ctx.fillStyle = `rgba(255, 50, 50, ${0.8 + Math.random() * 0.2})`;
                    ctx.fillRect(laser.x - laser.width/2, 0, laser.width, canvas.height);

                    ctx.restore();
                }
            }

            function draw() {"""
content = content.replace("function draw() {", draw_laser_func)
content = content.replace("drawSpecialProjectiles();", "drawSpecialProjectiles();\n                drawLaser();")

with open("index.html", "w") as f:
    f.write(content)

print("Done")
