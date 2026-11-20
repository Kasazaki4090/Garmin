# Known Bugs and Defects (BUGS.md)

> 缺陷、异常行为、回归与技术债追踪。格式源自 [`ProjectManagementTemplate/BUGS_TEMPLATE.md`](ProjectManagementTemplate/BUGS_TEMPLATE.md)。
> 严重度：`Critical` 崩溃/内存溢出/阻塞发布 · `Major` 核心功能不可用且无绕行 · `Minor` 边缘/外观/非阻塞性能。
> 待办类需求写 [`TODO.md`](TODO.md)，不要写在本文件。

---

## Bug Index

| Bug ID | 严重度 | 状态 | 摘要 | 发现分区 |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | 暂无记录 | — |

---

## 记录格式（复制使用）

```markdown
## BUG-00X: [标题]

### Summary
一句话描述症状。

### Severity
Critical / Major / Minor

### Environment
* 机型 / 屏幕：fenix7 (MIP 260x260) / fr965 (AMOLED 454x454) / 模拟器版本
* 工具链：Connect IQ SDK 版本、Monkey C 插件版本
* 短码：复现时使用的主题短码（如适用）

### Reproduction Steps
1. ...
2. Observed: 实际表现
3. Expected: 期望表现

### Root Cause Analysis
代码层面的原因（API 误用、内存/帧循环、色值量化误差等）。

### Resolution & Prevention
修复方式与新增的回归自测（模拟器用例 / 网页断言 / Python 校验）。

### Status
Open / Fixed (日期或 commit)
```
