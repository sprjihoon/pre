# 프리패킹 예측 및 운영관리 시스템

물류센터 프리패킹(선포장) 작업을 위한 예측 및 운영 관리 시스템입니다.

## 기술 스택

- **백엔드**: FastAPI, SQLAlchemy (async), PostgreSQL, Alembic
- **프론트엔드**: React 19, TypeScript, Vite, Zustand, Recharts
- **예측 엔진**: 규칙기반 + PyTorch (LSTM/Transformer)
- **검증 엔진**: OpenAI GPT
- **인프라**: Docker Compose

## 시작하기

### Docker Compose 실행 (권장)

```bash
cd prepacking
docker-compose up -d
```

- 백엔드: http://localhost:8000
- 프론트엔드: http://localhost:5173
- API 문서: http://localhost:8000/docs

### 로컬 개발

**백엔드:**

```bash
cd prepacking/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**프론트엔드:**

```bash
cd prepacking/frontend
npm install
npm run dev
```

**PostgreSQL:**

```bash
docker-compose up -d db
```

## 시스템 구조

```
prepacking/
├── backend/          # FastAPI 백엔드
│   ├── models/       # SQLAlchemy ORM 모델
│   ├── schemas/      # Pydantic 스키마
│   ├── routers/      # API 라우터
│   ├── services/     # 비즈니스 로직
│   ├── engines/      # 예측 엔진 (딥러닝, LLM)
│   └── utils/        # 유틸리티
├── frontend/         # React 프론트엔드
│   └── src/
│       ├── api/      # API 호출 레이어
│       ├── components/ # 공통 컴포넌트
│       ├── pages/    # 페이지 컴포넌트
│       ├── stores/   # Zustand 상태 관리
│       └── types/    # TypeScript 타입
├── model_store/      # PyTorch 모델 파일 저장
└── docker-compose.yml
```

## 주요 기능

1. **업로드**: 배송통계 엑셀/CSV 파일 업로드, 파싱, 버전 관리
2. **분석**: 반복 SKU/조합 분석, 요일 패턴, 변동성 분석
3. **규칙기반 엔진**: 7일/30일/요일 평균 기반 추천값 생성
4. **추천/승인/실행**: 추천 목록 → 승인/수정/거절 → 실행 기록
5. **로케이션/재고**: 위치 관리, 재고 추적, 해체/원복
6. **작업 지시서**: HTML 기반 A4 인쇄용 지시서
7. **검증/리포트**: 예측 vs 실제 비교, 정확도 분석
8. **딥러닝**: LSTM/Transformer 모델 학습, 백테스트
9. **LLM 검증**: OpenAI 연동 추천 검토, 실패 분석
10. **업체 프로파일**: 업체별 설정 관리

## 환경 변수

```env
DATABASE_URL=postgresql+asyncpg://prepacking:prepacking1234@localhost:5432/prepacking
OPENAI_API_KEY=sk-...
```
