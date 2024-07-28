import json


class Language:
    def __init__(self, language_file: str, translation_file: str):
        with open(language_file) as f:
            self.config_data = json.load(f)

        with open(translation_file) as f:
            self.translations = json.load(f)
            
    def get_text(self, key: str, language: str = "english") -> str:
        return (
            self.translations.get("general_texts", {}).get(key, {}).get(language)
            or 
            self.translations.get("general_texts", {}).get(key, {}).get("english")
        )

    def get_button_text(self, key: str, language: str = "english") -> str:
        return (
            self.translations.get("button_texts", {}).get(key, {}).get(language)
            or 
            self.translations.get("button_texts", {}).get(key, {}).get("english")
        )
        
    def get_config(self) -> dict:
        return self.config_data
