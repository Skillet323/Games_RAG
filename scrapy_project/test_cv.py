# test_cv.py
from fandom_parser.cv_runner import analyze_image

test_url = "https://static.wikia.nocookie.net/celestegame/images/9/94/Average_Celeste_Screen.jpg"
result = analyze_image(test_url)
print("Описание:", result['caption'])
print("Объекты:", result['objects'])