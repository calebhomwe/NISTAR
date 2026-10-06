# NISTAR Production Pipeline

**Episode 1: PRIDE — "I Always Make It"**

Mature psychological seinen anime production pipeline using WAN 2.2 MAX (14B Q8) for video generation and ElevenLabs for dialogue/SFX.

## Play / Test

```bash
pip install -r requirements.txt pytest
python -m pytest -q                              # 29 tests
python scripts/generate_dialogue.py --dry-run    # full dialogue plan, no API calls
```
Windows: `SETUP.bat` then `START_HERE.bat`. CI (`.github/workflows/test.yml`) runs the
tests plus the manifest/prompt export and audio dry runs. Real generation needs an
ElevenLabs key (`.env`), approved character stills and a WAN 2.2 GPU box;
`VALIDATE_WAN_INPUTS.bat` reports missing input frames until stills are added.

## Quick Start

1. **Run SETUP.bat** — creates venv, installs deps, unpacks audio, builds manifests, runs tests
2. **Add your ElevenLabs API key** — copy `.env.example` to `.env`, add your key
3. **Add approved character stills** — place canonical references in `stills/characters/<name>/`
4. **Run PREPARE_WAN_SHOTS.bat** — validates stills, creates 832x480 inputs, exports prompts

## WAN 2.2 MAX Workflow

### How to Generate Each Shot

1. Open your WAN 2.2 MAX interface (ComfyUI or standalone)
2. Open the prompt file from `wan/prompts/episode_01/` for the shot you want
3. Configure these settings from the file header:
   - **Mode:** Image to Video (or Text to Video for atmosphere shots)
   - **Model:** WAN 2.2 MAX 14B Q8
   - **Width:** 832 | **Height:** 480
   - **Frames:** 81 | **Steps:** 20
   - **Speed LoRA:** OFF
   - **Seed:** Leave blank for discovery, lock after approval
4. Load the input image from `wan/input_frames/<SHOT_ID>_input.png`
5. Paste the **POSITIVE PROMPT** and **NEGATIVE PROMPT** from the file
6. Generate 3 takes per shot (discovery passes)
7. Save generated MP4s with the shot ID in the filename

### Importing Generated Clips

Place your generated MP4 files in `wan/output_clips/` with the shot ID in the filename, then run:

```bash
python scripts/ingest_wan_outputs.py
```

This matches clips to shots, assigns take numbers, and records metadata.

### Selecting Approved Takes

```bash
python scripts/select_wan_take.py --shot E01_SH008A --take 2
```

### ComfyUI Integration (Optional)

If ComfyUI is running at `http://127.0.0.1:8188`, the pipeline can optionally submit jobs directly. This is detected automatically — prompt-pack mode always works regardless.

## Audio Workflow

### Dialogue Generation

```bash
# Dry run (no API calls)
python scripts/generate_dialogue.py --dry-run

# Generate single scene
python scripts/generate_dialogue.py --scene SC01

# Generate all
python scripts/generate_dialogue.py
```

### SFX Generation

```bash
python scripts/generate_sfx.py --dry-run
python scripts/generate_sfx.py
```

### Selecting Takes

```bash
python scripts/select_audio_takes.py --line REN_001 --take 2
```

## DaVinci Resolve Export

```bash
python scripts/export_resolve.py
```

Creates ordered video clips, dialogue, SFX, cue sheets, and edit guides in `davinci/episode_01/`.

## Validation

```bash
python scripts/validate_wan_inputs.py    # Check stills, prompts, refs
python scripts/validate_audio_source.py  # Check audio package
python scripts/estimate_generation_load.py  # Time/VRAM estimate
```

## Key Directories

| Directory | Contents |
|-----------|----------|
| `config/` | All YAML configuration (WAN settings, style lock, characters, voices) |
| `stills/characters/` | Canonical character reference images |
| `stills/episode_01/approved/` | Approved keyframe stills for I2V |
| `wan/input_frames/` | 832x480 prepared inputs (auto-generated) |
| `wan/prompts/episode_01/` | Paste-ready WAN prompt files |
| `wan/output_clips/` | Raw generated clips (organized by shot) |
| `wan/approved_clips/` | Selected final takes |
| `audio/dialogue/` | Generated dialogue WAVs |
| `audio/sfx/` | Generated SFX WAVs |
| `audio/selected/` | Approved audio takes |
| `davinci/episode_01/` | Resolve-ready export package |

## Safety

- No paid generation starts automatically (all launchers require confirmation)
- Every command supports `--dry-run`
- API keys are never committed (`.env` is in `.gitignore`)
- All takes are preserved (selecting doesn't delete alternatives)
- Input images are never overwritten
