import os
import time
from .utils import rgba2rgb_tensor


class ImageRGBA2RGB:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",)
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "convert"
    CATEGORY = "AIRedoon"

    def convert(self, image):
        out = rgba2rgb_tensor(image)
        return (out,)


class PreviewText:

    NAME = "AIRedoonPreviewText"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "preview_text"
    CATEGORY = "AIRedoon"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True})
            }
        }
    
    def preview_text(self, text):
        if text is None:
            text = ""
        value = text.strip()
        print(f"Output text: {value}")

        # 输出到ComfyUI界面
        return {"ui": {"text": (value,)}, "result": (value,)}


class SaveText:

    NAME = "AIRedoonSaveText"
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "save_text"
    CATEGORY = "AIRedoon"
    OUTPUT_NODE = True

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "save_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "filename": ("STRING", {"forceInput": True}),
            }
        }
    
    def save_text(self, text, save_path, filename=""):
        if text is None:
            text = ""

        text_to_save = text.strip()
        if save_path is None:
            raise ValueError(f"save_path can't be None")
        
        if filename is None or filename == "":
            filename = f"redoon-{int(time.time())}.txt"
        
        filepath = os.path.join(save_path, filename)
        
        with open(filepath, "w", encoding="utf-8") as fs:
            fs.write(text_to_save)

        return ()


class ConcatText:

    CATEGORY = "AIRedoon"
    FUNCTION = "concat"
    RETURN_TYPES = ("STRING",)
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text1": ("STRING", {"multiline": True, "default": ""}),
            "text2": ("STRING", {"multiline": True, "default": ""}),
            "delimiter": ("STRING", {"default": ","}),
        },
    }

    def concat(self, text1="", text2="", delimiter=","):
        text1 = "" if text1 == "undefined" else text1
        text2 = "" if text2 == "undefined" else text2

        if delimiter == "\\n":
            delimiter = "\n"

        _texts = list()
        if text1 != "":
            _texts.append(text1)
        
        if text2 != "":
            _texts.append(text2)

        concated_text = delimiter.join(_texts)

        return {
            "ui": {"text": (concated_text,)}, 
            "result": (concated_text,)
        }
