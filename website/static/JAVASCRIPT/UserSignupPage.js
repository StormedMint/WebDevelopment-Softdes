const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('capture-btn');
const retakeBtn = document.getElementById('retake-btn');
const context = canvas.getContext('2d');

// 1. Access the camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error accessing camera: ", err);
        alert("Could not access camera. Please ensure you have given permission.");
    });

// 2. Capture Function
captureBtn.addEventListener('click', (e) => {
    e.preventDefault();

    // Match visible video size
    canvas.width = video.clientWidth;
    canvas.height = video.clientHeight;

    // Get video dimensions
    const videoWidth = video.videoWidth;
    const videoHeight = video.videoHeight;

    // Calculate crop to match object-fit: cover
    const videoRatio = videoWidth / videoHeight;
    const canvasRatio = canvas.width / canvas.height;

    let sx, sy, sWidth, sHeight;

    if (videoRatio > canvasRatio) {
        // Video is wider
        sHeight = videoHeight;
        sWidth = sHeight * canvasRatio;
        sx = (videoWidth - sWidth) / 2;
        sy = 0;
    } else {
        // Video is taller
        sWidth = videoWidth;
        sHeight = sWidth / canvasRatio;
        sx = 0;
        sy = (videoHeight - sHeight) / 2;
    }

    // Draw cropped image
    context.drawImage(
        video,
        sx,
        sy,
        sWidth,
        sHeight,
        0,
        0,
        canvas.width,
        canvas.height
    );

    // Swap display
    video.style.display = 'none';
    canvas.style.display = 'block';

    captureBtn.style.display = 'none';
    retakeBtn.style.display = 'inline-block';

    const imageData = canvas.toDataURL("image/jpeg");
    document.getElementById("picture").value = imageData;
});

// 3. Retake Function
retakeBtn.addEventListener('click', () => {
    // UI Swap: Show video, hide canvas
    video.style.display = 'block';
    canvas.style.display = 'none';
    
    // Button Swap: Show capture, hide retake
    captureBtn.style.display = 'inline-block';
    retakeBtn.style.display = 'none';
});