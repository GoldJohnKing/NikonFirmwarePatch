# v0.4.1 验证范围 / Validation coverage

本版 v0.4.1（本 fork，基于上游 XinmiaoZhao v0.4.0）以用户自行取得的原厂 Z8 C 3.11 为输入。上游 v0.4.0 的源码、预编译单元和固件补丁与其 v0.4.0-rc.2 相同，曾对 15 种组合逐组合独立解封装，核对身份、补丁窗口、未改动字节、共享菜单和资源边界，并比对源码重编与预编译单元，四组功能的行为证据沿用。本 fork 新增第五组 `video-orientation` 与自定义快门声，非空组合增至 31 种，证据见下表。构建时选择的固件版本号用于区分文件；以下按功能组合说明证据。

| 项目 | 已验证的范围 |
|---|---|
| 五组构建 | 31 种非空组合的全部配方冻结并纳入核验范围；单选与“四视频组＋视频方向”产物经 `verify.py` 独立核验通过。全量 31 腿组合验证待完整工具包产出后执行（见[已知问题](known-issues.md)维护者事项） |
| 有界启动 | 每种组合从解密 MAIN 启动，使用模拟外设进入菜单，两次到固件版本页，停在更新入口。机身更新流程不在模拟范围内 |
| N-RAW 回放 | 使用上游 v0.4.0 的全选固件。Z8 机身回放旧录的 S-Log3 和新录的 Log3G10，详情页名称均正确，测试者确认开启辅助后的还原观感符合各自片段。屏摄记录了名称和 ASSIST 图标；面板色度没有仪器测量 |
| ProRes | 此前同一编码实现的全选固件在 SD 上记录 1 段 HQ、3 段 LT。四段 4K 29.97p、10-bit 4:2:2 全部解码到片尾 |
| RAW 预拍 | 同一照片实现的 FX／DX 样本中，选择“无损”实际记录 HE★。99 张预拍 NEF 全部解码，59 个配对 JPEG 与同次快门一致。直接选择 DX、C30、仅 RAW、HE★ 的组合仍待补测 |
| 像素位移 | 机内合成 4 张和 16 张两组，从非 0001 编号起拍。两份 NEFX 均完整解码；每份抽查 16,388 个位置，红、绿与源帧重建一致，蓝的差异仅位于 AF 校正行 |
| 共享设置与显示 | 先前的有界执行覆盖菜单分流、星标刷新、菜单库字段复制。机身试用反馈反挤压绿点正常。跨库切换、取电重开、取景器边缘及各回放页仍需分别观察 |
| 记录视频方向 | 含 `video-orientation` 的构建通过全量单元测试，`verify.py` 对单选与“四视频组＋视频方向”产物独立核验通过；非空组合增至 31 种，全部配方冻结（15 份无照片工具组合真实构建逐字节复验，16 份含照片工具组合经混合装配与结构审计冻结）。仿真通过：全系统引导零异常横幅、首开页武装默认状态且幂等、行值为原厂布尔开关样式并随库双向搬运。实机：菜单行为（保存、菜单库切换、断电回默认开、菜单重设）与已发布的 H.265 档位功能完全一致；相机录制的全部格式逐握持验证旋转标记正确（H.265 10-bit 与 8-bit MOV、H.264 8-bit MP4/MOV、N-RAW 及同录代理、ProRes RAW 10/12-bit 及代理），全部文件经 ffprobe 核验。该组随本 fork 的 v0.4.1 发布，详见[记录视频方向指南](video-orientation.md) |
| 自定义快门声 | 16 种选择全矩阵（任意非空功能组合＋快门声，或仅快门声）构建并独立核验通过；源码与预编译单元在 LLVM 19.1.7 下逐字节等价；7 项负控全部按预期拒绝；上游 27+13 项 ARM 回归通过。四组功能基底加自定义快门声的完整组合已实机验证通过，详见[自定义快门声指南](custom-shutter-sound.md)与[更新日志](../CHANGELOG.md) v0.4.1 小节 |

录像色彩与模型对照见[色彩报告](log-colour-report.md)。可选 F LUT 已做格点、插值和中性轴数值检查；剪辑软件及显示器的端到端输出另需校验。发布工具包在 Windows Python 3.12 和 3.13 上的实际运行状态见 [Host checks](https://github.com/GoldJohnKing/NikonFirmwarePatch/actions/workflows/host-checks.yml)。[机器摘要](validation-summary.json) · [历史像素位移修订](validation-v0.3.1.md) · [历史预拍修订](validation-v0.2.0.md)

## English

This release, v0.4.1 in this fork, builds on upstream XinmiaoZhao v0.4.0 and takes the user-supplied original Z8 C 3.11 as its input. The upstream source, compiled units and firmware patches match v0.4.0-rc.2; upstream independently decoded all 15 of its selections, checked identity, patch windows, preserved bytes and shared-resource boundaries, and compared source rebuilds with the precompiled units, so the four upstream groups' behavioural evidence carries over. This fork adds the fifth group `video-orientation` and the custom shutter sound, raising nonempty selections to 31. The original package is checked before building. Each bounded emulator run boots decrypted MAIN with synthetic peripherals, enters the firmware version page twice and stops at the update entry.

The upstream v0.4.0 all-feature firmware was tested on a Z8. A previously recorded S-Log3 N-RAW clip and a newly recorded Log3G10 clip showed the correct names in playback. The tester confirmed the expected assist rendering; the photographs document the label and ASSIST indicator. Display colour accuracy was not measured.

The fifth group `video-orientation` ships in this fork's v0.4.1. Its offline checks pass: the full unit suite, `verify.py` on the single-group and four-video-groups-plus-orientation outputs, and the frozen 31 combination recipes (15 rebuilt byte-exactly; the 16 photo-tools combinations via hybrid assembly with a structural audit; the full 31-leg validator run is pending, see the maintainer notes in [known issues](known-issues.md)). Emulation passes: full-system boot with zero exception banners, first-open arming with idempotence, the stock boolean value render and per-bank carrying across menu-bank switches. On the camera, the menu behaviour matches the shipped H.265 tier feature exactly, and every format the camera records is verified per grip (H.265 10-bit and 8-bit MOV, H.264 8-bit MP4/MOV, N-RAW with its simultaneous proxy, ProRes RAW 10/12-bit with proxies), with every file checked through ffprobe. See the [video-orientation guide](video-orientation.md).

The custom shutter sound passes the 16-selection offline matrix (any nonempty feature combination plus the sound, or the sound alone on a version-stamped stock base) with independent verification after every build, byte-exact source/prebuilt parity under LLVM 19.1.7, seven negative controls rejected as expected, and the upstream 27+13 ARM regressions. A four-group base plus the custom shutter sound passed complete on-camera verification. See the [custom shutter sound guide](custom-shutter-sound.md) and the v0.4.1 changelog section.

Earlier all-feature camera checks on the same recording and photo implementations covered four decoded ProRes HQ/LT recordings, 99 decoded pre-capture NEFs and 59 matching JPEGs, DX/FX lossless-to-HE★ fallback, and two fully decoded 4-/16-frame pixel-shift merges from non-default starting file numbers. The tester also reported normal lit AF points with desqueeze. Menu-bank/power-cycle transitions and individual playback icons, small-viewfinder or subject-detection geometries remain separate checks.

See the [colour measurements](log-colour-report.en.md), [known limitations](known-issues.md) and [Windows toolkit CI](https://github.com/GoldJohnKing/NikonFirmwarePatch/actions/workflows/host-checks.yml). Windows jobs build on Python 3.12 and 3.13 using the released ZIP and verify the full-selection output against the supplied reference digest.
