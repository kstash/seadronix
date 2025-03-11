1. default MongoDB 연결 필요 (docker 사용했음)
2. 로컬로 실행할 경우 사용자`ffmpeg` 지정 위치에 따라 오류가 발생할 수 있습니다.
   1. `which ffmpeg` 로 사용중이신 `ffmpeg` 라이브러리 경로를 찾아 해당 위치에 따라 변경해주시면 됩니다.
      1. `ffmpeg` 경로를 변경하는 코드는 [main.py] 파일에서 주석처리 되어있습니다.
