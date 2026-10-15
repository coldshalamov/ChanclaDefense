1.  **Add a Dynamic Combo Counter Display:**
    The game currently tracks `comboCount` (and increases it when a projectile is slapped, chaining, etc., and resets it when damage is taken or a slap is missed), and uses it to calculate score, trigger "Fiesta Mode", and generate float text, but it does *not* display the current combo count permanently on the HUD. This feels inferior to modern arcade games where maintaining a high combo is central to the visual feedback and player engagement.
    I will inject a new `drawComboCounter()` function inside the HUD rendering logic. This counter will display when `comboCount >= 2` on the middle-left side of the screen.

    **Specific Changes:**
    In `index.html` and `chancla_bomb.html`, inside `drawHUD()`:

    ```javascript
<<<<<<< SEARCH
                // Label
                ctx.fillStyle = '#fff';
                ctx.font = '10px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText("Isa's Anger", angerBarX + angerBarWidth / 2, angerBarY - 2);

                ctx.restore();
            }
=======
                // Label
                ctx.fillStyle = '#fff';
                ctx.font = '10px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText("Isa's Anger", angerBarX + angerBarWidth / 2, angerBarY - 2);

                // Combo Counter
                if (comboCount >= 2) {
                    ctx.save();
                    const comboPulse = Math.sin(timeElapsed * 15);
                    const scale = 1 + comboPulse * 0.1;

                    ctx.translate(50, 100);
                    ctx.rotate(-0.1 + comboPulse * 0.05); // Slight dynamic tilt
                    ctx.scale(scale, scale);

                    ctx.textAlign = 'center';

                    // Main combo number
                    ctx.font = 'bold 36px sans-serif';
                    ctx.fillStyle = '#ff79c6';
                    ctx.strokeStyle = '#222';
                    ctx.lineWidth = 4;
                    ctx.strokeText(comboCount, 0, 0);
                    ctx.fillText(comboCount, 0, 0);

                    // "COMBO" label
                    ctx.font = 'bold 14px sans-serif';
                    ctx.fillStyle = '#fff';
                    ctx.lineWidth = 2;
                    ctx.strokeText('COMBO', 0, 20);
                    ctx.fillText('COMBO', 0, 20);

                    // Hype Text based on getComboPhrase logic
                    let hypeText = '';
                    if (comboCount >= 25) hypeText = 'LEGEND!';
                    else if (comboCount >= 15) hypeText = 'IMPOSSIBLE!';
                    else if (comboCount >= 10) hypeText = 'DIOS MIO!';
                    else if (comboCount >= 6) hypeText = 'FUEGO!';
                    else if (comboCount >= 3) hypeText = 'SPICY!';

                    if (hypeText) {
                        ctx.font = 'bold 12px sans-serif';
                        ctx.fillStyle = '#ffd700';
                        ctx.strokeText(hypeText, 0, 40);
                        ctx.fillText(hypeText, 0, 40);
                    }

                    ctx.restore();
                }

                ctx.restore();
            }
>>>>>>> REPLACE
    ```

2.  **Verify the change:**
    I will use `grep -A 40 "Combo Counter" index.html` to confirm the changes are successfully applied in `index.html` and `chancla_bomb.html`.

3.  **Run tests & pre-commit steps:**
    Run python test scripts to ensure everything is working fine. `Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.`

4.  **Submit the code:**
    Call `submit` to push the changes.
