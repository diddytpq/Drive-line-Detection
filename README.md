# Drive_line_detect
차선인식에 쓰이는 알고리즘 공부 및 실습


### version 1
인식과정
---------------------
영상입력->가우시안 블러(영상의 노이즈 제거)->영상을 그레이 스케일로 변환 -> canny 알고리즘을 이용해 엣지 추출 -> 도로를 제외한 불필요한 영역을 삭제(Roi 설정) -> 허프 변환을 이용해 차선 후보 추출 -> 차선 후보의 기울기를 측정해 차선이라 생각되는 선만 선별 -> 원본 이미지에 선 추가

결과


![ezgif com-video-to-gif](https://user-images.githubusercontent.com/67572161/87751020-fbb63400-c837-11ea-90cb-53c77436cfd8.gif)


도로가 검정에서 밝은 도로로 이동하였을때  왼쪽 노란색 차선과 아스팔트 색이 구분되지 않아 그레이 스케일에서 도로를 제대로 검출하지 못함


### version 2
인식과정
---------------------
영상입력->가우시안 블러(영상의 노이즈 제거)->영상을 그레이,HSV(노락색을 검출하기 위해)-> HSV에서 yollow에 해당하는 색 영역만 검출 -> 그레이 스케일 canny 알고리즘을 이용해 엣지 추출 -> 노랑색만 추출한 HSV 스케일 canny 알고리즘으로 엣지 추출 -> canny(그레이)+canny(HSV) 합치기 -> 도로를 제외한 불필요한 영역을 삭제(Roi 설정) -> 허프 변환을 이용해 차선 후보 추출 -> 차선 후보의 기울기를 측정해 차선이라 생각되는 선만 선별 -> 원본 이미지에 선 추가

HSV에서 노란색만 검출 결과

![ezgif com-video-to-gif (1)](https://user-images.githubusercontent.com/67572161/87751833-e5a97300-c839-11ea-876a-e5f0660c015b.gif)


결과

![ezgif com-video-to-gif (2)](https://user-images.githubusercontent.com/67572161/87752119-97e13a80-c83a-11ea-95ef-c33595eb0ab1.gif)



do-to
1. top_view(bird_view) 적용해보기
2. 차선 후보에서 대표선을 선정
3. 대표선을 기준으로 조절해야 하는 핸들 각도 계산
