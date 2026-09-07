# 任意提示词到3D预演｜编译合同

## 目标

把自然语言提示词中已经存在的镜头信息，编译成可重复执行的3D解释。视频展示的是该解释的镜头结果，不是对某个AI视频模型最终像素的预测。

## 输入

最小输入只有原始提示词：

```json
{"prompt": "中文视频提示词"}
```

可选传入 `requested_duration_s`、`fps`、`aspect_ratio`。输入可以是单镜、多镜、有或没有时间码，且不限制30秒。

## 切镜和时长规则

按以下优先级执行：

1. 明确镜号、时间码、硬切、切到或转场：按原文拆镜。
2. 只有连续动作：保持一个连续镜头，不因动作变多擅自切镜。
3. 只写总时长和明确镜头数：平均分配并标记固定默认。
4. 单镜无时长：默认4秒。
5. 多镜无时长：默认每镜3秒。
6. 切点对齐整帧，默认24fps、960×540、16:9。

“蒙太奇、多角度、快速切换”没有明确镜头数量时列为 `unresolved`，不能暗中编出一套分镜。

## 数值来源

每个补齐值记录以下来源之一：

- `explicit`：用户明确写出；
- `semantic_mapping`：从明确电影术语确定映射；
- `derived`：从其他明确值计算；
- `deterministic_default`：为了可执行而使用的固定默认；
- `unresolved`：不重新导演就无法确定。

默认值必须带 `prediction_claim: false`。

## 最小默认

- 未写摄影机运动：静止。
- “推进”无距离：前移初始机距15%。
- “横移”无距离：横移初始机距25%。
- “环绕”无角度：20°。
- “升高／下降”无距离：主体高度50%。
- “跟拍”：保持开始时相对偏移。
- 未写焦段：35mm；广角：24mm；长焦：85mm。
- 未写景别：中全景；低机位为主体高度25%，高机位为150%，普通机位为75%。
- 未写场景：地面网格、地平线和必要的前中后景参照。
- 未写人物动作：原地保持。
- 只写“打斗”但没有主体顺序、方向和接触时刻：双方对峙并标记调度未定义，不自动编武打。

## `previs-compiler/1.0` 最小结构

```json
{
  "schema_version": "previs-compiler/1.0",
  "meta": {
    "title": "title",
    "purpose": "camera_and_blocking_previs",
    "prediction_claim": false
  },
  "playback": {
    "fps": 24,
    "resolution": [960, 540],
    "aspect_ratio": "16:9",
    "duration_s": 4,
    "duration_origin": "deterministic_default"
  },
  "compile": {
    "status": "ready_with_defaults",
    "assumptions": [],
    "unresolved": [],
    "warnings": []
  },
  "scene": {
    "units": "meter",
    "geometry": []
  },
  "cast": [],
  "camera": {
    "sensor_width_mm": 36,
    "rigs": []
  },
  "timeline": {
    "shots": [],
    "cuts": []
  },
  "validation_targets": {
    "duration_tolerance_frames": 1,
    "require_decodable_mp4": true,
    "require_visible_camera_motion_when_requested": true
  }
}
```

场景几何首版支持 `grid_plane` 和 `box`；人形代理支持 `humanoid` 与 `humanoid_mecha`。摄影机关键帧必须包含全局 `time_s`、三维 `position`、`look_at`、`lens_mm` 和 `easing`。

## 忠实度口径

- 存在默认值时：称为“诊断预演”。
- 关键镜头信息全部明确且通过：可称为“忠实执行预演”。
- 有会改变镜头职责的 `unresolved`：可以输出诊断视频，但不得声称已忠实执行。

## 物理构图冲突门

编译前同时检查焦段、摄影机距离、主体高度、景别和提示词要求必须看见的环境参照。若这些条件无法同时满足，必须写入 `compile.warnings` 或 `compile.unresolved`，并把结果标为诊断预演。

例如，50mm、距2米高人物2.5米的正后方跟拍会形成非常紧的背部构图；若同一句又要求左右护栏和箱体产生明显视差，二者可能物理冲突。不得静默改变焦段、距离或机位来冒充忠实执行；可以输出原条件的诊断视频，让用户直接看到冲突，或在用户允许后生成一个明确标注的替代解释。

## 打斗提示词能力边界

“打斗”不是两个人物根节点相向移动。编译器只有在执行后端具备关节／骨骼动作、武器握持、共享接触点和受击姿势时，才能把进攻、格挡、碰撞、拖拽或蹬墙标记为可执行。

正式长打戏前必须先编译一个2—4秒单动作门，并让独立观看者不读提示词完成复述。以下情况直接失败：

- 武器在接触帧不位于攻击方向前方；
- 武器和防守肢体没有实际相遇，只靠碰撞球提示；
- 人物部件围绕自身中心旋转，无法形成关节动作剪影；
- 接触前后只有根节点位移，没有重心、姿势和反作用变化；
- 独立观看者只能描述“方块靠近／穿插／分开”，不能描述具体攻防。

当前执行后端若只支持粗体块、基础走位和摄影机，应拒绝动作密集打斗，或明确输出失败诊断；不得因媒体可播放、时长正确或切镜完整而升级为打斗预演通过。

## `previs-action/1.0` 动作扩展

动作密集规格继续使用外层 `previs-compiler/1.0`，并增加 `meta.execution_backend=rigged_joint_solver_v1` 与 `action_program`。普通镜头规格不需要该扩展，也不受动作脚本限制。

```json
{
  "meta": {"execution_backend": "rigged_joint_solver_v1"},
  "action_program": {
    "schema_version": "previs-action/1.0",
    "backend": "baked_joint_ik",
    "profile": "implemented_action_profile",
    "contact_frame": 29,
    "hold_frames": 6,
    "constraints": {
      "weapon_grips": ["primary_hand", "secondary_hand"],
      "weapon_contact_socket": "weapon_impact_face",
      "defense_contact_sockets": ["defender_contact_a", "defender_contact_b"],
      "single_shared_contact": true,
      "no_root_only_fight": true
    },
    "beats": [
      {"id": "anticipation", "start_frame": 1, "end_frame": 12},
      {"id": "attack", "start_frame": 13, "end_frame": 28},
      {"id": "contact_hold", "start_frame": 29, "end_frame": 34},
      {"id": "recoil", "start_frame": 35, "end_frame": 67}
    ]
  }
}
```

动作节拍必须从第1帧连续覆盖到末帧；武器握点、接触参与方和共享接触不可省略。`scripts/validate_compiled_previs.py` 在 `require_attack_block_contact_recoil_readability=true` 时必须拒绝没有动作扩展的旧体块规格。

当前关节后端使用刚性机械部件、解析两段IK和逐帧烘焙，不要求软体蒙皮。人物手、武器、索线和接触面的最终位置必须按实际渲染几何复核。例如索线经过重采样后，验收应测手到最终圆柱线段的距离，而不是手到渲染前控制点的距离；缠绕还要同时存在柄前和柄后索段，并在可读机位中形成遮挡或视差。

已实现的动作 profile 只是可执行动作片段，不是“相似招式自动替代”许可。新提示词若包含未实现的武器、肢体结构、接触方式或连续动作，必须先新增相应执行片段并通过2—4秒动作门，才能扩成长段。
