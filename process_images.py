import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    DIRECTORY_TO_WATCH = "./data"  # The directory to watch

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Process the new file if it has a valid image extension
            file_name = os.path.basename(event.src_path)
            valid_extensions = ('.jpg', '.jpeg', '.png')
            if file_name.lower().endswith(valid_extensions):
                print(f"New file detected: {file_name}")
                command = f"./darknet detector test data/obj.data yolo-obj.cfg backup/yolo-obj_best.weights -ext_output data/{file_name}"
                subprocess.run(command, shell=True)
                print(f"Processed file: {file_name}")
            else:
                print(f"Ignored file: {file_name}")

if __name__ == '__main__':
    w = Watcher()
    w.run()
