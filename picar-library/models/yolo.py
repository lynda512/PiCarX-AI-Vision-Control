from ultralytics import YOLO

class YOLOModel:
    """A class to handle YOLO model loading, training and prediction."""

    def __init__(self,
                 model_path='yolov8n.pt',
                 model_path12='yolo12n.pt',
                 epochs: int = 10,
                 batch_size: int = 5):
        """
            Initialize the YOLO models and store models paths

        Args:
        :param model_path: yolov8n model path
        :param model_path12: yolo12n model path
        :param epochs: number of epochs for training
        :param batch_size: batch size for training
        """
        self.model8 = YOLO(model_path)
        self.model8_augmented = YOLO(model_path)
        self.model12 = YOLO(model_path12)
        self.data_path_normal = 'picar-library/models/datasets/yolo_dataset/data.yaml'
        self.data_path_augmented = 'picar-library/models/datasets/augmented_noised_yolo_dataset/data.yaml'
        self.epochs = epochs
        self.batch_size = batch_size

    def run_training_yolo_dataset(self):
        """
          Train self.model8 using the normal yolo dataset
        """
        print("\n--- Starting YOLOv8 Training ---")
        self.model8.train(
            data=self.data_path_normal,
            epochs=self.epochs,
            imgsz=640,
            batch=self.batch_size,
            name='yolov8n-normal-picar'
        )
        print("--- YOLOv8 Training Complete ---")

    def run_training_augmented_yolo_dataset(self):
        """
          Train self.model8 using the augmented yolo dataset
        """
        print("\n--- Starting augmented YOLOv8 Training ---")
        self.model8_augmented.train(
            data=self.data_path_augmented,
            epochs=self.epochs,
            imgsz=640,
            batch=self.batch_size,
            name='yolov8n-augmented-picar'
        )
        print("--- Augmented YOLOv8 Training Complete ---")

    """def run_training(self):
        Trains both models. The model objects in memory
        (self.model8, self.model12) will be the trained models.

        print("\n--- Starting YOLOv8 Training ---")
        self.model8.train(
            data=self.data_path_normal,
            epochs=self.epochs,
            imgsz=640,
            batch=10,
            name='yolov8n-picar'
        )
        print("--- YOLOv8 Training Complete ---")

        print("\n--- Starting YOLOv12 Training ---")
        self.model12.train(
            data=self.data_path_normal,
            epochs=self.epochs,
            imgsz=640,
            batch=10,
            name='yolo12n-picar'
        )
        print("--- YOLOv12 Training Complete ---")"""

    def run_training_on_apple_silicon(self):
        """
        Trains both models on Mac (Apple Silicon). The model objects in memory
        (self.model8, self.model12) will be the trained models.
        """

        print("\n--- Starting YOLOv8 Training ---")
        self.model8.train(
            data=self.data_path_normal,
            epochs=self.epochs,
            imgsz=640,
            batch=self.batch_size,
            name='yolov8n-picar',
            device='mps'
        )
        print("--- YOLOv8 Training Complete ---")

        print("\n--- Starting YOLOv12 Training ---")
        self.model12.train(
            data=self.data_path_normal,
            epochs=self.epochs,
            imgsz=640,
            batch=self.batch_size,
            name='yolo12n-picar',
            device='mps'
        )
        print("--- YOLOv12 Training Complete ---")

    """def check_performance(self):
        Validates the performance of the trained models in memory.
        This should be called *after* run_training().
        It will print the key performance metrics.

        print("\n--- Validating YOLOv8 Model ---")
        # Calling .val() on the trained model object
        metrics8 = self.model8.val()
        print(f"YOLOv8 mAP50-95: {metrics8.box.map}")
        print(f"YOLOv8 mAP50: {metrics8.box.map50}")

        print("\n--- Validating YOLOv12 Model ---")
        metrics12 = self.model12.val()
        print(f"YOLOv12 mAP50-95: {metrics12.box.map}")
        print(f"YOLOv12 mAP50: {metrics12.box.map50}")"""