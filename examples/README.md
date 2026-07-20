# 공개용 핵심 소스 예제

이 폴더는 대표 프로젝트의 핵심 설계 판단을 보여주기 위해 **새로 작성한 재구현 예제**입니다.

- 실무 원본 코드를 복사하지 않았습니다.
- 실제 기관·EMR·그룹웨어·API·DB 구조를 사용하지 않습니다.
- 환자·직원·계좌·진료정보가 없습니다.
- 실제 URL·서버·자격증명·n8n credential이 없습니다.
- 그대로 운영환경에 배포하기 위한 코드가 아닙니다.

| 프로젝트 | 공개 예제 | 보여주는 핵심 |
|---|---|---|
| 지출결의서 RPA | `expense-rpa/task_manager.py` | 작업 상태·취소·타임아웃·실패 증거 |
| 자격 불일치 알림 | `eligibility-workflow/double_filter.js` | 화면 규칙 재검증·0건 종료·시간대 |
| 의료문서 AI 초안 | `document-draft-review/review_gate.py` | 초안·검토·승인 상태와 원문 근거 |
| EMR 내부 API | `internal-api/MedicationHistoryFacade.java` | 레거시 계층 재사용·입력/null 방어 |
| 금전 업무 자동화 | `safe-payment-guard/safety_guard.py` | 이중 필터·부분처리 전체 중단 |
| 배치 서버 이관 | `batch-retry/retry_client.py` | 제한 재시도·타임아웃·실패 분류 |

실행 가능한 통합 데모는 별도 저장소인 [`mock-clinic-n8n-automation`](https://github.com/Emillsoo/mock-clinic-n8n-automation)에 있습니다.

