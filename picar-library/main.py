from hardware.movement import Movement
import time
from models.yolo import YOLOModel

from status.action import Action

if __name__=="__main__":
    # Testing code:
    user_input = int(input("1. Check movement\n2. Train model\n"))
    if user_input == 1:
        # Testing the Movement class
        move = Movement()

        move.forward()
        time.sleep(1)
        move.forward()
        time.sleep(1)
        move.turn(Action.LEFT, 30)
        time.sleep(1)
        move.turn(Action.RIGHT, 30)
        time.sleep(1)
        move.stop()
        time.sleep(1)
        move.backward()
        time.sleep(1)
        move.stop()
    elif user_input == 2:
        # Testing the model training

        device_input = int(input("1. Train on normal device\n2. Train on Apple Silicon\n"))
        epochs = int(input("Enter number of epochs for training (e.g., 10): "))
        batch_size = int(input("Enter batch size for training (e.g., 32): "))
        
        if device_input == 2:
            # Training on Apple Silicon (Mac)
            trainer = YOLOModel(epochs=epochs, batch_size=batch_size)
            trainer.run_training_on_apple_silicon()
        else:
            # Training on normal device (GPU/CPU)
            trainer = YOLOModel(epochs=epochs, batch_size=batch_size)
            trainer.run_training_yolo_dataset()
            trainer.run_training_augmented_yolo_dataset()
    
        print("\nTraining finished.")

