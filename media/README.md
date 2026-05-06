# Media Files Guide — Jeeva First Aid Bot

Place all your image and video files in this `/media` folder.
Use the **exact filenames** listed below. The bot will automatically send the
correct media after each step's text message.

Supported formats:
- Images: `.jpg` or `.png`
- Videos: `.mp4`

---

## Scene Safety & Primary Assessment

| Step | Filename | Type | What to show |
|------|----------|------|--------------|
| 4 | `scene_safety_avpu_scale.jpg` | Image | AVPU scale diagram (Alert/Voice/Pain/Unresponsive) |
| 6 | `scene_safety_carotid_pulse.jpg` | Image | How to check carotid pulse on neck |
| 7 | `scene_safety_recovery_position.jpg` | Image | Recovery position demonstration |

---

## Heart Attack

| Step | Filename | Type | What to show |
|------|----------|------|--------------|
| 1 | `heart_attack_recognize_signs.jpg` | Image | Heart attack warning signs diagram |
| 7 | `heart_attack_cpr_start.mp4` | Video | Starting CPR on heart attack victim |

---

## Stroke

| Step | Filename | Type | What to show |
|------|----------|------|--------------|
| 1 | `stroke_befast_mnemonic.jpg` | Image | BEFAST mnemonic diagram |

---

## Fits / Seizures

| Step | Filename | Type | What to show |
|------|----------|------|--------------|
| 2 | `seizure_safety_position.jpg` | Image | Clearing area and placing pillow under head |
| 5 | `seizure_recovery_position.jpg` | Image | Recovery position after seizure |

---

## Low Blood Sugar

| Step | Filename | Type | What to show |
|------|----------|------|--------------|
| 2 | `low_sugar_give_glucose.jpg` | Image | Giving juice/sugar to conscious patient |

---

## Snake Bite

| Step | Filename | Type | What to show |
|------|----------|------|--------------|
| 3 | `snake_bite_splint_limb.jpg` | Image | How to splint/immobilize a bitten limb |

---

## Trauma / Road Accident

| Step | Filename | Type | What to show |
|------|----------|------|--------------|
| 2 | `trauma_rice_method.jpg` | Image | RICE method diagram for fractures |
| 4 | `trauma_tourniquet_apply.mp4` | Video | How to apply tourniquet correctly |
| 6 | `trauma_neck_stabilization.mp4` | Video | Neck stabilization / cervical collar |
| 7 | `trauma_log_roll.mp4` | Video | Log roll technique with 4 people |
| 8 | `trauma_helmet_removal.mp4` | Video | Safe helmet removal procedure |

---

## Burns

| Step | Filename | Type | What to show |
|------|----------|------|--------------|
| 2 | `burns_cool_running_water.mp4` | Video | Cooling burn under running water for 15-20 min |
| 3 | `burns_fire_blanket_roll.mp4` | Video | Stop drop and roll / fire blanket technique |

---

## Cardiac Arrest / CPR

| Step | Filename | Type | What to show |
|------|----------|------|--------------|
| 4 | `cpr_carotid_pulse_check.mp4` | Video | How to check carotid pulse within 10 seconds |
| 5 | `cpr_chest_compressions_position.mp4` | Video | Hand placement and body position for compressions |
| 6 | `cpr_compression_depth_rate.mp4` | Video | Correct depth and rate of compressions |
| 8 | `cpr_aed_usage.mp4` | Video | How to use AED step by step |
| 10 | `cpr_infant_two_finger.mp4` | Video | Two finger / two thumb CPR for infants |

---

## Choking

| Step | Filename | Type | What to show |
|------|----------|------|--------------|
| 2 | `choking_back_slaps.mp4` | Video | Back slap technique for conscious choking adult |
| 3 | `choking_heimlich_maneuver.mp4` | Video | Heimlich maneuver / abdominal thrusts |
| 5 | `choking_pregnant_chest_thrust.mp4` | Video | Chest thrust for pregnant women |
| 6 | `choking_infant_back_blows.mp4` | Video | Back blows and chest thrusts for choking infant |
| 7 | `choking_self_heimlich.mp4` | Video | Self Heimlich maneuver using chair/counter |

---

## Infections / Animal Bites

| Step | Filename | Type | What to show |
|------|----------|------|--------------|
| 2 | `animal_bite_wound_wash.jpg` | Image | Washing animal bite wound with soap and water |

---

## Notes

- If a file is missing, the bot will still send the text step normally — no crash
- You can add more media by editing `features/media_map.py`
- Keep video files under 50MB for Telegram compatibility
- Recommended video format: MP4 (H.264)
- Recommended image format: JPG (under 5MB)
