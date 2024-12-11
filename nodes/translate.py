import os
import re
import requests
import logging
import torch
from unittest.mock import patch
from pathlib import Path
from transformers.dynamic_module_utils import get_imports
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoProcessor

import comfy.model_management as mm
from comfy.utils import ProgressBar
import folder_paths


def fixed_get_imports(filename: str | os.PathLike) -> list[str]:
    if not str(filename).endswith("modeling_florence2.py"):
        return get_imports(filename)
    
    imports = get_imports(filename)
    try:
        imports.remove("flash_attn")
    except:
        print(f"No flash_attn import to remove")
        pass

    return imports


# 判断是否含有中文
def has_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')  # 匹配中文字符的正则表达式
    return bool(pattern.search(text))


class QwenModelLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ([item.name for item in Path(folder_paths.models_dir, "LLM").iterdir() if item.is_dir()], {"tooltip": "models are excepted to be in models/LLM folder"}),
                "precision": [["fp16", "bf16", "fp32"], {"default": "fp16"}],
                "attention": (["flash_attention_2", "sdpa", "eager"], {"default": "sdpa"}),
            },
        }
    
    RETURN_TYPES = ("QwenModel",)
    RETURN_NAMES = ("qwen_model",)
    FUNCTION = "load_model"
    CATEGORY = "AIRedoon"

    def load_model(self, model, precision, attention):
        device = mm.get_torch_device()
        dtype = {
            "bf16": torch.bfloat16,
            "fp16": torch.float16,
            "fp32": torch.float32
        }[precision]
        model_path = Path(folder_paths.models_dir, "LLM", model)

        logging.info(f"Loading model from {model_path}")
        logging.info(f"Using {attention} for attention")

        with patch("transformers.dynamic_module_utils.get_imports",
                   fixed_get_imports):  # workaround for unnecessary flash_attn requirement
            model = AutoModelForCausalLM.from_pretrained(model_path, attn_implementation=attention, device_map=device,
                                                         torch_dtype=dtype, trust_remote_code=True)
        processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        qwen_model = {
            "model": model,
            "processor": processor,
            "tokenizer": tokenizer,
            "dtype": dtype
        }

        return (qwen_model,)


class Translator:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {"multiline": True}),
                "qwen_model": ("QwenModel",),
                "max_length": ("INT", {"default": 512, "min": 64, "max": 1024}),
            },
            "optional": {
                "keep_model_loaded": ("BOOLEAN", {"default": False}),
                "api_key": ("STRING", {"default": ""}),
            }
        }
    
    NAME = "AIRedoonTranslator"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Trans Text",)
    FUNCTION = "translate"
    CATEGORY = "AIRedoon"
    
    def translate(self, input_text, qwen_model, max_length=512, keep_model_loaded=False, api_key=None):
        """
        文本翻译：
        1、使用本地大模型进行翻译
        2、如支持外网访问,通过调用openai接口进行翻译
        """
        # 非中文输入，直接返回
        if not has_chinese(input_text):
            return (input_text, )

        if api_key:
            trans_text = self.translate_by_openai(input_text=input_text)
        else:
            trans_text = self.translate_by_qwen(input_text, qwen_model, max_length, keep_model_loaded)

        print(f"Trans text: {input_text} => {trans_text}")
        
        return (trans_text,)
    
    def translate_by_qwen(self, input_text, qwen_model, max_length, keep_model_loaded):
        """
        通过本地大模型进行翻译
        """
        device = mm.get_torch_device()
        offload_device = mm.unet_offload_device()

        model = qwen_model["model"]
        tokenizer = qwen_model["tokenizer"]
        dtype = qwen_model["dtype"]

        model.to(device)

        prompt = f"请将以下文本翻译成英语：{input_text}"

        messages = [
            {"role": "system", "content": "你是一个AI翻译器,仅仅执行翻译任务。"},
            {"role": "user", "content": prompt}
        ]

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        print(f"AIRedoon input prompt: {prompt}")

        pbar = ProgressBar(1)

        # 编码输入
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        # 生成翻译
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=max_length
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        # 解码输出
        translated_text = [tokenizer.decode(ids, skip_special_tokens=True) for ids in generated_ids]

        pbar.update(1)

        print(f"AIRedoon translated text: {translated_text}")

        if not keep_model_loaded:
            logging.info("Offloading model...")
            model.to(offload_device)
            mm.soft_empty_cache()
        
        return translated_text[0]
    
    def translate_by_openai(self, input_text) -> str:
        """
        通过openai接口进行翻译, 支持外网访问时可用
        """
        trans_text = input_text
        
        return trans_text
