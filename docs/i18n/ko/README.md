<div align="center">

# Open Film Skills

**아이디어와 시나리오에서 연출, 시각 자산, 쇼트, 프롬프트, 영상 제작과 실제 검수까지.**

[English](../../../README.md#english-overview) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · **한국어**

</div>

![전체 영상 제작 워크플로](../../assets/workflow-overview.svg)

[전체 노드·인계·Mermaid 원본](../../WORKFLOW.md) · [사용자가 수락한 14개 이미지](../../../README.md#本轮14张用户接受成图) · [모듈 목록](../../../SKILL_CATALOG.md)

## 현재 소스와 기존 릴리스

현재 소스는 **일반 18개＋실험 2개＝20개 모듈**이며, 상세 가이드는English와简体中文으로 총40개입니다. 이 한국어 페이지는 개요이며 20개 상세 가이드의 한국어 번역이 아닙니다.

- 현재Storyboard Director 소스는 **5.6**입니다. 명시된 작품 폴더에서 연출 의도, 선택한 쇼트와 장면 상태를 저장하고 복원합니다.
- 공개된 **v1.3.0**은 **5.4.4**를 포함한 과거 스냅샷입니다. 소스 변경으로 기존ZIP이 바뀌지는 않습니다.
- 별도 표시된5.6 단독Preview도 다른 배포물입니다. 이번 소스 갱신은 새 전체 패키지Release가 게시되었다는 뜻이 아닙니다.

[소스와ZIP 선택](../../INSTALLATION.md) · [40개 가이드](../../skills/INDEX.md)

## 필요한 결과로 선택

| 결과 | 모듈 |
|---|---|
| 시나리오·대사 수정과 연출 판단 | [director-agent](../../skills/en/director-agent.md) |
| 카메라, 쇼트, 완전한 생성 프롬프트 | [ai-storyboard-director](../../skills/en/ai-storyboard-director.md) |
| 인물·공간·소품 참조 | [자산 모듈](../../../SKILL_CATALOG.md#asset-definition) |
| 장르별 빛·색·구도·재질 | [8개 일반 장르](../../../SKILL_CATALOG.md#genre-visual-language)와[하드SF 실험](../../skills/en/hard-sci-fi-visual-director.md) |
| 기초3D 카메라·동선 프리뷰 | [whitebox-previs-executor](../../skills/en/whitebox-previs-executor.md), 실험 배포 |
| 실제 생성·편집·사운드·전체 재생 검수 | [produce-ai-video](../../skills/en/produce-ai-video.md) |

기존 결과가 있으면 해당 단계부터 계속합니다. 외부[xianxia-visual-director](https://github.com/liyue-aigc/xianxia-visual-director)는 선협 워크플로를 위한 링크이며, 확인된 재배포 허가가 없어 소스나ZIP에 넣지 않습니다. 저장소의 영상 모듈19개＋웹 보조1개에 외부 선협을 더하면 전체 흐름은 영상 역할20개＋웹 보조1개가 됩니다.

## 소스 설치

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
git log -1 --oneline
python scripts/install_skill.py ai-storyboard-director --platform codex
```

실제로 체크아웃한 버전을 확인하세요. 게시되지 않은 로컬 변경은 공개 기본 브랜치에 포함되지 않습니다. 실험 패키지는 명시적인`--experimental`선택이 필요합니다.[Installation](../../INSTALLATION.md)과[Compatibility](../../COMPATIBILITY.md)를 참고하세요.

## 실제 예시와 한계

14개 원본 생성 이미지는 사용자가 명시적으로 수락했습니다. 전체 화면 비율의 미리보기, 원본PNG와 출처·상태는[공개 매니페스트](../../showcase/manifest.json)에 기록됩니다. 이전 버전과 동일 프롬프트A/B 비교를 수행하지 않았으며, 보편적인 성공률이나 영상 품질을 보장하지 않습니다.

구도·빛·재질·색은 장면에 맞게 선택합니다. 황금 시간대, 얕은 심도, 네온은 필수가 아닙니다. 화이트박스 프리뷰는 구현된 대상과 개별 검증 동작에 한정되며 임의의 긴 전투를 보장하지 않습니다.5.6 상태 검사는 미적 판단을 대신하지 않습니다.

[설계·검수 원칙](../../SKILL_DESIGN_SYSTEM.md) · [공개 범위](../../../PUBLICATION_SCOPE.md) · [Apache License 2.0](../../../LICENSE) · [피드백](https://github.com/62656456/ai-film-skills/issues)
