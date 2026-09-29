"""Offline RN50 loaders; use the official OpenAI archive without Hub lookup."""
from pathlib import Path


def load_backend(backend, weights):
    weights = Path(weights)
    if backend == 'cn':
        import cn_clip.clip as clip
        model, transform = clip.load_from_name('RN50', device='cuda', download_root=str(weights))
        return model.float().eval(), transform, clip.tokenize
    import open_clip
    from open_clip.openai import load_openai_model
    from open_clip.transform import image_transform
    from open_clip.constants import OPENAI_DATASET_MEAN, OPENAI_DATASET_STD
    model = load_openai_model(str(weights / 'RN50.pt'), precision='fp32', device='cuda')
    transform = image_transform(224, is_train=False, mean=OPENAI_DATASET_MEAN,
                                std=OPENAI_DATASET_STD, interpolation='bicubic', resize_mode='shortest')
    return model.eval(), transform, open_clip.get_tokenizer('RN50')
