from ultralytics import YOLO

# Load your model
model = YOLO('best.pt')

# Print the list of things this model can see
print("---------------------------------")
print("YOUR MODEL DETECTS THESE CLASSES:")
print(model.names)
print("---------------------------------")