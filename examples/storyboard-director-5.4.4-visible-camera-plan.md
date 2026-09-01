# Storyboard Director 5.4.4: visible camera-plan example

This public example demonstrates one text behavior: every segment heading exposes the actual camera plan instead of using a story-only label. It does not claim that a video model reproduced the plan or that a user approved the resulting imagery.

## Request

Design an eight-second, 16:9 realistic watch-repair scene. A middle-aged watchmaker lifts a small brass gear with tweezers, the gear slips, her other hand catches it, and she reinstalls it so the movement resumes. Do not add another character, dialogue, background music, or fantasy effects.

The three shots must demonstrate:

1. a 75mm macro view with a high angle, lateral move, and focus handoff;
2. a locked camera and locked focus stated explicitly;
3. compound camera motion and staged speed changes stated explicitly.

## Why the old heading is insufficient

```text
[2.20–4.50s | The gear slips]
```

The event is named, but a human still cannot see the lens, camera position, movement, focus behavior, or physical endpoint.

## 5.4.4 segment headings

```text
[0.00–2.20s | 75mm macro close-up | southwest above the bench, 25° high angle | left-to-right slide 30cm with a slight tilt down | ease in -> constant speed -> soft stop | focus: gear teeth -> tweezer tips -> movement pivot | align the gear with the pivot]

[2.20–4.50s | 50mm hand close-up | southeast of the bench, 15° high angle | locked camera, facing northwest | completely still | focus locked to the gear's fall path; the receiving palm enters the same focal plane | falling gear makes physical contact with the hand]

[4.50–8.00s | 35mm medium close-up | southwest of the watchmaker, starting 10° low | follow the hand forward 20cm -> arc clockwise around the movement 30cm -> rise to eye level | ease in -> accelerate when the movement starts -> soft stop at eye level | focus: gear -> balance wheel -> watchmaker's eyes | movement resumes; the watchmaker exhales]
```

## Continuity and physics carried by the full prompt

- The watchmaker remains south of the bench and faces north.
- The movement remains in front of her; the tool box remains west; the practical lamp remains northeast.
- The gear follows one causal chain: tweezers hold it → it slips → gravity pulls it down → the palm contacts it → fingers close → tweezers lift it again → it enters the pivot → the movement resumes.
- The gear cannot float, teleport, reset itself, pass through the hand, or drive the movement without contact.
- No extra fingers, characters, mirrored workbench, unsupported light, captions, logos, watermark, or music.

## Recorded validation

| Check | Recorded result |
|---|---|
| Visible segment headings | 3/3 |
| Required heading fields | 7/7 in every heading |
| Timeline | 0.00–8.00s, no gap or overlap |
| Locked camera and focus | Explicit |
| Compound path and speed | Explicit |
| Unresolved placeholders | 0 |
| Internal asset codes in user-visible text | 0 |

Status: **internal text-behavior validation passed; video-model execution and user visual acceptance were not run.**

Try the Skill with the prompts in [quick-start-prompts.md](quick-start-prompts.md), or read the exact [runtime contract](../skills/ai-storyboard-director/SKILL.md).
