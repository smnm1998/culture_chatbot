from django.db import models

class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CityCountyTown(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f"{self.province.name} - {self.name}"

class Assistant(models.Model):
    name = models.CharField(max_length=255)  # 어시스턴트 이름
    photo = models.ImageField(upload_to='assistant_photos/')  # 어시스턴트 관련 이미지
    description = models.TextField(default='No description available')  # 어시스턴트 설명
    country = models.CharField(max_length=100, default='한국')  # 나라
    province = models.ForeignKey(Province, on_delete=models.CASCADE, default=1)  # 기본값으로 ID 1인 Province 사용
    city_county_town = models.ForeignKey(CityCountyTown, on_delete=models.CASCADE)  # 시군읍 정보
    assistant_variable = models.CharField(max_length=255, default='default_assistant')  # 어시스턴트 연결 변수

    def __str__(self):
        return self.name

# sql 추가 코드
# INSERT INTO assistant_province (name) VALUES ('서울');
# INSERT INTO assistant_province (name) VALUES ('경기도');
# INSERT INTO assistant_province (name) VALUES ('경상북도');
# INSERT INTO assistant_province (name) VALUES ('경상남도');
# INSERT INTO assistant_province (name) VALUES ('전라북도');
# INSERT INTO assistant_province (name) VALUES ('전라남도');
# INSERT INTO assistant_province (name) VALUES ('충청북도');
# INSERT INTO assistant_province (name) VALUES ('충청남도');
#
# -- 서울의 6개 구
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('종로구', 1);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('중구', 1);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('강남구', 1);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('서초구', 1);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('성북구', 1);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('동대문구', 1);
#
# -- 경기도의 6개 시
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('수원시', 2);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('성남시', 2);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('고양시', 2);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('용인시', 2);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('부천시', 2);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('안양시', 2);
#
# -- 경상북도의 6개 시
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('안동시', 3);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('포항시', 3);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('경주시', 3);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('구미시', 3);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('영주시', 3);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('문경시', 3);
#
# -- 경상남도의 6개 시
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('창원시', 4);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('김해시', 4);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('진주시', 4);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('사천시', 4);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('통영시', 4);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('거제시', 4);
#
# -- 전라북도의 6개 시
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('전주시', 5);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('군산시', 5);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('익산시', 5);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('정읍시', 5);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('남원시', 5);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('김제시', 5);
#
# -- 전라남도의 6개 시
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('여수시', 6);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('순천시', 6);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('목포시', 6);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('나주시', 6);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('광양시', 6);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('해남군', 6);
#
# -- 충청북도의 6개 시
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('청주시', 7);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('충주시', 7);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('제천시', 7);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('음성군', 7);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('단양군', 7);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('옥천군', 7);
#
# -- 충청남도의 6개 시
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('천안시', 8);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('아산시', 8);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('서산시', 8);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('논산시', 8);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('공주시', 8);
# INSERT INTO assistant_citycountytown (name, province_id) VALUES ('보령시', 8);
