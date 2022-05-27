docker-compose -p mailu up -d
docker-compose -p mailu exec admin flask mailu admin admin mangmaytinh.vip root
docker-compose -p mailu exec admin flask mailu user test1 mangmaytinh.vip 1234

