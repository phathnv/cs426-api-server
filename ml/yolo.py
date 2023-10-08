from ultralytics import YOLO
from PIL import Image
import io

model = YOLO("ml/best_s.pt")
labels = {0: 'Apples', 1: 'Artichokes', 2: 'Banana', 3: 'Bell Peppers', 4: 'Broccoli', 5: 'Cabbage', 
          6: 'Cantaloupe', 7: 'Carrots', 8: 'Cheese', 9: 'Figs', 10: 'Cucumbers', 
          11: 'Grapes', 12: 'Grapefruit', 13: 'Lemons', 14: 'Mangoes', 15: 'Mushrooms', 
          16: 'Oranges', 17: 'Peaches', 18: 'Pears', 19: 'Pomegranates', 20: 'Potatoes', 
          21: 'Pumpkin', 22: 'Radishes', 23: 'Strawberries', 24: 'Tomatoes', 25: 'Zucchini'}

def detect_ingredients(image_data):
    image = Image.open(io.BytesIO(image_data))
    results = model.predict(image)
    result = list(results)[0]
    output = []
    for box in result.boxes:
        id = box.cls[0].item()
        conf = box.conf[0].item()
        output.append([conf, labels[id]])
    output.sort(reverse=True)
    if len(output) > 0:
        return output[0][1]
    else:
        return ''