from .nodes.translate import Translator, QwenModelLoader
from .nodes.image_captioning import ImageCaptioning
from .nodes.loras import LoRAStack, ApplyLoRAStack
from .nodes.checker import CheckLoraFile, CheckModelFile
from .nodes.kits import PreviewText, SaveText, ConcatText, ImageRGBA2RGB

WEB_DIRECTORY = "./js"

NODE_CLASS_MAPPINGS = {
    "AIRedoonQwenModelLoader": QwenModelLoader,
    "AIRedoonTranslator": Translator,
    "AIRedoonImageCaptioning": ImageCaptioning,
    "AIRedoonLoRAStack": LoRAStack,
    "AIRedoonApplyLoRAStack": ApplyLoRAStack,
    "AIRedoonCheckLoraFile": CheckLoraFile,
    "AIRedoonCheckModelFile": CheckModelFile,
    "AIRedoonImageRGBA2RGB": ImageRGBA2RGB,
    "AIRedoonPreviewText": PreviewText,
    "AIRedoonSaveText": SaveText,
    "AIRedoonConcatText": ConcatText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AIRedoonQwenModelLoader": "AIRedoon Qwen Model Loader",
    "AIRedoonTranslator": "AIRedoon Translator",
    "AIRedoonImageCaptioning": "AIRedoon Image Caption",
    "AIRedoonLoRAStack": "AIRedoon LoRA Stack",
    "AIRedoonApplyLoRAStack": "AIRedoon Apply LoRA Stack",
    "AIRedoonCheckLoraFile": "AIRedoon Check LoRA",
    "AIRedoonCheckModelFile": "AIRedoon Check Model",
    "AIRedoonImageRGBA2RGB": "AIRedoon Image RGBA2RGB",
    "AIRedoonPreviewText": "AIRedoon Preview Text",
    "AIRedoonSaveText": "AIRedoon Save Text",
    "AIRedoonConcatText": "AIRedoon Concat Text",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
