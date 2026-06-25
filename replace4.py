import sys

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    target_snippet = """                // Fill bar
                if (isa.anger > 0) {
                    const angerProgress = isa.anger / isa.maxAnger;
                    const angerFillWidth = angerBarWidth * angerProgress;"""

    replacement = """                // Delayed visual health (displayAnger)
                if (isa.displayAnger > 0) {
                    const displayProgress = isa.displayAnger / isa.maxAnger;
                    const displayFillWidth = angerBarWidth * displayProgress;

                    ctx.fillStyle = '#fff';
                    ctx.save();
                    ctx.beginPath();
                    roundRect(ctx, angerBarX, angerBarY, displayFillWidth, angerBarHeight, 8);
                    ctx.clip();
                    roundRect(ctx, angerBarX, angerBarY, displayFillWidth, angerBarHeight, 8);
                    ctx.fill();
                    ctx.restore();
                }

                // Fill bar
                if (isa.anger > 0) {
                    const angerProgress = isa.anger / isa.maxAnger;
                    const angerFillWidth = angerBarWidth * angerProgress;"""

    if target_snippet not in content:
        print(f"Target snippet not found in {filepath} (Step 4)")
        return

    content = content.replace(target_snippet, replacement)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated {filepath}")

replace_in_file('index.html')
replace_in_file('chancla_bomb.html')
