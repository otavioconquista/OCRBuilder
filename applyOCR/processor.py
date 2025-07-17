from paddleocr import PaddleOCR
import pandas as pd
import numpy as np

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(lang='pt', use_angle_cls=True)

    def process_image(self, image_path):
        result = self.ocr.ocr(image_path)
        result_data = result[0]

        texts = result_data['rec_texts']
        scores = result_data['rec_scores']
        polys = result_data['rec_polys']

        text_data = []
        for text, score, poly in zip(texts, scores, polys):
            poly_array = np.array(poly)
            x_center = float(np.mean(poly_array[:, 0]))
            y_center = float(np.mean(poly_array[:, 1]))

            text_data.append({
                'text': text,
                'score': score,
                'x_center': x_center,
                'y_center': y_center,
                'box': poly
            })

        df = pd.DataFrame(text_data)
        df = df.sort_values(by=['y_center', 'x_center']).reset_index(drop=True)
        return df

#df = OCRProcessor().process_image('C:\\OCRBuilder\\LAUDO Exemplo.jpg')
#print(df.head(1000))
#df.to_excel('C:\\OCRBuilder\\output.xlsx', index=False, engine='openpyxl')