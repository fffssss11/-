from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Tuple

import numpy as np
from PIL import Image, ImageFilter


@dataclass
class VisualScore:
    color_similarity: float
    brightness_similarity: float
    edge_similarity: float
    final_score: float
    interpretation: str
    suggestions: list[str]


def _prepare(img: Image.Image, size: Tuple[int, int] = (256, 256)) -> Image.Image:
    return img.convert("RGB").resize(size)


def _color_hist(img: Image.Image) -> np.ndarray:
    arr = np.asarray(img)
    hist_parts = []
    for channel in range(3):
        hist, _ = np.histogram(arr[:, :, channel], bins=32, range=(0, 255), density=True)
        hist_parts.append(hist)
    hist_all = np.concatenate(hist_parts)
    return hist_all / (np.linalg.norm(hist_all) + 1e-8)


def _brightness(img: Image.Image) -> float:
    arr = np.asarray(img.convert("L"), dtype=np.float32)
    return float(arr.mean())


def _edge_density(img: Image.Image) -> float:
    gray = img.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    arr = np.asarray(edges, dtype=np.float32) / 255.0
    return float(arr.mean())


def _sim_distance(a: float, b: float, max_delta: float) -> float:
    return max(0.0, min(1.0, 1.0 - abs(a - b) / max_delta))


def compare_images(robot_img: Image.Image, ref_img: Image.Image) -> Dict:
    """对机器人图片和参考鸟类/环境图片做轻量级视觉相似度评估。

    注意：这不是严格学术视觉模型，只用于答辩材料中的辅助量化演示。
    """
    robot = _prepare(robot_img)
    ref = _prepare(ref_img)

    h1 = _color_hist(robot)
    h2 = _color_hist(ref)
    color_similarity = float(np.dot(h1, h2))

    brightness_similarity = _sim_distance(_brightness(robot), _brightness(ref), 255.0)
    edge_similarity = _sim_distance(_edge_density(robot), _edge_density(ref), 0.35)

    final_score = 100 * (0.50 * color_similarity + 0.25 * brightness_similarity + 0.25 * edge_similarity)

    suggestions: list[str] = []
    if color_similarity < 0.65:
        suggestions.append("颜色分布差异较大：建议调整机翼表面纹理、羽毛色块或拍摄背景。")
    if brightness_similarity < 0.75:
        suggestions.append("明暗差异较大：建议统一光照条件，避免机器人表面反光过强。")
    if edge_similarity < 0.70:
        suggestions.append("轮廓/边缘密度差异较大：建议优化翼尖、尾翼和机身过渡线条。")
    if not suggestions:
        suggestions.append("整体相似度较好，可继续补充动态飞行姿态对比视频。")

    if final_score >= 80:
        interpretation = "视觉融合度较高，适合用于真假鸟互动展示。"
    elif final_score >= 60:
        interpretation = "具备一定仿生效果，但仍需优化颜色、轮廓或场景光照。"
    else:
        interpretation = "当前相似度偏低，建议先优化外观涂装和拍摄场景。"

    return asdict(VisualScore(
        color_similarity=round(color_similarity, 3),
        brightness_similarity=round(brightness_similarity, 3),
        edge_similarity=round(edge_similarity, 3),
        final_score=round(final_score, 1),
        interpretation=interpretation,
        suggestions=suggestions,
    ))
