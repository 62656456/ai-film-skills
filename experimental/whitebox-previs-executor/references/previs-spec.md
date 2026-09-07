# Previs Spec v0.1

该合同只在启动白模预演时生成。它是已确定分镜到渲染器的中间层，不是用户正式分镜或视频提示词。

## 坐标与时间

- 右手坐标：`X` 向右，`Y` 向场景深处，`Z` 向上；地面为 `Z=0`。
- 位置和尺寸以米为单位。
- 时间以秒为单位，转换为帧时使用顶层 `fps`。
- 镜头必须从 `0` 开始连续覆盖，不允许重叠和空档。

## 最小顶层结构

```json
{
  "schema_version": "0.1",
  "title": "sequence title",
  "fps": 24,
  "resolution": [960, 540],
  "compile_notes": [],
  "world": {},
  "actors": [],
  "shots": []
}
```

## 场景

```json
"world": {
  "floor": {"size": [14, 12], "grid": 1},
  "walls": [
    {"id": "back", "center": [0, 5, 1.5], "size": [10, 0.2, 3]}
  ],
  "props": [
    {"id": "table", "type": "box", "center": [0, 1, 0.45], "size": [2, 1, 0.9]}
  ]
}
```

`walls` 和 `props` 第一版都使用轴对齐长方体。场景不需要材质和纹理。

## 人物

```json
{
  "id": "A",
  "label": "A",
  "height": 1.75,
  "tone": 0.92,
  "keyframes": [
    {"time": 0, "position": [-2, 1, 0], "facing": 0, "action": "idle"},
    {"time": 3, "position": [0, 2, 0], "facing": 20, "action": "walk"}
  ]
}
```

- `facing` 为角度，`0`° 面向 `+Y`，`90`° 面向 `+X`。
- 基础动作支持 `idle`、`walk`、`run`、`turn`、`sit`、`reach`。打戏压力测试增加 `dash`、`guard`、`slash`、`slash_hold`、`block`、`thrust` 和 `recoil`，都只是调度级白模近似。`slash_hold` 用于碰撞停帧期间保持劈砍终点姿态。
- 位移精确按关键帧插值；手脚摆动只用于显示步态，不属于表演验收。
- 可选 `weapon` 只生成白模长刃代理：`{"type":"sword","length":3.6}`。它用于显示攻击方向和接触点，不代表正式道具设计。
- `rig` 默认为 `humanoid`。非人形双臂悬浮代理使用 `two-arm-hover`，只绘制中央主体、头部与两条触地臂爪，不得生成骨盆、下半身或后腿。
- 实体重槌代理使用 `{"type":"hammer","length":12,"head_size":[4,2,2]}`。

## 接触效果

可选顶层 `effects` 用于标记格挡、碰撞等关键接触帧：

```json
"effects": [
  {"type": "impact", "time": 6.4, "duration": 0.25, "position": [0, 1, 3], "radius": 1.2}
]
```

它只是时间与空间标记，不是正式特效。

## 线缆和索刃路径

可选顶层 `tethers` 使白模视频保留线缆来源、目标和激活时段：

```json
"tethers": [
  {
    "id": "enemy-cable",
    "start": 10.3,
    "end": 23.6,
    "from": {"actor": "B", "offset": [0, -2, 8]},
    "to": {"actor": "A", "offset": [0, 0, 8]},
    "tone": 0.78
  },
  {
    "id": "hero-anchor",
    "start": 23.6,
    "end": 30,
    "from": {"actor": "A", "offset": [0, -1, 10]},
    "to": {"world": [0, -25, 8]},
    "tone": 0.95
  }
]
```

线缆是连续性和受力路径标记，不做柔体物理验收。

## 镜头

```json
{
  "id": "S01",
  "label": "WIDE DOLLY",
  "start": 0,
  "end": 3,
  "camera_keyframes": [
    {
      "time": 0,
      "position": [0, -7, 2.2],
      "look_at": [0, 1, 1.1],
      "lens_mm": 28,
      "easing": "smooth"
    },
    {
      "time": 3,
      "position": [0, -5.5, 2],
      "look_at": [0, 1.5, 1.1],
      "lens_mm": 35,
      "easing": "smooth"
    }
  ]
}
```

- 摄影机关键帧的 `time` 使用全局时间，必须落在镜头起止范围内。
- `position` 是摄影机中心，`look_at` 是当前焦点/朝向目标。
- `lens_mm` 默认按 36mm 宽全画幅换算水平视角。
- `easing` 支持 `linear` 和 `smooth`。
- 多个关键帧可表达推进、后撤、横移、升降、弧线近似、跟随和焦段变化。

## 编译约定

- 景别不只写标签：必须通过摄影机距离、高度、`look_at` 和 `lens_mm` 实际构成。
- “缓慢”默认使用 `smooth`；“匀速”使用 `linear`；不得用变焦暗中代替机位移动。
- 同一世界中的人物和场景不因切镜移动；只切换摄影机。
- 含糊词必须记入 `compile_notes`。若两种解释会改变镜头职责，停止该镜头并请用户裁定。
