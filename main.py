import os
from applyOCR.processor import OCRProcessor
#from createJSON.generateWithoutKeys import generate_json
from createJSON.generateWithKeys import generate_json

def main():
    image_path = input("Enter the path to the image: ")
    
    if not os.path.exists(image_path):
        print("The specified image path does not exist.")
        return
    
    ocr_processor = OCRProcessor()
    text_data = ocr_processor.process_image(image_path)
    
    if text_data.empty:
        print("OCR processing failed or returned no data.")
        return

    json_output = generate_json(text_data.to_dict(orient="records"))

    print("JSON output generated:")
    print(json_output)

if __name__ == "__main__":
    main()