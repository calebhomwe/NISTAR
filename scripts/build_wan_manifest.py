"""Build the Episode 1 shot manifest with all 20 initial proof shots."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.models import Shot
from nistar_pipeline.manifests import save_shot_manifest, save_shot_manifest_csv, save_shot_manifest_md
from nistar_pipeline.wan import GLOBAL_NEGATIVE


def build_episode_01_shots() -> list[Shot]:
    shots = []

    shots.append(Shot(
        shot_id="E01_SH001",
        scene="SC01_DREAM",
        title="Dream Highway",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH001_input.png",
        characters=["ren"],
        environment="elevated highway, dream version",
        vehicle="R34 GTR (idealised, dream state)",
        camera="low exterior side tracking shot, one continuous movement, no orbit",
        primary_action="R34 driving at controlled speed through empty elevated highway",
        secondary_motion=["wheels rotating", "suspension movement", "passing pillars", "restrained speed blur", "subtle turbo vibration"],
        lighting="richer dream colours, clean blue and cyan undertones",
        colour_script="Blue, cyan, violet, controlled red road lights — no orange-purple wash",
        positive_prompt="Young man driving idealised silver R34 GTR through empty elevated highway at night, low exterior side tracking shot, continuous smooth camera movement, wheels rotating, passing concrete pillars, subtle turbo heat haze, restrained motion blur, dream-quality lighting, clean blue and cyan reflections, violet undertones, controlled red road-light streaks",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH002",
        scene="SC01_DREAM",
        title="The Void",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH002_input.png",
        characters=["ren"],
        environment="highway dissolving into void",
        vehicle="R34 GTR",
        camera="interior-facing or medium exterior, static hold",
        primary_action="Highway disappears — lane markings vanish one at a time",
        secondary_motion=["city colour drains progressively", "darkness expands from edges", "Ren remains calm with slight smile"],
        lighting="draining from colour to black",
        colour_script="Colour progressively bleeds out — blue to grey to black",
        positive_prompt="Highway dissolving into black void, lane markings vanishing one at a time, city colour draining away progressively, young man driving remains calm with slight knowing smile, darkness expanding from frame edges, gradual desaturation",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH003",
        scene="SC02_CRASH",
        title="Crash Aftermath",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH003_input.png",
        characters=["ren"],
        environment="beneath highway interchange, rain",
        vehicle="R34 GTR (upside-down, damaged)",
        camera="low angle, static or very slow push",
        primary_action="Upside-down damaged car beneath the interchange",
        secondary_motion=["rain falling", "steam rising from engine", "flickering headlight", "one wheel slowly rotating", "fingers twitch once"],
        lighting="cold clinical rain, single amber headlight flicker",
        colour_script="Desaturated except flickering amber headlight",
        positive_prompt="Upside-down damaged silver R34 GTR beneath concrete highway interchange, rain falling steadily, steam rising from crumpled engine bay, one headlight flickering amber, single rear wheel slowly rotating to stop, driver's fingers twitch once, wet asphalt reflections, cold rain atmosphere",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH004",
        scene="SC03_APARTMENT",
        title="Ren Awakens",
        duration_target_seconds=3,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH004_input.png",
        characters=["ren"],
        environment="small messy apartment, couch",
        camera="medium close-up, stable",
        primary_action="Ren violently wakes on the couch",
        secondary_motion=["sudden gasp", "hand strikes coffee table", "energy drink can falls", "television static flicker", "chest heaving"],
        lighting="sickly warm TV glow, amber can",
        colour_script="Television static glow, can amber, sweat-damp warm skin",
        positive_prompt="Young man violently waking on worn couch, sudden gasp, hand strikes coffee table, energy drink can falls and rolls, old television showing static in background, chest heaving with rapid breathing, small messy apartment, warm sickly lighting from TV",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH005",
        scene="SC04_GARAGE",
        title="Garage Reveal",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH005_input.png",
        characters=["ren"],
        environment="small residential garage",
        vehicle="R34 GTR (battered, real condition)",
        camera="slow straight dolly forward",
        primary_action="Garage door opens revealing battered R34",
        secondary_motion=["garage door lifts", "fluorescent light flickers on", "dust particles in light beam", "slow dolly reveals car"],
        lighting="harsh fluorescent flicker, morning light from opening door",
        colour_script="Cold fluorescent + warm morning light shaft",
        positive_prompt="Garage door slowly opening, fluorescent tube light flickering on, revealing battered silver R34 GTR inside small residential garage, dust particles floating in morning light beam, slow straight dolly push forward, worn concrete floor, tools on wall",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH006",
        scene="SC05_DRIVING",
        title="Fuel Warning",
        duration_target_seconds=3,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH006_input.png",
        characters=["ren"],
        environment="car interior, night driving",
        vehicle="R34 GTR (interior)",
        camera="dashboard angle showing gauge cluster and driver face",
        primary_action="Fuel warning light pulses on dashboard",
        secondary_motion=["warning light pulses amber", "engine vibration through frame", "subtle eye movement down to gauge", "hand silences warning"],
        lighting="dashboard glow, passing streetlights",
        colour_script="Amber warning + cool blue passing light",
        positive_prompt="Car interior dashboard view at night, fuel warning light pulsing amber on gauge cluster, young man's face lit by dashboard glow, subtle eye movement glancing down at gauge, hand reaches to silence warning, engine vibration, passing streetlights casting moving shadows",
        negative_prompt=GLOBAL_NEGATIVE + ", readable text on dashboard",
    ))

    shots.append(Shot(
        shot_id="E01_SH007",
        scene="SC05_DRIVING",
        title="Semi-Truck Threat",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH007_input.png",
        characters=["ren"],
        environment="highway, rain, night",
        vehicle="R34 GTR interior + semi-truck",
        camera="interior windscreen shot, no cut",
        primary_action="Semi-truck crosses into lane ahead",
        secondary_motion=["truck headlights fill windscreen", "Ren grips steering wheel", "rain intensifies on glass", "wipers sweep"],
        lighting="blinding truck headlights through rain",
        colour_script="White headlight flare into rain-diffused warmth",
        positive_prompt="Interior car shot through rain-covered windscreen, massive semi-truck crossing into lane ahead, truck headlights filling the frame with blinding white light, driver gripping steering wheel, rain intensifying on glass, wipers sweeping once, no camera cut, building tension",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH008A",
        scene="SC05_DRIVING",
        title="Guardian Reveal",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH008A_input.png",
        characters=["guardian"],
        environment="car hood exterior, highway rain",
        vehicle="R34 GTR (exterior hood)",
        camera="slow push toward guardian's face",
        primary_action="Guardian already crouched on the moving car hood",
        secondary_motion=["rain hitting worn canvas jacket", "coat fabric movement in wind", "approaching headlights from behind", "slow camera push toward weathered face"],
        lighting="rain reflections, approaching headlights from behind",
        colour_script="Cool rain blue + warm approaching amber headlights",
        positive_prompt="Weary human-looking guardian figure crouched on hood of moving car in rain, worn canvas jacket and steel-toe boots, scarred hands gripping metal, rain hitting fabric, coat moving in wind, approaching headlights from behind casting long shadows, slow push toward gaunt weathered face, pale grey tired eyes, no wings no halo no glow",
        negative_prompt=GLOBAL_NEGATIVE + ", wings, halo, glow, ethereal, angelic, demonic",
    ))

    shots.append(Shot(
        shot_id="E01_SH008B",
        scene="SC05_DRIVING",
        title="Mechanical Correction",
        duration_target_seconds=3,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH008B_input.png",
        characters=["guardian"],
        environment="car exterior, close on wheel/steering",
        vehicle="R34 GTR",
        camera="close-up, locked on hands and wheel mechanism",
        primary_action="Guardian's hand physically forces the steering wheel direction",
        secondary_motion=["metal flexing under force", "tyre rotation changing direction", "suspension loading", "rain on scarred knuckles"],
        lighting="rain-diffused, streetlight passing",
        colour_script="Steel grey + amber street-light sweep",
        positive_prompt="Extreme close-up of scarred weathered hands physically forcing car steering mechanism, metal flexing under supernatural strength, tyre rotation changing direction, suspension compressing under load, rain running over scarred knuckles, no magical effects, purely mechanical physical force",
        negative_prompt=GLOBAL_NEGATIVE + ", magic, glow, energy effects, lightning",
    ))

    shots.append(Shot(
        shot_id="E01_SH009",
        scene="SC05_DRIVING",
        title="Near Miss",
        duration_target_seconds=3,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH009_input.png",
        characters=["ren"],
        environment="highway, rain",
        vehicle="R34 GTR + semi-truck",
        camera="exterior medium, following car",
        primary_action="Truck passes inches from car",
        secondary_motion=["violent wind pressure wave", "side mirror folds from force", "car rocks on suspension", "Ren reacts inside"],
        lighting="truck running lights + rain",
        colour_script="Dark blue rain + amber truck lights sweeping past",
        positive_prompt="Silver R34 GTR swerving as massive semi-truck passes within inches, violent wind pressure wave visible in rain spray, side mirror folding from air force, car rocking on suspension, driver reacting with shock inside, rain and spray cloud",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH010",
        scene="SC05_DRIVING",
        title="Still Got It",
        duration_target_seconds=3,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH010_input.png",
        characters=["ren"],
        environment="car interior after near-miss",
        camera="close-up on Ren's face, stable",
        primary_action="Ren's small arrogant smile forms after the save",
        secondary_motion=["breathing settling", "hand tremor on wheel", "small proud smile forming", "police lights appearing in rear window"],
        lighting="dashboard glow + emerging red-blue police light",
        colour_script="Warm interior + cold red/blue creeping in",
        positive_prompt="Close-up on young man's face inside car after near-miss, breathing settling, hand still trembling on steering wheel, small arrogant proud smile forming on lips, red and blue police lights beginning to appear reflected in rear window, grey-blue eyes, messy dark hair, guarded pride",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH011",
        scene="SC05_DRIVING",
        title="Chase Interior",
        duration_target_seconds=3,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH011_input.png",
        characters=["ren"],
        environment="car interior, police chase",
        camera="interior medium, controlled camera shake",
        primary_action="Ren's pride intensifies as chase begins",
        secondary_motion=["red and blue police reflections sweeping across interior", "controlled camera shake", "gear change motion", "slight grin widening"],
        lighting="red/blue police light wash over interior",
        colour_script="Alternating red-blue wash, dashboard amber",
        positive_prompt="Car interior during police chase, red and blue light reflections sweeping across surfaces and young man's face, controlled camera vibration from speed, hand performing gear change, slight confident grin widening, pride visible in expression, night highway",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH012",
        scene="SC06_WAREHOUSE",
        title="Warehouse Arrival",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH012_input.png",
        characters=["ren"],
        environment="industrial yard, warehouse",
        vehicle="R34 GTR",
        camera="locked wide shot",
        primary_action="R34 slides into industrial yard and stops",
        secondary_motion=["controlled drift arc", "realistic vehicle weight and momentum", "tyre smoke settling", "dust cloud"],
        lighting="sodium industrial lights, harsh",
        colour_script="Harsh sodium amber + cool night blue",
        positive_prompt="Silver R34 GTR performing controlled drift slide into industrial warehouse yard, wide locked camera, realistic vehicle weight and momentum, tyre smoke rising and settling, dust cloud, car coming to controlled stop, sodium industrial overhead lights casting harsh amber, night blue sky",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH013",
        scene="SC06_WAREHOUSE",
        title="Sato and Puppy",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH013_input.png",
        characters=["ren", "sato"],
        environment="warehouse interior",
        camera="medium two-shot, stable",
        primary_action="Quiet warehouse confrontation",
        secondary_motion=["puppy trembles in Sato's arm", "Sato strokes puppy calmly", "Ren's expression falls", "fluorescent light flickers once"],
        lighting="cold fluorescent overhead, harsh green-white",
        colour_script="Cold fluorescent green-white, puppy warm spot",
        positive_prompt="Warehouse interior confrontation, older man in grey suit calmly stroking small trembling puppy in his arm, younger man opposite with expression falling from confidence to unease, harsh fluorescent overhead light flickering once, cold industrial space, quiet menace through stillness",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH014",
        scene="SC06_WAREHOUSE",
        title="Final Dashboard",
        duration_target_seconds=3,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH014_input.png",
        characters=["ren"],
        environment="car interior, parked",
        vehicle="R34 GTR interior",
        camera="close on hands and dashboard",
        primary_action="Ren holds cash envelope inside car",
        secondary_motion=["shaking hands holding thick envelope", "red warning light pulsing on dash", "engine fails then catches again", "controlled bitter smile"],
        lighting="red warning glow + ambient",
        colour_script="Red warning pulse dominant",
        positive_prompt="Close-up inside parked car, young man's shaking hands holding thick cash envelope, red fuel warning light pulsing on dashboard, engine stuttering and catching, controlled bitter smile forming, grey-blue eyes reflecting red warning light",
        negative_prompt=GLOBAL_NEGATIVE + ", readable text, numbers on dashboard",
    ))

    shots.append(Shot(
        shot_id="E01_SH015",
        scene="SC07_RAIN",
        title="Wallet in Rain",
        duration_target_seconds=3,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH015_input.png",
        characters=[],
        environment="wet pavement, rain",
        camera="locked close-up on ground",
        primary_action="Wallet falls from coat onto wet pavement",
        secondary_motion=["wallet falling and landing", "water splash on impact", "car drives away in background", "rain continuing on leather"],
        lighting="streetlight above, rain reflections",
        colour_script="Dark wet surface + warm streetlight reflection",
        positive_prompt="Locked close-up on wet pavement, leather wallet falling from above and landing with small water splash, car tail-lights driving away in soft background blur, rain continuing to fall on wallet surface, wet asphalt reflections of streetlight",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH016",
        scene="SC07_RAIN",
        title="Service Station Mentor",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH016_input.png",
        characters=["ren", "mentor"],
        environment="service station, dead fluorescents, rain",
        camera="medium two-shot, stable",
        primary_action="Ren meets the Christian mentor beneath dead lights",
        secondary_motion=["rain curtain in background", "mentor extends hand holding wallet", "Ren approaches cautiously", "small eye movements between them"],
        lighting="broken fluorescent tube flicker + rain ambient",
        colour_script="Dead fluorescent + rain reflections as only warmth",
        positive_prompt="Two men meeting at empty service station in rain, older man in simple clothes extending hand holding leather wallet, younger man in dark coat approaching cautiously, dead fluorescent tube overhead flickering, rain curtain visible behind them, careful eye contact, no large mouth movements, grounded human interaction",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH017",
        scene="SC07_RAIN",
        title="Prayer",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH017_input.png",
        characters=["ren", "mentor"],
        environment="service station",
        camera="medium close, stable",
        primary_action="Mentor places hand on Ren's shoulder",
        secondary_motion=["Ren grabs mentor's wrist reflexively", "fluorescent lights flicker", "rain briefly appears unnaturally precise/still", "faces remain stable and readable"],
        lighting="flickering fluorescent + rain light",
        colour_script="Cold white flicker + momentary stillness",
        positive_prompt="Older man placing gentle hand on younger man's shoulder, younger man reflexively grabbing the wrist, fluorescent lights flickering overhead, rain in background briefly appearing unnaturally still for one moment, faces remaining stable and readable, quiet profound moment, service station at night",
        negative_prompt=GLOBAL_NEGATIVE + ", magic, glow, energy effects",
    ))

    shots.append(Shot(
        shot_id="E01_SH018",
        scene="SC08_REINA",
        title="Reina Call",
        duration_target_seconds=3,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH018_input.png",
        characters=["reina"],
        environment="Reina's private room, cracked mirror",
        camera="restrained camera push toward mirror",
        primary_action="Reina speaks by phone before a cracked mirror",
        secondary_motion=["subtle smug expression", "cracked mirror reflecting her face", "red-stone ring catching light", "restrained slow camera push"],
        lighting="warm controlled interior — wine, cream, gold tones",
        colour_script="Warm wine-cream-gold interior, mirror cold",
        positive_prompt="Elegant dangerous woman speaking on phone before cracked mirror, subtle smug expression, dark plum clothing, red-stone ring on finger catching warm light, cracked mirror reflecting her face with distortion, restrained slow camera push toward reflection, warm interior lighting in wine cream and gold tones, stillness as power",
        negative_prompt=GLOBAL_NEGATIVE + ", halloween witch, theatrical costume",
    ))

    shots.append(Shot(
        shot_id="E01_SH019",
        scene="SC09_PRISON",
        title="Prison Prayer",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH019_input.png",
        characters=["daisuke"],
        environment="prison chapel",
        camera="low angle, minimal movement",
        primary_action="Daisuke kneels beside his Bible in prayer",
        secondary_motion=["quiet breathing", "hands tightening on Bible", "fluorescent light flicker", "minimal camera movement"],
        lighting="institutional cold + single warm light (candle/lamp)",
        colour_script="Cold institutional blue-white, one warm spot",
        positive_prompt="Weathered older man kneeling in prayer beside worn Bible in sparse prison chapel, quiet breathing visible, hands tightening around book, single fluorescent light flickering overhead, institutional cold light with one warm spot from small lamp, scars visible on knuckles, humbled powerful frame, minimal camera movement",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    shots.append(Shot(
        shot_id="E01_SH020",
        scene="SC09_PRISON",
        title="Post-Credit Visitor",
        duration_target_seconds=4,
        generation_mode="image_to_video",
        input_image="wan/input_frames/E01_SH020_input.png",
        characters=["daisuke"],
        environment="prison chapel",
        camera="hold on expression, stable",
        primary_action="Daisuke learns his wife has arrived",
        secondary_motion=["prison guard entering frame from side", "Daisuke slowly looking up from prayer", "chapel light flickering once", "held expression — complex emotion"],
        lighting="same chapel lighting, guard silhouette",
        colour_script="Institutional cold + guard shadow",
        positive_prompt="Prison chapel, kneeling older man slowly looking up as uniformed guard enters frame from side, chapel fluorescent light flickering once, complex emotion crossing weathered scarred face, held stable expression, quiet moment of revelation, minimal movement, institutional cold lighting",
        negative_prompt=GLOBAL_NEGATIVE,
    ))

    return shots


def main():
    print("Building Episode 01 shot manifest...")
    shots = build_episode_01_shots()
    save_shot_manifest(shots, "episode_01")
    save_shot_manifest_csv(shots, "episode_01")
    save_shot_manifest_md(shots, "episode_01")
    print(f"Created manifest with {len(shots)} shots")
    print("  JSON: wan/manifests/episode_01_shots.json")
    print("  CSV:  wan/manifests/episode_01_shots.csv")
    print("  MD:   wan/manifests/episode_01_shots.md")


if __name__ == "__main__":
    main()
