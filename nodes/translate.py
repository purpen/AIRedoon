import requests

class Translator:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", ),
                "API_KEY": ("STRING", {"default": ""}),
            }
        }
        
    RETURN_TYPES = ("STRING",)
    FUNCTION = "translate"
    CATEGORY = "AIRedoon"
    OUTPUT_NODE = True
    
    def translate(self, input_text, api_key=None) -> tuple:
        """
        通过调用openai接口进行翻译,支持外网访问
        """
        if api_key:
            trans_text = self.translate_by_openai(input_text=input_text)
        else:
            trans_text = self.translate_by_llama(input_text=input_text)
        
        return (trans_text, )
    
    
    def translate_by_llama(self, input_text):
        """
        通过本地模型进行翻译
        """
        trans_text = ""
        
        return trans_text
    
    
    def translate_by_openai(self, input_text) -> str:
        """
        通过openai接口进行翻译, 支持外网访问时可用
        """
        trans_text = ""
        
        return trans_text
