import cv2
import threading
import time
import logging


class VisionProcessor:
    """
    Handles camera capture and object detection in a separate thread.
    """

    def __init__(self, config: dict):
        self.config = {
            "index": int(config["index"]),
            "frame_width": int(config["frame_width"]),
            "frame_height": int(config["frame_height"]),
            "cascade_path": config["cascade_path"],
            "scale_factor": float(config["scale_factor"]),
            "min_neighbors": int(config["min_neighbors"]),
        }

        self.cap = None
        self.latest_frame = None
        self.is_running = False
        self._thread = None

        self.classifier = cv2.CascadeClassifier(self.config["cascade_path"])
        if self.classifier.empty():
            raise IOError(
                f"Could not load Haar Cascade from {self.config['cascade_path']}"
            )

    def start(self) -> bool:
        """Starts the camera and the frame-grabbing thread."""

        camera_index = self.config["index"]

        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            logging.error(f"Cannot open camera at index {camera_index}.")
            return False

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config["frame_width"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config["frame_height"])

        self.is_running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

        logging.info(
            f"VisionProcessor started successfully on camera index {camera_index}."
        )
        return True

    def _run(self):
        """The main loop for the thread that continuously reads frames."""
        while self.is_running:
            if not self.cap or not self.cap.isOpened():
                logging.error("Camera is not available during threaded run.")
                time.sleep(1)
                continue

            ret, frame = self.cap.read()
            if not ret:
                logging.warning("Failed to grab frame from camera. Retrying...")
                time.sleep(0.5)
                continue
            self.latest_frame = frame

    def detect_stop_sign(self, frame) -> tuple[bool, list]:
        """Performs stop sign detection on a given frame."""
        if frame is None:
            return False, []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        stop_signs = self.classifier.detectMultiScale(
            gray,
            scaleFactor=self.config["scale_factor"],
            minNeighbors=self.config["min_neighbors"],
        )

        detection = len(stop_signs) > 0

        return detection, list(stop_signs)

    def stop(self):
        """Stops the thread and releases the camera."""
        self.is_running = False
        if self._thread:
            self._thread.join()
        if self.cap:
            self.cap.release()
        logging.info("VisionProcessor stopped.")
