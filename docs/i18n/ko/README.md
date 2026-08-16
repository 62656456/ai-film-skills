<div align="center">

<img src="../../assets/hero.svg" width="100%" alt="Open Film Skills — AI 영화 제작을 위한 스토리, 디자인, 쇼트, 제작 지능" />

# Open Film Skills

**AI 네이티브 영화 제작을 위한 재사용 가능한 연출 지능.**

[English](../../../README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · **한국어**

</div>

## 목적에 따라 선택하기

| 목적 | Skill |
|---|---|
| 시나리오 작성·수정, 인물 인과관계, 자연스러운 대사 | [`director-agent`](../../../skills/director-agent/) |
| 승인된 시나리오를 쇼트와 생성 프롬프트로 설계 | [`ai-storyboard-director`](../../../skills/ai-storyboard-director/) |
| 캐릭터·장면·소품 참조 자산 정의 | [`character-asset`](../../../skills/character-asset/) · [`scene-asset`](../../../skills/scene-asset/) · [`prop-asset`](../../../skills/prop-asset/) |
| 승인된 소재를 AI 영상으로 제작 | [`produce-ai-video`](../../../skills/produce-ai-video/) |
| 웹 인터페이스 설계·구현·검토 | [`web-design-director`](../../../skills/web-design-director/) |

이 저장소는 이야기의 인과관계, 인물의 목적, 블로킹, 공간 연속성, 물리적 동작, 조명, 재질, 제작 게이트를 재사용 가능한 실행 계약으로 바꿉니다. 유행어를 쌓은 프롬프트 모음이 아닙니다.

## 설치

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

`experimental/`은 기본 설치에 포함되지 않습니다. 자세한 상태는 [Skill catalog](../../../SKILL_CATALOG.md)를 확인하세요.

표현 구조는 [OmniRoute](https://github.com/diegosouzapw/OmniRoute)의 명확한 탐색, 다국어 진입점, 다이어그램, 빠른 시작, 상태 표시를 참고했지만 브랜드, 이미지, 문구, 코드는 복제하지 않았습니다.

## 라이선스

별도 표기가 없다면 개인 창작 부분은 [Apache License 2.0](../../../LICENSE)을 따릅니다.
