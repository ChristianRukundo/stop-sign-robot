import cv2
import configparser
import logging
from vision_module import VisionProcessor
from communication_module import SerialCommunicator
from state_machine import StateMachine, RobotState


def setup_logging(config):
    """Configures the logging system."""
    log_level = getattr(logging, config["logging"]["log_level"].upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(config["logging"]["log_file"]),
            logging.StreamHandler(),
        ],
    )


def main():
    """Main application entry point."""
    config = configparser.ConfigParser()
    config.read("config.ini")

    setup_logging(config)

    try:
        vision_config = dict(config["camera"], **config["detection"])
        vision = VisionProcessor(vision_config)

        comm_config = config["serial"]
        communicator = SerialCommunicator(
            comm_config["port"], int(comm_config["baud_rate"])
        )

        state_machine = StateMachine(int(config["detection"]["stop_duration_seconds"]))
    except (KeyError, IOError) as e:
        logging.critical(f"Initialization failed due to config/file error: {e}")
        return

    if not vision.start():
        logging.critical("Failed to start vision module. Exiting.")
        return
    if not communicator.connect():
        logging.warning("Running without serial communication.")

    logging.info("System is running. Press 'q' to exit.")

    try:
        while True:
            frame = vision.latest_frame
            if frame is None:
                continue

            detected, signs = vision.detect_stop_sign(frame)

            state_machine.update(detected)
            signal_to_send = state_machine.get_signal()

            communicator.send_signal(signal_to_send)

            for x, y, w, h in signs:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

            state_text = f"STATE: {state_machine.current_state.name}"
            color = (
                (0, 0, 255)
                if state_machine.current_state == RobotState.STOPPING
                else (0, 255, 0)
            )
            cv2.putText(
                frame, state_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2
            )

            cv2.imshow("Production Stop Sign Detector", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        logging.info("Shutting down system...")
        vision.stop()
        communicator.disconnect()
        cv2.destroyAllWindows()
        logging.info("Shutdown complete.")


if __name__ == "__main__":
    main()
