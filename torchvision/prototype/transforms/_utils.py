from typing import Any, Tuple, Type, Union

import PIL.Image
import torch
from torch.utils._pytree import tree_flatten
from torchvision.prototype import features

from .functional._meta import get_dimensions_image_pil, get_dimensions_image_tensor


def query_image(sample: Any) -> Union[PIL.Image.Image, torch.Tensor, features.Image]:
    flat_sample, _ = tree_flatten(sample)
    for i in flat_sample:
        if type(i) == torch.Tensor or isinstance(i, (PIL.Image.Image, features.Image)):
            return i

    raise TypeError("No image was found in the sample")


def get_image_dimensions(image: Union[PIL.Image.Image, torch.Tensor, features.Image]) -> Tuple[int, int, int]:
    if isinstance(image, features.Image):
        channels = image.num_channels
        height, width = image.image_size
    elif isinstance(image, torch.Tensor):
        channels, height, width = get_dimensions_image_tensor(image)
    elif isinstance(image, PIL.Image.Image):
        channels, height, width = get_dimensions_image_pil(image)
    else:
        raise TypeError(f"unable to get image dimensions from object of type {type(image).__name__}")
    return channels, height, width


def has_any(sample: Any, *types: Type) -> bool:
    flat_sample, _ = tree_flatten(sample)
    return any(issubclass(type(obj), types) for obj in flat_sample)


def has_all(sample: Any, *types: Type) -> bool:
    flat_sample, _ = tree_flatten(sample)
    return not bool(set(types) - set([type(obj) for obj in flat_sample]))


def is_simple_tensor(input: Any) -> bool:
    return isinstance(input, torch.Tensor) and not isinstance(input, features._Feature)
