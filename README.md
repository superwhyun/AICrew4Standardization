
# CrewAI Interaction

CrewAI Interaction은 Flask와 Flask-SocketIO를 사용하여 국제표준화 회의에서 제안자와 반대자가 상호작용할 수 있는 웹 애플리케이션입니다. 이 애플리케이션은 OpenAI의 GPT-4 모델을 사용하여 제안자와 반대자의 의견을 생성하고, 이를 통해 새로운 표준화 항목에 대해 논의합니다.

## 기능

- 제안자가 새로운 표준화 항목을 제안합니다.
- 반대자가 제안된 표준화 항목에 대한 반대 의견을 제시합니다.
- 동의 여부를 판단하여 최종 합의에 도달합니다.
- 실시간으로 각 이터레이션 결과를 웹 페이지에 표시합니다.

## 설치

이 프로젝트를 실행하기 위해서는 Python과 pip, 그리고 `conda`가 필요합니다.

### 환경 설정

먼저 conda 환경을 설정합니다.

```bash
conda create --name crewai_env python=3.11
conda activate crewai_env
```

### 종속성 설치

필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

### .env 파일 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고, OpenAI API 키를 추가합니다.

```plaintext
OPENAI_API_KEY=your_openai_api_key
```

## 실행

Flask 애플리케이션을 실행합니다.

```bash
python web.py
```

브라우저에서 `http://localhost:5002`에 접속하여 애플리케이션을 사용할 수 있습니다.

## 사용 예시

1. 웹 페이지에 접속하여 주제를 입력합니다.
2. 이터레이션 수, 제안자와 반대자의 배경 설명을 입력합니다.
3. `Submit` 버튼을 클릭하여 상호작용을 시작합니다.
4. 각 이터레이션의 결과가 실시간으로 표시됩니다.
5. 최종 합의에 도달하면 결과가 표시됩니다.

## 파일 구조

```plaintext
.
├── .env                # 환경 변수 파일
├── app.py              # Flask 애플리케이션
├── requirements.txt    # 필요한 패키지 목록
├── templates
│   └── index.html      # 웹 페이지 템플릿
└── README.md           # README 파일
```

## 기여

기여를 환영합니다! 버그 보고, 기능 요청 또는 풀 리퀘스트를 통해 기여할 수 있습니다.

## 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 LICENSE 파일을 참고하세요.
