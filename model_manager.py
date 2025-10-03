import os
from huggingface_hub import hf_hub_download

import appdirs

# Define the local directory where models will be cached
# This path should be mounted as a volume in Docker to persist models.
config_dir = appdirs.user_config_dir('noScribe')
MODELS_DIR = os.path.join(config_dir, "models")


# Define model repositories on Hugging Face
WHISPER_MODELS = {
    "precise": "mobiuslabsgmbh/faster-whisper-large-v3-turbo",
    "fast": "mukowaty/faster-whisper-int8"
}
PYANNOTE_MODELS = {
    "segmentation": "pyannote/segmentation-3.0",
    "embedding": "pyannote/wespeaker-voxceleb-resnet34-LM"
}

def ensure_whisper_model(name: str):
    """
    Ensures a specific Whisper model repository is downloaded using snapshot_download.
    """
    model_path = os.path.join(MODELS_DIR, name)
    if not os.path.exists(os.path.join(model_path, 'model.bin')):
        print(f"Whisper model '{name}' not found. Downloading...")
        from huggingface_hub import snapshot_download
        snapshot_download(
            repo_id=WHISPER_MODELS[name],
            local_dir=model_path,
            local_dir_use_symlinks=False # Set to False to download files directly
        )
        print(f"Whisper model '{name}' downloaded successfully.")
    else:
        print(f"Whisper model '{name}' already exists.")


def ensure_pyannote_models():
    """
    Ensures all necessary Pyannote models are downloaded.
    """
    print("Checking for Pyannote models...")
    try:
        # hf_hub_download will download the file if it's not in the cache,
        # or use the cached version if it is.
        hf_hub_download(repo_id=PYANNOTE_MODELS["segmentation"], filename="pytorch_model.bin")
        hf_hub_download(repo_id=PYANNOTE_MODELS["embedding"], filename="pytorch_model.bin")
        print("All Pyannote models are ready.")
    except Exception as e:
        print(f"Error downloading Pyannote models: {e}")
        raise

def get_model_path(model_name: str) -> str:
    """
    Returns the local path for a given model name.
    """
    return os.path.join(MODELS_DIR, model_name)

if __name__ == '__main__':
    # This allows the script to be run directly to pre-download all models
    print("Downloading all necessary models...")
    ensure_whisper_model("precise")
    ensure_whisper_model("fast")
    ensure_pyannote_models()
    print("All models are downloaded and ready.")