// trafficLight.js

export function changeLight(lights, currentLight) {
    if (!lights.length || !lights[currentLight]) return currentLight;  // ⬅️ chặn null

    lights.forEach(light => light.classList.remove('active'));
    lights[currentLight].classList.add('active');
    return (currentLight + 1) % lights.length;
}

export function startTrafficLightCycle() {
    const lights = document.querySelectorAll('.light1');
    if (!lights.length) {
        // Không có loader trên trang này, bỏ qua
        console.warn('No .light1 elements found – skipping traffic light loader');
        return;
    }

    let currentLight = 0;
    setInterval(() => {
        currentLight = changeLight(lights, currentLight);
    }, 1000);
}
