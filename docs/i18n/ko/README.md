<div align="center">

<img src="../../assets/hero.svg" width="100%" alt="Open Film Skills — AI 영화 제작을 위한 스토리, 디자인, 쇼트, 제작 지능" />

# Open Film Skills

**Codex, Claude Code, TRAE, CodeBuddy, WorkBuddy 및 기타 Agent에서 재사용할 수 있는 모듈형 연출 지능.**

[English](../../../README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · **한국어**

</div>

## GitHub에서 읽기

19개 모듈에는 목적, 설계 원칙, 입력, 워크플로, 되돌림, 리뷰 게이트, 통과 기준, 출력, 경계, Agent 요구사항을 설명하는 개별 페이지가 있습니다. 현재 38개 상세 페이지는 **English와 简体中文으로만** 제공됩니다. 이 한국어 페이지는 저장소 개요이며, 19개 상세 페이지가 한국어로 번역되었다고 주장하지 않습니다.

- [English / 简体中文 전체 모듈 색인](../../skills/INDEX.md)
- [공통 되돌림·리뷰·통과 로직](../../SKILL_DESIGN_SYSTEM.md)
- [19개 모듈, 런타임 `SKILL.md`, ZIP 비교](../../../SKILL_CATALOG.md)

## 목적에 따라 선택하기

| 목적 | 설계 가이드 | 런타임 | ZIP |
|---|---|---|---|
| 시나리오 작성·수정, 인물 인과관계, 자연스러운 대사 | [`director-agent` (English)](../../skills/en/director-agent.md) | [`SKILL.md`](../../../skills/director-agent/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/director-agent.zip) |
| 승인된 시나리오를 쇼트와 생성 프롬프트로 설계 | [`ai-storyboard-director` (English)](../../skills/en/ai-storyboard-director.md) | [`SKILL.md`](../../../skills/ai-storyboard-director/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-storyboard-director.zip) |
| 캐릭터·장면·소품 참조 자산 정의 | [Asset guides (English)](../../../SKILL_CATALOG.md#asset-definition) | [Runtime index](../../skills/INDEX.md) | [Latest release](https://github.com/62656456/ai-film-skills/releases/latest) |
| 승인된 소재를 AI 영상으로 제작 | [`produce-ai-video` (English)](../../skills/en/produce-ai-video.md) | [`SKILL.md`](../../../skills/produce-ai-video/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/produce-ai-video.zip) |
| 웹 인터페이스 설계·구현·검토 | [`web-design-director` (English)](../../skills/en/web-design-director.md) | [`SKILL.md`](../../../skills/web-design-director/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/web-design-director.zip) |

이 저장소는 이야기의 인과관계, 인물의 목적, 블로킹, 공간 연속성, 물리적 동작, 조명, 재질, 제작 게이트를 재사용 가능한 실행 계약으로 바꿉니다. 유행어를 쌓은 프롬프트 모음이 아닙니다.

각 모듈은 자신이 명시한 결과 범위 안에서 독립적으로 사용할 수 있습니다. 하지만 스타일 모듈이 시나리오까지 작성하거나, 이미지 도구 없이 자산 이미지가 이미 생성되거나, 제작 모듈이 비용·권리·게시 권한을 우회할 수 있다는 뜻은 아닙니다.

## 설치

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
python scripts/install_skill.py ai-storyboard-director --platform claude-code
```

동일한 자체 완결형 폴더를 Codex, Claude Code, TRAE, CodeBuddy에 설치할 수 있고 WorkBuddy에서는 ZIP으로 업로드할 수 있습니다. 다른 Agent에서는 `SKILL.md`와 로컬 리소스를 지침으로 가져올 수 있습니다. 지침을 읽을 수 있는 것과 호스트가 Skill을 네이티브로 검색·실행하는 것은 같지 않습니다. 자세한 내용은 [Compatibility](../../COMPATIBILITY.md)와 [Installation](../../INSTALLATION.md)을 참조하세요. `experimental/`은 기본 전체 패키지에 포함되지 않습니다.

표현 구조는 [OmniRoute](https://github.com/diegosouzapw/OmniRoute)의 명확한 탐색, 다국어 진입점, 다이어그램, 빠른 시작, 상태 표시를 참고했지만 브랜드, 이미지, 문구, 코드는 복제하지 않았습니다.

연락처: [haldissita@gmail.com](mailto:haldissita@gmail.com)

## 라이선스

별도 표기가 없다면 개인 창작 부분은 [Apache License 2.0](../../../LICENSE)을 따릅니다.
