// trafficData.js

// Helper function to get the color for traffic lights based on the status
export function getTrafficLightColor(status) {
    status = status.toLowerCase();
    switch (status) {
        case 'red':
            return '#ff0000';  // Red
        case 'green':
            return '#00ff00';  // Green
        case 'yellow':
            return '#ffff00';  // Yellow
        default:
            return '#000000';  // Default (black if no match)
    }
}

// Function to fetch traffic data and update the UI
export async function updateTrafficData() {
    try {
        const response = await fetch('/traffic_data');
        const data = await response.json();

        console.log('Traffic data from server:', data);  // debug

        // Các ID này khớp với main_page.html
        document.getElementById('vehicleCount').textContent = data.vehicle_count;
        document.getElementById('avgSpeed').textContent =
            data.avg_speed.toFixed(2) + ' km/h';
        document.getElementById('trafficJam').textContent =
            data.is_traffic_jam ? 'Yes' : 'No';
        document.getElementById('heavyVehicles').textContent =
            data.too_many_heavy_vehicles ? 'Yes' : 'No';
        document.getElementById('clearanceTime').textContent =
            data.estimated_clearance_time.toFixed(2) + ' s';

        // traffic_light_decision = ['red', 30]
        const [lightColor, duration] = data.traffic_light_decision;

        // Cập nhật text "for 30 s" + màu chữ
        const trafficLightTextElements = document.querySelectorAll('#trafficLight');
        trafficLightTextElements.forEach(element => {
            element.textContent = `for ${duration} s`;
            element.style.color = getTrafficLightColor(lightColor);
        });

        // Cập nhật đèn tròn bên trái
        const lightElement = document.querySelector('.trafficlight .light');
        if (lightElement) {
            lightElement.style.backgroundColor = getTrafficLightColor(lightColor);
        }
    } catch (error) {
        console.error('Error fetching traffic data:', error);
    }
}

// KHÔNG export, chỉ chạy khi file được import (app.js import dưới dạng module)
window.addEventListener('load', () => {
    updateTrafficData();              // gọi lần đầu
    setInterval(updateTrafficData, 3000); // lặp lại mỗi 3 giây
});
