# Project Overview
**Shiori** 는 개인 일기를 작성하고, AI를 활용해 일주일 일지 요약과 감정 태깅을 제공하는 서비스입니다.  

### 기술 스택
- Python (3.11)
- FastAPI  
- MySQL  
- MongoDB  
- Redis
- Celery

## System Architecture

<img width="1107" height="644" alt="system drawio" src="https://github.com/user-attachments/assets/3c0f65da-35ed-4b2f-bf5f-6d096b9dc79b" />

| Component | 역할 |
|-----------|------|
| **FastAPI** | API 서버. 요청 수신, 인증, 내부 API 관리 및 DB 저장 |
| **Redis** | 세션 저장소 및 메시지 큐 브로커 |
| **Celery Worker** | 감정 추론(Hugging Face) 및 요약(OpenAI) 수행 |
| **Hugging Face Model** | 일기별 감정 분석 수행 |
| **OpenAI API** | 감정 + 일기 데이터를 기반으로 요약문 생성 |
| **MySQL** | 사용자 및 요약 결과 관리 |
| **MongoDB** | 일지 및 메타 데이터 저장 |



## 프로젝트 주요 목표
1. 요약 기능은 **외부 네트워크 지연 상황에서도 안정적인 사용자 경험**을 제공할 수 있어야 합니다. 

2. 일기 저장 시 발생할 수 있는 **동시성 이슈**를 제어하여 단일 저장만 보장할 수 있어야 합니다. 

## 고민한 것들
1. 요약 기능의 외부 LLM API 호출 지연으로 인해 **사용자 경험이 저하**되는 문제를 어떻게 해결할까?  

2. 다중 로그인이 가능한 상황에서 동일 날짜 일지 저장요청이 **동시에 발생**할 때 이를 어떻게 처리할까?

<br>

### 고민 1. 외부 LLM API 지연으로 인한 응답 지연 문제 -> [**전체 글 보기**](https://github.com/jungyu333/SHIORI-BE/wiki/%EC%9A%94%EC%95%BD-%EA%B8%B0%EB%8A%A5%EC%9D%98-%EB%B9%84%EB%8F%99%EA%B8%B0-%EB%A9%94%EC%8B%9C%EC%A7%80-%ED%81%90-%EA%B5%AC%EC%A1%B0-%EC%A0%84%ED%99%98)

#### 문제 인식  
외부 LLM API 호출이 포함된 요약 기능에서 **평균 10초 이상의 응답 지연**이 발생  

사용자는 요청이 멈춘 것처럼 느꼈고, 여러 사용자가 동시에 요청할 경우 **응답 시간이 20초 이상**으로 늘어나는 문제가 발생함  

<br>

#### 해결 방법  
**비동기 메시지 큐(Celery + Redis)** 기반 구조로 전환하여 요약 요청과 LLM 호출을 완전히 분리  

- FastAPI는 요청을 받자마자 Celery Task로 등록 후 즉시 응답


- Celery Worker가 비동기로 LLM 요약 및 감정 분석을 수행  


- 결과는 내부 API를 통해 DB에 저장  

<img width="100%" alt="celery drawio" src="https://github.com/user-attachments/assets/a7a7a5c6-1821-4678-8c8f-6e3ed7ddad59" />

결과적으로 **응답 속도를 약 1초 수준으로 단축**하고 외부 LLM 지연이 서버 응답에 영향을 주지 않는 구조로 개선됨  

<br>

### 고민 2. 일지 저장 시 동시성 제어 -> [**전체 글 보기**](https://github.com/jungyu333/SHIORI-BE/wiki/%EB%8F%99%EC%9D%BC-%EB%82%A0%EC%A7%9C-%EC%9D%BC%EC%A7%80-%EC%A0%80%EC%9E%A5-%EC%8B%9C-%EB%8F%99%EC%8B%9C%EC%84%B1-%EC%A0%9C%EC%96%B4-%ED%95%98%EA%B8%B0)

#### 문제 인식  
여러 기기에서 동일 날짜의 일기를 동시에 저장할 경우 **일부 요청만 성공하고 나머지는 반영되지 않는 불안정한 결과**가 발생

<img src="https://github.com/user-attachments/assets/1400a4af-258d-4968-b61d-3eed99b5a18c" width="100%" alt="update conflict diagram" />

<br>


#### 문제 원인  
MongoDB는 문서 단위로 락을 잡기 때문에 **동일 문서에 대한 동시 update 시 락 경합(lock contention)** 이 발생

락을 획득하지 못한 요청은 대기 상태에서 **타임아웃 후 실패(500)** 하며 결과적으로 **일부 요청만 성공**하는 불안정한 상황이 발생

<br>


#### 해결 방법  
**낙관적 락(Optimistic Concurrency Control)** 을 적용  
- `version` 기반 **CAS(compare-and-swap)** 로 단 하나의 요청만 성공 보장  


- 나머지 요청은 `409 Conflict`로 명시적 실패 처리
<br/>

결과적으로 **데이터 정합성을 보장하면서도 충돌 상황을 명시적으로 제어**할 수 있게 됨
