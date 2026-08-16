# 短剧可控性合同

仅在对应任务需要时加载本文件。合同可直接写进 `shots.json` 或工作单；字段缺失即标记 `pending`。

## 1. narrative_beat_contract

~~~json
{"scene_id":"E01S01","source_form":"script|outline|sketch|oral","assumptions":[],"director_analysis_ref":"","visual_concept_ref":"","hook":"","information_gap":"","actors":[{"asset_id":"C01","want":"","obstacle":"","strategy_shift":"","in_state":"","out_state":""}],"power_turn":"","audience_emotion_curve":[],"cost":"","cliffhanger":"","evidence_shots":[]}
~~~

## 2. asset_registry_entry

~~~json
{"asset_id":"C01","version":"v1.0","status":"approved","reference_images":[],"locked_features":[],"state_variants":[],"used_by_shots":[],"last_reviewed":"YYYY-MM-DD"}
~~~

## 3. blocking_map

~~~json
{"blocking_map_id":"BM_E01S01_003","orientation":"screen-left-to-right","space_anchors":{"left":"","mid":"","right":"","foreground":"","background":""},"power_geometry":{"start":"","turn":"","end":""},"axis":{"a":"","b":"","camera_side":""},"beats":[{"id":"T0","actors":[{"asset_id":"C01","position":"left-mid","depth":"mid","facing":"right","eyeline":"C02","entry_exit":"","occlusion":""}],"props":[{"asset_id":"P01","holder":"C01","facing":"","position":""}],"camera":{"position":"","heading":"","lens":"","shot_size":""}},{"id":"T1","changes":[]},{"id":"T2","changes":[]}]}
~~~

## 4. lighting_plan

~~~json
{"lighting_plan_id":"LP_E01S01_003","narrative_purpose":"","key":{"source":"","direction":"","kelvin":0,"target":""},"fill":{"source":"","ratio":"","target":""},"rim_or_background":{"source":"","direction":"","target":""},"darkness_purpose":"","continuity":{"T0":"","T2":""},"bans":["no unmotivated glow","no unreadable key action"]}
~~~

## 5. action_ledger

~~~json
{"action_ledger_id":"AL_E01S01_003","feasibility":{"causal_beats":1,"actor_count":2,"camera_motion":"","decision":"keep|split|offscreen"},"beats":[{"id":"A1","seconds":"0-1.2","initiator":"C01","start":"","path":"","end":"","contact_or_miss":"","reaction":"","screen_direction":"","camera_relation":"","bans":[]}],"tail_frame":""}
~~~

## 6. sketch_to_shot_brief

~~~json
{"sketch_id":"SK01","inherits":{"composition":"","horizon":"","camera_angle":"","subject_scale":"","eyeline":"","key_direction":""},"must_resolve_from_assets":["identity","wardrobe","materials"],"must_resolve_from_style":["palette","texture","lens"],"do_not_inherit":["unapproved face","placeholder text","ambiguous hand detail"]}
~~~

## 7. QC 对照顺序

1. 核对 Cxx/Sxx/Pxx 与批准版本；再核对 T0、T1、T2 调度。
2. 核对光源方向、色温与暗部目的；再核对镜头和轴线。
3. 对动作逐拍核对发力、路径、接触/落空和反应；最后核对尾帧。
4. 若草图参与，核对只继承允许字段，且没有替代资产合同。
