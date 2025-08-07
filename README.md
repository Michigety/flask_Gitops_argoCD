# Flask Health Check API

간단한 헬스 체크 API를 제공하는 Flask 애플리케이션입니다.

## 기능

- `/health` 엔드포인트: 애플리케이션 상태 확인
- `/` 엔드포인트: API 정보 제공

## 로컬 실행

### 1. Python 가상환경 생성 및 의존성 설치

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 애플리케이션 실행

```bash
python app.py
```

애플리케이션이 `http://localhost:5000`에서 실행됩니다.

## Docker 실행

### 1. Docker 이미지 빌드 및 실행

```bash
docker-compose up --build
```

### 2. 백그라운드 실행

```bash
docker-compose up -d --build
```

### 3. 컨테이너 중지

```bash
docker-compose down
```

## API 엔드포인트

### GET /health

헬스 체크 정보를 반환합니다.

**응답 예시:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000",
  "service": "flask-health-check",
  "version": "1.0.0",
  "environment": "production"
}
```

### GET /

API 정보를 반환합니다.

**응답 예시:**
```json
{
  "message": "Flask Health Check API",
  "endpoints": {
    "health": "/health"
  }
}
```

## 테스트

### curl을 사용한 테스트

```bash
# 헬스 체크
curl http://localhost:5000/health

# 루트 엔드포인트
curl http://localhost:5000/
```

### 브라우저에서 확인

- `http://localhost:5000/health`
- `http://localhost:5000/`

## 환경 변수

- `ENVIRONMENT`: 실행 환경 (기본값: development)
- `FLASK_ENV`: Flask 환경 (기본값: development)

## Docker 헬스 체크

Docker 컨테이너는 30초마다 `/health` 엔드포인트를 확인하여 애플리케이션 상태를 모니터링합니다.

## GitOps 배포

이 프로젝트는 GitOps 방식으로 Kubernetes에 배포됩니다. 자세한 설정 방법은 [GITOPS_SETUP.md](GITOPS_SETUP.md)를 참조하세요.

### GitOps 파이프라인 흐름:

1. **소스 코드 변경** → GitHub Actions 트리거
2. **Docker 이미지 빌드** → GHCR.io에 푸시
3. **Kustomize 매니페스트 업데이트** → 배포 레포지토리에 커밋
4. **ArgoCD 자동 배포** → Kubernetes 클러스터에 배포

### 빠른 시작:

```bash
# 1. GitHub Secrets 설정
# DEPLOYMENT_REPO: 배포 레포지토리 이름
# DEPLOYMENT_TOKEN: Personal Access Token

# 2. 배포 레포지토리 생성 및 Kustomize 매니페스트 복사

# 3. ArgoCD 설치 및 Application 배포
kubectl apply -f argocd/applications/flask-health-check-prod.yaml
```
