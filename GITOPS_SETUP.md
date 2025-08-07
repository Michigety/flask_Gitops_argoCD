# GitOps 설정 가이드

이 문서는 Flask Health Check API를 위한 GitOps 파이프라인 설정 방법을 설명합니다.

## 아키텍처 개요

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Source Code   │───▶│  GitHub Actions │───▶│   GHCR.io       │
│   Repository    │    │   CI Pipeline   │    │   Registry      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Deployment     │───▶│   ArgoCD        │
                       │  Repository     │    │   (GitOps)      │
                       └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   Kubernetes    │
                                               │   Cluster       │
                                               └─────────────────┘
```

## 1. GitHub Secrets 설정

### 현재 레포지토리에서 설정할 Secrets:

1. **DEPLOYMENT_REPO**: 배포 레포지토리 이름 (예: `your-username/deployment-repo`)
2. **DEPLOYMENT_TOKEN**: 배포 레포지토리에 접근할 수 있는 Personal Access Token

### Personal Access Token 생성 방법:

1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" 클릭
3. 다음 권한 선택:
   - `repo` (전체 레포지토리 접근)
   - `workflow` (워크플로우 실행)
4. 토큰 생성 후 복사하여 GitHub Secrets에 저장

## 2. 배포 레포지토리 설정

### 배포 레포지토리 구조:

```
deployment-repo/
├── k8s/
│   ├── base/
│   │   ├── kustomization.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   └── overlays/
│       ├── development/
│       │   ├── kustomization.yaml
│       │   └── replica-patch.yaml
│       └── production/
│           ├── kustomization.yaml
│           └── resource-patch.yaml
└── argocd/
    └── applications/
        └── flask-health-check-prod.yaml
```

## 3. ArgoCD 설치 및 설정

### ArgoCD 설치 (Kubernetes 클러스터에):

```bash
# ArgoCD 설치
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# ArgoCD 서버 접근을 위한 포트 포워딩
kubectl port-forward svc/argocd-server -n argocd 8080:443

# 초기 비밀번호 확인
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### ArgoCD Application 배포:

```bash
# ArgoCD Application 매니페스트 적용
kubectl apply -f argocd/applications/flask-health-check-prod.yaml
```

## 4. 워크플로우 동작 과정

### 1단계: Docker 이미지 빌드 및 푸시
- GitHub Actions가 소스 코드 변경을 감지
- Dockerfile을 사용하여 컨테이너 이미지 빌드
- GHCR.io에 이미지 푸시

### 2단계: Kustomize 매니페스트 업데이트
- 빌드된 이미지 태그를 배포 레포지토리의 Kustomize 매니페스트에 자동 업데이트
- 변경사항을 배포 레포지토리에 커밋 및 푸시

### 3단계: ArgoCD 자동 배포
- ArgoCD가 배포 레포지토리 변경을 감지
- Kubernetes 클러스터에 자동 배포

## 5. 환경별 설정

### 개발 환경:
- 레플리카 수: 1
- 리소스 요청: 64Mi 메모리, 50m CPU
- 이미지 태그: `develop`

### 프로덕션 환경:
- 레플리카 수: 5
- 리소스 요청: 128Mi 메모리, 100m CPU
- 이미지 태그: `latest`

## 6. 모니터링 및 로그

### ArgoCD 대시보드:
- URL: `https://localhost:8080` (포트 포워딩 후)
- 사용자: `admin`
- 비밀번호: 초기 비밀번호 또는 설정한 비밀번호

### 애플리케이션 상태 확인:
```bash
# ArgoCD CLI 사용
argocd app get flask-health-check-prod

# Kubernetes 직접 확인
kubectl get pods -n production
kubectl logs -n production deployment/flask-health-check
```

## 7. 트러블슈팅

### 일반적인 문제들:

1. **이미지 푸시 실패**: GHCR 권한 확인
2. **배포 레포지토리 접근 실패**: DEPLOYMENT_TOKEN 확인
3. **ArgoCD 동기화 실패**: 매니페스트 문법 오류 확인
4. **애플리케이션 시작 실패**: 리소스 제한, 환경 변수 확인

### 로그 확인:
```bash
# GitHub Actions 로그
# GitHub 레포지토리 → Actions 탭에서 확인

# ArgoCD 로그
kubectl logs -n argocd deployment/argocd-server

# 애플리케이션 로그
kubectl logs -n production deployment/flask-health-check
```

## 8. 보안 고려사항

1. **Secrets 관리**: 민감한 정보는 Kubernetes Secrets 사용
2. **RBAC**: ArgoCD와 애플리케이션에 적절한 권한 설정
3. **네트워크 정책**: 필요한 포트만 노출
4. **이미지 스캔**: 컨테이너 이미지 보안 취약점 스캔

## 9. 확장 가능한 개선사항

1. **다중 환경**: staging, testing 환경 추가
2. **롤백 기능**: 이전 버전으로 자동 롤백
3. **알림**: Slack, Teams 등으로 배포 알림
4. **메트릭**: Prometheus, Grafana 연동
5. **로깅**: ELK 스택 연동
