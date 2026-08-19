# -*- coding: utf-8 -*-
"""Camera matrix + rigid transform helpers.

Two ideas from the advisor conversation:

1. Camera matrix: position + look_at + look_up define a camera frame. They can
   be converted to/from a 4x4 view matrix, which is what Unity/OpenGL use.
2. Agent-to-agent transform: two agents building the same scene with different
   camera frames produce maps in different coordinate systems. A rigid
   transform (rotation R + translation t, optional mirror) maps one frame into
   the other; estimate it from matched 3D points (Kabsch/Umeyama).
"""
import numpy as np


def _normalize(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def build_view_matrix(position, target, up, unity=False):
    """Build a 4x4 view matrix from camera params.

    OpenGL convention: camera looks down -Z (right-handed).
    Unity convention: camera looks along +Z (left-handed), which is what
    Unity's worldToCameraMatrix / transform expect in practice.
    """
    position = np.asarray(position, dtype=float)
    target = np.asarray(target, dtype=float)
    up = np.asarray(up, dtype=float)

    forward = _normalize(target - position)
    right = _normalize(np.cross(forward, up))
    up_ = np.cross(right, forward)

    eye = position
    if unity:
        # Unity: camera forward is +Z; use right, up, forward as axes.
        R = np.array([right, up_, forward])
        t = -R @ eye
        M = np.eye(4)
        M[:3, :3] = R
        M[:3, 3] = t
        return M
    # OpenGL-style view matrix (camera looks down -Z).
    R = np.array([right, up_, -forward])
    t = -R @ eye
    M = np.eye(4)
    M[:3, :3] = R
    M[:3, 3] = t
    return M


def decompose_view_matrix(M, unity=False):
    """Extract position (camera center) and rotation from a view matrix."""
    R = M[:3, :3]
    t = M[:3, 3]
    position = -R.T @ t
    return position, R


def estimate_rigid_transform(src, dst, allow_mirror=True):
    """Estimate y = R x + t mapping src points onto dst points (Kabsch/Umeyama).

    Works for 2D or 3D points (n x d). Returns R, t, rmse, mirror.
    """
    src = np.asarray(src, dtype=float)
    dst = np.asarray(dst, dtype=float)
    if src.shape[0] < 2 or src.shape != dst.shape:
        return None

    pc = src.mean(axis=0)
    qc = dst.mean(axis=0)
    X = src - pc
    Y = dst - qc
    H = X.T @ Y
    U, _, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    mirror = False
    if np.linalg.det(R) < 0:
        if allow_mirror:
            mirror = True
        else:
            Vt[-1] *= -1
            R = Vt.T @ U.T

    t = qc - R @ pc
    rmse = float(np.sqrt(np.mean(np.sum(((src @ R.T + t) - dst) ** 2, axis=1))))
    return {"R": R, "t": t, "rmse": rmse, "mirror": mirror}


def apply_transform(points, R, t):
    points = np.asarray(points, dtype=float)
    return points @ R.T + t


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    # Random rotation + translation, recover it.
    A = rng.normal(size=(3, 3))
    Q, _ = np.linalg.qr(A)
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    t_true = np.array([1.0, -2.0, 3.0])
    src = rng.normal(size=(10, 3))
    dst = src @ Q.T + t_true
    est = estimate_rigid_transform(src, dst)
    print("rmse:", est["rmse"], "mirror:", est["mirror"])
    print("rotation recovered:", np.allclose(est["R"], Q, atol=1e-8))
    print("translation recovered:", np.allclose(est["t"], t_true, atol=1e-8))

    pos = np.array([1.0, 2.0, 3.0])
    target = np.array([1.0, 2.0, 5.0])
    up = np.array([0.0, 1.0, 0.0])
    M = build_view_matrix(pos, target, up)
    print("view matrix shape:", M.shape)
    print("camera position recovered:", decompose_view_matrix(M)[0])
