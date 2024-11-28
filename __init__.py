from .nodes.translate import Translator
from .nodes.image_captioning import ImageCaptioning

NODE_CLASS_MAPPINGS = {
    "AIRedoonTranslator": Translator,
    "AIRedoonImageCaptioning": ImageCaptioning,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AIRedoonTranslator": "AIRedoon Translator",
    "AIRedoonImageCaptioning": "AIRedoon Image Caption",
}
