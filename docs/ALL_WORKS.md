# 전체 작업물 카탈로그

이 문서는 대표 프로젝트만 추린 목록이 아니라, 로컬 근거가 확인된 개발·자동화·연동·운영·개선 작업을 가능한 한 빠짐없이 정리한 공개용 인벤토리다.

실제 회사 코드, 환자·직원 데이터, 내부 주소, 서버명, API 경로, 테이블·컬럼명, 자격증명은 공개하지 않는다. `examples/`의 코드는 실무 원본이 아니라 같은 문제 해결 원칙을 가상 데이터로 재구현한 것이다.

## 상태 표기

- 운영: 실제 운영 근거가 확인된 항목
- 운영·개선: 운영하면서 수정·안전성 개선을 이어가는 항목
- 완료·운영: 이관이나 구축을 완료하고 운영하는 항목
- 운영 전환 진행: 개발은 되었으나 운영 선행조건·통합 검증이 남은 항목
- 개발·검증: 코드와 산출물은 있으나 운영 완료를 확정하지 않은 항목
- 설계·대기: 요구사항·구성·알고리즘은 있으나 구현 또는 선행 연동을 기다리는 항목
- 운영 지원: 직접 제품 개발이 아니라 플랫폼·프로세스 운영 항목

---

## A. AX·업무자동화

### A01. 지출결의서 RPA 자동화

- 상태: 운영
- 역할: 외부 최소 화면 골격을 기반으로 핵심 기능 전체 직접 구현
- 기술: Python, Flask, Flask-SocketIO, Robot Framework, Selenium, Playwright
- 구성: 입력 변환 → 작업 API → 브라우저 자동화 → 실시간 상태 → 증적·취소
- 알고리즘: 사전 정의 명령만 실행하고 작업별 상태를 격리한다. 제한시간 초과·사용자 취소·비정상 종료를 서로 다른 상태로 기록한다.
- 핵심 소스: [`task_manager.py`](../examples/expense-rpa/task_manager.py)

### A02. 콜당직 착신전환 RPA

- 상태: 운영, Playwright 전환·개선
- 역할: 레거시 화면 탐색, 착신번호 조회·변경, 확인, 증적과 웹 실행 화면 직접 구현
- 기술: Robot Framework, Selenium, Python, Playwright
- 구성: 일정 입력 → 대상 검증 → 레거시 화면 조회 → 변경 → 재조회 검증 → 알림
- 알고리즘: 현재 상태를 먼저 읽고 목표 상태와 다를 때만 변경한다. 변경 뒤 같은 조회를 다시 수행해 일치할 때만 성공으로 판정한다.
- 핵심 소스: [`state_reconcile.py`](../examples/call-duty/state_reconcile.py)

### A03. 재원환자 자격 불일치 알림

- 상태: 운영·개선
- 역할: EMR 화면 규칙 분석, SQL, n8n, 예외처리와 모니터링 직접 구현
- 기술: n8n, Oracle, JavaScript, Sheets, Gmail
- 구성: 후보 조회 → 최신 결과 선택 → 입력·조회 이중 필터 → 중복 제거 → 알림
- 알고리즘: 서버가 선택한 행을 워크플로우가 다시 검증하며 대상 0건은 정상 종료한다.
- 핵심 소스: [`double_filter.js`](../examples/eligibility-workflow/double_filter.js)

### A04. 위수탁검사비 수납처리 자동화

- 상태: 운영·안전 재설계
- 역할: 전담 개발, 장애 원인 분석, 복구, 전체 중단 가드와 모니터링 구현
- 기술: n8n, 내부 API, JavaScript
- 구성: 수납 후보 조회 → 이중 필터 → 금액 대조 → 처리 → 실제 데이터 재조회
- 알고리즘: 한 행이라도 조건·금액이 다르면 전체 배치를 중단한다. API 응답과 실제 수납 결과를 별도로 검증한다.
- 핵심 소스: [`safety_guard.py`](../examples/safe-payment-guard/safety_guard.py)

### A05. 내시경 예약 재배정 자동화

- 상태: 운영·재설계
- 역할: 자동화 구현, silent failure 원인 분석, 조회·수정 정합성 검증 구현
- 기술: n8n, 내부 API, Oracle
- 구성: 예약 후보 조회 → 재배정 가능성 검증 → 처리 → 예약 상태 재조회 → 불일치 알림
- 알고리즘: HTTP 성공을 업무 성공으로 간주하지 않고 처리 직후 원본 상태가 목표 상태로 바뀌었는지 확인한다.
- 핵심 소스: [`post_write_verify.py`](../examples/endoscopy-reassignment/post_write_verify.py)

### A06. 건강증진팀 사전안내 SMS 자동발송

- 상태: 운영·장애 복구
- 역할: 자동발송, 1인 즉시발송, 수동 재발송, 공통 발송 흐름과 결과 모니터링 구현
- 기술: n8n, 내부 API, Python
- 구성: 대상 조회 → 메시지 조립 → 발송 요청 → 발송 실적 대조 → 재처리 분기
- 알고리즘: 화면상 성공이 아니라 발송 요청 ID와 실제 발송 실적을 대조한다. 재발송은 미발송으로 확정된 건만 허용한다.
- 핵심 소스: [`delivery_reconcile.py`](../examples/sms-delivery/delivery_reconcile.py)

### A07. 입퇴원요약 AI 초안 자동작성

- 상태: 운영·지속 개선
- 역할: 원문 조회, 분할·병합, 항목별 프롬프트, 적재, 감사, 알림과 검토 게이트 직접 구현
- 기술: n8n, LLM, Oracle, 내부 EMR API
- 구성: 원문 분할 조회 → 항목별 초안 → 병합 게이트 → 임시저장 → 의료진 검토
- 알고리즘: 근거가 없는 항목은 생성하지 않고 모든 병렬 분기가 완료된 뒤에만 저장 단계로 이동한다.
- 핵심 소스: [`review_gate.py`](../examples/document-draft-review/review_gate.py)

### A08. 전담간호팀 입원초진기록 AI 초안

- 상태: 개발·검증, 운영 이력 확인
- 역할: 양 기관 데이터 소스 분석, 기록 추출, 본문 결합, 완결도 관리와 삼각대조 검증 구현
- 기술: n8n, Oracle, JavaScript, LLM
- 구성: 기관별 기록 조회 → 서식·원문 정규화 → 본문 결합 → 초안 → 완결도 점검
- 알고리즘: 기관별 차이는 어댑터에서 흡수하고 공통 본문 모델로 변환한다. 원문·초안·화면 표시를 삼각대조한다.
- 핵심 소스: [`source_merge.py`](../examples/initial-record-draft/source_merge.py)

### A09. 당일입원 예정환자 병실 자동배정

- 상태: 로컬 워크플로우 산출물 확인, 현재 운영 상태 별도 확인 필요
- 역할: 입원 예정 대상과 병실 조건을 연결하는 자동화 워크플로우 구현
- 기술: n8n, Oracle, 내부 API
- 구성: 입원 예정 조회 → 병실 후보 조회 → 금지조건 제거 → 우선순위 배정 → 결과 검증
- 알고리즘: 병실 수용 조건을 모두 통과한 후보만 점수화하고 동점이면 결정 가능한 정렬키를 사용한다. 후보가 없으면 자동 배정하지 않는다.
- 핵심 소스: [`room_assignment.py`](../examples/room-assignment/room_assignment.py)

### A10. AI 회의 간사 프로토타입

- 상태: MVP 프로토타입
- 역할: 회의 유형, 참석·발언 순서, 발언 로그와 AI 요약 UI·서버 흐름 구현
- 기술: React, Node.js, LLM API
- 구성: 회의 설정 → 참석·순서 관리 → 발언 로그 → 요약 요청 → 결과 표시
- 알고리즘: 회의 원문을 발언자 단위로 구조화하고 결정사항·담당·기한 중심의 요약 입력으로 변환한다.
- 핵심 소스: [`meeting_summary_input.js`](../examples/meeting-facilitator/meeting_summary_input.js)

### A11. 전산개발 회의 자동화 시스템

- 상태: Phase 1 MVP
- 역할: 참석 체크, 보고 순서, 보고 입력, 간사 로테이션과 요약 구조 설계·구현
- 기술: FastAPI, SQLAlchemy, SQLite, Next.js, React
- 구성: 오늘 회의 생성 → 참석·보고 → 회의 상태 전이 → 요약 → 회의록
- 알고리즘: 회의 상태를 준비·진행·종료·요약완료로 제한하고 허용된 전이만 수행한다. 간사 후보는 제외 조건과 이력을 반영해 순환한다.
- 핵심 소스: [`meeting_state.py`](../examples/meeting-automation/meeting_state.py)

### A12. AI 프로젝트 일일보고 자동화

- 상태: 개발·로컬 운영 검토
- 역할: 열린 작업 조회, 로컬 작업기록 수집, 키워드 귀속, 보고서 생성, 중복방지와 재조회 검증 구현
- 기술: Python, 작업관리 API, 규칙 기반 요약, 선택적 LLM
- 구성: 열린 작업 조회 → 당일 기록 수집 → 작업별 매칭 → 보고 초안 → 미리보기 → 등록·재조회
- 알고리즘: 기본은 dry-run이며 강제 승인 없이는 외부 등록하지 않는다. 같은 날짜·작업의 기존 보고를 확인해 중복 등록을 막는다.
- 핵심 소스: [`report_matcher.py`](../examples/daily-report/report_matcher.py)

### A13. 새롬 본원 채용검진 수납 자동화

- 상태: 설계
- 역할: 월말 청구 생성과 입금 처리 흐름 분석, 스케줄 자동화 구상
- 기술: n8n, Excel/CSV, 업무 시스템 연동
- 구성: 대상 파일 입력 → 청구 후보 매칭 → 금액 대조 → 승인 대기 → 처리 결과 알림
- 알고리즘: 비정기·저빈도 업무이므로 자동 쓰기보다 사전 대조표와 승인 가능한 실행 계획을 먼저 만든다.
- 핵심 소스: [`reconciliation_plan.py`](../examples/sarom-reconciliation/reconciliation_plan.py)

### A14. 새롬 공단 입금 처리 자동화

- 상태: 부분 자동화 설계
- 역할: 포털 수작업과 내부 처리 단계를 분리하고 Excel 기반 매칭·입금 처리 구조 설계
- 기술: n8n, Excel/CSV, 업무 시스템 연동
- 구성: 지급내역 파일 → 청구·미수 후보 → 일대일 매칭 → 불일치 격리 → 승인 후 처리
- 알고리즘: 일대일로 확정되지 않은 행은 자동 처리하지 않고 예외 목록으로 분리한다.
- 핵심 소스: [`reconciliation_plan.py`](../examples/sarom-reconciliation/reconciliation_plan.py)

### A15. Robot Framework 자동화의 Playwright 전환

- 상태: 개발·검증
- 역할: 지출결의서·콜당직 자동화의 단일 워커, 진행상태, 타임아웃, 배포 런북 중심 재구성
- 기술: Python, Playwright, Flask/FastAPI
- 구성: 웹 요청 → 단일 작업 큐 → Playwright 실행 → 진행 이벤트 → 결과·증적
- 알고리즘: 브라우저 자동화는 한 워커만 실행하도록 잠그고 광역 프로세스 종료 대신 자신이 만든 프로세스만 정리한다.
- 핵심 소스: [`single_worker.py`](../examples/playwright-runtime/single_worker.py)

---

## B. EMR API·시스템 연동

### B01. DUR·개인투약이력 내부 API

- 상태: 운영
- 역할: EMR Java 컴포넌트, 서비스 연결, DAO·매퍼, 입력 검증과 배포 절차 직접 구현
- 기술: Java, iBatis, Oracle, 레거시 EMR 프레임워크
- 구성: 내부 요청 → 입력 검증 → 기존 판정 서비스 → 이력 조회 → 감사 → 표준 응답
- 핵심 소스: [`MedicationHistoryFacade.java`](../examples/internal-api/MedicationHistoryFacade.java)

### B02. 콜프로그램 연동 API

- 상태: 운영·연동 개선
- 역할: 다수 조회 API, 코드 매핑, 조회·수정 건수 정합성, 벤더 연동과 장애 대응
- 기술: Java, iBatis, REST/SOAP
- 구성: 벤더 요청 → 내부 API → 업무 서비스·조회 → 응답 표준화
- 알고리즘: 요청별 계약을 명시하고 조회 건수와 반환 건수를 대조한다. 외부 시스템의 성공 코드만으로 내부 결과를 확정하지 않는다.
- 핵심 소스: [`contract_guard.py`](../examples/vendor-api/contract_guard.py)

### B03. 케어메시지 연동 API

- 상태: 운영·지속 개선
- 역할: 여러 업무군 API, 상태 매핑, 단순 API 전환, 호출 검증과 운영 문서 구현
- 기술: Java, iBatis, REST/SOAP
- 구성: 업무군별 요청 → 공통 계약 검증 → 업무별 조회 어댑터 → 상태 매핑 → 응답
- 알고리즘: 내부 상태를 외부 계약 값으로 변환하는 매핑을 한곳에 모으고 미정의 값은 전송하지 않는다.
- 핵심 소스: [`contract_guard.py`](../examples/vendor-api/contract_guard.py)

### B04. 건진 검사장비 수치연동

- 상태: 운영 전환 진행
- 역할: 파일 감시 데몬, 장비별 파서, 제출 게이트웨이, GUI, 설치 패키지와 전환 체크리스트 구현
- 기술: Python, PowerShell, 내부 API, Windows
- 구성: 장비 파일·폴더 → 안정화 대기 → 형식 파싱 → 검사코드 매핑 → 내부 API → 재조회
- 알고리즘: 파일 크기·수정시간이 안정된 뒤 한 번만 처리하고 장비별 파서를 공통 레코드로 변환한다. 운영 모드는 사람이 명시적으로 전환한다.
- 핵심 소스: [`stable_file_parser.py`](../examples/device-integration/stable_file_parser.py)

### B05. 사내 OCR API 서비스

- 상태: 운영
- 역할: FastAPI 서비스, PaddleOCR 연동, 업로드 검증, 동시성 가드, Windows 서비스 배포와 모니터링 구현
- 기술: FastAPI, PaddleOCR, asyncio, nssm
- 구성: 이미지 업로드 → 형식·크기 검증 → 단일 추론 큐 → 텍스트 정규화 → 응답·로그
- 알고리즘: CPU 추론 동시성을 제한하고 허용된 확장자와 최대 크기만 처리한다.
- 핵심 소스: [`ocr_request_guard.py`](../examples/ocr-service/ocr_request_guard.py)

### B06. OCR 엔진 비교·검증 PoC

- 상태: 검증 완료
- 역할: 비교 기준 사전 정의, 동일 표본 반복 측정, CER·WER·응답시간·비용·보안 위험 비교
- 기술: Python, PaddleOCR, 외부 OCR 비교, 통계
- 구성: 합성·비식별 표본 → 엔진별 반복 실행 → 정규화 → CER/WER → 판정표
- 알고리즘: 결과를 보기 전에 합격 기준을 정하고 같은 표본과 같은 정규화 규칙을 적용한다.
- 핵심 소스: [`benchmark_metrics.py`](../examples/ocr-benchmark/benchmark_metrics.py)

### B07. NHIC 자격조회 배치와 서버 이관

- 상태: 완료·운영
- 역할: Java/SOAP 배치 분석, 32비트 COM·폐쇄망 환경 구성, 내부 API 전환과 재시도 운영
- 기술: Java, Python, SOAP, 32비트 COM, Windows Server
- 구성: 스케줄 → 자격조회 → 결과 변환 → 내부 반영 → 로그·재시도
- 알고리즘: 재시도 가능한 일시 오류만 제한 횟수로 다시 시도하고 업무 오류는 즉시 중단한다.
- 핵심 소스: [`retry_client.py`](../examples/batch-retry/retry_client.py)

### B08. 외래 간소화 배치·쪽지 장애 개선

- 상태: 개선 완료 근거 확인
- 역할: 두 배치의 원본 대비 기능 차이 분석, 쪽지 발송 경로 보완, SQL·Java 수정과 검증
- 기술: Java, iBatis, Oracle, 그룹웨어 메시지 연동
- 구성: 대기 대상 조회 → 상태 판정 → 안내 대상 생성 → 쪽지 전송 → 결과 검증
- 알고리즘: 기존 배치 동작을 기준선으로 두고 변경 전후 대상 집합과 발송 결과를 비교한다.
- 핵심 소스: [`notification_diff.py`](../examples/outpatient-simplification/notification_diff.py)

### B09. 진료실 재호출 메시지

- 상태: EMR 측 기능 반영, 전광판 재방송 통합 연동 진행
- 역할: 화면 상태전이 분석, 재호출 식별값, 메시지 컴포넌트와 벤더 연동 설계·구현
- 기술: Java, iBatis, 메시지 연동
- 구성: 재호출 요청 → 현재 상태 검증 → 재호출 버전 증가 → 메시지 → 전광판 폴링
- 알고리즘: 같은 대상도 재호출 버전이 증가하면 새 이벤트로 인식하며 중복 클릭은 멱등키로 차단한다.
- 핵심 소스: [`recall_version.py`](../examples/outpatient-recall/recall_version.py)

### B10. 외래 전광판 진료지연시간·공지 연동

- 상태: 개발·협력업체 통합 진행
- 역할: 실제 폴링 구조 분석, 병원·EMR·전광판 업체 역할 분리, 통합 요청과 테스트 계획 수립
- 기술: Java/.NET 연동, XML, 폴링 인터페이스
- 구성: EMR 대기정보 → 폴링 응답 → 전광판 어댑터 → 지연시간·공지·재호출 표시
- 알고리즘: 지연시간·공지의 유효시간을 검증하고 폴링 페이로드에 필요한 최소 필드만 추가한다.
- 핵심 소스: [`display_payload.py`](../examples/outpatient-display/display_payload.py)

### B11. VIP 진료·검사 일정 데일리 알림

- 상태: 착수 예정·요구정의
- 역할: 기존 메시지 인프라 재사용, VIP 판정과 담당자 매핑 블로커 식별, 단계별 개발 계획
- 기술: n8n, Oracle, 그룹웨어 메시지
- 구성: VIP 대상 → 일정 조회 → 담당자 매핑 → 중복 제거 → 데일리 알림
- 알고리즘: VIP 판정과 담당자 매핑이 모두 확정된 행만 발송 후보로 만든다.
- 핵심 소스: [`alert_candidate.py`](../examples/scheduled-alerts/alert_candidate.py)

### B12. 임상연구 대상 외래·응급실 방문 알림

- 상태: 착수 예정·선행 벤더 연동 대기
- 역할: 선행 데이터 동기화와 자체 트리거·알림 단계를 분리한 실행 계획 수립
- 기술: n8n, Oracle, 메시지 연동
- 구성: 대상 동기화 → 방문 이벤트 → 연구 대상 매칭 → 담당자 알림
- 알고리즘: 선행 동기화 완료 시각 이후의 이벤트만 처리하고 연구 대상·방문 이벤트가 모두 일치할 때만 알린다.
- 핵심 소스: [`alert_candidate.py`](../examples/scheduled-alerts/alert_candidate.py)

### B13. FRAX 골절위험 알림

- 상태: 설계·기준 합의 대기
- 역할: 트리거 대안 비교, Outbox 패턴, 파라미터화, 이중 알림과 fail-safe 설계
- 기술: n8n, Oracle, 메시지 연동
- 구성: 위험도 결과 → 기준값 판정 → Outbox → EMR·그룹웨어 알림 → 발송 상태
- 알고리즘: 임상 기준은 코드에 고정하지 않고 버전 있는 파라미터로 관리하며 Outbox의 미발송 건만 처리한다.
- 핵심 소스: [`outbox.py`](../examples/frax-alert/outbox.py)

### B14. QR·Barcode 간편결제 연동

- 상태: 협력업체 개발·인계
- 역할: 요구사항·인계·연동 검토. 직접 개발 성과와 분리
- 기술: 결제 연동, QR/Barcode, 운영 인계
- 구성: 결제 요청 → 벤더 결제 → 결과 콜백 → 내부 대조 → 미결 예외
- 알고리즘: 외부 성공 응답과 내부 수납 반영을 별도 원장으로 대조하며 미일치 건은 자동 재처리하지 않는다.
- 공개 산출물: 구성·검증 체크리스트만 공개하며 실결제 코드는 공개하지 않는다.

---

## C. 인프라·운영·개선 체계

### C01. 자체개발 프로그램 형상관리 체계

- 상태: 운영·지속 개선
- 역할: 관리 책임, 커밋·PR·배포키·SSH·롤백 규칙과 서버 운영 원칙 수립
- 구성: 개발 브랜치 → 검토·승인 → 배포 매니페스트 → 서버 반영 → 헬스체크 → 롤백
- 핵심 소스: [`deploy_manifest.py`](../examples/release-governance/deploy_manifest.py)

### C02. Playwright 자동화 서버 운영

- 상태: 운영·개선
- 역할: 자동화 스크립트 등록, 단일 워커, 타임아웃, 운영 매뉴얼과 변경 매니페스트 관리
- 구성: 요청 API → 작업 큐 → 브라우저 워커 → 증적 → 헬스체크
- 핵심 소스: [`single_worker.py`](../examples/playwright-runtime/single_worker.py)

### C03. Windows 서버 모니터링 데스크톱 도구

- 상태: 구현 완료
- 역할: C# WinForms로 서버·서비스 목록, WMI 지표, 저장·불러오기, HTML·Excel 보고 구현
- 기술: C#, .NET Framework 4.7.2, WMI, WinForms
- 구성: 서버 목록 → 자격정보 보호 저장 → WMI 수집 → 서비스 상태 → 보고서
- 핵심 소스: [`HealthSnapshot.cs`](../examples/server-monitor/HealthSnapshot.cs)

### C04. 병원 AI 플랫폼 운영·유지보수

- 상태: 운영 지원
- 역할: Docker·프로세스·벡터DB·로그·리소스 운영. 플랫폼 자체 개발로 표현하지 않음
- 구성: 웹·API → 모델·검색 서비스 → 벡터DB → 프로세스·컨테이너 모니터링
- 핵심 소스: [`service_health.py`](../examples/ai-platform-ops/service_health.py)

### C05. CSI 2분기 반복업무 자동화 개선안

- 상태: 개선활동 기획
- 역할: 지출결의·당직·수납·카드승인 등 운영 자동화 사례를 서비스 개선 프레임으로 구조화
- 구성: 업무 목록 → 빈도·위험·시간 분석 → 우선순위 → 자동화 → 효과 측정
- 핵심 소스: [`improvement_prioritizer.py`](../examples/csi-improvement/improvement_prioritizer.py)

### C06. CSI 3분기 EMR 운영업무 처리 개선

- 상태: 진행
- 역할: 화면·서브밋·테이블 탐색 문제를 서비스 청사진·원인분석·우선순위·실험안으로 정리
- 구성: 운영 요청 → 화면 식별 → 코드 색인 → 조회 근거 → 처리 가이드
- 핵심 소스: [`operation_index.py`](../examples/csi-improvement/operation_index.py)

### C07. 전산개발위원회 과제 분석·연동 조정

- 상태: 상시 수행
- 역할: 현업 요청을 요구사항, 시스템 경계, 담당 주체, 선행조건, 테스트와 운영 전환 계획으로 변환
- 구성: 요청서 → 현행 분석 → 역할 분담 → 기술 명세 → 테스트 → 인계
- 핵심 소스: [`request_triage.py`](../examples/project-governance/request_triage.py)

### C08. 장애 대응·재발방지 플레이북

- 상태: 운영 원칙 적용
- 범위: silent failure, 32비트 COM·폐쇄망, DNS·프록시, iBatis 매퍼, Java 인코딩, 단일 워커, OCR 모델 캐시·동시성
- 구성: 증상 → 영향 격리 → 관찰 채널 → 최소 재현 → 원인 → 복구 → 재발방지 가드
- 핵심 소스: [`incident_classifier.py`](../examples/incident-response/incident_classifier.py)

---

## D. 기타 제작·AI 활용 실험

### D01. CREEPER RUN — PowerPoint VBA 게임

- 상태: 제작 완료
- 역할: 게임 규칙·난이도·오브젝트 수명주기·키 입력 제약을 프롬프트로 명세하고 VBA 결과물을 검증·개선
- 기술: PowerPoint VBA, AI-assisted development
- 구성: 게임 초기화 → 입력 폴링 → 오브젝트 생성·이동 → 충돌 → 점수·생명 → 종료
- 알고리즘: 매 프레임 생성물 수를 제한하고 화면 밖 오브젝트를 제거해 슬라이드 도형 누적을 막는다.
- 핵심 소스: [`GameLoop.bas`](../examples/creeper-run/GameLoop.bas)

---

## 공개에서 제외한 로컬 폴더

아래는 작업물 누락이 아니라 공개 부적합 또는 개발 프로젝트가 아닌 항목이다.

- 인증서·키·자격증명 폴더
- 개인 문서, 사업자등록증, 브라우저·SQL 도구와 설치 프로그램
- 원본 의료 데이터, 환자·직원 식별정보, 운영 로그와 캡처
- 내부 EMR 전체 저장소와 벤더 원본 소스
- 백업·중복 버전·빌드 결과·실행 파일
- 학습·승진시험 자료

## 수량 요약

- AX·업무자동화: 15개
- API·시스템 연동: 14개
- 인프라·운영·개선 체계: 8개
- 기타 제작·AI 활용 실험: 1개
- 총 공개 카탈로그: 38개
