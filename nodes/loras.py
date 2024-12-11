import folder_paths
import comfy.utils


class LoRAStack:

    @classmethod
    def INPUT_TYPES(cls):
    
        loras = ["None"] + folder_paths.get_filename_list("loras")
        
        return {
            "required": {
                "switch_1": (["Off","On"],),
                "lora_name_1": (loras,),
                "model_weight_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "clip_weight_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "trigger_word_1": ("STRING", {"default": ""}),
                "switch_2": (["Off","On"],),
                "lora_name_2": (loras,),
                "model_weight_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "clip_weight_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "trigger_word_2": ("STRING", {"default": ""}),
                "switch_3": (["Off","On"],),
                "lora_name_3": (loras,),
                "model_weight_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "clip_weight_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "trigger_word_3": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("LORA_STACK", "STRING",)
    RETURN_NAMES = ("LoRA Stack", "Trigger Words",)
    FUNCTION = "lora_stacker"
    CATEGORY = "AIRedoon"

    def lora_stacker(self, switch_1, lora_name_1, model_weight_1, clip_weight_1, trigger_word_1, switch_2, lora_name_2, model_weight_2, clip_weight_2, trigger_word_2, switch_3, lora_name_3, model_weight_3, clip_weight_3, trigger_word_3):

        # Initialise the list
        lora_list = list()
        trigger_words = list()
        
        if lora_name_1 != "None" and  switch_1 == "On":
            lora_list.extend([(lora_name_1, model_weight_1, clip_weight_1)])
            trigger_words.append(trigger_word_1)
            
        if lora_name_2 != "None" and  switch_2 == "On":
            lora_list.extend([(lora_name_2, model_weight_2, clip_weight_2)])
            trigger_words.append(trigger_word_2)

        if lora_name_3 != "None" and  switch_3 == "On":
            lora_list.extend([(lora_name_3, model_weight_3, clip_weight_3)])
            trigger_words.append(trigger_word_3)
        
        return (lora_list, ",".join(trigger_words), )


class ApplyLoRAStack:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_stack": ("LORA_STACK",),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", )
    RETURN_NAMES = ("MODEL", "CLIP", )
    FUNCTION = "apply_lora_stack"
    CATEGORY = "AIRedoon"

    def apply_lora_stack(self, model, clip, lora_stack=None):
        # Initialise the list
        lora_params = list()
 
        # Extend lora_params with lora-stack items 
        if lora_stack:
            lora_params.extend(lora_stack)
        else:
            return (model, clip,)

        # Initialise the model and clip
        model_lora = model
        clip_lora = clip

        # Loop through the list
        for lora_info in lora_params:
            lora_name, strength_model, strength_clip = lora_info
            
            lora_path = folder_paths.get_full_path("loras", lora_name)
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            
            model_lora, clip_lora = comfy.sd.load_lora_for_models(model_lora, clip_lora, lora, strength_model, strength_clip)  

        return (model_lora, clip_lora,)
