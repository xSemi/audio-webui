import gradio
import huggingface_hub
import webui.modules.models as mod

model_types = ['text-to-speech', 'automatic-speech-recognition', 'audio-to-audio']


class AutoModel:
    def __init__(self, repo_id, model_type):
        self.repo_id = repo_id
        self.model_type = model_type

    def __str__(self):
        return self.repo_id


def fill_models(model_type: str):
    if model_type == 'text-to-speech':
        return [m for m in mod.all_tts() if not m.no_install]
    return [model.modelId for model in
            huggingface_hub.list_models(filter=huggingface_hub.ModelFilter(task=model_type), sort='downloads')]


def get_file_name(repo_id: str):
    return repo_id.replace('/', '--')


def hub_download(repo_id: str, model_type: str):
    try:
        huggingface_hub.snapshot_download(repo_id, local_dir_use_symlinks=False,
                                          local_dir=f'data/models/{model_type}/{get_file_name(repo_id)}')
    except Exception as e:
        return [f'<p style="color: red;">{str(e)}</p>', gradio.Dropdown.update()]
    return [f"Successfully downloaded <a target='_blank' href='https://www.huggingface.co/{repo_id}'>{repo_id}</a>", mod.refresh_choices()]