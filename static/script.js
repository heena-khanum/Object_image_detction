document.addEventListener('DOMContentLoaded', () => {
    const objectDetectionButton = document.getElementById('objectDetectionButton');
    const imageDetectionButton = document.getElementById('imageDetectionButton');
    const backButton = document.getElementById('backButton');
    const searchButton = document.getElementById('searchButton');
    const searchInput = document.getElementById('searchInput');
    const video = document.getElementById('video');
    const detectingMessage = document.getElementById('detectingMessage');
    const runButton = document.getElementById('runButton');
    const stopButton = document.getElementById('stopButton');
    const backgroundVideo = document.getElementById('backgroundVideo'); // Add this line to reference the background video element

    let mediaStream = null;
    let detectionMode = null; // Define the detectionMode variable

    // Function to start the webcam
    function startWebcam() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    mediaStream = stream;
                    video.srcObject = stream;
                    video.play();
                })
                .catch(error => {
                    console.error('Error accessing webcam:', error);
                });
        }
    }

    // Function to stop the webcam
    function stopWebcam() {
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
            mediaStream = null;
        }
    }

    // Handle Object Detection Button Click
    objectDetectionButton.addEventListener('click', () => {
        detectionMode = 'object'; // Set detectionMode to 'object'
        document.querySelector('#detectionTitle').textContent = 'Discover any Object instantly and find it on Amazon';
        document.querySelector('.slider').style.transform = 'translateX(-100%)';
        if (!mediaStream) {
            startWebcam();
        }
    });

    // Handle Image Detection Button Click
    imageDetectionButton.addEventListener('click', () => {
        detectionMode = 'image'; // Set detectionMode to 'image'
        document.querySelector('#detectionTitle').textContent = 'Identify anyone’s face instantly and find their information';
        document.querySelector('.slider').style.transform = 'translateX(-100%)';
        if (!mediaStream) {
            startWebcam();
        }
    });

    // Handle Run Button Click
    runButton.addEventListener('click', () => {
        stopWebcam();
        video.classList.add('hidden');
        backgroundVideo.classList.remove('hidden'); // Show the background video
        detectingMessage.classList.remove('hidden');
        runButton.classList.add('hidden');
        stopButton.classList.remove('hidden');

        if (detectionMode === 'object') {
            // Handle object detection logic
            fetch('/run-script', { method: 'POST' })
                .then(response => response.text())
                .then(data => alert(data))
                .catch(error => console.error('Error running object detection:', error));
        } else if (detectionMode === 'image') {
            // Handle image detection logic
            fetch('/face-recognition', { method: 'POST' })
                .then(response => response.text())
                .then(data => alert(data))
                .catch(error => console.error('Error running face recognition:', error));
        }
    });

    // Handle Stop Button Click
    stopButton.addEventListener('click', () => {
        detectingMessage.classList.add('hidden');
        backgroundVideo.classList.add('hidden'); // Hide the background video
        video.classList.remove('hidden'); // Show the webcam video
        startWebcam();
        runButton.classList.remove('hidden');
        stopButton.classList.add('hidden');
    });

    // Handle Back Button Click
    backButton.addEventListener('click', () => {
        stopWebcam();
        document.querySelector('.slider').style.transform = 'translateX(0%)';
    });

    // Handle Search Button Click
    searchButton.addEventListener('click', () => {
        searchInput.style.display = searchInput.style.display === 'none' || searchInput.style.display === '' ? 'block' : 'none';
    });

    // Modal functionality for About Page
    const aboutButton = document.querySelector('.nav-button[href="#about"]');
    const modal = document.createElement('div');
    const modalContent = document.createElement('div');
    const closeModal = document.createElement('span');

    modal.classList.add('modal');
    modalContent.classList.add('modal-content');
    closeModal.classList.add('close');
    closeModal.textContent = '×';

    modalContent.innerHTML = `
        <h2>About Detection Technologies</h2>
        <p>Detection services leverage cutting-edge AI and machine learning technologies to identify and analyze objects and images with high accuracy and speed. Object detection algorithms can recognize a wide range of items in various environments, from everyday objects to complex scenes. Image detection focuses on identifying and processing visual information to understand and categorize images based on predefined criteria. These technologies are used in various applications, including security systems, automated surveillance, and image analysis for various industries.</p>
    `;

    modalContent.appendChild(closeModal);
    modal.appendChild(modalContent);
    document.body.appendChild(modal);

    // Show modal on About button click
    aboutButton.addEventListener('click', () => {
        modal.style.display = 'flex';
    });

    // Hide modal on close button click
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Hide modal on outside click
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});
