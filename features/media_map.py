"""
features/media_map.py
Maps scenario + step number to a media file in the /media folder.
Filenames match exactly what is present in the media/ folder.
"""

import os

MEDIA_DIR = os.path.join(os.path.dirname(__file__), "..", "media")

MEDIA_MAP = {

    # ── Scene Safety & Primary Assessment ────────────────────────────────
    ("scene_safety_primary_assessment", 4): "scene_safety_avpu_scale.png",
    ("scene_safety_primary_assessment", 6): "scene_safety_carotid_pulse.mp4",
    ("scene_safety_primary_assessment", 7): "scene_safety_recovery_position.mp4",

    # ── Heart Attack ──────────────────────────────────────────────────────
    ("heart_attack", 1): "heart_attack_recognize_signs.jpg",
    ("heart_attack", 7): "heart_attack_cpr_start.mp4",

    # ── Stroke ────────────────────────────────────────────────────────────
    ("stroke", 1): "stroke_befast_mnemonic.jpg",

    # ── Fits / Seizures ───────────────────────────────────────────────────
    ("fits_seizures", 5): "seizure_recovery_position.jpg",

    # ── Snake Bite ────────────────────────────────────────────────────────
    ("snake_bite", 3): "snake_bite_splint_limb.webp",

    # ── Trauma / Road Accident ────────────────────────────────────────────
    ("trauma_road_accident", 2): "trauma_rice_method.png",
    ("trauma_road_accident", 4): "trauma_tourniquet_apply.mp4",
    ("trauma_road_accident", 6): "trauma_neck_stabilization.mp4",
    ("trauma_road_accident", 7): "trauma_log_roll.mp4",
    ("trauma_road_accident", 8): "trauma_helmet_removal.mp4",

    # ── Burns ─────────────────────────────────────────────────────────────
    ("burns", 2): "burns_cool_running_water.mp4",
    ("burns", 3): "burns_fire_blanket_roll.mp4",

    # ── Cardiac Arrest / CPR (ADULT ONLY — steps 1-9) ────────────────────
    ("cardiac_arrest_cpr", 8): "cpr_aed_usage.mp4",

    # ── Choking (ADULT ONLY — steps 1-4 and 7) ───────────────────────────
    ("choking", 2): "choking_back_slaps.mp4",
    ("choking", 3): "choking_heimlich_maneuver.mp4",
    ("choking", 7): "choking_self_heimlich.mp4",

    # ── Infections / Animal Bites ─────────────────────────────────────────
    ("infections_animal_bites", 2): "animal_bite_wound_wash.jpg",
}

def get_media_path(scenario: str, step: int):
    filename = MEDIA_MAP.get((scenario, step))
    if not filename:
        return None, None

    full_path = os.path.join(MEDIA_DIR, filename)
    if not os.path.exists(full_path):
        print(f"[MEDIA] File not found: {full_path}")
        return None, None

    ext = filename.rsplit(".", 1)[-1].lower()
    media_type = "video" if ext == "mp4" else "photo"
    return full_path, media_type

# Cache: filename -> Telegram file_id after first upload
_file_id_cache = {}

def get_cached_file_id(filename: str):
    return _file_id_cache.get(filename)

def cache_file_id(filename: str, file_id: str):
    _file_id_cache[filename] = file_id