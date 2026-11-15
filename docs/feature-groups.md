# 五组安装选项 / Five feature groups

| 构建选项 | 安装内容 | 相机中的主要入口 |
|---|---|---|
| `framing` | 3:2 开放门、N-RAW 四档画质、反挤压显示 | 画面尺寸／帧频、N-RAW 画质、反挤压 |
| `video-quality` | ProRes 四档与 HQ 星标、H.265 五档码率及对应星标 | ProRes 画质、H.265 画质 |
| `log-colour` | N-Log、S-Log3、Log3G10 选择及相关显示／标签 | Log 设定 |
| `photo-tools` | C15/C30 RAW 预拍、像素偏移合成 | 普通画质、RAW 记录、像素变化合成 |
| `video-orientation` | 记录视频方向：开录锁存竖拍／倒置姿态，把旋转元数据写入录像容器 | 视频拍摄菜单的“记录视频方向”行 |

每组可以独立从原厂 C 3.11 构建，也可一次选择多组，共 31 种非空组合。N-RAW 画质与开放门共同使用码率及剩余时间逻辑，保留在同一组。反挤压可在菜单关闭；RAW 预拍与像素偏移使用各自入口。自定义快门声不属于构建组，由 `shutter_sound.py` 叠加在任意非空组合或仅打版本戳的原厂基底上，见[自定义快门声指南](custom-shutter-sound.md)。

构建选项决定安装哪些功能，机内菜单决定每项功能如何使用。先选择所需组，再从原厂包一次构建完整固件；不要向已经修改的固件继续叠加。

旧版选项 `prores / precapture / pixelshift / opengate-nraw` 仅用于对应的旧版源码。当前 CLI 会明确拒绝旧名称。复现旧包时使用该版本的源码或完整工具包。

## 第五组：记录视频方向

`video-orientation` 在视频拍摄菜单新增“记录视频方向”行：开启后相机在开录时锁存竖拍或 180° 倒置姿态，并把旋转元数据写入录像容器；横拍输出与原厂一致。该行按视频拍摄菜单库 A–D 保存，默认开。此组随本 fork 的 v0.4.1 发布，行为细节见[记录视频方向指南](video-orientation.md)。

功能指南：[开放门](opengate-nraw.md)、[反挤压](anamorphic.md)、[ProRes](prores.md)、[H.265](h265.md)、[Log](log-colour.md)、[RAW 预拍](raw-precapture.md)、[像素偏移](pixelshift.md)、[记录视频方向](video-orientation.md)。

## English

The five installation choices are `framing`, `video-quality`, `log-colour`, `photo-tools` and `video-orientation`. Each builds independently from the original C 3.11 image; multiple groups are composed in one build. There are 31 nonempty combinations. Open gate stays paired with N-RAW quality, while desqueeze can be disabled in the camera. Pre-capture and pixel-shift keep separate controls. The custom shutter sound is not a build group; `shutter_sound.py` stacks it on any nonempty combination or on a version-stamped stock base (see the [custom shutter sound guide](custom-shutter-sound.md)).

Build-time choices install features; camera settings select their behavior. Legacy option names belong to older source/toolkit versions and are rejected by the current CLI.

The fifth group, `video-orientation`, adds a Record video orientation row to the movie shooting menu. When On, the camera latches a portrait or 180-degree upside-down pose at recording start and writes rotation metadata into the recorded containers; landscape output matches stock. The row is saved per movie shooting bank A-D and defaults to On. This group ships in this fork's v0.4.1; see the [video-orientation guide](video-orientation.md) for details.
