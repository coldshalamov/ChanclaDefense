for filename in ['index.html', 'chancla_bomb.html']:
    with open(filename, 'r') as f:
        content = f.read()

    # prestige button
    old_btn = """                // Prestige Confirmation Button
                ctx.fillStyle = '#ffb347';
                roundRect(ctx, 50, 390, canvas.width - 100, 50, 12);
                ctx.fill();
                ctx.fillStyle = '#111';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('PRESTIGE NOW', canvas.width / 2, 422);

                ctx.fillStyle = '#ff5252';
                ctx.font = 'bold 12px sans-serif';
                ctx.fillText('WARNING: CANNOT BE UNDONE!', canvas.width / 2, 460);"""
    new_btn = """                // Prestige Confirmation Button
                ctx.fillStyle = '#ffb347';
                roundRect(ctx, 50, 460, canvas.width - 100, 50, 12);
                ctx.fill();
                ctx.fillStyle = '#111';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('PRESTIGE NOW', canvas.width / 2, 492);

                ctx.fillStyle = '#ff5252';
                ctx.font = 'bold 12px sans-serif';
                ctx.fillText('WARNING: CANNOT BE UNDONE!', canvas.width / 2, 530);"""
    content = content.replace(old_btn, new_btn)

    # handler click box
    old_box = """                    // Check Prestige Confirmation (50, 390, w-100, 50)
                    if (pos.y >= 390 && pos.y <= 440 && pos.x >= 50 && pos.x <= canvas.width - 50) {"""
    new_box = """                    // Check Prestige Confirmation (50, 460, w-100, 50)
                    if (pos.y >= 460 && pos.y <= 510 && pos.x >= 50 && pos.x <= canvas.width - 50) {"""
    content = content.replace(old_box, new_box)

    with open(filename, 'w') as f:
        f.write(content)
