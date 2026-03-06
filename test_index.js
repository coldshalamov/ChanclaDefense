const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

try {
  const scriptContent = html.split('<script>')[1].split('</script>')[0];
  const mockEnv = `
    const document = {
      getElementById: () => ({ getContext: () => ({ createLinearGradient: () => ({ addColorStop: () => {} }), createRadialGradient: () => ({ addColorStop: () => {} }) }), style: {}, addEventListener: () => {}, getBoundingClientRect: () => ({ width: 400, height: 700, left: 0, top: 0 }), dataset: {} }),
      querySelector: () => ({ addEventListener: () => {}, style: {} }),
      body: { classList: { toggle: () => {} } }
    };
    const window = { addEventListener: () => {}, AudioContext: function() {}, webkitAudioContext: function() {} };
    const requestAnimationFrame = () => {};
    const localStorage = { getItem: () => null, setItem: () => {} };
    const Math = global.Math;
  `;
  eval(mockEnv + scriptContent);
  console.log("Syntax OK");
} catch (e) {
  console.error("Syntax Error:", e);
}
