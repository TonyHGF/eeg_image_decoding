"""Load tensor checkpoints with the NumPy scalar metadata used by upstream."""
import numpy as np
import torch


def load_eeg_checkpoint(path):
    # The author's validation loss is a NumPy scalar. Do not enable arbitrary
    # pickle globals just to read this numeric metadata under PyTorch 2.6.
    allowed = [np.core.multiarray.scalar, np.dtype,
               type(np.dtype('float64')), type(np.dtype('float32'))]
    with torch.serialization.safe_globals(allowed):
        return torch.load(path, map_location='cpu', weights_only=True)
