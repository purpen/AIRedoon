import os
import logging
import folder_paths


class CheckLoraFile:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_name": ("STRING", {"default": ""})
            }
        }
    
    NAME = "AIRedoonCheckLoraFile"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("File Exist",)
    FUNCTION = "check_lora"
    CATEGORY = "AIRedoon"

    def check_lora(self, file_name):
        """
        验证文件是否存在
        """
        is_exist = "No"

        _, ext = os.path.splitext(file_name)

        for root_path in folder_paths.get_folder_paths("loras"):

            lora_file = os.path.join(root_path, file_name)

            logging.info(f"Check lora file: {lora_file}")

            if ext.lower() == ".safetensors" and os.path.exists(lora_file):
                is_exist = "Yes"
                break

        logging.info(f"Lora file: {is_exist}")

        return (is_exist,)



class CheckModelFile:

    NAME = "AIRedoonCheckModelFile"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("File Exist",)
    FUNCTION = "check_model"
    CATEGORY = "AIRedoon"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_name": ("STRING", {"default": ""})
            }
        }
    
    def check_model(self, file_name):
        """
        验证文件是否存在
        """
        is_exist = "No"

        _, ext = os.path.splitext(file_name)

        for root_path in folder_paths.get_folder_paths("checkpoints"):
            model_file = os.path.join(root_path, file_name)

            logging.info(f"Check model file: {model_file}")

            if ext.lower() == ".safetensors" and os.path.exists(model_file):
                is_exist = "Yes"
                break

        logging.info(f"Model file： {is_exist}")

        return (is_exist,)
