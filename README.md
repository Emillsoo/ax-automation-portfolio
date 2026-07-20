# AX Automation Portfolio

의료기관의 현업 업무와 시스템 환경을 이해하고, n8n·자동화 스크립트·RPA·Java API로 실제 업무를 개선해 온 프로젝트 포트폴리오입니다.

## Positioning

> 의료업무의 규칙을 분석해 자동화와 내부 API로 구현하고, 배포·모니터링·장애 대응까지 연결하는 AX 엔지니어

## Complete Work Catalog

대표 사례뿐 아니라 개발·설계·운영·개선활동을 포함한 **전체 38개
작업물**을 [전체 작업물 카탈로그](docs/ALL_WORKS.md)에 정리했습니다.
각 항목에는 진행 상태, 담당 범위, 구성, 핵심 알고리즘과 공개
재구현 소스가 연결되어 있습니다.

## Featured Projects

### 지출결의서 RPA 자동화

- [핵심 공개용 소스](examples/expense-rpa/task_manager.py)
- 외부 기반의 최소 골격 위에 핵심 자동화 기능 직접 구현
- Flask API, 작업 상태, Robot Framework, iframe·팝업 제어
- 타임아웃·취소·실패 증거와 운영 가시성 설계

### 재원환자 자격 불일치 알림

- [핵심 공개용 소스](examples/eligibility-workflow/double_filter.js)
- EMR 화면의 업무 규칙을 SQL과 n8n으로 재현
- 최신 결과·기관 범위·시간대·0건 처리 안정화
- 업무 시트와 담당자 알림 연계

### 입퇴원요약 AI 초안 자동작성

- [핵심 공개용 소스](examples/document-draft-review/review_gate.py)
- 긴 의료기록의 분할 조회·병합
- 항목별 LLM 초안과 동기화 게이트
- EMR 임시저장, 감사로그, 의료진 검토 단계

### DUR·개인투약이력 내부 API

- [핵심 공개용 소스](examples/internal-api/MedicationHistoryFacade.java)
- Java·iBatis 기반 레거시 EMR 컴포넌트 직접 개발
- 화면 내부 기능을 자동화와 타 시스템이 재사용할 수 있도록 확장
- 설정·매퍼·실호출 검증을 포함한 배포 절차

### 안전한 금전 업무 자동화

- [핵심 공개용 소스](examples/safe-payment-guard/safety_guard.py)
- 대상 이중 필터
- 조건 불일치 시 전체 중단
- 처리 후 실제 데이터 재조회
- 실행 흐름과 모니터링 분리

### 폐쇄망 배치 서버 이관

- [핵심 공개용 소스](examples/batch-retry/retry_client.py)
- 32비트 COM과 오프라인 패키지 대응
- 방화벽·DNS·프록시 단계별 진단
- 승인된 내부 API로 데이터 경로 전환

## Documents

- [전체 38개 작업물 카탈로그](docs/ALL_WORKS.md)
- [전체 프로젝트 사례](docs/PROJECTS.md)
- [경력기술서](docs/CAREER.md)
- [자기소개](docs/ABOUT.md)
- [제출용 PDF](AX_Automation_Portfolio.pdf)
- [프로젝트별 핵심 공개용 소스](examples/README.md)

## Public Demo

실무 코드와 데이터는 공개하지 않습니다. 가상 API와 완전 생성 데이터로 안전 설계 원칙을 재구현한 데모는 아래 저장소에서 확인할 수 있습니다.

- [Mock Clinic n8n Automation](https://github.com/Emillsoo/mock-clinic-n8n-automation)

## Security

- 실제 환자·직원·기관 데이터 없음
- 실제 EMR·DB·API 주소와 테이블 구조 없음
- 실무 n8n export와 credential 없음
- 정량 성과는 검증된 근거 없이 사용하지 않음
- 모든 시스템·협력업체 식별정보 일반화

## Contact

- Email: `dntjqdlaks@gmail.com`
- GitHub: https://github.com/Emillsoo
- Notion: https://app.notion.com/p/Notion-2a151a3de62d809c8934d99c48e90f5d
