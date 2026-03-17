from playwright.sync_api import sync_playwright
import os

def verify_feature():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="verification/video",
            viewport={'width': 450, 'height': 800},
            has_touch=True,
            is_mobile=True
        )
        page = context.new_page()

        file_path = f"file://{os.path.abspath('index.html')}"
        page.goto(file_path)
        page.wait_for_timeout(1000)

        # Better way to expose the variables: dynamically rewrite the IIFE using page.route or similar.
        # Given it's a simple HTML file we can just replace the bottom of the script
        content = page.content()
        modified_content = content.replace("initTitle();\n        })();", """initTitle();
            window.isa = isa;
            window.player = player;
            window.chanclas = chanclas;
            window.fireParticles = fireParticles;
        })();""")

        # Load the modified content
        page.set_content(modified_content)
        page.wait_for_timeout(1000)

        # Click Play button using precise coordinates
        page.evaluate("""() => {
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const clickEvent = new MouseEvent('click', {
                clientX: rect.left + 200,
                clientY: rect.top + 400,
                bubbles: true
            });
            canvas.dispatchEvent(clickEvent);
        }""")

        page.wait_for_timeout(1000)

        # Force Enraged state
        page.evaluate("() => { window.isa.anger = 20; }")

        # Wait a moment for the state to trigger and particles/aura to render
        page.wait_for_timeout(2500)

        page.screenshot(path="verification/rage_phase.png")

        context.close()
        browser.close()

if __name__ == "__main__":
    os.makedirs("verification/video", exist_ok=True)
    verify_feature()
