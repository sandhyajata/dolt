from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    aiops_enabler_base_url: str = "https://aiopsenabler.com"
    aiops_enabler_api_key: str = ""
    aiops_learning_search_path: str = "/api/v1/learnings/search"
    aiops_learning_contribute_path: str = "/api/v1/learnings"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
