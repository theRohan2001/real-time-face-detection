const video = document.querySelector("video");
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const ws = new WebSocket("ws://localhost:8000/ws/live");

async function enableCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    video.onloadedmetadata = () => {
      startStreaming();
    };

  } catch (error) {
    console.error("Error accessing camera:", error);
  }
}

function startStreaming() {
  function sendFrame() {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      ctx.drawImage(video, 0, 0);

      const frame = canvas.toDataURL("image/jpeg", 0.6);
      ws.send(frame);
    }

    setTimeout(sendFrame, 100); // ~10 FPS
  }

  sendFrame();
}